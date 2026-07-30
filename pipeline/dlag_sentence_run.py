"""Nocny bieg: D_lag z nullem zdaniowym dla calego pilota (runda 3 konsultacji).

Liczony NIEZALEZNIE od werdyktu recenzenta - nadzbior danych obsluguje kazda
z rozwazanych opcji (W1: nowa definicja, W3: dwie metryki). Decyzja rozstrzyga,
co wchodzi do par. 5 protokolu, nie co mierzymy.

Wykorzystuje komponenty zachowane po pomiarze pilota na maszynie:
measurements/positional_mu.npz + windows.json. Potrzebuje swiezych forwardow
(aktywacje nie sa skladowane), wiec biegnie na maszynie pomiarowej:

    python -m pipeline.dlag_sentence_run          # teksty glowne + nulle
Checkpoint per tekst, wznawianie ta sama komenda.
"""

import json
import sys
import time
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from corpus.build import VARIANTS, build_scenario
from corpus.stats import render_gemma_chat_with_spans
from corpus.tokens import TokenCounter
from pipeline.memory_guard import check_foreign_vram, check_peak_memory
from pipeline.metrics import d_lag_sentence
from pipeline.preprocess import zscore_channels
from pipeline.runner import (
    NULL_VARIANTS,
    load_scenarios,
    plan_texts,
    variant_turns,
)

OUT_DIR = REPO / "measurements"
SKIP_FIRST = 32


def sentence_ids_for_text(tok, turns):
    """Tokenizuje render i przypisuje kazdemu tokenowi id zdania (-1 = szablon).

    Zwraca (input_ids_tensor, keep_mask, sentence_ids_po_maskowaniu).
    Mapowanie przez offsety szybkiego tokenizera: token nalezy do zdania,
    jesli jego pierwszy znak lezy w zakresie znakowym zdania.
    """
    text, spans = render_gemma_chat_with_spans(turns)
    enc = tok(text, return_tensors="pt", add_special_tokens=False,
              return_offsets_mapping=True)
    offsets = enc.pop("offset_mapping")[0].tolist()
    ids = enc["input_ids"][0]
    special = np.isin(ids.cpu().numpy(), tok.all_special_ids)

    bounds = np.array([(a, b, i) for a, b, i in spans])
    sent_of_token = np.full(len(offsets), -1, dtype=np.int64)
    starts = bounds[:, 0]
    ends = bounds[:, 1]
    for ti, (a, _b) in enumerate(offsets):
        j = np.searchsorted(starts, a, side="right") - 1
        if j >= 0 and a < ends[j]:
            sent_of_token[ti] = bounds[j, 2]

    keep = np.ones(len(offsets), dtype=bool)
    keep[:SKIP_FIRST] = False
    keep &= ~special
    return enc, keep, sent_of_token[keep]


def main():
    import yaml

    cfg = yaml.safe_load((REPO / "config.yaml").read_text(encoding="utf-8"))

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    name, rev = cfg["model"]["hf_name"], cfg["model"]["hf_revision"]
    print(f"[dlag-sent] {name} @ {rev[:12]}", flush=True)
    tok = AutoTokenizer.from_pretrained(name, revision=rev)
    model = AutoModelForCausalLM.from_pretrained(name, revision=rev,
                                                 dtype=torch.bfloat16,
                                                 device_map="cuda:0")
    model.eval()

    tc = TokenCounter.load()
    if not tc.exact:
        print("[dlag-sent] STOP: brak tokenizera w corpus/.tokenizer")
        return 1

    mu_file, win_file = OUT_DIR / "positional_mu.npz", OUT_DIR / "windows.json"
    if not (mu_file.exists() and win_file.exists()):
        print("[dlag-sent] STOP: brak checkpointu przebiegu 1 z pomiaru pilota")
        return 1
    data = np.load(mu_file)
    langs = sorted({k.split("|")[0] for k in data.files})
    mu = {lang: [data[f"{lang}|{i}"] for i in range(
        sum(1 for k in data.files if k.startswith(lang + "|")))] for lang in langs}
    windows = json.loads(win_file.read_text(encoding="utf-8"))["windows"]

    band_lo, band_hi = cfg["measurement"]["layer_indexing"]["band_block_indices"]
    excluded = set(cfg["measurement"]["layer_indexing"]["excluded_from_measurement"])
    seed = cfg["seeds"]["permutation_tests"]
    scenarios = load_scenarios()
    budget = cfg["measurement"]["token_budget"]

    ckpt = OUT_DIR / "dlag_sentence.checkpoint.jsonl"
    done = set()
    if ckpt.exists():
        for line in ckpt.read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            done.add((r["scenario_id"], r["variant"], r["null"]))
        print(f"[dlag-sent] wznowienie: {len(done)} tekstow policzonych", flush=True)

    plan = plan_texts(scenarios, include_nulls=True)
    t0 = time.time()
    for item in plan:
        key = (item["scenario_id"], item["variant"], item["null"])
        if key in done:
            continue
        sc = next(s for s in scenarios if s["scenario_id"] == item["scenario_id"])
        built = build_scenario(sc, tc, budget=budget)
        turns = variant_turns(built, item["variant"], item["null"], seed)

        free_b, total_b = torch.cuda.mem_get_info()
        check_foreign_vram(total_b, free_b, torch.cuda.memory_allocated())

        enc, keep, sent_ids = sentence_ids_for_text(tok, turns)
        enc = {k: v.to("cuda:0") for k, v in enc.items()}
        torch.cuda.reset_peak_memory_stats()
        with torch.no_grad():
            out = model(**enc, output_hidden_states=True)
        check_peak_memory(torch.cuda.max_memory_allocated(),
                          cfg["compute"]["memory_guard_limit_gb"], "bf16")

        n = windows[sc["scenario_id"]]
        lang = sc["language"]
        rows = []
        for hs_idx in range(1, len(out.hidden_states)):
            if hs_idx in excluded:
                continue
            block = hs_idx - 1
            if not (band_lo <= block <= band_hi):
                continue
            arr = out.hidden_states[hs_idx][0].float().cpu().numpy()[keep][:n]
            # mu[lang] ma 34 elementy o indeksach rownych indeksom hidden_states
            # 0..33 (wykluczona jest wylacznie warstwa 34) - patrz runner pass 1
            mu_arr = mu[lang][hs_idx]
            Z, _ = zscore_channels(arr - mu_arr[:n])
            z = d_lag_sentence(Z, sent_ids[:n],
                               n_permutations=cfg["analysis"]["d_lag_permutations"],
                               rng=np.random.default_rng([seed, 7, hs_idx]))
            rows.append({**item, "hidden_state_index": hs_idx, "block": block,
                         "T_prime": n, "D_lag_sentence": z,
                         "n_sentences": int(len(set(sent_ids[:n])) - (1 if -1 in sent_ids[:n] else 0))})
        del out
        torch.cuda.empty_cache()
        with ckpt.open("a", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        el = time.time() - t0
        print(f"  {item['scenario_id']} {item['variant']}"
              f"{'/' + item['null'] if item['null'] else ''} ({el:.0f} s)", flush=True)

    import pandas as pd
    rows = [json.loads(l) for l in ckpt.read_text(encoding="utf-8").splitlines()]
    pd.DataFrame(rows).to_parquet(OUT_DIR / "dlag_sentence.parquet", index=False)
    print(f"[dlag-sent] zapisane: {len(rows)} wierszy", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
