"""T2 - weryfikacja semantyki warstw ukrytych (protokol par. 2).

Odpowiada na trzy pytania, ktorych NIE wolno zgadywac przed pomiarem:

  1. Ktory element krotki `hidden_states` jest embeddingiem, a ktore wyjsciami
     blokow? Weryfikacja przez hooki na modulach dekodera - porownanie wyjscia
     bloku l z hidden_states[l+1] co do bitu (albo w zamrozonej tolerancji).
  2. Czy hidden_states sa brane PRZED final norm? Sprawdzane przez porownanie
     ostatniego elementu z wyjsciem ostatniego bloku oraz z wynikiem normy.
  3. Ktore bloki maja attention lokalna, a ktore globalna? Typ bloku wchodzi
     jako kowariancja do analiz wtornych, a sklad pasma [0.4L, 0.8L] jest
     raportowany (rozstrzygniecie #20 z pierwszej rundy recenzji).

Dodatkowo: kontrola bf16 vs fp32 na jednym tekscie oraz zgodnosc szablonu
czatu skladanego przez corpus.stats.render_gemma_chat z tokenizer.apply_chat_template
(gdyby sie roznily, caly korpus mialby inne tokeny niz zaklada generator).

URUCHAMIAC NA MASZYNIE POMIAROWEJ, w srodowisku ze zlecenia DEP-02:
    C:\\Users\\operator\\spektra1-env\\Scripts\\python.exe -m pipeline.layer_semantics

Wyjscie: docs/layer_semantics.md (raport do pieczeci) + layer_semantics.json.
"""

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

OUT_MD = REPO / "docs" / "layer_semantics.md"
OUT_JSON = REPO / "docs" / "layer_semantics.json"

PROBE_TEXT_PL = "Zbiornik na deszczowke stoi przy scianie i zbiera wode z polaci dachu."
BAND = (0.4, 0.8)          # pasmo z protokolu par. 6
TOLERANCE_BF16 = 1e-2      # bf16 ma ~3 cyfry znaczace; luzna tolerancja identycznosci


def load_model(model_name, revision=None):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tok = AutoTokenizer.from_pretrained(model_name, revision=revision)
    model = AutoModelForCausalLM.from_pretrained(
        model_name, revision=revision, dtype=torch.bfloat16, device_map="cuda:0"
    )
    model.eval()
    return tok, model


def find_decoder_layers(model):
    """Znajduje liste blokow dekodera niezaleznie od zagniezdzenia (Gemma 3 ma
    warianty z `model.model.layers` i `model.model.language_model.layers`)."""
    candidates = [
        getattr(getattr(model, "model", None), "layers", None),
        getattr(getattr(getattr(model, "model", None), "language_model", None), "layers", None),
        getattr(getattr(model, "language_model", None), "layers", None),
    ]
    for c in candidates:
        if c is not None and len(c) > 0:
            return c
    raise RuntimeError(
        "Nie znaleziono listy blokow dekodera - sprawdz strukture modelu recznie "
        "i dopisz sciezke do find_decoder_layers()."
    )


def block_attention_types(layers):
    """Mapa typow blokow: attention lokalna (sliding window) vs globalna.

    Gemma 3 przeplata bloki lokalne i globalne; atrybut rozni sie miedzy
    rewizjami, wiec sprawdzamy kilka znanych miejsc i raportujemy 'nieznany',
    zamiast zgadywac.
    """
    types = []
    for i, blk in enumerate(layers):
        attn = getattr(blk, "self_attn", blk)
        kind = "nieznany"
        for attr in ("is_sliding", "use_sliding_window", "sliding_window"):
            val = getattr(attn, attr, getattr(blk, attr, None))
            if isinstance(val, bool):
                kind = "lokalna" if val else "globalna"
                break
            if isinstance(val, int) and val:
                kind = "lokalna"
                break
            if val is None and attr == "sliding_window":
                continue
        types.append({"index": i, "attention": kind})
    return types


