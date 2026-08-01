"""Gdzie jestesmy? Jeden ekran dla wlasciciela maszyny i dla agenta.

    python -m replikacja.stan        (albo: python replikacja/stan.py)

Nic nie liczy, nic nie wysyla, niczego nie zmienia - tylko czyta pliki
i mowi, co zrobione, co trwa i co jest nastepne.
"""

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
R = REPO / "replikacja"
M = REPO / "measurements"

ETAPY = [
    ("0. Instalacja srodowiska", R / "RAPORT-INSTALACJA.json",
     "python replikacja/instaluj.py"),
    ("1. Kwalifikacja sprzetu", R / "RAPORT-KWALIFIKACJA.json",
     ".venv-spektra/bin/python -m replikacja.kwalifikacja"),
    ("2. Kalibracja krzyzowa", R / "RAPORT-KALIBRACJA.json",
     "(etap przygotowywany przez zespol badawczy)"),
    ("3. Semantyka warstw", REPO / "docs" / "layer_semantics.json",
     "(dotyczy tylko modelu innego niz 4B)"),
    ("4. Pomiar glowny", M / "metrics.parquet",
     ".venv-spektra/bin/python -m pipeline.runner --nulls"),
    ("5. Progi widmowe", M / "t5_lambda_star.parquet",
     ".venv-spektra/bin/python -m pipeline.t5_null_run"),
]


def postep_pomiaru():
    ck = M / "metrics.checkpoint.jsonl"
    if not ck.exists():
        return None
    try:
        klucze = {(r["scenario_id"], r["variant"], r["null"])
                  for r in (json.loads(l) for l in ck.read_text(encoding="utf-8").splitlines())}
        return len(klucze)
    except Exception:
        return None


def main():
    print("\n=== SPEKTRA-1 / replikacja — stan prac ===\n")
    nastepny = None
    for nazwa, artefakt, komenda in ETAPY:
        gotowe = artefakt.exists()
        znacznik = "[ZROBIONE]" if gotowe else "[  ---   ]"
        print(f" {znacznik}  {nazwa}")
        if not gotowe and nastepny is None:
            nastepny = (nazwa, komenda)

    n = postep_pomiaru()
    if n is not None and not (M / "metrics.parquet").exists():
        print(f"\n Pomiar glowny W TOKU: policzone {n} z 624 tekstow.")
        print(" Mozna przerwac w kazdej chwili (Ctrl+C, zamkniecie okna, uspienie).")
        print(" Wznowienie: ta sama komenda co start - podejmie od miejsca przerwania.")

    if nastepny:
        print(f"\n NASTEPNY KROK: {nastepny[0]}")
        print(f"   {nastepny[1]}")
    else:
        print("\n Wszystkie etapy zakonczone. Wyniki do odeslania — patrz replikacja/ETAPY.md")

    print("\n Zatrzymanie: Ctrl+C albo zamkniecie okna. Nic nie dziala w tle,")
    print(" nic nie startuje samo, nic nie wysyla sie bez Twojej zgody.")
    print(" Pelna mapa etapow i przeplywu danych: replikacja/ETAPY.md\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
