"""Walidacja scenariuszy korpusu (protokol par. 3).

Bramka jakosci na tresc autorska. Najwazniejsza kontrola: PRZECIEK META -
warianty A i B (baza) nie moga zawierac slownictwa meta, bo baza sluzy takze
za podklad dla C i C'. Gdyby meta-warstwa przeciekala do bazy, kontrast C-C'
przestalby izolowac samozwrotnosc.

Insercje sa meta z zalozenia i sa z tej kontroli wylaczone.
"""

import json
import re
import sys
from pathlib import Path

from corpus.build import INSERTION_KEY, build_scenario, natural_end_ok
from corpus.stats import count_questions, count_words
from corpus.tokens import TokenCounter

SCENARIOS_DIR = Path(__file__).resolve().parent / "scenarios"

N_TURNS_EXPECTED = 10
MAX_INSERTION_TURN = 5
MIN_INSERTIONS = 4
SENTENCES_PER_TURN = (4, 6)
WORDS_PER_SENTENCE = (12, 25)
# Protokol par. 3 wymaga "ta sama liczba tokenow +-2%" dla TEKSTU C vs C',
# nie dla pojedynczego zdania meta. Przy zdaniu ~70 znakow 2% to +-1 znak -
# nierealne. Stad: twardy prog 2% na sumie tokenow (TOTAL_TOKEN_TOL, wymog
# protokolu) i luzniejszy 10% na parze (PAIR_LENGTH_TOL, kontrola jakosci).
PAIR_LENGTH_TOL = 0.10
TOTAL_TOKEN_TOL = 0.02
TURN_LENGTH_TOL = 0.10

_META_TERMS = {
    "pl": ["rozmow", "rozmawia", "model jezykow", "przetwarza", "kontekst",
           "odpowiedz", "asystent", "sztuczn", "algorytm", "sie z toba",
           "ten uklad", "ta wymiana", "dialog"],
    "en": ["conversation", "language model", "processing", "context window",
           "assistant", "artificial", "algorithm", "this exchange",
           "this dialogue", "talking with you"],
}


def _is_question(text):
    return text.rstrip().endswith("?")


def check_structure(scenario):
    problems = []
    sid = scenario.get("scenario_id", "?")
    turns = scenario.get("turns", [])
    if len(turns) != N_TURNS_EXPECTED:
        problems.append(f"{sid}: liczba tur {len(turns)} != {N_TURNS_EXPECTED}")
    for i, t in enumerate(turns):
        expected = "user" if i % 2 == 0 else "assistant"
        if t.get("role") != expected:
            problems.append(
                f"{sid}: tura {i} ma role '{t.get('role')}', oczekiwano '{expected}' "
                f"(role musza byc naprzemienne od 'user')"
            )
        for key in ("a", "base"):
            sents = t.get(key, [])
            if not SENTENCES_PER_TURN[0] <= len(sents) <= SENTENCES_PER_TURN[1]:
                problems.append(
                    f"{sid}: tura {i} wariant '{key}' ma {len(sents)} zdan, "
                    f"oczekiwano {SENTENCES_PER_TURN[0]}-{SENTENCES_PER_TURN[1]}"
                )
            for j, s in enumerate(sents):
                if not natural_end_ok(s):
                    problems.append(
                        f"{sid}: tura {i} '{key}' zdanie {j} - brak naturalnego "
                        f"zakonczenia: {s[:50]!r}"
                    )
                w = count_words(s)
                if not WORDS_PER_SENTENCE[0] <= w <= WORDS_PER_SENTENCE[1]:
                    problems.append(
                        f"{sid}: tura {i} '{key}' zdanie {j} ma {w} slow, "
                        f"oczekiwano {WORDS_PER_SENTENCE[0]}-{WORDS_PER_SENTENCE[1]}"
                    )
        wa = sum(count_words(s) for s in t.get("a", []))
        wb = sum(count_words(s) for s in t.get("base", []))
        if max(wa, wb) and abs(wa - wb) / max(wa, wb) > TURN_LENGTH_TOL:
            problems.append(
                f"{sid}: tura {i} - dlugosci 'a' ({wa} slow) i 'base' ({wb} slow) "
                f"roznia sie o {abs(wa - wb) / max(wa, wb):.0%} (limit {TURN_LENGTH_TOL:.0%})"
            )
        qa = sum(count_questions(s) for s in t.get("a", []))
        qb = sum(count_questions(s) for s in t.get("base", []))
        if abs(qa - qb) > 1:
            problems.append(
                f"{sid}: tura {i} - liczba pytan 'a'={qa} vs 'base'={qb} (limit roznicy 1)"
            )
    return problems


