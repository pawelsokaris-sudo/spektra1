import numpy as np
import pytest

from power.permutation import n_exact_permutations, paired_permutation_test


def test_exact_enumeration_for_small_n():
    # 8 scenariuszy -> 2^8 = 256 znakowan, wyliczalne dokladnie
    assert n_exact_permutations(8) == 256
    res = paired_permutation_test(np.array([0.1] * 8), rng=np.random.default_rng(0))
    assert res["exact"] is True
    assert res["n_permutations"] == 256
    # wszystkie roznice dodatnie i rowne -> obserwowana srednia jest maksymalna
    assert res["p_value"] == pytest.approx(1 / 256)


def test_switches_to_sampling_for_large_n():
    diffs = np.full(30, 0.05)
    res = paired_permutation_test(diffs, n_permutations=5000,
                                  rng=np.random.default_rng(1))
    assert res["exact"] is False
    assert res["n_permutations"] == 5000


def test_null_data_is_not_significant():
    rng = np.random.default_rng(2)
    diffs = rng.standard_normal(20) * 0.1  # brak efektu
    res = paired_permutation_test(diffs, n_permutations=5000,
                                  rng=np.random.default_rng(3))
    assert res["p_value"] > 0.05


def test_strong_effect_is_significant_at_alpha_001():
    rng = np.random.default_rng(4)
    diffs = 1.0 + rng.standard_normal(20) * 0.3  # d_z ~ 3
    res = paired_permutation_test(diffs, n_permutations=5000,
                                  rng=np.random.default_rng(5))
    assert res["p_value"] < 0.01


def test_one_sided_ignores_effects_in_wrong_direction():
    """H1 jest kierunkowa: silny efekt UJEMNY nie moze dac istotnosci."""
    rng = np.random.default_rng(6)
    diffs = -1.0 + rng.standard_normal(20) * 0.3
    res = paired_permutation_test(diffs, n_permutations=5000,
                                  rng=np.random.default_rng(7))
    assert res["p_value"] > 0.9


def test_reports_effect_size_d_z():
    diffs = np.array([0.8, 1.2, 1.0, 0.9, 1.1])
    res = paired_permutation_test(diffs, rng=np.random.default_rng(8))
    expected = diffs.mean() / diffs.std(ddof=1)
    assert res["d_z"] == pytest.approx(expected)


def test_reports_confidence_interval_at_requested_level():
    rng = np.random.default_rng(9)
    diffs = 0.5 + rng.standard_normal(25) * 0.5
    res = paired_permutation_test(diffs, n_permutations=2000, ci_level=0.99,
                                  rng=np.random.default_rng(10))
    lo, hi = res["ci"]
    assert lo < diffs.mean() < hi
    assert res["ci_level"] == 0.99


def test_is_deterministic_for_fixed_seed():
    diffs = np.linspace(-0.2, 0.9, 17)
    a = paired_permutation_test(diffs, n_permutations=3000, rng=np.random.default_rng(11))
    b = paired_permutation_test(diffs, n_permutations=3000, rng=np.random.default_rng(11))
    assert a["p_value"] == b["p_value"]


def test_rejects_empty_input():
    with pytest.raises(ValueError, match="pusta"):
        paired_permutation_test(np.array([]), rng=np.random.default_rng(12))
