"""Przepisanie wariantu samozwrotnego w korpusie SPEKTRY-2.

DLACZEGO. Sonda na 24 parach (docs/SPEKTRA-2-fraza-samozwrotna.md) pokazala,
ze "to przetwarzanie" NIE jest niezawodnie czytane jako samoodniesienie:
3,94 (PL) i 3,90 (EN) na skali 1-7, czyli ponizej srodka. W rzemioslach,
ktore same sa przetworstwem, czytelnik podstawia pod te fraze proces w swiecie.
Wariant, ktory ma byc samozwrotny, w polowie przypadkow samozwrotny nie jest.

CO ROBI. Podmienia fraze referenta w polu `self`, zachowujac przypadek
gramatyczny. Niczego wiecej nie dotyka.

BEZPIECZENSTWO. Sprawdzone przed napisaniem: fraza "przetwarzanie/processing"
NIE wystepuje nigdzie poza polem `self` (465 wystapien, wszystkie w `self`).
Mimo to podmiana idzie linia po linii i tylko w liniach klucza "self" - JSON
jest zapisany po jednym kluczu na linie.

FORMAT. Pliki maja CRLF, wciecie 2, polskie znaki niescapowane i BRAK
konczacej nowej linii. Podmiana operuje na tekscie, nie przez json.dump,
zeby formatowanie zostalo nietkniete co do bajtu.

Uruchomienie:
    python -m corpus.przepisz_self --sprawdz    # tylko raport, bez zapisu
    python -m corpus.przepisz_self
"""

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
KATALOG = REPO / "corpus" / "scenarios-2"

# DLACZEGO "ta rozmowa", A NIE "ten tok pytan".
# Pierwsze podejscie uzywalo "toku pytan", bo rodzaj meski niezywotny ma
# biernik rowny mianownikowi, wiec podmiana byla jednoznaczna bez patrzenia
# na kontekst. To byl argument WYGODY IMPLEMENTACYJNEJ, nie jezykowy - i mial
# cene: fraza jest o slowo dluzsza, przez co rownanie tokenow +-2% pekalo
# w trzynastu polskich scenariuszach.
#
# Sprawdzenie kontekstu usuwa powod tamtego wyboru: wszystkie 47 wystapien
# "to przetwarzanie" stoi po czasowniku "przypomina", czyli w BIERNIKU.
# Dwuznacznosci nie ma zadnej, a "ta rozmowa" ma te sama liczbe slow co fraza
# zastepowana.
#
# DLACZEGO Z "nasza". Kandydatow sprawdzono na korpusie, licząc realne
# naruszenia rownania dlugosci i tokenow, zamiast dobierac fraze na oko:
#     "ten tok pytań"    -> 38 naruszen w 13 scenariuszach (za krotka)
#     "tę rozmowę"       -> 314 naruszen w 44 scenariuszach (duzo za krotka)
#     "tę naszą rozmowę" ->   3 naruszenia w 3 scenariuszach
# "Nasza" niesie przy okazji to samo, co angielskie "of ours" w materiale
# kalibracyjnym: referent jest jawnie WSPOLNY dla obu rozmowcow.
PODMIANY = {
    "tym przetwarzaniu": "tej naszej rozmowie",   # miejscownik
    "tym przetwarzaniem": "tą naszą rozmową",     # narzednik
    "to przetwarzanie": "tę naszą rozmowę",       # biernik (asercja nizej)
    "this processing": "this conversation",
    # pl-05 i dwa scenariusze EN uzywaly juz frazy dyskursywnej, ale w innej
    # postaci - korpus ma byc JEDNORODNY, bo niejednorodnosc wariantu
    # samozwrotnego byla wlasnie zrodlem calego problemu.
    "tym toku pytań": "tej naszej rozmowie",
    "tym tokiem pytań": "tą naszą rozmową",
    "ten tok pytań": "tę naszą rozmowę",
}

# Czasownik wymuszajacy biernik. Jesli kiedys pojawi sie inny kontekst dla
# "to przetwarzanie", skrypt ma stanac, a nie zgadywac przypadek.
BIERNIK_PO = "przypomina"

DOZWOLONE = ("tej naszej rozmowie", "tą naszą rozmową", "tę naszą rozmowę",
             "this conversation")


def podmien_linie(linia):
    """Zwraca (nowa_linia, uzyta_fraza) albo (linia, None)."""
    for a, b in PODMIANY.items():
        if a in linia:
            if linia.count(a) != 1:
                raise ValueError(f"fraza {a!r} wystepuje {linia.count(a)} razy")
            if a in ("to przetwarzanie", "ten tok pytań") \
                    and f"{BIERNIK_PO} {a}" not in linia:
                raise ValueError(
                    f"fraza {a!r} nie stoi po {BIERNIK_PO!r} - przypadek "
                    f"gramatyczny niepewny, nie zgaduje: {linia.strip()[:90]}")
            return linia.replace(a, b), a
    return linia, None


