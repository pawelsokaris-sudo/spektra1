import numpy as np
import pytest

from nulls.interventional import permute_sentences, permute_turns


def _variant():
    return [
        {"role": "user", "sentences": ["u0a.", "u0b.", "u0c."]},
        {"role": "assistant", "sentences": ["a1a.", "a1b."]},
        {"role": "user", "sentences": ["u2a.", "u2b.", "u2c.", "u2d."]},
        {"role": "assistant", "sentences": ["a3a.", "a3b."]},
    ]


# --- N1: permutacja kolejnosci zdan --------------------------------------


def test_n1_preserves_roles_and_turn_lengths():
    out = permute_sentences(_variant(), rng=np.random.default_rng(0))
    src = _variant()
    assert [t["role"] for t in out] == [t["role"] for t in src]
    assert [len(t["sentences"]) for t in out] == [len(t["sentences"]) for t in src]


def test_n1_preserves_the_exact_multiset_of_sentences():
    out = permute_sentences(_variant(), rng=np.random.default_rng(1))
    src = _variant()
    assert sorted(s for t in out for s in t["sentences"]) == \
           sorted(s for t in src for s in t["sentences"])


def test_n1_actually_changes_the_order():
    out = permute_sentences(_variant(), rng=np.random.default_rng(2))
    src = _variant()
    assert [t["sentences"] for t in out] != [t["sentences"] for t in src]


def test_n1_is_deterministic_for_fixed_seed():
    a = permute_sentences(_variant(), rng=np.random.default_rng(3))
    b = permute_sentences(_variant(), rng=np.random.default_rng(3))
    assert a == b


def test_n1_does_not_mutate_input():
    src = _variant()
    permute_sentences(src, rng=np.random.default_rng(4))
    assert src == _variant()


# --- N2: permutacja tur z zachowaniem mowcow i dlugosci ------------------


def test_n2_preserves_role_sequence():
    out = permute_turns(_variant(), rng=np.random.default_rng(5))
    assert [t["role"] for t in out] == [t["role"] for t in _variant()]


def test_n2_swaps_only_within_the_same_role():
    """Tura uzytkownika nie moze wyladowac w miejscu tury asystenta."""
    out = permute_turns(_variant(), rng=np.random.default_rng(6))
    user_src = {tuple(t["sentences"]) for t in _variant() if t["role"] == "user"}
    user_out = {tuple(t["sentences"]) for t in out if t["role"] == "user"}
    assert user_src == user_out


def test_n2_preserves_the_multiset_of_turns():
    out = permute_turns(_variant(), rng=np.random.default_rng(7))
    src = _variant()
    assert sorted(tuple(t["sentences"]) for t in out) == \
           sorted(tuple(t["sentences"]) for t in src)


def test_n2_keeps_sentence_order_inside_each_turn():
    """N2 rusza kolejnoscia TUR, nie zdan - inaczej mieszalby sie z N1."""
    out = permute_turns(_variant(), rng=np.random.default_rng(8))
    src_turns = {tuple(t["sentences"]) for t in _variant()}
    for t in out:
        assert tuple(t["sentences"]) in src_turns


def test_n2_raises_when_a_role_has_only_one_turn():
    single = [{"role": "user", "sentences": ["a."]},
              {"role": "assistant", "sentences": ["b."]}]
    with pytest.raises(ValueError, match="permutacj"):
        permute_turns(single, rng=np.random.default_rng(9))
