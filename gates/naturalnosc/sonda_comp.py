"""Sonda: czy wariant obliczeniowy jest slabszy, czy tylko GORZEJ POKAZANY.

CO SIE STALO. Powtorzenie bramki dalo wariantowi obliczeniowemu jasnosc
4,29 (PL) wobec 6,30 dla zewnetrznego osadzonego, mimo ze specyfikacja par. 1
wymaga, by oba referenty byly OBECNE. Wyglądalo to na wade korpusu.

CO SIE OKAZALO. Referent obliczeniowy pada przed wstawka we WSZYSTKICH
24 scenariuszach - nie brakuje go nigdy. Rozklad jasnosci zalezy wylacznie
od tego, czy miesci sie w oknie czterech zdan, ktore pokazywano oceniajacym:

    referent w oknie 4 zdan : osadzony 6,76 | obliczeniowy 6,50   (rownowaga)
    referent poza oknem     : osadzony 5,25 | obliczeniowy 3,64   (przepasc)

Model widzi CALY dialog. Oceniajacy widzial cztery zdania. Zmierzona slabosc
wariantu obliczeniowego moze wiec byc artefaktem procedury oceniania, a nie
wlasnoscia korpusu - i wtedy poprawianie korpusu byloby naprawianiem pomiaru
przez psucie bodzca.

CO ROBI TA SONDA. Te same 24 scenariusze, te same dwie wstawki, ale kontekst
= CALY dialog do miejsca wstawki, czyli dokladnie to, co dostaje model.
Jesli roznica zniknie - wada byla w pomiarze. Jesli zostanie - jest realna
i wtedy dopiero wolno ruszac korpus.

Korpusu ta sonda NIE dotyka.

Uruchomienie:
    python -m gates.naturalnosc.sonda_comp
"""

import json
import random
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
KATALOG = Path(__file__).resolve().parent
ZIARNO = 20260805
OCENIAJACYCH = 9

WERSJE = {"osadzony": "external_grounded", "obliczeniowy": "external_computational"}


def pelny_kontekst(sc, ins):
    """Wszystko, co model ma przed soba w chwili wstawki."""
    zdania = [s for t in sc["turns"][:ins["turn"]] for s in t["base"]]
    zdania += sc["turns"][ins["turn"]]["base"][:ins["after_sentence"] + 1]
    return " ".join(zdania)


def zbuduj():
    probka = json.loads((KATALOG / "probka-s2b.json").read_text(encoding="utf-8"))
    pliki = {p.stem: p for p in (REPO / "corpus" / "scenarios-2").glob("*/*.json")}
    elementy, problemy = [], []

    for e in probka["elementy"]:
        if e["wariant"] != "CprimComp":
            continue
        sc = json.loads(pliki[e["scenariusz"]].read_text(encoding="utf-8"))
        ins = next((i for i in sc["insertions"]
                    if i["external_computational"] == e["zdanie"]), None)
        if ins is None:
            problemy.append(f"{e['scenariusz']}: nie znaleziono wstawki")
            continue
        k = pelny_kontekst(sc, ins)
        for wersja, klucz in WERSJE.items():
            elementy.append({
                "scenariusz": e["scenariusz"], "jezyk": e["jezyk"],
                "wersja": wersja, "kontekst": k, "zdanie": ins[klucz],
            })

    rng = random.Random(ZIARNO)
    rng.shuffle(elementy)
    for i, el in enumerate(elementy):
        el["id"] = f"C{i:03d}"
    return elementy, problemy


def kontrola(elementy):
    """Obie wersje maja dzielic KONTEKST i rame; roznic sie ma sama fraza."""
    problemy = []
    pary = {}
    for e in elementy:
        pary.setdefault((e["jezyk"], e["scenariusz"]), {})[e["wersja"]] = e

    for klucz, para in pary.items():
        if len(para) != 2:
            problemy.append(f"{klucz}: niepelna para")
            continue
        a, b = para["osadzony"], para["obliczeniowy"]
        if a["kontekst"] != b["kontekst"]:
            problemy.append(f"{klucz}: ROZNY kontekst - porownanie nieuczciwe")
        sa, sb = a["zdanie"].split(), b["zdanie"].split()
        p = 0
        while p < min(len(sa), len(sb)) and sa[p] == sb[p]:
            p += 1
        s = 0
        while (s < min(len(sa), len(sb)) - p
               and sa[len(sa)-1-s] == sb[len(sb)-1-s]):
            s += 1
        if len(sa[p:len(sa)-s]) > 4 or len(sb[p:len(sb)-s]) > 4:
            problemy.append(f"{klucz}: roznica szersza niz fraza referenta")
    return problemy


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    elementy, problemy = zbuduj()
    problemy += kontrola(elementy)
    if problemy:
        print(f"=== {len(problemy)} PROBLEMOW - nie zapisuje ===")
        for x in problemy[:10]:
            print("  -", x)
        return 1

    (KATALOG / "sonda-comp.json").write_text(json.dumps({
        "opis": ("Wariant osadzony wobec obliczeniowego przy PELNYM kontekscie - "
                 "tym samym, ktory dostaje model. Sprawdza, czy zmierzona slabosc "
                 "wariantu obliczeniowego jest wlasnoscia korpusu, czy artefaktem "
                 "okna czterech zdan pokazywanego oceniajacym."),
        "ziarno": ZIARNO, "elementy": elementy,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    slepe = [{k: e[k] for k in ("id", "jezyk", "kontekst", "zdanie")} for e in elementy]
    for n in range(1, OCENIAJACYCH + 1):
        kop = list(slepe)
        random.Random(13000 + n).shuffle(kop)
        (KATALOG / f"do-oceny-comp-{n}.json").write_text(
            json.dumps({"oceniajacy": str(n), "elementy": kop},
                       ensure_ascii=False, indent=2), encoding="utf-8")

    dl = [len(e["kontekst"]) for e in elementy]
    print(f"elementow: {len(elementy)} (24 scenariusze x 2 warianty)")
    print(f"kontekst: {min(dl)}-{max(dl)} znakow, mediana "
          f"{sorted(dl)[len(dl)//2]}")
    print(f"plikow do oceny: {OCENIAJACYCH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
