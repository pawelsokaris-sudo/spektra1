"""GATE 3 - odpornosc wyniku (protokol par. 7).

Napisany PRZED biegami kontrolnymi, tak samo jak GATE 2 przed progami.
Powod jest praktyczny, nie ceremonialny: kryteria odpornosci sa progami
liczbowymi, a progi ogladane po wyniku maja zwyczaj sie przesuwac.

TRZY KRYTERIA (protokol par. 7, GATE 3):
  a) bf16 vs fp32 na podzbiorze: |delta I_total| < 0.005 per tekst
     (tolerancja zamrozona w par. 2) ORAZ znak Delta_1 ten sam
     i |zmiana estymaty| <= 25%
  b) z/bez odejmowania komponentu pozycyjnego: znak i <= 25%
  c) obie repliki jezykowe osobno: znak i <= 25%

Niepowodzenie NIE uniewaznia wyniku - klasyfikuje go jako "niestabilny"
i tak zostaje opublikowany (par. 7 wprost).

OGRANICZENIE ZAMIERZONE (zlecenie DEP-08): progi lambda* NIE sa przeliczane
dla biegow kontrolnych - to kolejny dzien maszyny, a kryteria dotycza znaku
i wzglednej zmiany. Skutek: kryterium ZNAKU jest mocne, kryterium WIELKOSCI
przybliżone. Raport mowi to wprost zamiast udawac, ze mamy jedno i drugie.

Uruchomienie:
    python -m gates.gate3
"""

import argparse
import json
from pathlib import Path

import numpy as np

from gates.gate2 import (load_band, load_lambda_star, load_spectra,
                         paired_diffs, per_text_endpoints)

DTYPE_TOLERANCE = 0.005     # par. 2, zamrozona
MAX_REL_CHANGE = 0.25       # par. 7, zamrozona
PAIR = ("C", "CprimG")


def delta1(df, lang, scenarios=None):
    """Delta_1 = srednia parowana Ī(C) - Ī(C'-G), opcjonalnie na podzbiorze."""
    d = df if scenarios is None else df[df.scenario_id.isin(scenarios)]
    diffs, scen = paired_diffs(d, lang, *PAIR)
    return float(diffs.mean()), diffs, scen


def relative_change(base, other):
    """|zmiana| wzgledem biegu glownego. Nieokreslona przy zerowej bazie."""
    if base == 0:
        return float("inf")
    return abs((other - base) / base)


def compare_run(main_df, ctrl_df, label):
    """Porownanie biegu kontrolnego z glownym NA TYCH SAMYCH scenariuszach."""
    out = {"bieg": label, "repliki": [], "kryterium_spelnione": True}
    for lang in sorted(ctrl_df.language.unique()):
        scen = sorted(set(ctrl_df[ctrl_df.language == lang].scenario_id))
        base, base_diffs, _ = delta1(main_df, lang, scen)
        ctrl, ctrl_diffs, _ = delta1(ctrl_df, lang, scen)
        rel = relative_change(base, ctrl)
        same_sign = bool(np.sign(base) == np.sign(ctrl) and base != 0)
        ok = bool(same_sign and rel <= MAX_REL_CHANGE)
        out["repliki"].append({
            "language": lang, "n_scenarios": len(scen),
            "delta1_glowny": base, "delta1_kontrolny": ctrl,
            "zmiana_wzgledna": rel, "znak_ten_sam": same_sign,
            "spelnione": ok,
        })
        out["kryterium_spelnione"] &= ok
    return out


def dtype_tolerance_check(main_df, fp32_df):
    """Per tekst: |I_total(bf16) - I_total(fp32)| < 0.005 (par. 2).

    To jest kontrola SUROWSZA niz kryterium kontrastowe: sprawdza sam pomiar,
    nie tylko roznice miedzy wariantami. Przekroczenie = stop i diagnoza.
    """
    key = ["scenario_id", "language", "variant"]
    m = main_df[main_df["null"].isna()].set_index(key).iota
    f = fp32_df[fp32_df["null"].isna()].set_index(key).iota
    wspolne = m.index.intersection(f.index)
    d = (m.loc[wspolne] - f.loc[wspolne]).abs()
    przekroczenia = [{"tekst": list(k), "delta": float(v)}
                     for k, v in d[d >= DTYPE_TOLERANCE].items()]
    return {"n_tekstow": int(len(wspolne)), "max_delta": float(d.max()) if len(d) else 0.0,
            "srednia_delta": float(d.mean()) if len(d) else 0.0,
            "tolerancja": DTYPE_TOLERANCE, "n_przekroczen": len(przekroczenia),
            "przekroczenia": przekroczenia[:10],
            "spelnione": bool(len(przekroczenia) == 0)}


