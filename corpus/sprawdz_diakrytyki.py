"""Weryfikacja przywrocenia polskich znakow: TYLKO ortografia, zero zmian tresci.

Przy przepisywaniu 48 plikow najwiekszym ryzykiem nie jest zly znak, tylko
autor, ktory "przy okazji" poprawi zdanie. Ta kontrola to wyklucza mechanicznie:
po zdjeciu diakrytykow nowy tekst musi byc IDENTYCZNY CO DO ZNAKU z wersja
zapisana w gicie.

Uruchomienie:
    python -m corpus.sprawdz_diakrytyki                 # kontrola wzgledem HEAD
    python -m corpus.sprawdz_diakrytyki --ref <commit>  # wzgledem innego punktu
"""

import argparse
import json
import subprocess
import sys
import unicodedata
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
KATALOG = "corpus/scenarios-2/pl"

# 'l' z kreska nie ma postaci rozlozonej w Unicode - trzeba osobno
RECZNE = {"ł": "l", "Ł": "L"}


def zdejmij_diakrytyki(tekst):
    """Fold do ASCII: rozklad kanoniczny + usuniecie znakow laczacych."""
    for a, b in RECZNE.items():
        tekst = tekst.replace(a, b)
    rozlozony = unicodedata.normalize("NFD", tekst)
    return "".join(c for c in rozlozony if unicodedata.category(c) != "Mn")


def teksty_scenariusza(sc):
    """Wszystkie pola tekstowe, ktore autor mogl ruszyc - w stalej kolejnosci."""
    out = [sc.get("topic", "")]
    for t in sc.get("turns", []):
        out.extend(t.get("base", []))
    for ins in sc.get("insertions", []):
        out.extend(v for k, v in sorted(ins.items()) if isinstance(v, str))
    return out


def wersja_z_gita(sciezka, ref):
    r = subprocess.run(["git", "show", f"{ref}:{sciezka}"], cwd=REPO,
                       capture_output=True, text=True, encoding="utf-8")
    return json.loads(r.stdout) if r.returncode == 0 else None


def sprawdz(ref="HEAD"):
    problemy, sprawdzone, dodane = [], 0, 0
    for p in sorted((REPO / KATALOG).glob("*.json")):
        wzgl = f"{KATALOG}/{p.name}"
        stary = wersja_z_gita(wzgl, ref)
        if stary is None:
            problemy.append(f"{p.name}: brak w {ref} - plik nowy, nie ma z czym porownac")
            continue
        nowy = json.loads(p.read_text(encoding="utf-8"))
        a, b = teksty_scenariusza(stary), teksty_scenariusza(nowy)
        if len(a) != len(b):
            problemy.append(f"{p.name}: ZMIENIONA LICZBA pol tekstowych {len(a)} -> {len(b)}")
            continue
        for i, (s, n) in enumerate(zip(a, b)):
            if zdejmij_diakrytyki(n) != s:
                problemy.append(
                    f"{p.name}: pole {i} zmienione POZA diakrytykami\n"
                    f"      bylo: {s[:70]}\n"
                    f"      jest: {zdejmij_diakrytyki(n)[:70]}")
        dodane += sum(1 for x in b for c in x if zdejmij_diakrytyki(c) != c)
        sprawdzone += 1
    return sprawdzone, dodane, problemy


def main():
    ap = argparse.ArgumentParser(description="kontrola przywrocenia diakrytykow")
    ap.add_argument("--ref", default="HEAD")
    args = ap.parse_args()
    n, dodane, problemy = sprawdz(args.ref)
    print(f"plikow sprawdzonych: {n} | znakow diakrytycznych dodanych: {dodane}")
    if problemy:
        print(f"\n=== {len(problemy)} PROBLEMOW ===")
        for x in problemy[:30]:
            print(f"  - {x}")
        return 1
    print("=== TRESC NIETKNIETA, zmieniona wylacznie ortografia ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
