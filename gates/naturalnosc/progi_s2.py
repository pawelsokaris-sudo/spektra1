"""Progi bramki naturalnosci z probki korpusu SPEKTRY-2.

Material tej probki ma WLASCIWA konstrukcje: szesc wariantow dzieli rame
i rozni sie wylacznie fraza referenta (spec par. 2). Kalibracja na SPEKTRZE-1
tego nie miala - tam warianty byly osobnymi zdaniami. Stad przewidywanie,
ktore ta probka sprawdza: rozstep miedzy wariantami ma byc MNIEJSZY.

Scenariusze z probki sa WYLACZONE Z BADANIA (warunek niekolistosci).

Uruchomienie:
    python -m gates.naturalnosc.progi_s2
"""

import json
import statistics as st
import sys
from itertools import combinations
from pathlib import Path

from .kryteria import (BUDZET, WARIANTY, ocen_scenariusz, rachunek_osiagalnosci,
                       stale_z_rozkladu)

KATALOG = Path(__file__).resolve().parent
SKALE = ("naturalnosc", "jasnosc_odniesienia", "samozwrotnosc")

# Wartosci orientacyjne z kalibracji SPEKTRY-1 - sprawdzane, nie stosowane.
S1_PROG_NATURALNOSCI = {"pl": 3.22, "en": 3.78}
S1_ROZSTEP_WARIANTOW = {"pl": 3.27, "en": 2.52}


