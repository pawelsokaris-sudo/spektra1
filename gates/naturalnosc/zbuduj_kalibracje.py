"""Budowa zestawu kalibracyjnego bramki naturalnosci - wersja 2.

DLACZEGO WERSJA 2. Pierwszy zestaw mial cztery wady, kazda z osobna
wystarczajaca, zeby uniewaznic kalibracje:

1. ORTOGRAFIA JAKO ZDRADA. Frazy uszkadzajace PL pisano bez diakrytykow
   ("ta rzecz ktora tam byla", "tamten protokol"), a otaczajacy tekst
   diakrytyki ma. Oceniajacy wykrywal uszkodzenie po zapisie, nie po
   badanej wlasciwosci.
2. INTERPUNKCJA JAKO ZDRADA. Uszkodzone warianty gubily przecinek przed
   "gdzie", ktory zdania nienaruszone mialy.
3. URWANE ZDANIA PO ANGIELSKU. "Whatever sits the thing that was there" -
   zgubiona cala reszta zdania. To inne uszkodzenie niz zamierzone.
4. KLASA POZORNA. Wszystkie uszkodzenia wstrzykniete do wariantu `self`.
   W wariancie samozwrotnym odniesienie do rozmowy jest POPRAWNE, wiec
   podmiana jednego samozwrotnego referenta na drugi nie jest uszkodzeniem.
   Dwanascie elementow udawalo uszkodzone.

CO ROBI TA WERSJA. Kazde uszkodzenie powstaje z bliznieta nienaruszonego
przez podmiane WYLACZNIE frazy referenta, w ramie odczytanej mechanicznie
(gates/naturalnosc/ramy.py). Klasa uszkodzenia trafia do wariantu, w ktorym
jest faktycznie bledem.

Uruchomienie:
    python -m gates.naturalnosc.zbuduj_kalibracje
"""

import json
import random
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ramy import podmien, rozbierz  # noqa: E402

KATALOG = Path(__file__).resolve().parent
ZIARNO = 20260803  # zamrozone; kolejnosc elementow musi byc odtwarzalna

# Frazy uszkadzajace. Zasady doboru:
#  - poprawna ortografia i interpunkcja (inaczej wracamy do wady 1 i 2),
#  - BEZ zdania podrzednego wewnatrz frazy - inaczej trzeba by dokladac
#    przecinek zamykajacy, ktorego rama nie ma, i znow powstaje zdrada,
#  - fraza ma niesc DOKLADNIE jedna wlasciwosc, ktora klasa nazywa.
FRAZY = {
    "pl": {
        # referent ontologicznie niedopasowany - dzien tygodnia nie jest rzecza
        "niedopasowany": {"miejscownik": "tym wtorku", "mianownik": "wtorek"},
        # referent czytelny jako odniesienie do trwajacej rozmowy
        "samozwrotny": {"miejscownik": "tym naszym zastanawianiu",
                        "mianownik": "to nasze zastanawianie"},
        # referent nigdy nieprzedstawiony w rozmowie
        "nieosadzony": {"miejscownik": "tamtym protokole wymiany",
                        "mianownik": "tamten protokół wymiany"},
        # polaczenie gramatyczne, ale nienaturalne
        "niezgrabny": {"miejscownik": "tym całym takim czymś",
                       "mianownik": "to całe takie coś"},
    },
    "en": {
        "niedopasowany": {"np": "Tuesday"},
        "samozwrotny": {"np": "this wondering of ours"},
        "nieosadzony": {"np": "that exchange protocol"},
        "niezgrabny": {"np": "that whole other thing there"},
    },
}

# Gospodarz uszkodzenia: wariant, w ktorym dana klasa JEST bledem.
#   samozwrotny  -> wariant zewnetrzny osadzony (tam samozwrotnosc to blad)
#   nieosadzony  -> wariant neutralny (tam referent ma byc osadzony)
#   niedopasowany-> wariant zewnetrzny nieosadzony (niedopasowanie wszedzie zle)
#   niezgrabny   -> wariant samozwrotny (niezgrabnosc wszedzie zla)
GOSPODARZ = {
    "external_grounded": "samozwrotny",
    "neutral": "nieosadzony",
    "external_ungrounded": "niedopasowany",
    "self": "niezgrabny",
}


def bez_diakrytykow(t):
    t = t.replace("ł", "l").replace("Ł", "L")
    return "".join(c for c in unicodedata.normalize("NFD", t)
                   if unicodedata.category(c) != "Mn")


