"""Kwalifikacja sprzetu pod replikacje SPEKTRA-1 (uruchamiane przez agenta).

Odpowiada na jedno pytanie: czy TA maszyna moze wykonac pomiar spelniajacy
rygor pieczeci. Nie zaklada CUDA - wykrywa urzadzenie sama (cuda / mps / cpu).

Piec testow, kazdy z jawnym werdyktem:
  A. Srodowisko i sprzet (opisowe, do pieczeci repliki)
  B. GATE 0 numeryczny - bialy szum przez pipeline odtwarza Marchenko-Pastura
     (czysta numeryka, dziala wszedzie; jesli to padnie, problem jest powazny)
  C. Powtarzalnosc forwardu CO DO BITU - dwa identyczne przebiegi modelu
  D. Zgodnosc struktury modelu z zapieczetowana (35 stanow, hidden 2560)
  E. Tempo - sekundy na tekst 1024 tokenow (planowanie sesji)

Kod wyjscia 0 = kwalifikuje sie. 1 = nie kwalifikuje sie albo wymaga decyzji
zespolu. Obie odpowiedzi sa poprawnym wynikiem.
"""

import json
import os
import platform
import sys
import time
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from pipeline.preprocess import mask_tokens, zscore_channels
from pipeline.spectrum import gram_eigenvalues

# hf-xet wywraca snapshot_download na Apple Silicon (zgloszone z maszyny M5 Max,
# 2026-08-01): "Unable to parse string as hex hash value". Zwykly HTTPS przechodzi,
# bajty identyczne (test F to potwierdza). Ustawiane zanim cokolwiek pobierzemy.
os.environ.setdefault("HF_HUB_DISABLE_XET", "1")

MODEL = "google/gemma-3-4b-it"
REVISION = "093f9f388b31de276ce2de164bdc2081324b9767"
EXPECTED_HIDDEN_STATES = 35
EXPECTED_HIDDEN_SIZE = 2560
OUT_MD = Path(__file__).resolve().parent / "RAPORT-KWALIFIKACJA.md"
OUT_JSON = Path(__file__).resolve().parent / "RAPORT-KWALIFIKACJA.json"

PROBE = ("Zbiornik na deszczowke stoi przy scianie i zbiera wode z polaci dachu. "
         "Rynna schodzi do filtra, a przelew idzie do ogrodu. ") * 40


def pick_device(torch):
    if torch.cuda.is_available():
        return "cuda", torch.bfloat16
    if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        return "mps", torch.bfloat16
    return "cpu", torch.float32


def test_a_srodowisko(torch, device):
    info = {
        "system": platform.platform(),
        "processor": platform.processor() or platform.machine(),
        "python": platform.python_version(),
        "torch": torch.__version__,
        "device": device,
    }
    try:
        import transformers
        info["transformers"] = transformers.__version__
    except Exception as exc:
        info["transformers"] = f"BRAK ({exc})"
    if device == "cuda":
        info["gpu"] = torch.cuda.get_device_name(0)
        info["pamiec_gb"] = round(torch.cuda.get_device_properties(0).total_memory / 2**30, 2)
    else:
        try:
            import subprocess
            if platform.system() == "Darwin":
                chip = subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"],
                                      capture_output=True, text=True).stdout.strip()
                mem = subprocess.run(["sysctl", "-n", "hw.memsize"],
                                     capture_output=True, text=True).stdout.strip()
                info["gpu"] = chip or "Apple Silicon"
                info["pamiec_gb"] = round(int(mem) / 2**30, 2) if mem else None
        except Exception:
            info["gpu"] = "nieznany"
    return info


def test_b_gate0():
    """Bialy szum przez pipeline odtwarza krawedzie Marchenko-Pastura."""
    rng = np.random.default_rng(20260801)
    t_prime, d = 400, 1000
    H = rng.standard_normal((t_prime + 32, d))
    Z, _ = zscore_channels(mask_tokens(H, skip_first=32))
    eigs = gram_eigenvalues(Z)
    gamma = d / t_prime
    lo, hi = (1 - np.sqrt(gamma))**2, (1 + np.sqrt(gamma))**2
    obs_lo, obs_hi = float(eigs.min()), float(eigs.max())
    ok = obs_lo >= lo * 0.9 and obs_hi <= hi * 1.1
    return {"pass": bool(ok), "krawedzie_teoria": [lo, hi],
            "krawedzie_pomiar": [obs_lo, obs_hi],
            "slad_vs_D": round(float(eigs.sum()) / d, 4)}


