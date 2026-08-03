"""Kontrola rundy redakcyjnej: co dokladnie zmieniono wzgledem punktu odniesienia.

Weryfikator diakrytykow tu nie zadziala - runda redakcyjna ZMIENIA tresc
swiadomie. Pytanie brzmi inaczej: czy zmieniono WYLACZNIE pozycje z listy
redakcyjnej, i czy ktoras z nich nie siedzi przypadkiem we wstawce.

Rozroznienie baza / wstawka jest tu najwazniejsze. Poprawka w `turns[].base`
dotyka wszystkich szesciu wariantow tak samo i kontrastu nie rusza.
Poprawka w `insertions[]` dotyka JEDNEGO wariantu - czyli wchodzi wprost
do mierzonej roznicy i musi byc widoczna z osobna.

Uruchomienie:
    python -m corpus.sprawdz_redakcje --ref 5d6a1e4
    python -m corpus.sprawdz_redakcje --ref 5d6a1e4 --tylko-wstawki
"""

import argparse
import difflib
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
KATALOG = "corpus/scenarios-2/pl"


def pola(sc):
    """Mapa: etykieta pola -> tekst. Etykieta mowi, gdzie w scenariuszu siedzi."""
    out = {"topic": sc.get("topic", "")}
    for i, t in enumerate(sc.get("turns", [])):
        for j, z in enumerate(t.get("base", [])):
            out[f"turn{i}.base[{j}]"] = z
    for k, ins in enumerate(sc.get("insertions", [])):
        for klucz, v in sorted(ins.items()):
            if isinstance(v, str):
                out[f"WSTAWKA{k}.{klucz}"] = v
    return out


def wersja_z_gita(sciezka, ref):
    r = subprocess.run(["git", "show", f"{ref}:{sciezka}"], cwd=REPO,
                       capture_output=True, text=True, encoding="utf-8")
    return json.loads(r.stdout) if r.returncode == 0 else None


def slowa_roznice(stare, nowe):
    """Zwraca liste (bylo, jest) na poziomie slow - zwiezle, bez calych zdan."""
    a, b = stare.split(), nowe.split()
    zmiany = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b).get_opcodes():
        if tag != "equal":
            zmiany.append((" ".join(a[i1:i2]) or "-", " ".join(b[j1:j2]) or "-"))
    return zmiany


def sprawdz(ref, tylko_wstawki=False):
    raport, we_wstawkach, w_bazie = [], 0, 0
    for p in sorted((REPO / KATALOG).glob("*.json")):
        wzgl = f"{KATALOG}/{p.name}"
        stary = wersja_z_gita(wzgl, ref)
        if stary is None:
            raport.append((p.name, "PLIK NOWY", []))
            continue
        nowy = json.loads(p.read_text(encoding="utf-8"))
        a, b = pola(stary), pola(nowy)
        if a.keys() != b.keys():
            raport.append((p.name, "ZMIENIONA STRUKTURA POL", []))
            continue
        for klucz in a:
            if a[klucz] == b[klucz]:
                continue
            wstawka = klucz.startswith("WSTAWKA")
            if wstawka:
                we_wstawkach += 1
            else:
                w_bazie += 1
            if tylko_wstawki and not wstawka:
                continue
            raport.append((p.name, klucz, slowa_roznice(a[klucz], b[klucz])))
    return raport, we_wstawkach, w_bazie


def main():
    ap = argparse.ArgumentParser(description="kontrola rundy redakcyjnej")
    ap.add_argument("--ref", required=True, help="commit odniesienia, np. 5d6a1e4")
    ap.add_argument("--tylko-wstawki", action="store_true",
                    help="pokaz wylacznie zmiany w mierzonych wariantach")
    args = ap.parse_args()

    # bez tego konsola Windows (cp1250) gubi polskie znaki wlasnie w tych
    # miejscach, ktore mamy ocenic - raport bylby nieczytelny tam, gdzie liczy
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    raport, we_wstawkach, w_bazie = sprawdz(args.ref, args.tylko_wstawki)

    biezacy = None
    for plik, klucz, zmiany in raport:
        if plik != biezacy:
            print(f"\n{plik}")
            biezacy = plik
        znacznik = "  [WSTAWKA - WARIANT MIERZONY]" if klucz.startswith("WSTAWKA") else ""
        print(f"  {klucz}{znacznik}")
        for bylo, jest in zmiany:
            print(f"      {bylo!r}  ->  {jest!r}")

    print(f"\n=== zmienionych pol: {w_bazie} w bazie dialogu, "
          f"{we_wstawkach} we wstawkach ===")
    print("Kazda pozycja powyzej musi miec odpowiednik w corpus/LISTA-REDAKCYJNA-PL.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
