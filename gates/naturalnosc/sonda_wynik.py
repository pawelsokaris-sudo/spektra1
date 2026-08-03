"""Rozstrzygniecie sondy: ktora fraza samozwrotna wchodzi do korpusu.

KRYTERIUM GLOWNE NIE JEST NATURALNOSC. Specyfikacja autorska par. 1 wymaga,
by para `self` <-> `external_computational` miala oba referenty OBECNE
i bliskie - to byl caly powod dodania szostego wariantu, bo w SPEKTRZE-1
hipoteza glowna porownywala frazy rozniace sie takze obecnoscia.

Wygrywa wiec wersja, ktorej JASNOSC ODNIESIENIA jest blizsza jasnosci
wariantu obliczeniowego. Naturalnosc jest kryterium drugim, odczyt
samozwrotny warunkiem koniecznym (obie wersje musza pozostac samozwrotne).

Test: parowana permutacja dokladna w obrebie scenariusza (2^12 = 4096
przypisan znaku), osobno per jezyk. Repliki nigdy nie sa laczone.

Uruchomienie:
    python -m gates.naturalnosc.sonda_wynik
"""

import json
import statistics as st
import sys
from itertools import product
from pathlib import Path

KATALOG = Path(__file__).resolve().parent
SKALE = ("naturalnosc", "jasnosc_odniesienia", "samozwrotnosc")

# Zmierzone na probce korpusu (docs/SPEKTRA-2-progi-z-probki.md par. 2).
# To jest partner, do ktorego wariant samozwrotny ma pasowac obecnoscia.
JASNOSC_OBLICZENIOWEGO = {"pl": 4.23, "en": 5.01}


def wczytaj():
    sonda = json.loads((KATALOG / "sonda-self.json").read_text(encoding="utf-8"))
    meta = {e["id"]: e for e in sonda["elementy"]}
    oceny = {}
    for p in sorted(KATALOG.glob("oceny-self-*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        for o in d["oceny"]:
            oceny.setdefault(o["id"], {})[d["oceniajacy"]] = {s: o[s] for s in SKALE}
    braki = [i for i in meta if not oceny.get(i)]
    return meta, oceny, braki


def pary(meta, oceny, jezyk, skala):
    """[(wartosc_przetwarzanie, wartosc_rozmowa)] - parowane po scenariuszu."""
    per = {}
    for eid, m in meta.items():
        if m["jezyk"] != jezyk or eid not in oceny:
            continue
        per.setdefault(m["scenariusz"], {})[m["wersja"]] = st.mean(
            x[skala] for x in oceny[eid].values())
    return [(v["przetwarzanie"], v["rozmowa"])
            for v in per.values() if len(v) == 2]


def permutacja_parowana(roznice):
    """Dokladna permutacja znakow, p dwustronne."""
    n = len(roznice)
    if n > 16:
        raise ValueError("za duzo par na enumeracje dokladna")
    obs = abs(st.mean(roznice))
    skrajnych = sum(
        1 for znaki in product((1, -1), repeat=n)
        if abs(st.mean(z * r for z, r in zip(znaki, roznice))) >= obs - 1e-12)
    return skrajnych / 2 ** n


def raport(meta, oceny, jezyk):
    print(f"\n{'='*64}\n{jezyk.upper()}\n{'='*64}")
    wynik = {}
    for skala in SKALE:
        p = pary(meta, oceny, jezyk, skala)
        if not p:
            continue
        a = [x for x, _ in p]
        b = [y for _, y in p]
        roznice = [y - x for x, y in p]
        pv = permutacja_parowana(roznice)
        wynik[skala] = (st.mean(a), st.mean(b), st.mean(roznice), pv)
        print(f"\n{skala}:  n par = {len(p)}")
        print(f"  'to przetwarzanie' : {st.mean(a):.2f}")
        print(f"  'ten tok pytan'    : {st.mean(b):.2f}")
        print(f"  roznica            : {st.mean(roznice):+.2f}   p = {pv:.4f}")

    cel = JASNOSC_OBLICZENIOWEGO[jezyk]
    ja, jb = wynik["jasnosc_odniesienia"][0], wynik["jasnosc_odniesienia"][1]
    da, db = abs(ja - cel), abs(jb - cel)
    print("\n--- kryterium rozstrzygajace: dopasowanie OBECNOSCI do partnera ---")
    print(f"  jasnosc wariantu obliczeniowego (cel): {cel:.2f}")
    print(f"  'to przetwarzanie': {ja:.2f}  -> niedopasowanie {da:.2f}")
    print(f"  'ten tok pytan'   : {jb:.2f}  -> niedopasowanie {db:.2f}")
    lepsza = "ten tok pytan" if db < da else "to przetwarzanie"
    print(f"  LEPIEJ DOPASOWANA: '{lepsza}' (o {abs(da-db):.2f} pkt)")

    sa, sb = wynik["samozwrotnosc"][0], wynik["samozwrotnosc"][1]
    print("\n  warunek konieczny - obie wersje samozwrotne (>4)?")
    print(f"    'to przetwarzanie': {sa:.2f}   'ten tok pytan': {sb:.2f}"
          f"   -> {'SPELNIONY' if min(sa, sb) > 4 else 'NIESPELNIONY'}")

    return {"jezyk": jezyk, "lepiej_dopasowana": lepsza,
            "niedopasowanie": {"przetwarzanie": round(da, 2), "rozmowa": round(db, 2)},
            "skale": {k: {"przetwarzanie": round(v[0], 2), "rozmowa": round(v[1], 2),
                          "roznica": round(v[2], 2), "p": round(v[3], 4)}
                      for k, v in wynik.items()}}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    meta, oceny, braki = wczytaj()
    if braki:
        print(f"=== BRAK OCEN dla {len(braki)} elementow ===")
        return 1
    print(f"elementow: {len(meta)} | ocen na element: "
          f"{sorted({len(w) for w in oceny.values()})}")

    wyniki = [raport(meta, oceny, j) for j in ("pl", "en")]

    print(f"\n{'='*64}")
    zgodne = len({w["lepiej_dopasowana"] for w in wyniki}) == 1
    print("Repliki wskazuja " + ("TE SAMA wersje." if zgodne
                                 else "ROZNE wersje - decyzja wymaga rozstrzygniecia."))

    (KATALOG / "sonda-self-wynik.json").write_text(
        json.dumps({"kryterium": "dopasowanie jasnosci do wariantu obliczeniowego",
                    "wyniki": wyniki}, ensure_ascii=False, indent=2), encoding="utf-8")
    print("zapisano gates/naturalnosc/sonda-self-wynik.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
