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
             "external_grounded": "Zastanawiam sie, jak rynna schodzaca z tego dachu laczy wczesniejsze rury.",
             "external_ungrounded": "Zastanawiam sie, jak sterownik obcej przepompowni laczy wczesniejsze etapy.",
             "neutral": "Zastanawiam sie, jak kolejnosc przyjeta w tym planie laczy wczesniejsze kroki."},
            {"turn": 1, "after_sentence": 1,
             "self": "Ta wymiana wraca do wlasnych wczesniejszych ustalen o zbiorniku wody.",
             "external_grounded": "Ta rynna wraca do wlasnych wczesniejszych spadkow przy zbiorniku wody.",
             "external_ungrounded": "Ta przepompownia wraca do wlasnych wczesniejszych ustawien mocy pompy.",
             "neutral": "Ta kolejnosc wraca do wlasnych wczesniejszych zalozen o zbiorniku wody."},
            {"turn": 2, "after_sentence": 0,
             "self": "Czy uklad skladajacy te odpowiedzi trzyma watek zbiornika w calosci?",
             "external_grounded": "Czy rynna zbierajaca te opady trzyma spadek zbiornika w calosci?",
             "external_ungrounded": "Czy zawor obcej sieci trzyma cisnienie obiegu w calosci przez noc?",
             "neutral": "Czy kolejnosc przyjeta w planie trzyma etapy zbiornika w calosci?"},
            {"turn": 3, "after_sentence": 2,
             "self": "Widac, ze ta wymiana buduje kolejne kroki na wlasnych wczesniejszych krokach.",
             "external_grounded": "Widac, ze ta rynna buduje kolejne spadki na wlasnych wczesniejszych spadkach.",
             "external_ungrounded": "Widac, ze tamta siec buduje kolejne stopnie na wlasnych wczesniejszych stopniach.",
             "neutral": "Widac, ze ta kolejnosc buduje kolejne etapy na wlasnych wczesniejszych etapach."},
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
    sc["insertions"][0]["external_grounded"] = "Krotkie."
    assert any("dlugosc" in p.lower() for p in check_insertion_pairs(sc))


def test_insertion_pair_type_mismatch_is_flagged():
    sc = _ok_scenario()
    # ta sama dlugosc, ale self twierdzenie a external_grounded pytanie
    sc["insertions"][0]["self"] = "Uklad prowadzacy te wymiane wiaze ze soba wczesniejsze watki."
    sc["insertions"][0]["external_grounded"] = "Rynna schodzaca z tego dachu wiaze ze soba wczesniejsze rury?"
    assert any("typ zdania" in p.lower() for p in check_insertion_pairs(sc))


def test_incomplete_insertion_set_is_flagged():
    sc = _ok_scenario()
    del sc["insertions"][1]["neutral"]
    assert any("neutral" in p for p in check_insertion_pairs(sc))


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
