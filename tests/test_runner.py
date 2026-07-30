import numpy as np
import pytest

from pipeline.runner import (
    accumulate_positional,
    equalize_scenario,
    metrics_for_layer,
    plan_texts,
)


def _scenario_variants(lengths):
    """Atrapa aktywacji: {wariant: (T, D)} o zadanych dlugosciach."""
    rng = np.random.default_rng(0)
    return {k: rng.standard_normal((n, 6)) for k, n in lengths.items()}


def test_plan_texts_covers_all_variants_and_nulls():
    sc = {"scenario_id": "pl-01", "language": "pl"}
    plan = plan_texts([sc], include_nulls=True)
    kinds = {(p["variant"], p["null"]) for p in plan}
    assert ("C", None) in kinds
    assert ("CprimG", None) in kinds
    assert ("C", "N1") in kinds
    assert ("C", "N2") in kinds
    # nulle liczone tylko dla wariantow dialogowych, nie dla A
    assert ("A", "N1") not in kinds


def test_plan_without_nulls_is_five_texts_per_scenario():
    sc = {"scenario_id": "pl-01", "language": "pl"}
    plan = plan_texts([sc], include_nulls=False)
    assert len(plan) == 5


def test_equalize_truncates_to_shortest_variant():
    acts = _scenario_variants({"A": 40, "B": 44, "C": 42, "CprimG": 45, "CprimU": 43})
    out, dropped = equalize_scenario(acts)
    assert {v.shape[0] for v in out.values()} == {40}
    assert dropped["CprimG"] == 5
    assert dropped["A"] == 0


def test_positional_accumulator_matches_plain_mean():
    a = np.ones((10, 3))
    b = 3.0 * np.ones((10, 3))
    acc = accumulate_positional(None, a)
    acc = accumulate_positional(acc, b)
    np.testing.assert_allclose(acc["sum"] / acc["count"][:, None], 2.0 * np.ones((10, 3)))


def test_positional_accumulator_handles_ragged_lengths_like_protocol():
    """Par. 4: srednia per pozycja po korpusie; na pozycji t usredniane sa tylko
    teksty siegajace t. Rozne okna scenariuszy sa wiec LEGALNE - awaria pomiaru
    pilota 2026-07-30 wziela sie z za restrykcyjnego akumulatora, nie z protokolu.
    Wynik musi byc identyczny z corpus positional_mean (test na nierowne dlugosci
    istnieje tam od poczatku)."""
    from pipeline.preprocess import positional_mean

    t1 = np.ones((10, 2))
    t2 = 3.0 * np.ones((6, 2))
    acc = accumulate_positional(None, t1)
    acc = accumulate_positional(acc, t2)
    got = acc["sum"] / acc["count"][:, None]
    np.testing.assert_allclose(got, positional_mean([t1, t2]), atol=1e-12)


def test_positional_accumulator_grows_when_longer_text_arrives():
    acc = accumulate_positional(None, np.ones((6, 2)))
    acc = accumulate_positional(acc, 3.0 * np.ones((10, 2)))
    assert acc["sum"].shape == (10, 2)
    got = acc["sum"] / acc["count"][:, None]
    np.testing.assert_allclose(got[:6], 2.0 * np.ones((6, 2)))
    np.testing.assert_allclose(got[6:], 3.0 * np.ones((4, 2)))


def test_metrics_for_layer_returns_all_five_protocol_metrics():
    rng = np.random.default_rng(1)
    H = rng.standard_normal((60, 12))
    mu = np.zeros((60, 12))
    m = metrics_for_layer(H, mu, lambda_star=1.5, d_lag_permutations=50,
                          rng=np.random.default_rng(2))
    for key in ("I_total", "I_minus1", "k", "H_s", "D_lag", "trace", "rank",
                "n_excluded_channels"):
        assert key in m
    assert 0.0 <= m["I_total"] <= 1.0
    assert 0.0 <= m["H_s"] <= 1.0


def test_metrics_subtract_the_positional_component():
    """Wspolny komponent pozycyjny musi zniknac przed z-score."""
    rng = np.random.default_rng(3)
    base = rng.standard_normal((60, 12))
    pos = rng.standard_normal((60, 12)) * 10.0
    with_pos = metrics_for_layer(base + pos, pos, lambda_star=1.5,
                                 d_lag_permutations=20, rng=np.random.default_rng(4))
    without = metrics_for_layer(base, np.zeros_like(base), lambda_star=1.5,
                                d_lag_permutations=20, rng=np.random.default_rng(4))
    assert with_pos["I_total"] == pytest.approx(without["I_total"], abs=1e-9)
