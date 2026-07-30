import numpy as np
import pytest

from pipeline.metrics import d_lag, d_lag_sentence


def _blocks_of(ids_pattern):
    """ids_pattern: lista (id, dlugosc) -> tablica sentence_ids."""
    return np.concatenate([np.full(n, i) for i, n in ids_pattern])


def _within_sentence_ar(T, D, ids, phi, rng):
    """AR(1) wewnatrz kazdego zdania, zdania NIEZALEZNE (restart procesu)."""
    Z = np.zeros((T, D))
    prev_id = None
    for t in range(T):
        if ids[t] != prev_id:
            Z[t] = rng.standard_normal(D)          # restart na granicy zdania
        else:
            Z[t] = phi * Z[t - 1] + np.sqrt(1 - phi**2) * rng.standard_normal(D)
        prev_id = ids[t]
    return Z


def test_blind_to_within_sentence_structure():
    """WLASNOSC ROZROZNIAJACA: silna struktura tokenowa wewnatrz zdan przy
    niezaleznych zdaniach ma dawac |z| male dla metryki zdaniowej, a duze dla
    tokenowej. To jest dokladnie to, czego tokenowy D_lag nie umial (sanity N1)."""
    rng = np.random.default_rng(0)
    ids = _blocks_of([(i, 15) for i in range(20)])   # 20 zdan po 15 tokenow
    Z = _within_sentence_ar(300, 24, ids, phi=0.9, rng=rng)
    z_sent = d_lag_sentence(Z, ids, n_permutations=200, rng=np.random.default_rng(1))
    z_tok = d_lag(Z, n_permutations=200, rng=np.random.default_rng(2))
    assert abs(z_sent) < 3.0
    assert z_tok > 5.0


def test_detects_cross_sentence_drift():
    """Dryf na poziomie zdan (srednia zdania podaza AR miedzy zdaniami) ma byc
    widoczny dla metryki zdaniowej."""
    rng = np.random.default_rng(3)
    ids = _blocks_of([(i, 15) for i in range(20)])
    means = np.zeros((20, 24))
    for i in range(1, 20):
        means[i] = 0.9 * means[i - 1] + np.sqrt(1 - 0.81) * rng.standard_normal(24)
    Z = rng.standard_normal((300, 24)) * 0.3 + means[ids]
    z_sent = d_lag_sentence(Z, ids, n_permutations=200, rng=np.random.default_rng(4))
    # z > 3 to p < 0.001 - wykrycie; przy tej sile syntetycznego dryfu zmierzone 3.67
    assert z_sent > 3.0


def test_deterministic_for_fixed_seed():
    rng = np.random.default_rng(5)
    ids = _blocks_of([(i, 10) for i in range(12)])
    Z = rng.standard_normal((120, 16))
    a = d_lag_sentence(Z, ids, n_permutations=100, rng=np.random.default_rng(6))
    b = d_lag_sentence(Z, ids, n_permutations=100, rng=np.random.default_rng(6))
    assert a == b


def test_requires_at_least_two_blocks():
    rng = np.random.default_rng(7)
    Z = rng.standard_normal((30, 8))
    with pytest.raises(ValueError, match="blok"):
        d_lag_sentence(Z, np.zeros(30, dtype=int), n_permutations=50,
                       rng=np.random.default_rng(8))


def test_handles_glue_blocks_between_sentences():
    """Bloki -1 (tokeny szablonu miedzy zdaniami) sa osobnymi blokami i tez
    podlegaja permutacji - nie moga wywracac funkcji."""
    rng = np.random.default_rng(9)
    ids = _blocks_of([(0, 10), (-1, 3), (1, 10), (-1, 3), (2, 10)])
    Z = rng.standard_normal((36, 8))
    z = d_lag_sentence(Z, ids, n_permutations=100, rng=np.random.default_rng(10))
    assert np.isfinite(z)
