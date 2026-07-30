import numpy as np
import pytest

from pipeline.metrics import (
    d_lag,
    i_minus1,
    i_total,
    k_modes,
    lag_sigma1,
    spectral_entropy,
)


EIGS = np.array([5.0, 3.0, 2.0])  # tr = 10


def test_i_total_sums_modes_above_lambda_star_over_trace():
    assert i_total(EIGS, lambda_star=2.5) == pytest.approx(0.8)


def test_i_total_zero_when_nothing_above_threshold():
    assert i_total(EIGS, lambda_star=6.0) == 0.0


def test_i_minus1_removes_leading_mode_only_if_above_threshold():
    # (I_total * tr - lambda1 * 1[lambda1 > lambda*]) / tr
    assert i_minus1(EIGS, lambda_star=2.5) == pytest.approx(0.3)
    assert i_minus1(EIGS, lambda_star=6.0) == 0.0


def test_k_modes_counts_modes_above_threshold():
    assert k_modes(EIGS, lambda_star=2.5) == 2
    assert k_modes(EIGS, lambda_star=0.0) == 3


def test_spectral_entropy_is_one_for_flat_spectrum():
    assert spectral_entropy(np.array([2.0, 2.0, 2.0, 2.0])) == pytest.approx(1.0)


def test_spectral_entropy_is_zero_for_single_mode():
    assert spectral_entropy(np.array([4.0])) == 0.0
    assert spectral_entropy(np.array([4.0, 0.0, 0.0])) == 0.0  # zera wykluczone


def test_lag_sigma1_matches_direct_svd():
    # sigma1(C(1)) liczone trikiem Grama == bezposredni SVD malego przypadku
    rng = np.random.default_rng(20)
    Z = rng.standard_normal((40, 7))
    C1 = Z[1:].T @ Z[:-1] / Z.shape[0]
    direct = np.linalg.svd(C1, compute_uv=False)[0]
    # rel=1e-4: iteracja potegowa ma tolerancje 1e-5 na lambda (kompromis
    # kosztowy, patrz _sigma1_from_gram); na malym przypadku zbiega w pelni,
    # ale asercja nie powinna wymagac wiecej, niz obiecuje implementacja
    assert lag_sigma1(Z) == pytest.approx(direct, rel=1e-4)


def test_d_lag_detects_temporal_order_in_ar1():
    rng = np.random.default_rng(21)
    T, D, phi = 300, 24, 0.9
    Z = np.zeros((T, D))
    Z[0] = rng.standard_normal(D)
    for t in range(1, T):
        Z[t] = phi * Z[t - 1] + np.sqrt(1 - phi**2) * rng.standard_normal(D)
    z = d_lag(Z, n_permutations=200, rng=np.random.default_rng(22))
    assert z > 5.0


def test_d_lag_near_null_for_iid_noise():
    rng = np.random.default_rng(23)
    Z = rng.standard_normal((300, 24))
    z = d_lag(Z, n_permutations=200, rng=np.random.default_rng(24))
    assert abs(z) < 3.0
