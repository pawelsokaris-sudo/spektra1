"""Rozstrzygniecie sondy: wada korpusu czy wada pomiaru.

DWA PYTANIA, DWA PORÓWNANIA.

1. W TYM PRZEBIEGU, przy pelnym kontekscie: czy wariant obliczeniowy nadal
   odstaje od zewnetrznego osadzonego? Parowanie w obrebie scenariusza,
   permutacja dokladna.

2. MIEDZY PRZEBIEGAMI: o ile podnosi sie jasnosc wariantu obliczeniowego,
   gdy oceniajacy dostaje to samo, co model. Jesli roznica z punktu 1 znika
   w tym przejsciu - wada byla w procedurze oceniania, nie w korpusie,
   i korpusu nie wolno ruszac.

Uruchomienie:
    python -m gates.naturalnosc.sonda_comp_wynik
"""

import json
import statistics as st
import sys
from itertools import product
from pathlib import Path

KATALOG = Path(__file__).resolve().parent
SKALE = ("naturalnosc", "jasnosc_odniesienia", "samozwrotnosc")


def wczytaj(plik, wzor):
    meta = {e["id"]: e for e in
            json.loads((KATALOG / plik).read_text(encoding="utf-8"))["elementy"]}
    oceny = {}
    for p in sorted(KATALOG.glob(wzor)):
        d = json.loads(p.read_text(encoding="utf-8"))
        for o in d["oceny"]:
            oceny.setdefault(o["id"], {})[d["oceniajacy"]] = {s: o[s] for s in SKALE}
    return meta, oceny, [i for i in meta if not oceny.get(i)]


def permutacja_parowana(roznice):
    n = len(roznice)
    if n > 16:
        raise ValueError("za duzo par na enumeracje dokladna")
    obs = abs(st.mean(roznice))
    skrajnych = sum(1 for zn in product((1, -1), repeat=n)
                    if abs(st.mean(z * r for z, r in zip(zn, roznice))) >= obs - 1e-12)
    return skrajnych / 2 ** n


def srednia(oceny, eid, skala):
    return st.mean(x[skala] for x in oceny[eid].values())


def raport_wewnatrz(meta, oceny, jezyk):
    """Pytanie 1: osadzony wobec obliczeniowego przy pelnym kontekscie."""
    per = {}
    for eid, m in meta.items():
        if m["jezyk"] != jezyk:
            continue
        per.setdefault(m["scenariusz"], {})[m["wersja"]] = eid

    print(f"\n{'='*64}\n{jezyk.upper()} — pelny kontekst\n{'='*64}")
    wynik = {}
    for skala in SKALE:
        pary = [(srednia(oceny, v["osadzony"], skala),
                 srednia(oceny, v["obliczeniowy"], skala))
                for v in per.values() if len(v) == 2]
        roznice = [b - a for a, b in pary]
        pv = permutacja_parowana(roznice)
        wynik[skala] = (st.mean(a for a, _ in pary), st.mean(b for _, b in pary), pv)
        print(f"\n{skala}:  n par = {len(pary)}")
        print(f"  zewnetrzny osadzony : {wynik[skala][0]:.2f}")
        print(f"  obliczeniowy        : {wynik[skala][1]:.2f}")
        print(f"  roznica             : {st.mean(roznice):+.2f}   p = {pv:.4f}")
    return wynik


def raport_miedzy(meta_c, oceny_c, meta_b, oceny_b, jezyk):
    """Pytanie 2: okno czterech zdan wobec pelnego kontekstu."""
    mapa_b = {("CprimG", m["scenariusz"]): eid for eid, m in meta_b.items()
              if m["jezyk"] == jezyk and m["wariant"] == "CprimG"}
    mapa_b.update({("CprimComp", m["scenariusz"]): eid for eid, m in meta_b.items()
                   if m["jezyk"] == jezyk and m["wariant"] == "CprimComp"})
    mapa_c = {(("CprimG" if m["wersja"] == "osadzony" else "CprimComp"),
               m["scenariusz"]): eid for eid, m in meta_c.items() if m["jezyk"] == jezyk}

    print(f"\n  --- {jezyk.upper()}: okno 4 zdan -> pelny kontekst "
          f"(jasnosc odniesienia) ---")
    for wariant, nazwa in (("CprimG", "zewnetrzny osadzony"),
                           ("CprimComp", "obliczeniowy")):
        pary = [(srednia(oceny_b, mapa_b[k], "jasnosc_odniesienia"),
                 srednia(oceny_c, mapa_c[k], "jasnosc_odniesienia"))
                for k in mapa_c if k[0] == wariant and k in mapa_b]
        if not pary:
            continue
        roznice = [b - a for a, b in pary]
        print(f"    {nazwa:>20}: {st.mean(a for a, _ in pary):.2f} -> "
              f"{st.mean(b for _, b in pary):.2f}  ({st.mean(roznice):+.2f}, "
              f"p = {permutacja_parowana(roznice):.4f})")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    meta_c, oceny_c, braki = wczytaj("sonda-comp.json", "oceny-comp-*.json")
    if braki:
        print(f"=== BRAK OCEN dla {len(braki)} elementow ===")
        return 1
    print(f"elementow: {len(meta_c)} | ocen na element: "
          f"{sorted({len(w) for w in oceny_c.values()})}")

    wyniki = {j: raport_wewnatrz(meta_c, oceny_c, j) for j in ("pl", "en")}

    meta_b, oceny_b, _ = wczytaj("probka-s2b.json", "oceny-s2b-*.json")
    print(f"\n{'='*64}\nPORÓWNANIE Z PRZEBIEGIEM PRZY OKNIE CZTERECH ZDAN\n{'='*64}")
    for j in ("pl", "en"):
        raport_miedzy(meta_c, oceny_c, meta_b, oceny_b, j)

    print(f"\n{'='*64}")
    for j in ("pl", "en"):
        r = wyniki[j]["jasnosc_odniesienia"]
        luka = r[0] - r[1]
        print(f"{j.upper()}: luka jasnosci osadzony-obliczeniowy przy pelnym "
              f"kontekscie = {luka:+.2f} (p = {r[2]:.4f})")

    (KATALOG / "sonda-comp-wynik.json").write_text(json.dumps(
        {"wyniki": {j: {k: [round(x, 3) if isinstance(x, float) else x for x in v]
                        for k, v in w.items()} for j, w in wyniki.items()}},
        ensure_ascii=False, indent=2), encoding="utf-8")
    print("zapisano gates/naturalnosc/sonda-comp-wynik.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
