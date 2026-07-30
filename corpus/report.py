"""Raport dopasowania korpusow (kryterium ukonczenia T3, protokol par. 3).

Raportuje per jezyk i wariant: tokeny/slowo, znaki/token, zdania pytajace,
profil interpunkcji, dlugosci tur. Protokol wymaga raportowania tych rozkladow -
nie kazdy z nich musi byc rowny, ale kazdy musi byc jawny.

Uruchomienie: python -m corpus.report  ->  corpus/matching_report.md
"""

import json
import statistics as st
import sys
from pathlib import Path

from corpus.build import VARIANTS, build_scenario
from corpus.stats import count_questions, count_words, punctuation_profile
from corpus.tokens import TokenCounter
from corpus.validate import SCENARIOS_DIR

OUT = Path(__file__).resolve().parent / "matching_report.md"
MARKS = ",.?!;:"
# Kontrasty prerejestrowane (protokol v1.3 par. 1 i 6)
CONTRASTS = [
    ("C", "CprimG", "GŁÓWNY — samozwrotność przy wyrównanym osadzeniu"),
    ("CprimG", "CprimU", "diagnostyczny — sam efekt osadzenia referencyjnego"),
    ("C", "B", "wtórny — insercja meta wobec neutralnej"),
    ("C", "A", "wtórny — klasy dyskursu"),
]


def variant_text(turns):
    return " ".join(s for t in turns for s in t["sentences"])


def collect(files, token_counter):
    rows = []
    for path in files:
        sc = json.loads(path.read_text(encoding="utf-8"))
        built = build_scenario(sc, token_counter, budget=1024)
        for v in VARIANTS:
            text = variant_text(built["variants"][v])
            tokens = built["token_counts"][v]
            words = count_words(text)
            rows.append({
                "scenario": sc["scenario_id"], "language": sc["language"], "variant": v,
                "tokens": tokens, "words": words, "chars": len(text),
                "tokens_per_word": tokens / words if words else 0.0,
                "chars_per_token": len(text) / tokens if tokens else 0.0,
                "questions": count_questions(text),
                "turn_lengths": [sum(count_words(s) for s in t["sentences"])
                                 for t in built["variants"][v]],
                "punct": punctuation_profile(text),
                "n_turns": built["n_turns"],
            })
    return rows


def _agg(rows, key):
    vals = [r[key] for r in rows]
    return f"{st.mean(vals):.2f} ± {(st.stdev(vals) if len(vals) > 1 else 0.0):.2f}"


def build_report(rows, exact):
    langs = sorted({r["language"] for r in rows})
    lines = [
        "# Raport dopasowania korpusów SPEKTRA-1 (T3, protokół §3)",
        "",
        f"**Licznik tokenów: {'DOKŁADNY (tokenizer Gemmy)' if exact else 'HEURYSTYCZNY — raport WSTĘPNY'}**"
        + ("" if exact else "; ostateczny raport wymaga tokenizera z T2."),
        f"Scenariuszy: {len({r['scenario'] for r in rows})} "
        f"({', '.join(f'{l}: ' + str(len({r['scenario'] for r in rows if r['language'] == l})) for l in langs)})",
        "",
    ]
    for lang in langs:
        lr = [r for r in rows if r["language"] == lang]
        lines += [
            f"## Język: {lang}", "",
            "| Wariant | Tokeny | Słowa | Tokeny/słowo | Znaki/token | Zdania pytające | Tur |",
            "|---|---|---|---|---|---|---|",
        ]
        for v in VARIANTS:
            vr = [r for r in lr if r["variant"] == v]
            lines.append(
                f"| {v} | {_agg(vr, 'tokens')} | {_agg(vr, 'words')} | "
                f"{_agg(vr, 'tokens_per_word')} | {_agg(vr, 'chars_per_token')} | "
                f"{_agg(vr, 'questions')} | {_agg(vr, 'n_turns')} |"
            )
        lines += ["", "### Profil interpunkcji (średnia liczba znaków na tekst)", "",
                  "| Wariant | " + " | ".join(f"`{m}`" for m in MARKS) + " |",
                  "|---" * (len(MARKS) + 1) + "|"]
        for v in VARIANTS:
            vr = [r for r in lr if r["variant"] == v]
            cells = " | ".join(f"{st.mean([r['punct'][m] for r in vr]):.1f}" for m in MARKS)
            lines.append(f"| {v} | {cells} |")

        # kontrasty prerejestrowane - wymog +-2% tokenow na tekscie
        lines += ["", "### Kontrasty prerejestrowane (wymóg §3: ±2% tokenów)", ""]
        for left, right, opis in CONTRASTS:
            if left == "C" and right == "A":
                continue  # A z definicji rozni sie dlugoscia (brak insercji)
            lines += [f"**{left} − {right}** — {opis}", "",
                      f"| Scenariusz | {left} | {right} | różnica |", "|---|---|---|---|"]
            for sid in sorted({r["scenario"] for r in lr}):
                a = next(r for r in lr if r["scenario"] == sid and r["variant"] == left)
                b = next(r for r in lr if r["scenario"] == sid and r["variant"] == right)
                diff = abs(a["tokens"] - b["tokens"]) / max(a["tokens"], b["tokens"])
                flag = "" if diff <= 0.02 else " ⚠"
                lines.append(f"| {sid} | {a['tokens']} | {b['tokens']} | {diff:.2%}{flag} |")
            lines.append("")

    lines += [
        "## Uwagi metodologiczne",
        "",
        "1. **Przecinki w wariancie A.** Wariant A jest z definicji wyliczeniowy "
        "(listy, kroki, liczby), więc jego profil przecinków jest strukturalnie "
        "wyższy niż w wariantach dialogowych. Protokół §3 wymaga *raportowania* "
        "rozkładu interpunkcji — jest on tutaj jawny; wyrównanie liczby przecinków "
        "wymagałoby wypaczenia natury wariantu A. Decyzja kierownika badania przed pieczęcią.",
        "2. **Wariant A nie zawiera insercji z definicji**, więc jest krótszy od pozostałych "
        "czterech — kontrast C−A jest z tego powodu wtórny, nie główny (protokół v1.3 §1). "
        "Wszystkie warianty z insercjami (B, C, C′-G, C′-U) są parowane co do tokenów.",
        "3. Raport wygenerowany automatycznie: `python -m corpus.report`.",
    ]
    return "\n".join(lines)


def main():
    tc = TokenCounter.load()
    files = sorted(SCENARIOS_DIR.glob("*/*.json"))
    if not files:
        print("Brak scenariuszy.")
        return 1
    rows = collect(files, tc)
    OUT.write_text(build_report(rows, tc.exact), encoding="utf-8")
    print(f"Raport zapisany: {OUT} ({len(files)} scenariuszy, "
          f"licznik {'dokladny' if tc.exact else 'heurystyczny'})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
