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

from corpus.build import build_scenario, natural_end_ok
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
    for k, pair in enumerate(ins):
        s, e = pair.get("self", ""), pair.get("external", "")
        if pair.get("turn", 0) > MAX_INSERTION_TURN:
            problems.append(
                f"{sid}: insercja {k} w turze {pair.get('turn')} - dozwolone tury "
                f"0-{MAX_INSERTION_TURN} (dalsze moga nie przetrwac ciecia do budzetu)"
            )
        if max(len(s), len(e)) and abs(len(s) - len(e)) / max(len(s), len(e)) > PAIR_LENGTH_TOL:
            problems.append(
                f"{sid}: insercja {k} - dlugosc self={len(s)} vs external={len(e)} znakow, "
                f"roznica {abs(len(s) - len(e)) / max(len(s), len(e)):.1%} > {PAIR_LENGTH_TOL:.0%}"
            )
        if _is_question(s) != _is_question(e):
            problems.append(
                f"{sid}: insercja {k} - typ zdania rozny (self "
                f"{'pytanie' if _is_question(s) else 'twierdzenie'}, external "
                f"{'pytanie' if _is_question(e) else 'twierdzenie'})"
            )
        if not natural_end_ok(s) or not natural_end_ok(e):
            problems.append(f"{sid}: insercja {k} - brak naturalnego zakonczenia zdania")
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
    c, cp = out["token_counts"]["C"], out["token_counts"]["Cprim"]
    if max(c, cp) and abs(c - cp) / max(c, cp) > TOTAL_TOKEN_TOL:
        problems.append(
            f"{sid}: C={c} vs C'={cp} tokenow, roznica "
            f"{abs(c - cp) / max(c, cp):.1%} > {TOTAL_TOKEN_TOL:.0%} (wymog protokolu par. 3)"
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
            summaries.append(
                f"  {sc['scenario_id']:<28} {sc['language']}  tur={out['n_turns']:>2}  "
                f"A={out['token_counts']['A']:>4} B={out['token_counts']['B']:>4} "
                f"C={out['token_counts']['C']:>4} C'={out['token_counts']['Cprim']:>4}  "
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
