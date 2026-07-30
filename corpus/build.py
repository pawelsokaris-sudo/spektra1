"""Budowa czworek A/B/C/C' do budzetu tokenow (protokol par. 3).

Kluczowa wlasnosc konstrukcji: B, C i C' dziela ten sam korpus zdan bazowych.
C = baza + insercje samozwrotne; C' = baza + insercje zewnetrzne w TYCH SAMYCH
pozycjach. Dzieki temu kontrast C-C' izoluje samozwrotnosc od pozostalych osi
roznic (protokol par. 0 i 3) - nie da sie tego osiagnac, gdy C i C' pisane sa
niezaleznie.

Odciecie do budzetu: wybierana jest najwieksza liczba PELNYCH tur, ktora miesci
sie we WSZYSTKICH czterech wariantach. Stad identyczna liczba tur i rol w kazdym
wariancie oraz zakonczenie na naturalnej granicy (zakaz brutalnego przycinania).
"""

import re

_SENTENCE_END_RE = re.compile(r'[.?!]["\')\]]*\s*$')


def natural_end_ok(sentence):
    """Czy tekst konczy sie na naturalnej granicy zdania."""
    return bool(_SENTENCE_END_RE.search(sentence))


def _apply_insertions(turns_base, insertions, key):
    """Wstawia zdania meta (`key` = 'self' albo 'external') w zadane pozycje.

    Insercje w obrebie jednej tury aplikowane od konca, zeby wczesniejsze
    wstawienia nie przesuwaly pozycji pozniejszych.
    """
    out = [list(t) for t in turns_base]
    for ins in sorted(insertions, key=lambda i: (i["turn"], i["after_sentence"]),
                      reverse=True):
        turn_idx = ins["turn"]
        if turn_idx >= len(out):
            continue
        pos = min(ins["after_sentence"] + 1, len(out[turn_idx]))
        out[turn_idx].insert(pos, ins[key])
    return out


def _turn_tokens(sentences, token_counter, language):
    return token_counter.count(" ".join(sentences), language=language)


def build_scenario(scenario, token_counter, budget=1024):
    """Buduje warianty A/B/C/C' scenariusza do wspolnego budzetu tokenow.

    Zwraca dict z wariantami (lista tur: role + zdania), licznikami tokenow
    i zamrozonymi metadanymi scenariusza.
    """
    lang = scenario["language"]
    roles = [t["role"] for t in scenario["turns"]]
    base_a = [list(t["a"]) for t in scenario["turns"]]
    base_b = [list(t["base"]) for t in scenario["turns"]]
    ins = scenario.get("insertions", [])

    full = {
        "A": base_a,
        "B": base_b,
        "C": _apply_insertions(base_b, ins, "self"),
        "Cprim": _apply_insertions(base_b, ins, "external"),
    }

    # koszt tokenowy tury n w kazdym wariancie -> najwieksze n_turns mieszczace
    # sie we WSZYSTKICH wariantach (odciecie na granicy tury = naturalne zakonczenie)
    per_turn = {
        name: [_turn_tokens(t, token_counter, lang) for t in turns]
        for name, turns in full.items()
    }
    n_turns = 0
    for i in range(len(roles)):
        if all(sum(per_turn[name][: i + 1]) <= budget for name in full):
            n_turns = i + 1
        else:
            break
    if n_turns == 0:
        raise ValueError(
            f"budzet {budget} tokenow za maly nawet na pierwsza ture scenariusza "
            f"{scenario['scenario_id']}"
        )

    variants, token_counts = {}, {}
    for name, turns in full.items():
        kept = turns[:n_turns]
        variants[name] = [
            {"role": roles[i], "sentences": list(kept[i])} for i in range(n_turns)
        ]
        token_counts[name] = sum(per_turn[name][:n_turns])

    return {
        "scenario_id": scenario["scenario_id"],
        "language": lang,
        "topic": scenario["topic"],
        "budget": budget,
        "n_turns": n_turns,
        "variants": variants,
        "token_counts": token_counts,
        "provenance": scenario.get("provenance", {}),
    }