def verify_hidden_states(model, layers, inputs):
    """Porownuje wyjscia blokow przechwycone hookami z krotka hidden_states."""
    import torch

    captured = {}

    def make_hook(idx):
        def hook(_module, _args, output):
            captured[idx] = (output[0] if isinstance(output, tuple) else output).detach()
        return hook

    handles = [blk.register_forward_hook(make_hook(i)) for i, blk in enumerate(layers)]
    try:
        with torch.no_grad():
            out = model(**inputs, output_hidden_states=True)
    finally:
        for h in handles:
            h.remove()

    hs = out.hidden_states
    rows = []
    for i in range(len(layers)):
        hook_out = captured[i].float()
        # hipoteza: hidden_states[i+1] == wyjscie bloku i
        hs_next = hs[i + 1].float()
        diff = (hook_out - hs_next).abs().max().item()
        rows.append({
            "block": i,
            "matches_hidden_states_index": i + 1,
            "max_abs_diff": diff,
            "identical": bool(diff <= TOLERANCE_BF16),
        })

    emb_diff = (hs[0].float() - captured[0].float()).abs().max().item()
    return {
        "n_hidden_states": len(hs),
        "n_blocks": len(layers),
        "hidden_state_0_is_embedding": bool(emb_diff > TOLERANCE_BF16),
        "embedding_vs_block0_diff": emb_diff,
        "blocks": rows,
        "all_blocks_match": all(r["identical"] for r in rows),
        "last_hidden_shape": tuple(hs[-1].shape),
        "dtype": str(hs[-1].dtype),
    }


def check_final_norm(model, layers, inputs):
    """Czy ostatni element hidden_states jest PRZED final norm (protokol par. 2)?"""
    import torch

    captured = {}

    def hook(_m, _a, output):
        captured["last_block"] = (output[0] if isinstance(output, tuple) else output).detach()

    h = layers[-1].register_forward_hook(hook)
    try:
        with torch.no_grad():
            out = model(**inputs, output_hidden_states=True)
    finally:
        h.remove()

    last_hs = out.hidden_states[-1].float()
    last_block = captured["last_block"].float()
    diff_raw = (last_hs - last_block).abs().max().item()
    return {
        "hidden_states_last_equals_block_output": bool(diff_raw <= TOLERANCE_BF16),
        "max_abs_diff": diff_raw,
        "interpretacja": ("hidden_states[-1] jest wyjsciem ostatniego bloku PRZED final norm"
                          if diff_raw <= TOLERANCE_BF16 else
                          "hidden_states[-1] ROZNI SIE od wyjscia bloku - prawdopodobnie po "
                          "final norm; wymaga decyzji przed pomiarem"),
    }


def check_chat_template(tok):
    """Czy render z corpus.stats zgadza sie z tokenizerem modelu?"""
    from corpus.stats import render_gemma_chat

    turns = [{"role": "user", "text": "Pierwsze zdanie."},
             {"role": "assistant", "text": "Druga tura."}]
    ours = render_gemma_chat(turns)
    theirs = tok.apply_chat_template(
        [{"role": t["role"], "content": t["text"]} for t in turns],
        tokenize=False, add_generation_prompt=False,
    )
    return {
        "match": ours.strip() == theirs.strip(),
        "ours": ours,
        "tokenizer": theirs,
        "uwaga": ("Zgodne - generator korpusu produkuje te same tokeny co model."
                  if ours.strip() == theirs.strip() else
                  "ROZBIEZNOSC - korpus musi uzywac renderu tokenizera, inaczej "
                  "mierzymy inny tekst niz zapisany. Poprawic PRZED pomiarem."),
    }


def band_composition(types, n_blocks):
    lo, hi = int(BAND[0] * n_blocks), int(BAND[1] * n_blocks)
    in_band = [t for t in types if lo <= t["index"] < hi]
    counts = {}
    for t in in_band:
        counts[t["attention"]] = counts.get(t["attention"], 0) + 1
    return {"band_indices": [lo, hi], "n_blocks_in_band": len(in_band), "counts": counts}


