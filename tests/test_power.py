import numpy as np
import pytest

from power.simulate import min_n_for_alpha, power_at_n, required_m


def test_minimum_n_imposed_by_exact_permutation_floor():
    """Przy n parach najmniejsze osiagalne p to 1/2^n - to podloga, nie detal."""
    # 2^6 = 64 -> min p = 0.0156 > 0.01, wiec n=6 NIE MOZE dac istotnosci
    assert min_n_for_alpha(0.01) == 7          # 1/128 = 0.0078 < 0.01
    assert min_n_for_alpha(0.05) == 5          # 1/32  = 0.031  < 0.05


def test_power_is_zero_below_the_floor():
    p = power_at_n(n=6, d_z=5.0, alpha=0.01, n_sims=200, rng=np.random.default_rng(0))
    assert p == 0.0


def test_power_grows_with_sample_size():
    small = power_at_n(n=10, d_z=0.8, alpha=0.01, n_sims=400, rng=np.random.default_rng(1))
    large = power_at_n(n=40, d_z=0.8, alpha=0.01, n_sims=400, rng=np.random.default_rng(1))
    assert large > small


def test_power_grows_with_effect_size():
    weak = power_at_n(n=20, d_z=0.4, alpha=0.01, n_sims=400, rng=np.random.default_rng(2))
    strong = power_at_n(n=20, d_z=1.2, alpha=0.01, n_sims=400, rng=np.random.default_rng(2))
    assert strong > weak


def test_power_near_nominal_alpha_under_null():
    """Przy d_z = 0 odsetek odrzucen nie moze istotnie przekraczac alfa."""
    p = power_at_n(n=25, d_z=0.0, alpha=0.01, n_sims=2000, rng=np.random.default_rng(3))
    assert p <= 0.03


def test_required_m_finds_smallest_n_meeting_target():
    m, curve = required_m(target_power=0.90, d_z=0.8, alpha=0.01,
                          n_sims=400, n_max=80, rng=np.random.default_rng(4))
    assert m is not None
    assert curve[m] >= 0.90
    below = [n for n in curve if n < m]
    assert all(curve[n] < 0.90 for n in below)


def test_required_m_returns_none_when_unreachable():
    m, curve = required_m(target_power=0.90, d_z=0.05, alpha=0.01,
                          n_sims=100, n_max=12, rng=np.random.default_rng(5))
    assert m is None


def test_is_deterministic_for_fixed_seed():
    a = power_at_n(n=15, d_z=0.8, alpha=0.01, n_sims=300, rng=np.random.default_rng(6))
    b = power_at_n(n=15, d_z=0.8, alpha=0.01, n_sims=300, rng=np.random.default_rng(6))
    assert a == b