def zbuduj(stary_zestaw):
    nienaruszone = [e for e in stary_zestaw["elementy"] if e["klasa"] == "nienaruszony"]
    elementy = []

    for e in nienaruszone:
        elementy.append({k: e[k] for k in
                         ("scenariusz", "jezyk", "klasa", "wariant", "kontekst", "zdanie")})

        klasa = GOSPODARZ[e["wariant"]]
        _, referent, _, gniazdo = rozbierz(e["zdanie"], e["jezyk"])
        fraza = FRAZY[e["jezyk"]][klasa][gniazdo]
        elementy.append({
            "scenariusz": e["scenariusz"], "jezyk": e["jezyk"],
            "klasa": f"uszkodzony:{klasa}", "wariant": e["wariant"],
            "kontekst": e["kontekst"], "zdanie": podmien(e["zdanie"], e["jezyk"], fraza),
            "referent_zastapiony": referent, "referent_wstawiony": fraza,
        })

    random.Random(ZIARNO).shuffle(elementy)
    for i, el in enumerate(elementy):
        el["id"] = f"K{i:03d}"
    return elementy


def kontrola(elementy):
    """Uszkodzenie ma sie roznic od bliznieta WYLACZNIE fraza referenta."""
    problemy = []
    nien = {(e["scenariusz"], e["wariant"]): e
            for e in elementy if e["klasa"] == "nienaruszony"}

    for e in elementy:
        if e["klasa"] == "nienaruszony":
            continue
        b = nien[(e["scenariusz"], e["wariant"])]
        oczekiwane = b["zdanie"].replace(e["referent_zastapiony"],
                                         e["referent_wstawiony"], 1)
        if e["zdanie"] != oczekiwane:
            problemy.append(f"{e['id']}: zdanie != blizniak z podmieniona fraza")

        # zdrada ortograficzna: uszkodzone bez diakrytykow tam, gdzie
        # nienaruszone je ma - to wlasnie zabilo wersje 1
        if e["jezyk"] == "pl":
            gesty_b = sum(1 for c in b["zdanie"] if bez_diakrytykow(c) != c)
            gesty_e = sum(1 for c in e["zdanie"] if bez_diakrytykow(c) != c)
            if gesty_b > 0 and gesty_e == 0:
                problemy.append(f"{e['id']}: ZDRADA - uszkodzone bez diakrytykow")

        # zdrada interpunkcyjna: rozna liczba przecinkow poza sama fraza
        pb = b["zdanie"].count(",") - e["referent_zastapiony"].count(",")
        pe = e["zdanie"].count(",") - e["referent_wstawiony"].count(",")
        if pb != pe:
            problemy.append(f"{e['id']}: ZDRADA - inna interpunkcja ramy")

        # urwanie zdania: dlugosc ramy musi byc zachowana
        rb = len(b["zdanie"]) - len(e["referent_zastapiony"])
        re_ = len(e["zdanie"]) - len(e["referent_wstawiony"])
        if rb != re_:
            problemy.append(f"{e['id']}: ZDRADA - rama skrocona lub wydluzona")

    return problemy


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    stary = json.loads((KATALOG / "zestaw-kalibracyjny.json").read_text(encoding="utf-8"))
    elementy = zbuduj(stary)
    problemy = kontrola(elementy)

    if problemy:
        print(f"=== {len(problemy)} PROBLEMOW - nie zapisuje ===")
        for p in problemy[:20]:
            print("  -", p)
        return 1

    zestaw = {
        "opis": ("Kalibracja bramki naturalnosci na materiale SPEKTRY-1 (ofiarnym), "
                 "wersja 2. Uszkodzenia powstaja z bliznieta nienaruszonego przez "
                 "podmiane wylacznie frazy referenta. Klasa uszkodzenia trafia do "
                 "wariantu, w ktorym jest faktycznie bledem."),
        "ziarno_kolejnosci": ZIARNO,
        "elementy": elementy,
    }
    (KATALOG / "zestaw-kalibracyjny-v2.json").write_text(
        json.dumps(zestaw, ensure_ascii=False, indent=2), encoding="utf-8")

    slepy = [{k: e[k] for k in ("id", "jezyk", "kontekst", "zdanie")} for e in elementy]
    (KATALOG / "do-oceny-v2.json").write_text(
        json.dumps({"instrukcja_w_osobnym_pliku": True, "elementy": slepy},
                   ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"zapisano: {len(elementy)} elementow, kontrola bez zarzutu")
    return 0


if __name__ == "__main__":
    sys.exit(main())
