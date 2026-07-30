"""Przeliczenie D_discourse dla calego pilota (definicja zamrozona, runda 3).

Uruchamiane PO zamrozeniu definicji w docs/SPEKTRA-1-rozstrzygniecia-runda3.md.
Regula niezmiennosci: wynik tego biegu NIE moze juz zmienic definicji metryki.

    python -m pipeline.discourse_run
Checkpoint per tekst, wznawianie ta sama komenda. Koszt: ~208 forwardow bez
permutacji tokenowych (null dyskursu liczy sie na macierzach J x J) - minuty.
"""

import json
import sys
import time
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from corpus.build import build_scenario
from corpus.tokens import TokenCounter
from pipeline.dlag_sentence_run import sentence_ids_for_text
from pipeline.memory_guard import check_foreign_vram, check_peak_memory
from pipeline.metrics import d_discourse, sentence_representations
from pipeline.preprocess import zscore_channels
from pipeline.runner import load_scenarios, plan_texts, variant_turns

OUT_DIR = REPO / "measurements"


def main():
    import yaml

    cfg = yaml.safe_load((REPO / "config.yaml").read_text(encoding="utf-8"))

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    name, rev = cfg["model"]["hf_name"], cfg["model"]["hf_revision"]
    print(f"[discourse] {name} @ {rev[:12]}", flush=True)
    tok = AutoTokenizer.from_pretrained(name, revision=rev)
    model = AutoModelForCausalLM.from_pretrained(name, revision=rev,
                                                 dtype=torch.bfloat16,
                                                 device_map="cuda:0")
    model.eval()

    tc = TokenCounter.load()
    if not tc.exact:
        print("[discourse] STOP: brak tokenizera")
        return 1
    data = np.load(OUT_DIR / "positional_mu.npz")
    langs = sorted({k.split("|")[0] for k in data.files})
    mu = {lang: [data[f"{lang}|{i}"] for i in range(
        sum(1 for k in data.files if k.startswith(lang + "|")))] for lang in langs}
    windows = json.loads((OUT_DIR / "windows.json").read_text(encoding="utf-8"))["windows"]

    band_lo, band_hi = cfg["measurement"]["layer_indexing"]["band_block_indices"]
    seed = cfg["seeds"]["permutation_tests"]
    scenarios = load_scenarios()
    budget = cfg["measurement"]["token_budget"]

    ckpt = OUT_DIR / "discourse.checkpoint.jsonl"
    done = set()
    if ckpt.exists():
        for line in ckpt.read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            done.add((r["scenario_id"], r["variant"], r["null"]))
        print(f"[discourse] wznowienie: {len(done)} tekstow", flush=True)

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
        for hs_idx in range(band_lo + 1, band_hi + 2):   # hidden_states pasma
            arr = out.hidden_states[hs_idx][0].float().cpu().numpy()[keep][:n]
            Z, _ = zscore_channels(arr - mu[lang][hs_idx][:n])
            S = sentence_representations(Z, sent_ids[:n])
            res = d_discourse(S, n_permutations=cfg["analysis"]["d_lag_permutations"],
                              rng=np.random.default_rng([seed, 11, hs_idx]))
            rows.append({**item, "hidden_state_index": hs_idx,
                         "block": hs_idx - 1, "T_prime": n, **res})
        del out
        torch.cuda.empty_cache()
        with ckpt.open("a", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"  {item['scenario_id']} {item['variant']}"
              f"{'/' + item['null'] if item['null'] else ''} "
              f"({time.time() - t0:.0f} s)", flush=True)

    import pandas as pd
    rows = [json.loads(l) for l in ckpt.read_text(encoding="utf-8").splitlines()]
    pd.DataFrame(rows).to_parquet(OUT_DIR / "discourse.parquet", index=False)
    print(f"[discourse] zapisane: {len(rows)} wierszy", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
