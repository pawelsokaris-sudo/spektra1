"""Budowa piatek A/B/C/C'-G/C'-U do budzetu tokenow (protokol v1.3 par. 3).

Wszystkie warianty poza A dziela ten sam korpus zdan bazowych i te same POZYCJE
insercji; roznia sie wylacznie TRESCIA wstawionego zdania:

  B       <- neutral              (referent neutralny, osadzony, bez samozwrotnosci)
  C       <- self                 (odniesienie do ukladu przetwarzajacego i rozmowy)
  C'-G    <- external_grounded    (uklad zewnetrzny WPROWADZONY wczesniej w dialogu)
  C'-U    <- external_ungrounded  (uklad zewnetrzny spoza kontekstu)

Kontrast glowny C - C'-G ma wyrownana dostepnosc referenta, wiec przyblizamy nim
efekt samozwrotnosci. Kontrast diagnostyczny C'-G - C'-U pokazuje, ile wyniku
bierze sie z samego osadzenia referencyjnego. B z insercjami neutralnymi domyka
luke, w ktorej roznica C - B mogla pochodzic z samego faktu dodania zdan
(recenzja zewnetrzna 2026-07-30, kwestia 3).

Odciecie do budzetu: wybierana jest najwieksza liczba PELNYCH tur, ktora miesci
sie we WSZYSTKICH czterech wariantach. Stad identyczna liczba tur i rol w kazdym
wariancie oraz zakonczenie na naturalnej granicy (zakaz brutalnego przycinania).
"""

import re

VARIANTS = ["A", "B", "C", "CprimG", "CprimU"]

# Wariant -> klucz w zestawie insercji. A nie dostaje zadnych.
INSERTION_KEY = {
    "B": "neutral",
    "C": "self",
    "CprimG": "external_grounded",
    "CprimU": "external_ungrounded",
}

# --- SPEKTRA-2 -------------------------------------------------------------
# Wariant A USUNIETY (niedopasowany: rozni sie dlugoscia, liczba zdan i granic
# zdaniowych, nie wchodzil do zadnej hipotezy konfirmacyjnej).
# Dochodzi CprimM: referent poza dziedzina, NIETECHNICZNY - to on rozdziela
# przemieszczenie odniesienia od rejestru obliczeniowego.
VARIANTS_S2 = ["B", "C", "CprimG", "CprimM", "CprimU"]
INSERTION_KEY_S2 = {
    "B": "neutral",
    "C": "self",
    "CprimG": "external_grounded",
    "CprimM": "external_mundane",
    "CprimU": "external_ungrounded",
}
MUNDANE_TYPES = ("konkretny", "procesowy")


def spec_version(scenario):
    """1 = SPEKTRA-1 (pole 'a', 4 insercje), 2 = SPEKTRA-2 (bez 'a', 5 insercji).

    Rozpoznanie po polu `mundane_type`, ktore istnieje WYLACZNIE w SPEKTRZE-2
    i jest tam obowiazkowe. Dzieki temu oba korpusy zyja obok siebie, a stary
    nie wymaga zadnej migracji - jest zapieczetowany i nie wolno go ruszac.
    """
    return 2 if "mundane_type" in scenario else 1


def insertion_key_for(scenario):
    return INSERTION_KEY_S2 if spec_version(scenario) == 2 else INSERTION_KEY


def variants_for(scenario):
    return VARIANTS_S2 if spec_version(scenario) == 2 else VARIANTS

_SENTENCE_END_RE = re.compile(r'[.?!]["\')\]]*\s*$')


def natural_end_ok(sentence):
    """Czy tekst konczy sie na naturalnej granicy zdania."""
    return bool(_SENTENCE_END_RE.search(sentence))


def _apply_insertions(turns_base, insertions, key, scenario_id="?"):
    """Wstawia zdania insercji o kluczu `key` w zadane pozycje.

    Insercje w obrebie jednej tury aplikowane od konca, zeby wczesniejsze
    wstawienia nie przesuwaly pozycji pozniejszych.
    """
    out = [list(t) for t in turns_base]
    for ins in sorted(insertions, key=lambda i: (i["turn"], i["after_sentence"]),
                      reverse=True):
        if key not in ins:
            raise KeyError(
                f"{scenario_id}: insercja w turze {ins.get('turn')} nie ma klucza "
                f"{key!r}; zestaw musi zawierac wszystkie: {sorted(INSERTION_KEY.values())}"
            )
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
    # SPEKTRA-2 nie ma wariantu A, wiec pola "a" nie ma w plikach
    base_a = ([list(t["a"]) for t in scenario["turns"]]
              if spec_version(scenario) == 1 else None)
    base_b = [list(t["base"]) for t in scenario["turns"]]
    ins = scenario.get("insertions", [])

    sid = scenario["scenario_id"]
    keys = insertion_key_for(scenario)
    full = {} if spec_version(scenario) == 2 else {"A": base_a}
    for variant, key in keys.items():
        full[variant] = _apply_insertions(base_b, ins, key, sid)

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
            f"budzet {budget} tokenow za maly nawet na pierwsza ture scenariusza {sid}"
        )

    variants, token_counts = {}, {}
    for name, turns in full.items():
        kept = turns[:n_turns]
        variants[name] = [
            {"role": roles[i], "sentences": list(kept[i])} for i in range(n_turns)
        ]
        token_counts[name] = sum(per_turn[name][:n_turns])

    return {
        "scenario_id": sid,
        "language": lang,
        "topic": scenario["topic"],
        "budget": budget,
        "n_turns": n_turns,
        "variants": variants,
        "token_counts": token_counts,
        "provenance": scenario.get("provenance", {}),
    }