def test_f_wagi():
    """Czy pobrane wagi to CO DO BAJTU te, na ktorych zmierzono badanie glowne.

    Sumy kontrolne pochodza z zapieczetowanego config.yaml. To zamienia
    'ten sam model wg nazwy' w 'te same bajty' - bez tego replikacja
    opierala by sie na zaufaniu do nazwy katalogu.
    """
    import hashlib
    import yaml
    from huggingface_hub import snapshot_download

    cfg = yaml.safe_load((REPO / "config.yaml").read_text(encoding="utf-8"))
    oczekiwane = dict(cfg["model"]["weights_sha256"])
    oczekiwane.update(cfg["model"]["tokenizer_files_sha256"])
    snap = Path(snapshot_download(MODEL, revision=REVISION,
                                  allow_patterns=list(oczekiwane)))
    wyniki, zgodne = {}, True
    for nazwa, oczek in oczekiwane.items():
        plik = snap / nazwa
        if not plik.is_file():
            wyniki[nazwa] = "BRAK PLIKU"
            zgodne = False
            continue
        h = hashlib.sha256()
        with plik.open("rb") as f:
            for blok in iter(lambda: f.read(8 * 1024 * 1024), b""):
                h.update(blok)
        ok = h.hexdigest() == oczek
        wyniki[nazwa] = "zgodna" if ok else f"ROZNI SIE ({h.hexdigest()[:16]}...)"
        zgodne &= ok
    return {"pass": bool(zgodne), "snapshot": str(snap), "pliki": wyniki}


def test_cde_model(torch, device, dtype):
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tok = AutoTokenizer.from_pretrained(MODEL, revision=REVISION)
    model = AutoModelForCausalLM.from_pretrained(MODEL, revision=REVISION, dtype=dtype)
    model = model.to(device).eval()
    enc = tok(PROBE, return_tensors="pt", add_special_tokens=False)
    enc = {k: v[:, :1024].to(device) for k, v in enc.items()}

    t0 = time.time()
    with torch.no_grad():
        out1 = model(**enc, output_hidden_states=True)
    t_first = time.time() - t0
    with torch.no_grad():
        out2 = model(**enc, output_hidden_states=True)
    t_second = time.time() - t0 - t_first

    a = out1.hidden_states[20].float().cpu().numpy()
    b = out2.hidden_states[20].float().cpu().numpy()
    identyczne = bool(np.array_equal(a, b))
    maxdiff = float(np.abs(a - b).max())

    struktura = {
        "n_hidden_states": len(out1.hidden_states),
        "hidden_size": int(out1.hidden_states[0].shape[-1]),
        "dtype": str(out1.hidden_states[0].dtype),
        "n_tokenow": int(enc["input_ids"].shape[1]),
    }
    zgodna = (struktura["n_hidden_states"] == EXPECTED_HIDDEN_STATES
              and struktura["hidden_size"] == EXPECTED_HIDDEN_SIZE)
    return (
        {"pass": identyczne, "max_abs_diff": maxdiff,
         "uwaga": ("powtarzalnosc CO DO BITU" if identyczne else
                   "BRAK powtarzalnosci bitowej - decyzja zespolu (mozliwy pomiar na CPU)")},
        {"pass": bool(zgodna), **struktura,
         "oczekiwane": {"n_hidden_states": EXPECTED_HIDDEN_STATES,
                        "hidden_size": EXPECTED_HIDDEN_SIZE}},
        {"sekundy_pierwszy_forward": round(t_first, 2),
         "sekundy_kolejny_forward": round(t_second, 2),
         "szacunek_godzin_624_teksty": round(t_second * 624 * 2 / 3600, 1)},
    )