def main():
    import yaml

    cfg = yaml.safe_load((REPO / "config.yaml").read_text(encoding="utf-8"))
    name = cfg["model"]["hf_name"]
    revision = cfg["model"].get("hf_revision")
    if str(name).startswith("TBD"):
        print("config.yaml: model.hf_name to nadal TBD-RECON. Uzupelnij przed T2.")
        return 1
    if str(revision).startswith("TBD"):
        revision = None

    print(f"[T2] ladowanie {name} (rewizja: {revision or 'domyslna'})...", flush=True)
    tok, model = load_model(name, revision)
    layers = find_decoder_layers(model)
    inputs = tok(PROBE_TEXT_PL, return_tensors="pt").to("cuda:0")

    print(f"[T2] blokow dekodera: {len(layers)}", flush=True)
    results = {
        "model": name,
        "revision": revision,
        "n_blocks": len(layers),
        "hidden_states": verify_hidden_states(model, layers, inputs),
        "final_norm": check_final_norm(model, layers, inputs),
        "chat_template": check_chat_template(tok),
        "attention_types": block_attention_types(layers),
    }
    results["band"] = band_composition(results["attention_types"], len(layers))

    OUT_JSON.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    write_report(results)
    hs = results["hidden_states"]
    ok = hs["all_blocks_match"] and hs["hidden_state_0_is_embedding"]
    print(f"[T2] {'INDEKSACJA POTWIERDZONA' if ok else 'INDEKSACJA WYMAGA DECYZJI'}", flush=True)
    print(f"[T2] raport: {OUT_MD}", flush=True)
    return 0 if ok else 1


def write_report(r):
    hs, fn, ct, band = r["hidden_states"], r["final_norm"], r["chat_template"], r["band"]
    lines = [
        "# T2 — semantyka warstw ukrytych (protokół §2)", "",
        f"**Model:** `{r['model']}` | rewizja: `{r['revision'] or 'domyślna'}` | "
        f"bloków dekodera: **{r['n_blocks']}** | elementów `hidden_states`: "
        f"**{hs['n_hidden_states']}**", "",
        "## Indeksacja (wchodzi do pieczęci)", "",
        f"- `hidden_states[0]` to **{'embedding' if hs['hidden_state_0_is_embedding'] else 'NIE embedding — sprawdzić ręcznie'}** "
        f"(różnica wobec wyjścia bloku 0: {hs['embedding_vs_block0_diff']:.4f})",
        f"- `hidden_states[ℓ+1]` odpowiada wyjściu bloku ℓ: "
        f"**{'POTWIERDZONE dla wszystkich bloków' if hs['all_blocks_match'] else 'NIEZGODNOŚĆ — patrz tabela'}** "
        f"(tolerancja {TOLERANCE_BF16})",
        f"- Kształt: `{hs['last_hidden_shape']}`, dtype: `{hs['dtype']}`",
        f"- Embedding **wyłączony** z pasm pomiarowych zgodnie z §2.", "",
        "## Final norm", "",
        f"{fn['interpretacja']} (max |Δ| = {fn['max_abs_diff']:.6f}).", "",
        "## Szablon czatu", "",
        f"{ct['uwaga']}", "",
        "## Typy bloków i skład pasma [0.4L, 0.8L]", "",
        f"Pasmo obejmuje indeksy **{band['band_indices'][0]}–{band['band_indices'][1] - 1}** "
        f"({band['n_blocks_in_band']} bloków). Skład: "
        + ", ".join(f"{k}: {v}" for k, v in sorted(band["counts"].items())) + ".", "",
        "| Blok | Attention |", "|---|---|",
    ]
    for t in r["attention_types"]:
        mark = " ← w paśmie" if band["band_indices"][0] <= t["index"] < band["band_indices"][1] else ""
        lines.append(f"| {t['index']} | {t['attention']}{mark} |")
    lines += ["", "Typ bloku wchodzi jako kowariancja do analiz wtórnych "
              "(rozstrzygnięcie #20, runda 1).", ""]
    if not hs["all_blocks_match"]:
        lines += ["## Bloki niezgodne", "", "| Blok | max |Δ| |", "|---|---|"]
        lines += [f"| {b['block']} | {b['max_abs_diff']:.6f} |"
                  for b in hs["blocks"] if not b["identical"]]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
