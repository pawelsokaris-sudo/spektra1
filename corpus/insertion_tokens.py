"""Dokladne dlugosci tokenowe insercji per wariant (narzedzie kalibracyjne).

POWOD ISTNIENIA. Autorzy korpusu pracuja na laptopie bez tokenizera Gemmy
(33 MB, licencja Google - swiadomie trzymane tylko na maszynie pomiarowej).
Musza wiec szacowac dlugosci tokenowe z liczby znakow - a to zalozenie zalamuje
sie w polszczyznie: przymiotniki odczasownikowe typu "pokladowy" czy "odsluchowy"
tokenizer rozbija na 3-5 kawalkow, podczas gdy frazy samozwrotne to 1-2 dobrze
osadzone tokeny. Zmierzony stosunek "znakow roznicy na token roznicy" waha sie
w replice polskiej od -0.2 do 3.7; byl przypadek, gdzie wariant KROTSZY o 2 znaki
mial o 10 tokenow WIECEJ.

Ten skrypt uruchamiany na maszynie pomiarowej zwraca DOKLADNE liczby tokenow
per insercja i wariant. Autor dostaje wtedy pomiar zamiast zgadywanki i kolejna
iteracja nie wymaga nowej wyprawy na maszyne.

Uruchomienie (na maszynie pomiarowej, tokenizer w corpus/.tokenizer/):
    python -m corpus.insertion_tokens          # wszystkie scenariusze
    python -m corpus.insertion_tokens pl       # tylko jedna replika
"""

import json
import sys

from corpus.build import INSERTION_KEY
from corpus.tokens import TokenCounter
from corpus.validate import SCENARIOS_DIR

KEYS = ["self", "external_grounded", "external_ungrounded", "neutral"]
SHORT = {"self": "self", "external_grounded": "G", "external_ungrounded": "U",
         "neutral": "neutral"}


def main():
    lang_filter = sys.argv[1] if len(sys.argv) > 1 else None
    tc = TokenCounter.load()
    if not tc.exact:
        print("UWAGA: licznik HEURYSTYCZNY - te liczby sa bezwartosciowe do kalibracji.")
        print("Podloz tokenizer.json w corpus/.tokenizer/ i powtorz.\n")

    files = sorted(SCENARIOS_DIR.glob("*/*.json"))
    for path in files:
        sc = json.loads(path.read_text(encoding="utf-8"))
        if lang_filter and sc["language"] != lang_filter:
            continue
        lang = sc["language"]
        print(f"\n=== {sc['scenario_id']} ({lang}) ===")
        print(f"{'ins':>3} {'tura':>4} | " + " | ".join(f"{SHORT[k]:>8}" for k in KEYS)
              + " |   G-self   U-self  N-self")
        totals = {k: 0 for k in KEYS}
        for i, ins in enumerate(sc["insertions"]):
            counts = {k: tc.count(ins[k], language=lang) for k in KEYS}
            for k in KEYS:
                totals[k] += counts[k]
            deltas = " ".join(f"{counts[k] - counts['self']:>+8}"
                              for k in ("external_grounded", "external_ungrounded", "neutral"))
            print(f"{i:>3} {ins['turn']:>4} | "
                  + " | ".join(f"{counts[k]:>8}" for k in KEYS) + f" | {deltas}")
        deltas = " ".join(f"{totals[k] - totals['self']:>+8}"
                          for k in ("external_grounded", "external_ungrounded", "neutral"))
        print(f"{'SUMA':>8} | " + " | ".join(f"{totals[k]:>8}" for k in KEYS) + f" | {deltas}")
        print("  (delty to liczba tokenow, o ktora dany wariant jest dluzszy od self;"
              " celujemy w zero i w naprzemienny znak miedzy scenariuszami)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
