"""Runner pomiarowy: korpus -> aktywacje -> widma i metryki -> parquet (T4).

STRUKTURA DWUPRZEBIEGOWA. Komponent pozycyjny to srednia aktywacji per pozycja
po CALYM korpusie danego jezyka (protokol par. 4), wiec nie da sie go odjac
w tym samym przebiegu, w ktorym jest estymowany. Przebieg 1 liczy sumy
pozycyjne, przebieg 2 liczy metryki. Aktywacje nie sa trzymane miedzy
przebiegami - forward jest deterministyczny, wiec taniej je przeliczyc niz
skladowac 14 GB na jezyk.

KOLEJNOSC OPERACJI (istotna, kazda zmiana kolejnosci zmienia wynik):
  forward -> maskowanie (pierwsze 32 + tokeny specjalne)
          -> WYROWNANIE OKNA do min T' po wariantach scenariusza
          -> akumulacja / odjecie komponentu pozycyjnego
          -> z-score per kanal
          -> macierz Grama -> eigh -> metryki
Wyrownanie okna PRZED estymacja komponentu pozycyjnego jest celowe: srednia
liczona jest dokladnie na tych danych, ktore potem sa analizowane.

Uruchamiac na maszynie pomiarowej:
    python -m pipeline.runner            # pilot bez nulli
    python -m pipeline.runner --nulls    # z nullami N1 i N2
"""

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from corpus.build import VARIANTS, build_scenario
from corpus.stats import render_gemma_chat
from corpus.tokens import TokenCounter
from corpus.validate import SCENARIOS_DIR
from nulls.interventional import permute_sentences, permute_turns
from pipeline.memory_guard import check_foreign_vram, check_peak_memory
from pipeline.metrics import d_lag, i_minus1, i_total, k_modes, spectral_entropy
from pipeline.preprocess import mask_tokens, zscore_channels
from pipeline.spectrum import gram_eigenvalues
from pipeline.window import apply_window

OUT_DIR = REPO / "measurements"
NULL_VARIANTS = ["B", "C", "CprimG", "CprimU"]   # A nie ma insercji, nulle go nie dotycza


def plan_texts(scenarios, include_nulls=True):
    """Lista tekstow do zmierzenia: (scenariusz, wariant, null)."""
    plan = []
    for sc in scenarios:
        for v in VARIANTS:
            plan.append({"scenario_id": sc["scenario_id"], "language": sc["language"],
                         "variant": v, "null": None})
        if include_nulls:
            for v in NULL_VARIANTS:
                for null in ("N1", "N2"):
                    plan.append({"scenario_id": sc["scenario_id"],
                                 "language": sc["language"],
                                 "variant": v, "null": null})
    return plan


def equalize_scenario(activations):
    """Wspolne okno = min T' po wariantach scenariusza (protokol par. 4, aneks)."""
    return apply_window(activations, mode="equalize", report_dropped=True)


def accumulate_positional(acc, arr):
    """Akumulator sum pozycyjnych; strumieniowy, zeby nie trzymac korpusu w RAM.

    Obsluguje NIEROWNE dlugosci - okna sa per scenariusz, wiec teksty jednego
    jezyka maja rozne T'. Semantyka identyczna z corpus positional_mean
    (protokol par. 4): na pozycji t usredniane sa tylko teksty siegajace t.
    Pierwsza wersja odrzucala niezgodne dlugosci i polozyla pomiar pilota na
    drugim scenariuszu (raport DEP, ops/pomiar-pilota.md) - blad byl w tym
    akumulatorze, nie w definicji protokolarnej.
    """
    arr = np.asarray(arr, dtype=np.float64)
    if acc is None:
        return {"sum": arr.copy(), "count": np.ones(arr.shape[0])}
    t_old, t_new = acc["sum"].shape[0], arr.shape[0]
    if t_new > t_old:
        pad = np.zeros((t_new - t_old, acc["sum"].shape[1]))
        acc["sum"] = np.vstack([acc["sum"], pad])
        acc["count"] = np.concatenate([acc["count"], np.zeros(t_new - t_old)])
    acc["sum"][:t_new] += arr
    acc["count"][:t_new] += 1.0
    return acc