def przetworz(sciezka):
    tekst = sciezka.read_bytes().decode("utf-8")
    # Korpus ma NIEJEDNOLITE zakonczenia linii (47 plikow EN z LF, 36 PL z CRLF,
    # reszta odwrotnie) - slad po roznych autorach. Dzielenie po "\n" zostawia
    # ewentualne "\r" na koncu linii jako zwykly znak, wiec zlaczenie odtwarza
    # plik co do bajtu niezaleznie od konwencji. Ujednolicanie koncowek zrobiloby
    # ogromny diff niezwiazany z ta zmiana.
    linie = tekst.split("\n")
    zmian, juz_dobre, problemy = 0, 0, []

    for i, linia in enumerate(linie):
        if '"self":' not in linia:
            continue
        nowa, fraza = podmien_linie(linia)
        if fraza:
            linie[i] = nowa
            zmian += 1
        elif any(d in linia for d in DOZWOLONE):
            juz_dobre += 1
        else:
            problemy.append(f"{sciezka.name} linia {i+1}: "
                            f"nierozpoznana fraza samozwrotna")

    return "\n".join(linie), zmian, juz_dobre, problemy


def kontrola_bajtowa(stary_tekst, nowy_tekst):
    """Poza liniami klucza `self` plik ma byc IDENTYCZNY co do znaku.

    Kontrola JSON-owa tego nie zlapie: json.loads zjada roznice w zakonczeniach
    linii i we wcieciach. Wlasnie tak przeszla pierwsza wersja tego skryptu,
    ktora sklejala plik znakami CRLF niezaleznie od tego, czym byl rozdzielony.
    """
    a, b = stary_tekst.split("\n"), nowy_tekst.split("\n")
    if len(a) != len(b):
        return [f"ZMIENIONA LICZBA LINII {len(a)} -> {len(b)}"]
    return [f"linia {i+1}: zmieniona POZA polem self"
            for i, (x, y) in enumerate(zip(a, b))
            if x != y and '"self":' not in x]


def kontrola(stary_tekst, nowy_tekst):
    """Zmienic sie moga WYLACZNIE pola `self`, i to tylko fraza referenta."""
    a, b = json.loads(stary_tekst), json.loads(nowy_tekst)
    problemy = []

    if a.keys() != b.keys() or len(a["insertions"]) != len(b["insertions"]):
        return ["ZMIENIONA STRUKTURA pliku"]

    if a["turns"] != b["turns"] or a.get("topic") != b.get("topic"):
        problemy.append("ZMIENIONA baza dialogu albo temat")

    for k, (ia, ib) in enumerate(zip(a["insertions"], b["insertions"])):
        for klucz in ia:
            if klucz == "self":
                continue
            if ia[klucz] != ib.get(klucz):
                problemy.append(f"wstawka {k}: zmieniony wariant {klucz}")
        sa, sb = ia["self"].split(), ib["self"].split()
        p = 0
        while p < min(len(sa), len(sb)) and sa[p] == sb[p]:
            p += 1
        s = 0
        while (s < min(len(sa), len(sb)) - p
               and sa[len(sa)-1-s] == sb[len(sb)-1-s]):
            s += 1
        if len(sa[p:len(sa)-s]) > 3 or len(sb[p:len(sb)-s]) > 3:
            problemy.append(f"wstawka {k}: roznica szersza niz fraza referenta")
    return problemy


def main():
    ap = argparse.ArgumentParser(description="przepisanie wariantu samozwrotnego")
    ap.add_argument("--sprawdz", action="store_true", help="raport bez zapisu")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    pliki = sorted(KATALOG.glob("*/*.json"))
    razem, dobre, wszystkie_problemy, do_zapisu = 0, 0, [], []

    for p in pliki:
        stary = p.read_bytes().decode("utf-8")
        nowy, zmian, juz, problemy = przetworz(p)
        wszystkie_problemy += problemy
        if zmian:
            wszystkie_problemy += [f"{p.name}: {x}" for x in
                                   kontrola_bajtowa(stary, nowy) + kontrola(stary, nowy)]
            do_zapisu.append((p, nowy))
        razem += zmian
        dobre += juz

    if wszystkie_problemy:
        print(f"=== {len(wszystkie_problemy)} PROBLEMOW - nie zapisuje ===")
        for x in wszystkie_problemy[:20]:
            print("  -", x)
        return 1

    print(f"plikow: {len(pliki)} | podmian: {razem} | "
          f"juz zgodnych z decyzja: {dobre}")

    if args.sprawdz:
        print("tryb --sprawdz: nic nie zapisano")
        return 0

    for p, nowy in do_zapisu:
        p.write_bytes(nowy.encode("utf-8"))
    print(f"zapisano {len(do_zapisu)} plikow")
    return 0


if __name__ == "__main__":
    sys.exit(main())
