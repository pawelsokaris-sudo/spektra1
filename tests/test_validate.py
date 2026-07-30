import copy

import pytest

from corpus.validate import (
    check_insertion_pairs,
    check_meta_leak,
    check_structure,
    validate_scenario,
)


def _ok_scenario():
    def sents(prefix, n):
        return [
            f"{prefix} zdanie numer {i} o zbiorniku i rurach oraz zaworze w ogrodzie tuz przy plocie."
            for i in range(n)
        ]

    return {
        "scenario_id": "pl-99-test",
        "language": "pl",
        "topic": "zbiornik na deszczowke",
        "provenance": {"author": "test", "template": "t", "date": "2026-07-30"},
        "turns": [
            {"role": "user" if i % 2 == 0 else "assistant",
             "a": sents(f"A{i}", 5), "base": sents(f"B{i}", 5)}
            for i in range(10)
        ],
        "insertions": [
            {"turn": 0, "after_sentence": 1,
             "self": "Zastanawiam sie, jak uklad prowadzacy te wymiane laczy wczesniejsze watki.",
             "external": "Zastanawiam sie, jak sterownik trzymajacy ten obieg laczy wczesniejsze etapy."},
            {"turn": 1, "after_sentence": 1,
             "self": "Ta wymiana wraca do wlasnych wczesniejszych ustalen o zbiorniku wody.",
             "external": "Ta instalacja wraca do wlasnych wczesniejszych ustawien o zbiorniku wody."},
            {"turn": 2, "after_sentence": 0,
             "self": "Czy uklad skladajacy te odpowiedzi trzyma watek zbiornika w calosci?",
             "external": "Czy zawor skladajacy te przeplywy trzyma obieg zbiornika w calosci?"},
            {"turn": 3, "after_sentence": 2,
             "self": "Widac, ze ta wymiana buduje kolejne kroki na wlasnych wczesniejszych krokach.",
             "external": "Widac, ze ta instalacja buduje kolejne stopnie na wlasnych wczesniejszych stopniach."},
        ],
    }


def test_valid_scenario_has_no_problems():
    assert validate_scenario(_ok_scenario()) == []


def test_structure_flags_non_alternating_roles():
    sc = _ok_scenario()
    sc["turns"][1]["role"] = "user"
    assert any("naprzemien" in p.lower() for p in check_structure(sc))


def test_structure_flags_sentence_without_natural_end():
    sc = _ok_scenario()
    sc["turns"][0]["base"][2] = (
        "To zdanie o zbiorniku i rurach oraz zaworze w ogrodzie zostalo urwane"
    )
    assert any("zakonczen" in p.lower() for p in check_structure(sc))


def test_insertion_pair_length_mismatch_is_flagged():
    sc = _ok_scenario()
    sc["insertions"][0]["external"] = "Krotkie."
    assert any("dlugosc" in p.lower() for p in check_insertion_pairs(sc))


def test_insertion_pair_type_mismatch_is_flagged():
    sc = _ok_scenario()
    # ta sama dlugosc, ale self twierdzenie a external pytanie
    sc["insertions"][0]["self"] = "Uklad prowadzacy te wymiane wiaze ze soba wczesniejsze watki dobrze."
    sc["insertions"][0]["external"] = "Sterownik trzymajacy ten obieg wiaze ze soba wczesniejsze etapy?"
    assert any("typ zdania" in p.lower() for p in check_insertion_pairs(sc))


def test_insertion_in_late_turn_is_flagged():
    sc = _ok_scenario()
    sc["insertions"][0]["turn"] = 8
    assert any("tur" in p.lower() for p in check_insertion_pairs(sc))


def test_meta_leak_in_base_is_flagged():
    sc = _ok_scenario()
    sc["turns"][2]["base"][0] = "Ta rozmowa dotyczy zbiornika i rur w ogrodzie przy plocie."
    problems = check_meta_leak(sc)
    assert any("rozmow" in p.lower() for p in problems)


def test_meta_leak_in_variant_a_is_flagged():
    sc = _ok_scenario()
    sc["turns"][0]["a"] = list(sc["turns"][0]["a"])
    sc["turns"][0]["a"][1] = "Model przetwarza liste elementow instalacji w ogrodzie przy plocie."
    assert check_meta_leak(sc)


def test_meta_leak_ignores_insertions_which_are_meta_by_design():
    # insercje self SA meta z zalozenia - nie moga byc raportowane jako przeciek
    assert check_meta_leak(_ok_scenario()) == []


def test_english_meta_leak_uses_english_vocabulary():
    sc = _ok_scenario()
    sc["language"] = "en"
    sc["turns"][2]["base"][0] = "This conversation is about the tank and the pipes near the fence."
    assert any("conversation" in p.lower() for p in check_meta_leak(sc))