def metrics_for_layer(H, mu, lambda_star, d_lag_permutations=500, rng=None,
                      compute_d_lag=True):
    """Pelny lancuch metryk dla jednej warstwy jednego tekstu (protokol par. 5).

    compute_d_lag=False dla warstw poza pasmem konfirmacyjnym: D_lag to ~60%
    calego kosztu pomiaru (500 permutacji x iteracja potegowa), a hipoteza H5
    i sanity N1 potrzebuja go w pasmie; pelny profil warstwowy D_lag nalezy
    do eksploracji i mozna go policzyc pozniej z zachowanych aktywacji.
    """
    Z, n_excluded = zscore_channels(np.asarray(H, dtype=np.float64) - mu)
    eigs = gram_eigenvalues(Z)
    return {
        "I_total": i_total(eigs, lambda_star),
        "I_minus1": i_minus1(eigs, lambda_star),
        "k": k_modes(eigs, lambda_star),
        "H_s": spectral_entropy(eigs),
        "D_lag": (d_lag(Z, n_permutations=d_lag_permutations, rng=rng)
                  if compute_d_lag else float("nan")),
        "trace": float(eigs.sum()),
        "rank": int(eigs.size),
        "n_excluded_channels": n_excluded,
        "_eigs": eigs,
    }


# --- czesc wymagajaca modelu (uruchamiana tylko na maszynie pomiarowej) ----

def load_scenarios():
    return [json.loads(p.read_text(encoding="utf-8"))
            for p in sorted(SCENARIOS_DIR.glob("*/*.json"))]


def variant_turns(built, variant, null, seed):
    turns = built["variants"][variant]
    if null == "N1":
        return permute_sentences(turns, rng=np.random.default_rng(seed))
    if null == "N2":
        return permute_turns(turns, rng=np.random.default_rng(seed + 1))
    return turns


def forward_masked(model, tok, turns, cfg, device="cuda:0"):
    """Forward + maskowanie; zwraca liste (T', D) per warstwa oraz szczyt pamieci."""
    import torch

    # bramka na obce zuzycie karty PRZED forwardem - gdy uzytkownik maszyny
    # wlaczy gre w trakcie biegu, zatrzymujemy sie czysto na checkpointcie
    free_b, total_b = torch.cuda.mem_get_info()
    check_foreign_vram(total_b, free_b, torch.cuda.memory_allocated())

    text = render_gemma_chat([{"role": t["role"], "text": " ".join(t["sentences"])}
                              for t in turns])
    enc = tok(text, return_tensors="pt", add_special_tokens=False).to(device)
    ids = enc["input_ids"][0]
    special = np.isin(ids.cpu().numpy(), tok.all_special_ids)

    torch.cuda.reset_peak_memory_stats()
    with torch.no_grad():
        out = model(**enc, output_hidden_states=True)
    peak = torch.cuda.max_memory_allocated()
    check_peak_memory(peak, cfg["compute"]["memory_guard_limit_gb"], "bf16",
                      cfg["compute"]["fp32_control_limit_gb"])

    idx = cfg["measurement"]["layer_indexing"]
    keep = [i for i in range(len(out.hidden_states)) if i not in idx["excluded_from_measurement"]]
    layers = []
    for i in keep:
        h = out.hidden_states[i][0].float().cpu().numpy()
        layers.append(mask_tokens(h, special_mask=special,
                                  skip_first=cfg["measurement"]["skip_first_tokens"]))
    del out
    torch.cuda.empty_cache()
    return layers, keep, peak