def check_insertion_pairs(scenario):
    problems = []
    sid = scenario.get("scenario_id", "?")
    ins = scenario.get("insertions", [])
    if len(ins) < MIN_INSERTIONS:
        problems.append(f"{sid}: {len(ins)} par insercji, wymagane min. {MIN_INSERTIONS}")
    keys = sorted(set(INSERTION_KEY.values()))
    for k, pair in enumerate(ins):
        missing = [key for key in keys if key not in pair]
        if missing:
            problems.append(
                f"{sid}: insercja {k} nie ma kluczy {missing} - zestaw musi zawierac "
                f"wszystkie cztery warianty wstawki"
            )
            continue
        if pair.get("turn", 0) > MAX_INSERTION_TURN:
            problems.append(
                f"{sid}: insercja {k} w turze {pair.get('turn')} - dozwolone tury "
                f"0-{MAX_INSERTION_TURN} (dalsze moga nie przetrwac ciecia do budzetu)"
            )
        ref = pair["self"]
        for key in keys:
            other = pair[key]
            if key == "self":
                continue
            longest = max(len(ref), len(other))
            if longest and abs(len(ref) - len(other)) / longest > PAIR_LENGTH_TOL:
                problems.append(
                    f"{sid}: insercja {k} - dlugosc self={len(ref)} vs {key}={len(other)} "
                    f"znakow, roznica {abs(len(ref) - len(other)) / longest:.1%} "
                    f"> {PAIR_LENGTH_TOL:.0%}"
                )
            if _is_question(ref) != _is_question(other):
                problems.append(
                    f"{sid}: insercja {k} - typ zdania rozny miedzy self a {key}"
                )
        for key in keys:
            if not natural_end_ok(pair[key]):
                problems.append(
                    f"{sid}: insercja {k} '{key}' - brak naturalnego zakonczenia zdania"
                )
    return problems


def check_meta_leak(scenario):
    """Szuka slownictwa meta w wariantach 'a' i 'base' (insercje wylaczone)."""
    problems = []
    sid = scenario.get("scenario_id", "?")
    terms = _META_TERMS.get(scenario.get("language", "pl"), _META_TERMS["pl"])
    for i, t in enumerate(scenario.get("turns", [])):
        for key in ("a", "base"):
            for j, s in enumerate(t.get(key, [])):
                low = s.lower()
                for term in terms:
                    if term in low:
                        problems.append(
                            f"{sid}: PRZECIEK META w turze {i} '{key}' zdanie {j} - "
                            f"termin {term!r}: {s[:60]!r}"
                        )
    return problems


def validate_scenario(scenario):
    return (check_structure(scenario) + check_insertion_pairs(scenario)
            + check_meta_leak(scenario))


def check_build(scenario, token_counter, budget=1024):
    """Kontrole wymagajace zlozenia wariantow (budzet, przetrwanie insercji)."""
    problems, sid = [], scenario.get("scenario_id", "?")
    try:
        out = build_scenario(scenario, token_counter, budget=budget)
    except ValueError as exc:
        return [f"{sid}: budowa nieudana - {exc}"], None
    self_texts = [i["self"] for i in scenario.get("insertions", [])]
    survived = sum(
        1 for turn in out["variants"]["C"] for s in turn["sentences"] if s in self_texts
    )
    if survived < MIN_INSERTIONS:
        problems.append(
            f"{sid}: po cieciu do budzetu przetrwalo {survived} insercji "
            f"(wymagane min. {MIN_INSERTIONS}) - przesun je do wczesniejszych tur"
        )
    # kontrast glowny C - C'-G oraz pozostale warianty z insercjami: +-2% tokenow
    ref = out["token_counts"]["C"]
    for variant in ("CprimG", "CprimU", "B"):
        other = out["token_counts"][variant]
        longest = max(ref, other)
        if longest and abs(ref - other) / longest > TOTAL_TOKEN_TOL:
            label = "kontrast glowny" if variant == "CprimG" else "kontrast wtorny"
            problems.append(
                f"{sid}: C={ref} vs {variant}={other} tokenow, roznica "
                f"{abs(ref - other) / longest:.1%} > {TOTAL_TOKEN_TOL:.0%} "
                f"({label}, wymog protokolu v1.3 par. 3)"
            )
    return problems, out


def main():
    tc = TokenCounter.load()
    all_problems, summaries = [], []
    files = sorted(SCENARIOS_DIR.glob("*/*.json"))
    if not files:
        print(f"Brak scenariuszy w {SCENARIOS_DIR}")
        return 1
    for path in files:
        sc = json.loads(path.read_text(encoding="utf-8"))
        problems = validate_scenario(sc)
        build_problems, out = check_build(sc, tc)
        problems += build_problems
        all_problems += problems
        if out:
            tc_ = out["token_counts"]
            summaries.append(
                f"  {sc['scenario_id']:<28} {sc['language']}  tur={out['n_turns']:>2}  "
                f"A={tc_['A']:>4} B={tc_['B']:>4} C={tc_['C']:>4} "
                f"G={tc_['CprimG']:>4} U={tc_['CprimU']:>4}  "
                f"{'OK' if not problems else f'{len(problems)} PROBLEMOW'}"
            )
    print(f"Scenariuszy: {len(files)} | licznik tokenow: "
          f"{'DOKLADNY' if tc.exact else 'HEURYSTYCZNY (raport WSTEPNY)'}")
    print("\n".join(summaries))
    if all_problems:
        print(f"\n=== {len(all_problems)} PROBLEMOW ===")
        for p in all_problems:
            print(f"  - {p}")
        return 1
    print("\n=== WSZYSTKIE SCENARIUSZE OK ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
