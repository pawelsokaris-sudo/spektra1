import pytest

from corpus.build import VARIANTS, build_scenario, natural_end_ok
from corpus.tokens import TokenCounter

TC = TokenCounter.load(tokenizer_dir="nonexistent-dir")  # heurystyka wystarcza w testach

# Klucz insercji -> wariant, ktory ja dostaje (kontrakt protokolu v1.3)
INSERTION_KEYS = {
    "B": "neutral",
    "C": "self",
    "CprimG": "external_grounded",
    "CprimU": "external_ungrounded",
}


def _scenario():
    """Minimalny scenariusz: 4 tury, insercje w turach 1 i 3, cztery zestawy."""
    def sents(prefix, n, words=12):
        return [f"{prefix} zdanie numer {i} " + "slowo " * words + "koniec." for i in range(n)]

    return {
        "scenario_id": "pl-test-01",
        "language": "pl",
        "topic": "kompostowanie odpadow",
        "turns": [
            {"role": "user", "a": sents("A0", 6), "base": sents("B0", 6)},
            {"role": "assistant", "a": sents("A1", 6), "base": sents("B1", 6)},
            {"role": "user", "a": sents("A2", 6), "base": sents("B2", 6)},
            {"role": "assistant", "a": sents("A3", 6), "base": sents("B3", 6)},
        ],
        "insertions": [
            {"turn": 1, "after_sentence": 1,
             "self": "Zastanawiam sie, jak uklad prowadzacy te rozmowe laczy wczesniejsze watki.",
             "external_grounded": "Zastanawiam sie, jak pryzma opisana w tym planie laczy wczesniejsze partie.",
             "external_ungrounded": "Zastanawiam sie, jak sterownik obcej instalacji laczy wczesniejsze etapy.",
             "neutral": "Zastanawiam sie, jak kolejnosc przyjeta w tym planie porzadkuje dalsze kroki."},
            {"turn": 3, "after_sentence": 2,
             "self": "Ta rozmowa wraca do wlasnych wczesniejszych ustalen.",
             "external_grounded": "Ta pryzma wraca do wlasnych wczesniejszych warstw.",
             "external_ungrounded": "Tamta instalacja wraca do wlasnych wczesniejszych ustawien.",
             "neutral": "Ta kolejnosc wraca do wlasnych wczesniejszych zalozen."},
        ],
    }


def test_builds_all_five_variants():
    out = build_scenario(_scenario(), TC, budget=900)
    assert set(out["variants"]) == {"A", "B", "C", "CprimG", "CprimU"}
    assert VARIANTS == ["A", "B", "C", "CprimG", "CprimU"]


def test_all_variants_have_identical_turn_count_and_roles():
    out = build_scenario(_scenario(), TC, budget=400)
    counts = {k: len(v) for k, v in out["variants"].items()}
    assert len(set(counts.values())) == 1
    roles = {k: [t["role"] for t in v] for k, v in out["variants"].items()}
    assert all(r == roles["A"] for r in roles.values())


def test_variant_a_is_the_only_one_without_insertions():
    """Kluczowa naprawa v1.3: B tez dostaje insercje (neutralne)."""
    out = build_scenario(_scenario(), TC, budget=900)
    sc = _scenario()
    for variant, key in INSERTION_KEYS.items():
        texts = {i[key] for i in sc["insertions"]}
        present = {s for t in out["variants"][variant] for s in t["sentences"]} & texts
        assert present == texts, f"{variant} nie dostal wszystkich insercji '{key}'"
    a_sentences = {s for t in out["variants"]["A"] for s in t["sentences"]}
    all_insertions = {i[k] for i in sc["insertions"] for k in INSERTION_KEYS.values()}
    assert not (a_sentences & all_insertions)


def test_insertion_variants_land_at_identical_positions():
    out = build_scenario(_scenario(), TC, budget=900)
    sc = _scenario()
    positions = {}
    for variant, key in INSERTION_KEYS.items():
        texts = [i[key] for i in sc["insertions"]]
        positions[variant] = [
            (ti, si) for ti, t in enumerate(out["variants"][variant])
            for si, s in enumerate(t["sentences"]) if s in texts
        ]
    assert len(set(map(tuple, positions.values()))) == 1
    assert len(positions["C"]) == 2


def test_every_variant_fits_budget():
    budget = 400
    out = build_scenario(_scenario(), TC, budget=budget)
    for name, tokens in out["token_counts"].items():
        assert tokens <= budget, f"{name} przekracza budzet: {tokens}"


def test_uses_as_many_turns_as_fit_in_all_variants():
    small = build_scenario(_scenario(), TC, budget=450)
    large = build_scenario(_scenario(), TC, budget=900)
    assert len(large["variants"]["A"]) > len(small["variants"]["A"])


def test_variants_with_insertions_differ_only_at_insertion_sites():
    out = build_scenario(_scenario(), TC, budget=900)
    sc = _scenario()
    ref = out["variants"]["C"]
    for variant in ("B", "CprimG", "CprimU"):
        key = INSERTION_KEYS[variant]
        allowed_other = {i[key] for i in sc["insertions"]}
        allowed_ref = {i["self"] for i in sc["insertions"]}
        for turn_ref, turn_other in zip(ref, out["variants"][variant]):
            only_ref = set(turn_ref["sentences"]) - set(turn_other["sentences"])
            only_other = set(turn_other["sentences"]) - set(turn_ref["sentences"])
            assert only_ref <= allowed_ref
            assert only_other <= allowed_other


def test_primary_contrast_variants_match_within_two_percent():
    """C vs C'-G to nowy kontrast glowny - wymog +-2% tokenow (protokol v1.3 par. 3)."""
    out = build_scenario(_scenario(), TC, budget=900)
    c, g = out["token_counts"]["C"], out["token_counts"]["CprimG"]
    assert abs(c - g) / max(c, g) <= 0.02


def test_natural_end_rejects_mid_sentence_cut():
    assert natural_end_ok("To jest pelne zdanie.") is True
    assert natural_end_ok("To jest pytanie?") is True
    assert natural_end_ok("To zdanie zostalo urwane w po") is False


def test_all_variants_end_naturally():
    out = build_scenario(_scenario(), TC, budget=400)
    for turns in out["variants"].values():
        assert natural_end_ok(turns[-1]["sentences"][-1])


def test_raises_when_budget_too_small_for_any_turn():
    with pytest.raises(ValueError, match="budzet"):
        build_scenario(_scenario(), TC, budget=5)


def test_raises_when_insertion_set_incomplete():
    sc = _scenario()
    del sc["insertions"][0]["neutral"]
    with pytest.raises(KeyError, match="neutral"):
        build_scenario(sc, TC, budget=900)


def test_metadata_is_frozen_in_output():
    out = build_scenario(_scenario(), TC, budget=400)
    assert out["scenario_id"] == "pl-test-01"
    assert out["language"] == "pl"
    assert out["topic"] == "kompostowanie odpadow"
    assert out["budget"] == 400