def main():
    import yaml

    ap = argparse.ArgumentParser()
    ap.add_argument("--nulls", action="store_true", help="policz takze nulle N1 i N2")
    ap.add_argument("--limit", type=int, default=None, help="tylko N pierwszych scenariuszy")
    args = ap.parse_args()

    cfg = yaml.safe_load((REPO / "config.yaml").read_text(encoding="utf-8"))
    if str(cfg["measurement"]["token_window_mode"]).startswith("TBD"):
        print("config: token_window_mode nie zostal wybrany. Pipeline nie ruszy.")
        return 1

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    name, rev = cfg["model"]["hf_name"], cfg["model"]["hf_revision"]
    print(f"[runner] {name} @ {rev[:12]}", flush=True)
    tok = AutoTokenizer.from_pretrained(name, revision=rev)
    model = AutoModelForCausalLM.from_pretrained(name, revision=rev,
                                                 dtype=torch.bfloat16, device_map="cuda:0")
    model.eval()

    tc = TokenCounter.load()
    if not tc.exact:
        print("[runner] STOP: brak tokenizera w corpus/.tokenizer - licznik heurystyczny")
        return 1

    scenarios = load_scenarios()[: args.limit]
    budget = cfg["measurement"]["token_budget"]
    seed = cfg["seeds"]["permutation_tests"]
    OUT_DIR.mkdir(exist_ok=True)

    # --- przebieg 1: komponent pozycyjny per jezyk ------------------------
    # Checkpoint: mu i okna zapisywane po ukonczeniu przebiegu; restart wczytuje
    # je z dysku zamiast powtarzac 80 forwardow (uwaga DEP z pierwszego podejscia:
    # wznawialnosc dotyczyla tylko przebiegu 2).
    mu_file = OUT_DIR / "positional_mu.npz"
    win_file = OUT_DIR / "windows.json"
    OUT_DIR.mkdir(exist_ok=True)
    if mu_file.exists() and win_file.exists():
        data = np.load(mu_file, allow_pickle=False)
        langs = sorted({k.split("|")[0] for k in data.files})
        mu = {lang: [data[f"{lang}|{i}"] for i in range(
            sum(1 for k in data.files if k.startswith(lang + "|")))] for lang in langs}
        saved = json.loads(win_file.read_text(encoding="utf-8"))
        windows, dropped_log = saved["windows"], saved["dropped"]
        print(f"[runner] przebieg 1/2: wczytany z checkpointu ({', '.join(langs)})",
              flush=True)
    else:
        print("[runner] przebieg 1/2: komponent pozycyjny", flush=True)
        windows, dropped_log = {}, []
    pos_acc, t0 = {}, time.time()
    for sc in (scenarios if not windows else []):
        built = build_scenario(sc, tc, budget=budget)
        acts = {}
        for v in VARIANTS:
            layers, keep, _ = forward_masked(model, tok,
                                             variant_turns(built, v, None, seed), cfg)
            acts[v] = layers
        # wyrownanie okna liczone na pierwszej warstwie (wszystkie maja to samo T')
        lengths = {v: acts[v][0].shape[0] for v in VARIANTS}
        n = min(lengths.values())
        windows[sc["scenario_id"]] = n
        dropped_log.append({"scenario_id": sc["scenario_id"], **{
            f"dropped_{v}": lengths[v] - n for v in VARIANTS}})
        lang = sc["language"]
        pos_acc.setdefault(lang, [None] * len(acts[VARIANTS[0]]))
        for v in VARIANTS:
            for li, arr in enumerate(acts[v]):
                pos_acc[lang][li] = accumulate_positional(pos_acc[lang][li], arr[:n])
        print(f"  {sc['scenario_id']}: okno {n} tok. "
              f"({time.time() - t0:.0f} s)", flush=True)

    if pos_acc:
        mu = {lang: [a["sum"] / a["count"][:, None] for a in accs]
              for lang, accs in pos_acc.items()}
        np.savez_compressed(mu_file, **{f"{lang}|{i}": arr
                                        for lang, arrs in mu.items()
                                        for i, arr in enumerate(arrs)})
        win_file.write_text(json.dumps({"windows": windows, "dropped": dropped_log}),
                            encoding="utf-8")
        print(f"[runner] przebieg 1/2: checkpoint zapisany ({mu_file.name})", flush=True)

    # --- przebieg 2: metryki, z checkpointem per tekst ---------------------
    # Bieg trwa godziny; kazdy ukonczony tekst laduje natychmiast w jsonl,
    # a ponowne uruchomienie pomija teksty juz policzone. Przerwanie w polowie
    # kosztuje jeden tekst, nie caly bieg.
    print("[runner] przebieg 2/2: widma i metryki", flush=True)
    ckpt_metrics = OUT_DIR / "metrics.checkpoint.jsonl"
    ckpt_spectra = OUT_DIR / "spectra.checkpoint.jsonl"
    done = set()
    if ckpt_metrics.exists():
        for line in ckpt_metrics.read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            done.add((r["scenario_id"], r["variant"], r["null"]))
        print(f"[runner] wznowienie: {len(done)} tekstow juz policzonych", flush=True)

    band_lo, band_hi = cfg["measurement"]["layer_indexing"]["band_block_indices"]
    plan = plan_texts(scenarios, include_nulls=args.nulls)
    for item in plan:
        key = (item["scenario_id"], item["variant"], item["null"])
        if key in done:
            continue
        sc = next(s for s in scenarios if s["scenario_id"] == item["scenario_id"])
        built = build_scenario(sc, tc, budget=budget)
        turns = variant_turns(built, item["variant"], item["null"], seed)
        layers, keep, peak = forward_masked(model, tok, turns, cfg)
        n = windows[sc["scenario_id"]]
        lang = sc["language"]
        text_rows, text_spectra = [], []
        for li, arr in enumerate(layers):
            arr = arr[:n]
            block = keep[li] - 1
            in_band = band_lo <= block <= band_hi
            m = metrics_for_layer(arr, mu[lang][li][:n], lambda_star=float("inf"),
                                  d_lag_permutations=cfg["analysis"]["d_lag_permutations"],
                                  rng=np.random.default_rng([seed, li]),
                                  compute_d_lag=in_band)
            eigs = m.pop("_eigs")
            text_rows.append({**item, "hidden_state_index": keep[li], "block": block,
                              "in_band": in_band, "T_prime": n,
                              "peak_gb": peak / 2**30, **m})
            text_spectra.append({**item, "hidden_state_index": keep[li],
                                 "eigenvalues": eigs.tolist()})
        # zapis atomowy per tekst: wszystkie warstwy naraz, potem flush
        with ckpt_metrics.open("a", encoding="utf-8") as f:
            for r in text_rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        with ckpt_spectra.open("a", encoding="utf-8") as f:
            for r in text_spectra:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"  {item['scenario_id']} {item['variant']}"
              f"{'/' + item['null'] if item['null'] else ''}", flush=True)

    import pandas as pd
    rows = [json.loads(l) for l in ckpt_metrics.read_text(encoding="utf-8").splitlines()]
    spectra = [json.loads(l) for l in ckpt_spectra.read_text(encoding="utf-8").splitlines()]
    pd.DataFrame(rows).to_parquet(OUT_DIR / "metrics.parquet", index=False)
    pd.DataFrame(spectra).to_parquet(OUT_DIR / "spectra.parquet", index=False)
    pd.DataFrame(dropped_log).to_csv(OUT_DIR / "dropped_tokens.csv", index=False)
    print(f"[runner] zapisane: {len(rows)} wierszy metryk, {len(spectra)} widm", flush=True)
    print("[runner] UWAGA: lambda_star = inf (placeholder). Metryki I_total, I_-1 i k "
          "sa policzone wzgledem nieskonczonego progu i beda PRZELICZONE w T5 z widm "
          "w spectra.parquet, po estymacji nullu symulacyjnego.", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
