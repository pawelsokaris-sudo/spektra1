"""T5: null symulacyjny czas x kanal + progi lambda* (protokol par. 5-6).

Model separowalny: AR(1) po tokenach (phi per jezyk x warstwa, estymowane
z pilota jako srednia autokorelacja lag-1 kanalow po z-score) x iid kanaly.
Null przechodzi przez IDENTYCZNY pipeline (z-score -> Gram -> eigh).
Kwantyle 99% lambda_max per (warstwa, jezyk, T' scenariusza) - per scenariusz
zgodnie z uwaga zewnetrzna nr 2 (podloga szumu zalezy od T'/D, T' 811-1014).

Uruchamiac na maszynie pomiarowej:
    python -m pipeline.t5_null_run
Etap 1 (GPU, minuty): 80 forwardow tekstow glownych -> estymata phi.
Etap 2 (CPU, godziny): symulacja nulli, checkpoint per (scenariusz, warstwa).
"""

import json
import sys
import time
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from corpus.build import VARIANTS, build_scenario
from corpus.tokens import TokenCounter
from pipeline.dlag_sentence_run import sentence_ids_for_text
from pipeline.preprocess import zscore_channels
from pipeline.runner import load_scenarios, variant_turns

OUT_DIR = REPO / "measurements"
N_NULL = 600          # realizacji na (scenariusz, warstwa); q99 raportowane z ta licznoscia
QUANTILE = 0.99
D_MODEL = 2560


def estimate_phi():
    """Etap 1: phi(jezyk, warstwa) = srednia autokorelacja lag-1 kanalow Z."""
    import torch
    import yaml
    from transformers import AutoModelForCausalLM, AutoTokenizer

    cfg = yaml.safe_load((REPO / "config.yaml").read_text(encoding="utf-8"))
    tok = AutoTokenizer.from_pretrained(cfg["model"]["hf_name"],
                                        revision=cfg["model"]["hf_revision"])
    model = AutoModelForCausalLM.from_pretrained(
        cfg["model"]["hf_name"], revision=cfg["model"]["hf_revision"],
        dtype=torch.bfloat16, device_map="cuda:0")
    model.eval()
    tc = TokenCounter.load()
    data = np.load(OUT_DIR / "positional_mu.npz")
    mu = {lang: [data[f"{lang}|{i}"] for i in range(
        sum(1 for k in data.files if k.startswith(lang + "|")))]
        for lang in sorted({k.split("|")[0] for k in data.files})}
    windows = json.loads((OUT_DIR / "windows.json").read_text(encoding="utf-8"))["windows"]
    band_lo, band_hi = cfg["measurement"]["layer_indexing"]["band_block_indices"]
    seed = cfg["seeds"]["permutation_tests"]

    acc = {}
    for sc in load_scenarios():
        built = build_scenario(sc, tc, budget=cfg["measurement"]["token_budget"])
        for v in VARIANTS:
            enc, keep, _ = sentence_ids_for_text(tok, variant_turns(built, v, None, seed))
            enc = {k: t.to("cuda:0") for k, t in enc.items()}
            with torch.no_grad():
                out = model(**enc, output_hidden_states=True)
            n = windows[sc["scenario_id"]]
            for hs in range(band_lo + 1, band_hi + 2):
                arr = out.hidden_states[hs][0].float().cpu().numpy()[keep][:n]
                Z, _ = zscore_channels(arr - mu[sc["language"]][hs][:n])
                phi = float(np.mean(np.sum(Z[1:] * Z[:-1], axis=0)
                                    / np.sqrt(np.sum(Z[1:]**2, axis=0)
                                              * np.sum(Z[:-1]**2, axis=0))))
                acc.setdefault((sc["language"], hs), []).append(phi)
            del out
            torch.cuda.empty_cache()
        print(f"  phi: {sc['scenario_id']}", flush=True)
    table = {f"{lang}|{hs}": float(np.mean(v)) for (lang, hs), v in acc.items()}
    (OUT_DIR / "t5_phi.json").write_text(json.dumps(table, indent=1))
    return table


def simulate(table):
    """Etap 2: lambda* per (scenariusz, warstwa) - checkpoint per para."""
    import yaml
    cfg = yaml.safe_load((REPO / "config.yaml").read_text(encoding="utf-8"))
    windows = json.loads((OUT_DIR / "windows.json").read_text(encoding="utf-8"))["windows"]
    band_lo, band_hi = cfg["measurement"]["layer_indexing"]["band_block_indices"]
    langs = {s["scenario_id"]: s["language"] for s in load_scenarios()}

    ckpt = OUT_DIR / "t5_lambda_star.checkpoint.jsonl"
    done = set()
    if ckpt.exists():
        done = {(json.loads(l)["scenario_id"], json.loads(l)["hidden_state_index"])
                for l in ckpt.read_text(encoding="utf-8").splitlines()}
    t0 = time.time()
    for sid, n in windows.items():
        lang = langs[sid]
        for hs in range(band_lo + 1, band_hi + 2):
            if (sid, hs) in done:
                continue
            phi = table[f"{lang}|{hs}"]
            rng = np.random.default_rng([20260731, hash(sid) % 2**31, hs])
            scale = np.sqrt(1 - phi**2)
            lam_max = np.empty(N_NULL)
            for r in range(N_NULL):
                E = rng.standard_normal((n, D_MODEL))
                Z = np.empty_like(E)
                Z[0] = E[0]
                for t in range(1, n):
                    Z[t] = phi * Z[t - 1] + scale * E[t]
                Zs, _ = zscore_channels(Z)
                G = (Zs @ Zs.T) / n
                lam_max[r] = np.linalg.eigvalsh(G)[-1]
            row = {"scenario_id": sid, "language": lang, "hidden_state_index": hs,
                   "T_prime": n, "phi": phi, "n_null": N_NULL,
                   "lambda_star": float(np.quantile(lam_max, QUANTILE)),
                   "lam_max_mean": float(lam_max.mean()),
                   "lam_max_sd": float(lam_max.std(ddof=1))}
            with ckpt.open("a", encoding="utf-8") as f:
                f.write(json.dumps(row) + "\n")
            print(f"  {sid} hs={hs} lambda*={row['lambda_star']:.3f} "
                  f"({time.time() - t0:.0f} s)", flush=True)
    import pandas as pd
    rows = [json.loads(l) for l in ckpt.read_text(encoding="utf-8").splitlines()]
    pd.DataFrame(rows).to_parquet(OUT_DIR / "t5_lambda_star.parquet", index=False)
    print(f"[t5] zapisane: {len(rows)} progow", flush=True)


def main():
    phi_file = OUT_DIR / "t5_phi.json"
    if phi_file.exists():
        table = json.loads(phi_file.read_text(encoding="utf-8"))
        print("[t5] phi z checkpointu", flush=True)
    else:
        table = estimate_phi()
    simulate(table)
    return 0


if __name__ == "__main__":
    sys.exit(main())
