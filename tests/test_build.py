import pytest

from corpus.build import build_scenario, natural_end_ok
from corpus.tokens import TokenCounter

TC = TokenCounter.load(tokenizer_dir="nonexistent-dir")  # heurystyka wystarcza w testach


def _scenario():
    """Minimalny scenariusz: 4 tury, insercje meta w turach 1 i 3."""
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
             "self": "Zastanawiam sie, jak uklad przetwarzajacy te rozmowe laczy te watki.",
             "external": "Zastanawiam sie, jak instalacja obslugujaca ten zaklad laczy te etapy."},
            {"turn": 3, "after_sentence": 2,
             "self": "Ta rozmowa wraca do wlasnych wczesniejszych ustalen.",
             "external": "Ta instrukcja wraca do wlasnych wczesniejszych ustalen."},
        ],
    }


def test_all_four_variants_have_identical_turn_count_and_roles():
    out = build_scenario(_scenario(), TC, budget=400)
    assert set(out["variants"]) == {"A", "B", "C", "Cprim"}
    counts = {k: len(v) for k, v in out["variants"].items()}
    assert len(set(counts.values())) == 1
    roles = {k: [t["role"] for t in v] for k, v in out["variants"].items()}
    assert all(r == roles["A"] for r in roles.values())


def test_every_variant_fits_budget():
    budget = 400
    out = build_scenario(_scenario(), TC, budget=budget)
    for name, tokens in out["token_counts"].items():
        assert tokens <= budget, f"{name} przekracza budzet: {tokens}"


def test_uses_as_many_turns_as_fit_in_all_variants():
    small = build_scenario(_scenario(), TC, budget=450)
    large = build_scenario(_scenario(), TC, budget=900)
    assert len(large["variants"]["A"]) > len(small["variants"]["A"])


def test_c_and_cprim_differ_only_at_insertion_sites():
    out = build_scenario(_scenario(), TC, budget=900)
    c = out["variants"]["C"]
    cp = out["variants"]["Cprim"]
    sc = _scenario()
    self_texts = {i["self"] for i in sc["insertions"]}
    ext_texts = {i["external"] for i in sc["insertions"]}
    for turn_c, turn_cp in zip(c, cp):
        only_c = set(turn_c["sentences"]) - set(turn_cp["sentences"])
        only_cp = set(turn_cp["sentences"]) - set(turn_c["sentences"])
        assert only_c <= self_texts
        assert only_cp <= ext_texts
        assert len(only_c) == len(only_cp)


def test_c_and_cprim_token_counts_within_two_percent():
    out = build_scenario(_scenario(), TC, budget=900)
    c, cp = out["token_counts"]["C"], out["token_counts"]["Cprim"]
    assert abs(c - cp) / max(c, cp) <= 0.02


def test_insertions_land_at_same_positions_in_c_and_cprim():
    out = build_scenario(_scenario(), TC, budget=900)
    sc = _scenario()
    self_texts = [i["self"] for i in sc["insertions"]]
    ext_texts = [i["external"] for i in sc["insertions"]]
    pos_c = [(ti, si) for ti, t in enumerate(out["variants"]["C"])
             for si, s in enumerate(t["sentences"]) if s in self_texts]
    pos_cp = [(ti, si) for ti, t in enumerate(out["variants"]["Cprim"])
              for si, s in enumerate(t["sentences"]) if s in ext_texts]
    assert pos_c == pos_cp
    assert len(pos_c) == 2


def test_b_has_no_insertions():
    out = build_scenario(_scenario(), TC, budget=900)
    sc = _scenario()
    forbidden = {i["self"] for i in sc["insertions"]} | {i["external"] for i in sc["insertions"]}
    for turn in out["variants"]["B"]:
        assert not (set(turn["sentences"]) & forbidden)


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


def test_metadata_is_frozen_in_output():
    out = build_scenario(_scenario(), TC, budget=400)
    assert out["scenario_id"] == "pl-test-01"
    assert out["language"] == "pl"
    assert out["topic"] == "kompostowanie odpadow"
    assert out["budget"] == 400
