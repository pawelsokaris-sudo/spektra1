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

from corpus.build import (INSERTION_KEY, MUNDANE_TYPES, build_scenario,
                          insertion_key_for, natural_end_ok, spec_version,
                          variants_for)
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
        pola = ("a", "base") if spec_version(scenario) == 1 else ("base",)
        for key in pola:
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
        if spec_version(scenario) == 2:
            continue          # SPEKTRA-2 nie ma wariantu A - nie ma czego porownywac
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
    keys = sorted(set(insertion_key_for(scenario).values()))
    for k, pair in enumerate(ins):
        missing = [key for key in keys if key not in pair]
        if missing:
            problems.append(
                f"{sid}: insercja {k} nie ma kluczy {missing} - zestaw musi zawierac "
                f"wszystkie {len(keys)} wariantow wstawki"
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


_SAMOZWROTNE_RDZENIE = {
    # RDZENIE, nie pelne frazy: polski odmienia, wiec "to planowanie" wystepuje
    # w ramie jako "tym planowaniu". Dopasowanie po mianowniku nie zlapaloby nic.
    "pl": ["planowani", "decyzj", "oczekiwani", "wybor", "wybór", "zastanawiani",
           "wymian", "pytani", "prob", "prób", "rozmow", "przetwarzani"],
    "en": ["planning", "decision", "waiting", "choice", "exchange", "question",
           "attempt", "conversation", "processing"],
}


def differing_span(a, b):
    """Fragment, ktorym rozni sie dwa zdania: (wspolny prefiks, srodek_a, srodek_b).

    Warianty insercji dziela RAME i roznia sie wylacznie fraza rzeczownikowa
    (spec par. 2). Odcinajac wspolny poczatek i koniec dostajemy sama podmieniana
    fraze - i tylko ja sprawdzamy pod katem pulapek. Dzieki temu slowo z ramy
    (np. "pytanie" w pytajacej ramie) nie wywoluje falszywego alarmu.
    """
    i = 0
    while i < min(len(a), len(b)) and a[i] == b[i]:
        i += 1
    j = 0
    while j < min(len(a), len(b)) - i and a[len(a) - 1 - j] == b[len(b) - 1 - j]:
        j += 1
    return a[:i], a[i:len(a) - j], b[i:len(b) - j]


def check_mundane(scenario):
    """Kontrole wariantu zwyczajnego - istnieja WYLACZNIE w SPEKTRZE-2."""
    problems = []
    if spec_version(scenario) != 2:
        return problems
    sid = scenario.get("scenario_id", "?")
    mt = scenario.get("mundane_type")
    if mt not in MUNDANE_TYPES:
        problems.append(
            f"{sid}: mundane_type='{mt}' - dozwolone {list(MUNDANE_TYPES)}. "
            f"To pole pilnuje balansu konkretny/procesowy (spec par. 3)"
        )
    rdzenie = _SAMOZWROTNE_RDZENIE.get(scenario.get("language", "pl"), [])
    for k, pair in enumerate(scenario.get("insertions", [])):
        mundane, ref = pair.get("external_mundane"), pair.get("neutral")
        if not mundane or not ref:
            continue
        _, fraza_m, _ = differing_span(mundane, ref)
        if not fraza_m.strip():
            problems.append(
                f"{sid}: insercja {k} - wariant zwyczajny jest IDENTYCZNY "
                f"z neutralnym; podmieniona fraza musi sie roznic"
            )
            continue
        # udzial ramy: jesli rozni sie wiecej niz sama fraza, spec par. 2 zlamana
        if len(fraza_m) > 0.5 * len(mundane):
            problems.append(
                f"{sid}: insercja {k} - warianty roznia sie na "
                f"{len(fraza_m)}/{len(mundane)} znakow, czyli WIECEJ niz sama fraza "
                f"rzeczownikowa. Rama musi byc wspolna (spec par. 2)"
            )
        low = fraza_m.lower()
        for rdzen in rdzenie:
            if rdzen in low:
                problems.append(
                    f"{sid}: insercja {k} - referent zwyczajny '{fraza_m.strip()}' "
                    f"zawiera rdzen '{rdzen}', ktory w rozmowie czyta sie jako "
                    f"SAMOZWROTNY. Zakotwicz go poza rozmowa (spec par. 3, warunek 4)"
                )
                break
    return problems


def check_mundane_balance(scenarios):
    """Balans konkretny/procesowy w obrebie jezyka (spec par. 3, warunek 3).

    Bez tego wariant zwyczajny roznilby sie od pozostalych takze na osi
    konkretne-abstrakcyjne i wymienilibysmy jeden confound na drugi.
    """
    problems = []
    per_lang = {}
    for sc in scenarios:
        if spec_version(sc) != 2:
            continue
        per_lang.setdefault(sc.get("language", "?"), []).append(sc.get("mundane_type"))
    for lang, typy in sorted(per_lang.items()):
        n = len(typy)
        k = sum(1 for x in typy if x == "konkretny")
        p = sum(1 for x in typy if x == "procesowy")
        if abs(k - p) > 1:
            problems.append(
                f"[{lang}] balans mundane_type: konkretny={k}, procesowy={p} "
                f"z {n} scenariuszy - roznica {abs(k - p)}, dozwolona max 1"
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
            + check_meta_leak(scenario) + check_mundane(scenario))


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
    import argparse

    ap = argparse.ArgumentParser(description="walidator korpusu")
    ap.add_argument("--dir", default=None,
                    help="katalog scenariuszy; domyslnie corpus/scenarios "
                         "(SPEKTRA-1). Dla SPEKTRY-2: corpus/scenarios-2")
    args = ap.parse_args()

    katalog = Path(args.dir) if args.dir else SCENARIOS_DIR
    tc = TokenCounter.load()
    all_problems, summaries = [], []
    files = sorted(katalog.glob("*/*.json"))
    if not files:
        print(f"Brak scenariuszy w {katalog}")
        return 1
    wszystkie = []
    for path in files:
        sc = json.loads(path.read_text(encoding="utf-8"))
        wszystkie.append(sc)
        problems = validate_scenario(sc)
        build_problems, out = check_build(sc, tc)
        problems += build_problems
        all_problems += problems
        if out:
            tc_ = out["token_counts"]
            licz = "  ".join(f"{v}={tc_[v]}" for v in variants_for(sc) if v in tc_)
            summaries.append(
                f"  {sc['scenario_id']:<28} {sc['language']}  tur={out['n_turns']:>2}  "
                f"{licz}  {'OK' if not problems else f'{len(problems)} PROBLEMOW'}"
            )
    all_problems += check_mundane_balance(wszystkie)
    wersje = sorted({spec_version(s) for s in wszystkie})
    print(f"Scenariuszy: {len(files)} | specyfikacja: SPEKTRA-{'/'.join(map(str, wersje))} "
          f"| licznik tokenow: "
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
