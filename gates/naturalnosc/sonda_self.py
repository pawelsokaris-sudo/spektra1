"""Sonda: dwie wersje frazy samozwrotnej na tych samych dwunastu scenariuszach.

PYTANIE. Specyfikacja dopuszcza dla wariantu `self` dwa referenty naraz:
"biezaca wymiane" ORAZ "uklad, ktory ja prowadzi". Pomiar na probce pokazal,
ze to NIE sa rzeczy wymienne:

    "to przetwarzanie" (n=22)  -> naturalnosc 2,76 | jasnosc 2,36
    "ten tok pytan"    (n=2)   -> naturalnosc 5,72 | jasnosc 6,50

Pierwsza fraza wskazuje na czynnosc PRYWATNA dla modelu, druga na obiekt
WSPOLNY dla obu rozmowcow. Decyzja miedzy nimi jest definicja hipotezy
glownej, nie kwestia redakcyjna - a n=2 na wersje to za malo, zeby ja podjac.

Sonda robi obie wersje dla wszystkich 24 scenariuszy kalibracyjnych, wiec
kazda wersja dostaje n=12 na jezyk, parowane w obrebie scenariusza.

KRYTERIUM ROZSTRZYGAJACE nie jest naturalnosc, tylko OBECNOSC. Specyfikacja
par. 1 wymaga, by para `self` <-> `external_computational` miala oba referenty
OBECNE i bliskie - to byl caly powod dodania szostego wariantu. Wygrywa wersja,
ktorej jasnosc jest blizsza jasnosci wariantu obliczeniowego.

Korpusu ta sonda NIE dotyka.

Uruchomienie:
    python -m gates.naturalnosc.sonda_self
"""

import json
import random
import sys
from pathlib import Path

KATALOG = Path(__file__).resolve().parent
ZIARNO = 20260804
OCENIAJACYCH = 9

# Odmiana dobrana tak, by podmiana byla jednoznaczna. "tok pytan" jest rodzaju
# meskiego nieżywotnego, wiec biernik = mianownik - a wlasnie tej dwuznacznosci
# nie da sie rozstrzygnac w "to przetwarzanie" (mianownik i biernik tozsame).
PRZETWARZANIE_NA_ROZMOWE = {
    "to przetwarzanie": "ten tok pytań",
    "tym przetwarzaniu": "tym toku pytań",
    "tym przetwarzaniem": "tym tokiem pytań",
    "tego przetwarzania": "tego toku pytań",
    "temu przetwarzaniu": "temu tokowi pytań",
    "this processing": "this conversation",
}
ROZMOWA_NA_PRZETWARZANIE = {
    "ten tok pytań": "to przetwarzanie",
    "tym toku pytań": "tym przetwarzaniu",
    "tym tokiem pytań": "tym przetwarzaniem",
    "tego toku pytań": "tego przetwarzania",
    "this conversation": "this processing",
}


def przelicz(zdanie):
    """Zwraca (wersja_przetwarzanie, wersja_rozmowa) albo None."""
    for a, b in PRZETWARZANIE_NA_ROZMOWE.items():
        if a in zdanie:
            return zdanie, zdanie.replace(a, b, 1)
    for a, b in ROZMOWA_NA_PRZETWARZANIE.items():
        if a in zdanie:
            return zdanie.replace(a, b, 1), zdanie
    return None


def zbuduj():
    probka = json.loads((KATALOG / "probka-s2.json").read_text(encoding="utf-8"))
    elementy, nierozpoznane = [], []

    for e in probka["elementy"]:
        if e["wariant"] != "C":
            continue
        r = przelicz(e["zdanie"])
        if r is None:
            nierozpoznane.append((e["scenariusz"], e["zdanie"]))
            continue
        for wersja, zdanie in (("przetwarzanie", r[0]), ("rozmowa", r[1])):
            elementy.append({
                "scenariusz": e["scenariusz"], "jezyk": e["jezyk"],
                "wersja": wersja, "kontekst": e["kontekst"], "zdanie": zdanie,
            })

    rng = random.Random(ZIARNO)
    rng.shuffle(elementy)
    for i, el in enumerate(elementy):
        el["id"] = f"W{i:03d}"
    return elementy, nierozpoznane