def replica_agreement(main_df):
    """Kryterium (c): zgodnosc miedzy replikami, liczona z pomiaru glownego."""
    vals = {lang: delta1(main_df, lang)[0] for lang in sorted(main_df.language.unique())}
    langs = sorted(vals)
    if len(langs) != 2:
        return {"repliki": vals, "spelnione": None,
                "uwaga": "kryterium zdefiniowane dla dwoch replik"}
    a, b = vals[langs[0]], vals[langs[1]]
    same_sign = bool(np.sign(a) == np.sign(b) and a != 0)
    # zmiana wzgledem WIEKSZEJ co do modulu - inaczej wynik zalezalby od tego,
    # ktora replike nazwiemy pierwsza
    baza = a if abs(a) >= abs(b) else b
    rel = relative_change(baza, b if abs(a) >= abs(b) else a)
    return {"repliki": vals, "znak_ten_sam": same_sign, "zmiana_wzgledna": rel,
            "spelnione": bool(same_sign and rel <= MAX_REL_CHANGE)}


def werdykt(kryteria, wymagane=("a_dtype", "b_pozycyjny", "c_repliki")):
    """STABILNY tylko przy KOMPLECIE spelnionych kryteriow.

    Rzecz, ktora latwo przeoczyc: jesli brakuje biegu kontrolnego, a te obecne
    przechodza, naiwny rachunek oglasza stabilnosc na podstawie czesci sprawdzen.
    Brak danych NIE jest wynikiem pozytywnym. Odwrotnie jest dozwolone: jedno
    niespelnione kryterium wystarcza, zeby orzec niestabilnosc - dalsze biegi
    juz tego nie odwroca.
    """
    obecne = {k: v for k, v in kryteria.items() if "brak_danych" not in (v or {})}
    wyniki = [v.get("spelnione", v.get("kryterium_spelnione")) for v in obecne.values()]
    if any(w is False for w in wyniki):
        return "NIESTABILNY"
    if set(wymagane) - set(obecne):
        return "NIEKOMPLETNY"
    return "STABILNY" if all(wyniki) else "NIESTABILNY"


def endpoints_for(measurements_dir, lam, band):
    return per_text_endpoints(load_spectra(measurements_dir), lam, band)


def main():
    ap = argparse.ArgumentParser(description="GATE 3 - odpornosc")
    ap.add_argument("--main", default="measurements-glowny")
    ap.add_argument("--fp32", default="measurements-glowny/gate3-fp32")
    ap.add_argument("--nopos", default="measurements-glowny/gate3-nopos")
    ap.add_argument("--out", default="measurements-glowny/gate3_results.json")
    args = ap.parse_args()

    band, _ = load_band(args.main)
    lam = load_lambda_star(args.main)          # progi z biegu glownego, celowo
    main_df = endpoints_for(args.main, lam, band)

    res = {"tolerancja_dtype": DTYPE_TOLERANCE, "max_zmiana_wzgledna": MAX_REL_CHANGE,
           "lambda_star": "z biegu glownego (progi NIE przeliczane - DEP-08)",
           "kryteria": {}}

    res["kryteria"]["c_repliki"] = replica_agreement(main_df)

    for klucz, sciezka, etykieta in (("a_dtype", args.fp32, "fp32 wobec bf16"),
                                     ("b_pozycyjny", args.nopos,
                                      "bez komponentu pozycyjnego")):
        p = Path(sciezka)
        if not p.exists():
            res["kryteria"][klucz] = {"brak_danych": str(p)}
            continue
        ctrl = endpoints_for(p, lam, band)
        res["kryteria"][klucz] = compare_run(main_df, ctrl, etykieta)
        if klucz == "a_dtype":
            res["kryteria"][klucz]["tolerancja_per_tekst"] = \
                dtype_tolerance_check(main_df, ctrl)

    res["werdykt"] = werdykt(res["kryteria"])

    Path(args.out).write_text(json.dumps(res, indent=2, ensure_ascii=False),
                              encoding="utf-8")
    print(f"[gate3] zapisane: {args.out}")
    for k, v in res["kryteria"].items():
        if "brak_danych" in v:
            print(f"[gate3] {k}: BRAK DANYCH ({v['brak_danych']})")
        else:
            print(f"[gate3] {k}: {'OK' if v.get('spelnione', v.get('kryterium_spelnione')) else 'NIE'}")
    print(f"[gate3] WERDYKT: {res['werdykt']}")


if __name__ == "__main__":
    main()
