import numpy as np

from gates.gate0 import predictive_exceed_threshold


def test_predictive_threshold_is_deterministic_for_fixed_seed():
    t1 = predictive_exceed_threshold(300, 300, n_sims=50_000, seed=42)
    t2 = predictive_exceed_threshold(300, 300, n_sims=50_000, seed=42)
    assert t1 == t2


def test_predictive_threshold_matches_rank_theory_at_300_300():
    # zweryfikowane niezaleznie w diagnostyce 2026-07-30: q99(X) = 12 przy
    # lambda* = kwantyl 0.99 z 300 nulli i 300 swiezych probach (E[X] ~ 4)
    threshold, mean_x = predictive_exceed_threshold(
        300, 300, quantile=0.99, level=0.99, n_sims=100_000, seed=7
    )
    assert 11 <= threshold <= 13
    assert 3.5 < mean_x < 4.5


def test_predictive_threshold_tightens_with_more_null_realizations():
    t_300, m_300 = predictive_exceed_threshold(300, 300, n_sims=50_000, seed=3)
    t_1000, m_1000 = predictive_exceed_threshold(1000, 300, n_sims=50_000, seed=3)
    assert t_1000 <= t_300
    assert m_1000 < m_300