def kontrola(elementy):
    """Obie wersje musza roznic sie WYLACZNIE fraza referenta."""
    problemy = []
    pary = {}
    for e in elementy:
        pary.setdefault((e["jezyk"], e["scenariusz"]), {})[e["wersja"]] = e

    for klucz, para in pary.items():
        if len(para) != 2:
            problemy.append(f"{klucz}: niepelna para {sorted(para)}")
            continue
        a, b = para["przetwarzanie"]["zdanie"], para["rozmowa"]["zdanie"]
        sa, sb = a.split(), b.split()

        # Fraza alternatywna jest o slowo dluzsza ("ten tok pytan" wobec
        # "to przetwarzanie"), wiec rownosc dlugosci NIE jest tu kryterium.
        # Kryterium jest to, ze roznica tworzy JEDEN ciagly kawalek: wspolny
        # przedrostek, wspolny przyrostek, a miedzy nimi sama fraza referenta.
        p = 0
        while p < min(len(sa), len(sb)) and sa[p] == sb[p]:
            p += 1
        s = 0
        while (s < min(len(sa), len(sb)) - p
               and sa[len(sa) - 1 - s] == sb[len(sb) - 1 - s]):
            s += 1

        srodek_a, srodek_b = sa[p:len(sa) - s], sb[p:len(sb) - s]
        if not srodek_a or not srodek_b:
            problemy.append(f"{klucz}: wersje IDENTYCZNE albo pusta fraza")
        elif len(srodek_a) > 4 or len(srodek_b) > 4:
            problemy.append(f"{klucz}: roznica szersza niz fraza referenta: "
                            f"{' '.join(srodek_a)!r} -> {' '.join(srodek_b)!r}")
    return problemy


def roznica_dlugosci(elementy):
    """O ile wersja 'rozmowa' jest dluzsza - wazne dla budzetu tokenowego."""
    pary = {}
    for e in elementy:
        pary.setdefault((e["jezyk"], e["scenariusz"]), {})[e["wersja"]] = e["zdanie"]
    out = {}
    for (jezyk, _), p in pary.items():
        d = len(p["rozmowa"].split()) - len(p["przetwarzanie"].split())
        out.setdefault(jezyk, []).append(d)
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    elementy, nierozpoznane = zbuduj()

    if nierozpoznane:
        print(f"=== {len(nierozpoznane)} zdan o nierozpoznanej frazie samozwrotnej ===")
        for s, z in nierozpoznane:
            print(f"  {s}: {z[:90]}")
        return 1

    problemy = kontrola(elementy)
    if problemy:
        print(f"=== {len(problemy)} PROBLEMOW - nie zapisuje ===")
        for p in problemy[:10]:
            print("  -", p)
        return 1

    (KATALOG / "sonda-self.json").write_text(json.dumps({
        "opis": ("Dwie wersje frazy samozwrotnej na tych samych scenariuszach. "
                 "Kryterium rozstrzygajace: blizsza jasnosc wobec wariantu "
                 "external_computational (obecnosc referenta, spec par. 1)."),
        "ziarno": ZIARNO, "elementy": elementy,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    slepe = [{k: e[k] for k in ("id", "jezyk", "kontekst", "zdanie")} for e in elementy]
    for n in range(1, OCENIAJACYCH + 1):
        kop = list(slepe)
        random.Random(11000 + n).shuffle(kop)
        (KATALOG / f"do-oceny-self-{n}.json").write_text(
            json.dumps({"oceniajacy": str(n), "elementy": kop},
                       ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"elementow: {len(elementy)} (24 scenariusze x 2 wersje)")
    print("kontrola: obie wersje roznia sie wylacznie fraza referenta")
    print(f"plikow do oceny: {OCENIAJACYCH}")

    print("\nkoszt tokenowy wersji 'rozmowa' (roznica w slowach):")
    for jezyk, d in sorted(roznica_dlugosci(elementy).items()):
        print(f"  {jezyk}: {min(d)}..{max(d)} slowa, srednio {sum(d)/len(d):+.2f}")
    print("  -> po polsku fraza jest dluzsza; przy przyjeciu tej wersji trzeba")
    print("     sprawdzic, czy korpus utrzyma rownanie tokenow +-2%.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