def wczytaj(sufiks=""):
    probka = json.loads(
        (KATALOG / f"probka-s2{sufiks}.json").read_text(encoding="utf-8"))
    meta = {e["id"]: e for e in probka["elementy"]}

    oceny = {}
    for p in sorted(KATALOG.glob(f"oceny-s2{sufiks}-*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        for o in d["oceny"]:
            oceny.setdefault(o["id"], {})[d["oceniajacy"]] = {
                s: o[s] for s in SKALE}

    braki = [i for i in meta if not oceny.get(i)]
    return meta, oceny, probka["wykluczone_z_badania"], braki


def scenariusze(meta, oceny, jezyk):
    """{scenariusz: {wariant: {naturalnosc, jasnosc, samozwrotnosc}}} - srednie panelu."""
    out = {}
    for eid, m in meta.items():
        if m["jezyk"] != jezyk or eid not in oceny:
            continue
        w = oceny[eid].values()
        out.setdefault(m["scenariusz"], {})[m["wariant"]] = {
            "naturalnosc": st.mean(x["naturalnosc"] for x in w),
            "jasnosc": st.mean(x["jasnosc_odniesienia"] for x in w),
            "samozwrotnosc": st.mean(x["samozwrotnosc"] for x in w),
        }
    return {k: v for k, v in out.items() if len(v) == len(WARIANTY)}


def zgodnosc(oceny, skala):
    kto = sorted({k for w in oceny.values() for k in w})
    pary = []
    for a, b in combinations(kto, 2):
        xa = [oceny[i][a][skala] for i in oceny if a in oceny[i] and b in oceny[i]]
        xb = [oceny[i][b][skala] for i in oceny if a in oceny[i] and b in oceny[i]]
        if len(set(xa)) > 1 and len(set(xb)) > 1:
            pary.append(st.correlation(xa, xb))
    sd = [st.stdev([x[skala] for x in oceny[i].values()])
          for i in oceny if len(oceny[i]) > 1]
    return st.mean(pary) if pary else float("nan"), st.mean(sd) if sd else float("nan")


def raport_jezyka(jezyk, sc):
    lista = list(sc.values())
    print(f"\n{'='*66}\n{jezyk.upper()} — {len(lista)} scenariuszy\n{'='*66}")

    print("\nprofil wariantow (srednie panelu):")
    print(f"  {'wariant':>10} | {'naturalnosc':>11} | {'jasnosc':>8} | "
          f"{'samozwrotny':>11} | {'spadek nat.':>11}")
    baza = st.mean(s["B"]["naturalnosc"] for s in lista)
    profil = {}
    for w in WARIANTY:
        n = st.mean(s[w]["naturalnosc"] for s in lista)
        j = st.mean(s[w]["jasnosc"] for s in lista)
        z = st.mean(s[w]["samozwrotnosc"] for s in lista)
        profil[w] = n
        print(f"  {w:>10} | {n:>11.2f} | {j:>8.2f} | {z:>11.2f} | {n-baza:>+11.2f}")

    rozstep = max(profil.values()) - min(profil.values())
    bez_c = {w: v for w, v in profil.items() if w != "C"}
    rozstep_bez_c = max(bez_c.values()) - min(bez_c.values())
    s1 = S1_ROZSTEP_WARIANTOW[jezyk]

    print(f"\n  rozstep naturalnosci, wszystkie warianty : {rozstep:.2f}"
          f"   (SPEKTRA-1: {s1:.2f})")
    print(f"  rozstep BEZ wariantu samozwrotnego       : {rozstep_bez_c:.2f}")
    print(f"  udzial wariantu C w calym rozstepie      : "
          f"{(rozstep - rozstep_bez_c) / rozstep:.0%}")
    if rozstep_bez_c < 1.0:
        print("  -> WSPOLNA RAMA DZIALA: piec wariantow miesci sie w 1 punkcie.")
        print("     Caly rozstep bierze sie z JEDNEGO wariantu - samozwrotnego,")
        print("     ktorego fraza referenta jest oceniana jako nienaturalna.")
    else:
        print("  -> wspolna rama NIE wyrownala wariantow - problem szerszy niz C")

    stale = stale_z_rozkladu(lista)
    print(f"\nstale wyprowadzone z tej probki (tryb: {stale['tryb']}):")
    print(f"  K1 prog naturalnosci (wariant neutralny) : {stale['K1_prog_naturalnosci']:.2f}")
    for w, v in stale["K2_dopuszczalny_spadek"].items():
        print(f"  K2 dopuszczalny spadek {w:>10}        : {v:.2f}")
    for w, v in stale["K3_prog_jasnosci"].items():
        print(f"  K3 prog jasnosci {w:>10}              : {v:.2f}")
    for w, v in stale["K4_sufit_jasnosci_nieosadzonego"].items():
        print(f"  K4 sufit jasnosci {w:>10}             : {v:.2f}")
    for w, v in stale["K5_sufit_odczytu_samozwrotnego"].items():
        print(f"  K5 sufit odczytu samozwrotnego {w:>10}: {v:.2f}")

    if stale["tryb"] == "obwiednia":
        print(f"\n  UWAGA: tryb obwiedni. Przy {len(lista)} scenariuszach zaden "
              f"dodatni ogon\n  nie miesci sie w budzecie {BUDZET:.0%} - progi lezą "
              f"na skrajnych obserwacjach.\n  Sito percentylowe wymaga n >= "
              f"{stale.get('potrzebne_n', '?')} na jezyk.")

    print(f"\n  odrzucenie wlasnej probki: {rachunek_osiagalnosci(lista, stale):.0%}")

    # K6 - czy prog ze SPEKTRY-1 bylby osiagalny na tym materiale
    s1p = S1_PROG_NATURALNOSCI[jezyk]
    ponizej = sum(1 for s in lista if s["B"]["naturalnosc"] < s1p)
    print(f"\n  K6: prog naturalnosci ze SPEKTRY-1 ({s1p:.2f}) odrzucilby "
          f"{ponizej}/{len(lista)} kotwic")

    # kontrola pulapki samozwrotnej w wariancie zwyczajnym
    zle = [k for k, s in sc.items() if s["CprimM"]["samozwrotnosc"]
           > s["CprimComp"]["samozwrotnosc"] + 1.0]
    if zle:
        print(f"\n  SYGNAL: w {len(zle)} scenariuszach wariant zwyczajny czyta sie "
              f"bardziej samozwrotnie\n  niz obliczeniowy: {', '.join(sorted(zle)[:6])}")

    return {"jezyk": jezyk, "n": len(lista), "rozstep": round(rozstep, 2),
            "rozstep_spektra1": s1, "tryb": stale["tryb"],
            "stale": {k: v for k, v in stale.items() if k != "tryb"}}


def porownanie(sufiks_a, sufiks_b):
    """Parowane porownanie dwoch przebiegow bramki - te same scenariusze."""
    ma, oa, _, _ = wczytaj(sufiks_a)
    mb, ob, _, _ = wczytaj(sufiks_b)
    print(f"\n{'='*66}")
    print(f"PORÓWNANIE PAROWANE: przebieg '{sufiks_a or 'pierwszy'}' "
          f"-> '{sufiks_b or 'pierwszy'}'")
    print(f"{'='*66}")

    for jezyk in ("pl", "en"):
        sa, sb = scenariusze(ma, oa, jezyk), scenariusze(mb, ob, jezyk)
        wspolne = sorted(set(sa) & set(sb))
        print(f"\n{jezyk.upper()} — {len(wspolne)} scenariuszy wspolnych")
        print(f"  {'wariant':>10} | {'naturalnosc':>19} | {'jasnosc':>19} | "
              f"{'samozwrotny':>19}")
        for w in WARIANTY:
            kol = []
            for pole in ("naturalnosc", "jasnosc", "samozwrotnosc"):
                a = st.mean(sa[k][w][pole] for k in wspolne)
                b = st.mean(sb[k][w][pole] for k in wspolne)
                kol.append(f"{a:5.2f} -> {b:5.2f} ({b-a:+.2f})")
            print(f"  {w:>10} | " + " | ".join(kol))


def main():
    import argparse
    ap = argparse.ArgumentParser(description="progi bramki z probki korpusu")
    ap.add_argument("--sufiks", default="", help="ktory przebieg analizowac")
    ap.add_argument("--porownaj-z", default=None,
                    help="sufiks wczesniejszego przebiegu do porownania parowanego")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    meta, oceny, wykluczone, braki = wczytaj(args.sufiks)
    if braki:
        print(f"=== BRAK OCEN dla {len(braki)} elementow: {braki[:8]} ===")
        return 1

    print(f"elementow: {len(meta)} | ocen na element: "
          f"{sorted({len(w) for w in oceny.values()})}")
    for s in SKALE:
        r, sd = zgodnosc(oceny, s)
        print(f"zgodnosc panelu ({s}): r={r:.2f}, SD elementu {sd:.2f}")

    wyniki = [raport_jezyka(j, scenariusze(meta, oceny, j)) for j in ("pl", "en")]

    print(f"\n{'='*66}")
    print("SCENARIUSZE WYLACZONE Z BADANIA (kalibracja nie moze byc kolista):")
    for j, lista in wykluczone.items():
        print(f"  {j}: {len(lista)} scenariuszy")

    if args.porownaj_z is not None:
        porownanie(args.porownaj_z, args.sufiks)

    (KATALOG / f"progi-s2{args.sufiks}-wynik.json").write_text(
        json.dumps({"wykluczone_z_badania": wykluczone, "wyniki": wyniki},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    print("\nzapisano gates/naturalnosc/progi-s2-wynik.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