def main():
    wynik = {"model": MODEL, "revision": REVISION}
    try:
        import torch
    except Exception as exc:
        print(f"BRAK PyTorch: {exc}")
        return 1
    device, dtype = pick_device(torch)
    print(f"[kwalifikacja] urzadzenie: {device}, dtype: {dtype}", flush=True)

    wynik["A_srodowisko"] = test_a_srodowisko(torch, device)
    print("[kwalifikacja] A: srodowisko opisane", flush=True)

    wynik["B_gate0"] = test_b_gate0()
    print(f"[kwalifikacja] B: GATE 0 numeryczny -> "
          f"{'PASS' if wynik['B_gate0']['pass'] else 'FAIL'}", flush=True)

    try:
        wynik["F_wagi"] = test_f_wagi()
        print(f"[kwalifikacja] F: sumy kontrolne wag -> "
              f"{'PASS' if wynik['F_wagi']['pass'] else 'FAIL'}", flush=True)
    except Exception as exc:
        wynik["F_wagi"] = {"pass": False, "blad": f"{type(exc).__name__}: {exc}"}
        print(f"[kwalifikacja] F: nie udalo sie zweryfikowac wag: {exc}", flush=True)

    try:
        c, d, e = test_cde_model(torch, device, dtype)
        wynik["C_powtarzalnosc"], wynik["D_struktura"], wynik["E_tempo"] = c, d, e
        print(f"[kwalifikacja] C: powtarzalnosc -> {'PASS' if c['pass'] else 'FAIL'}", flush=True)
        print(f"[kwalifikacja] D: struktura modelu -> {'PASS' if d['pass'] else 'FAIL'}", flush=True)
        print(f"[kwalifikacja] E: {e['sekundy_kolejny_forward']} s/tekst, "
              f"szacunek {e['szacunek_godzin_624_teksty']} h na pelny pomiar", flush=True)
    except Exception as exc:
        wynik["blad_modelu"] = f"{type(exc).__name__}: {exc}"
        print(f"[kwalifikacja] BLAD przy modelu: {exc}", flush=True)

    kwalifikuje = (wynik.get("B_gate0", {}).get("pass")
                   and wynik.get("C_powtarzalnosc", {}).get("pass")
                   and wynik.get("D_struktura", {}).get("pass")
                   and wynik.get("F_wagi", {}).get("pass"))
    wynik["werdykt"] = "KWALIFIKUJE SIE" if kwalifikuje else "WYMAGA DECYZJI ZESPOLU"

    OUT_JSON.write_text(json.dumps(wynik, indent=2, ensure_ascii=False), encoding="utf-8")
    zapisz_md(wynik)
    print(f"[kwalifikacja] WERDYKT: {wynik['werdykt']}", flush=True)
    print(f"[kwalifikacja] raport: {OUT_MD}", flush=True)
    return 0 if kwalifikuje else 1


def zapisz_md(w):
    a = w.get("A_srodowisko", {})
    L = [f"# Raport kwalifikacji sprzętu — SPEKTRA-1", "",
         f"**Werdykt: {w['werdykt']}**", "",
         f"Maszyna: {a.get('gpu','?')} | pamięć: {a.get('pamiec_gb','?')} GB | "
         f"urządzenie obliczeniowe: `{a.get('device','?')}`",
         f"System: {a.get('system','?')} | Python {a.get('python','?')} | "
         f"torch {a.get('torch','?')} | transformers {a.get('transformers','?')}", "",
         "| Test | Wynik |", "|---|---|"]
    b = w.get("B_gate0")
    if b:
        L.append(f"| B. GATE 0 (białe widmo vs teoria) | {'PASS' if b['pass'] else 'FAIL'} — "
                 f"krawędzie pomiar {b['krawedzie_pomiar'][0]:.3f}–{b['krawedzie_pomiar'][1]:.3f} "
                 f"wobec teorii {b['krawedzie_teoria'][0]:.3f}–{b['krawedzie_teoria'][1]:.3f} |")
    c = w.get("C_powtarzalnosc")
    if c:
        L.append(f"| C. Powtarzalność forwardu | {'PASS' if c['pass'] else 'FAIL'} — "
                 f"max różnica {c['max_abs_diff']:.2e}; {c['uwaga']} |")
    f = w.get("F_wagi")
    if f:
        szczegol = (f"wszystkie {len(f.get('pliki',{}))} plików zgodnych co do bajtu"
                    if f["pass"] else f.get("blad") or
                    "; ".join(f"{k}: {v}" for k, v in f.get("pliki", {}).items() if v != "zgodna"))
        L.append(f"| F. Sumy kontrolne wag i tokenizera | "
                 f"{'PASS' if f['pass'] else 'FAIL'} — {szczegol} |")
    d = w.get("D_struktura")
    if d:
        L.append(f"| D. Struktura modelu | {'PASS' if d['pass'] else 'FAIL'} — "
                 f"{d['n_hidden_states']} stanów, wymiar {d['hidden_size']}, {d['dtype']} |")
    e = w.get("E_tempo")
    if e:
        L.append(f"| E. Tempo | {e['sekundy_kolejny_forward']} s/tekst → "
                 f"~{e['szacunek_godzin_624_teksty']} h na pełny pomiar (624 teksty × 2 przebiegi) |")
    if "blad_modelu" in w:
        L += ["", f"**Błąd przy modelu:** `{w['blad_modelu']}`"]
    L += ["", "## Co ten werdykt znaczy", "",
          "- **KWALIFIKUJE SIĘ** — maszyna liczy powtarzalnie i zgodnie z teorią; "
          "można na niej wykonać replikację spełniającą rygor pieczęci.",
          "- **WYMAGA DECYZJI ZESPOŁU** — najczęściej brak powtarzalności co do bitu "
          "na akceleratorze. To NIE dyskwalifikuje maszyny: pomiar można wykonać na "
          "procesorze (wolniej, ale deterministycznie) albo zamrozić łagodniejsze "
          "kryterium replikacji. Decyzja należy do zespołu badawczego, nie do operatora.", ""]
    OUT_MD.write_text("\n".join(L), encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
