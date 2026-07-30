import numpy as np
import pytest

from pipeline.metrics import d_discourse, sentence_representations


def test_reports_raw_values_not_only_z():
    rng = np.random.default_rng(0)
    S = rng.standard_normal((30, 16))
    out = d_discourse(S, n_permutations=100, rng=np.random.default_rng(1))
    for key in ("sigma1", "null_mean", "null_sd", "raw_diff", "p_empirical",
                "z_descriptive", "n_sentences"):
        assert key in out
    # empiryczne p ma rozdzielczosc 1/(n+1) i nigdy nie jest zerem
    assert out["p_empirical"] >= 1 / 101


def test_detects_order_across_sentences():
    rng = np.random.default_rng(2)
    S = np.zeros((40, 16))
    S[0] = rng.standard_normal(16)
    for j in range(1, 40):
        S[j] = 0.85 * S[j - 1] + np.sqrt(1 - 0.85**2) * rng.standard_normal(16)
    out = d_discourse(S, n_permutations=200, rng=np.random.default_rng(3))
    assert out["p_empirical"] <= 0.01
    assert out["raw_diff"] > 0


def test_silent_on_exchangeable_sentences():
    rng = np.random.default_rng(4)
    S = rng.standard_normal((40, 16))
    out = d_discourse(S, n_permutations=200, rng=np.random.default_rng(5))
    assert out["p_empirical"] > 0.05


def test_deterministic_and_rejects_tiny_J():
    S = np.random.default_rng(6).standard_normal((10, 8))
    a = d_discourse(S, n_permutations=100, rng=np.random.default_rng(7))
    b = d_discourse(S, n_permutations=100, rng=np.random.default_rng(7))
    assert a == b
    with pytest.raises(ValueError, match="J="):
        d_discourse(S[:2], n_permutations=50, rng=np.random.default_rng(8))


def test_sentence_representations_mean_and_template_exclusion():
    Z = np.arange(12, dtype=float).reshape(6, 2)
    ids = np.array([0, 0, -1, 1, 1, 1])
    S = sentence_representations(Z, ids)
    np.testing.assert_allclose(S[0], Z[:2].mean(axis=0))
    np.testing.assert_allclose(S[1], Z[3:].mean(axis=0))
    assert S.shape == (2, 2)
