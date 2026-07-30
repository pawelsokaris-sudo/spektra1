import numpy as np

from pipeline.preprocess import zscore_channels
from pipeline.spectrum import gram_eigenvalues


def test_gram_matches_direct_correlation_eigenvalues():
    # D < T: pelny rank, widmo z Grama == widmo bezposrednie C = Z^T Z / T
    rng = np.random.default_rng(10)
    Z, _ = zscore_channels(rng.standard_normal((60, 12)))
    C = Z.T @ Z / Z.shape[0]
    direct = np.sort(np.linalg.eigvalsh(C))[::-1]
    via_gram = gram_eigenvalues(Z)
    np.testing.assert_allclose(via_gram, direct[: len(via_gram)], rtol=1e-8, atol=1e-10)


def test_gram_handles_rank_deficient_case():
    # D > T: rank <= T-1 (po centrowaniu), same nieujemne wartosci
    rng = np.random.default_rng(11)
    Z, _ = zscore_channels(rng.standard_normal((20, 50)))
    eigs = gram_eigenvalues(Z)
    assert len(eigs) <= 20
    assert np.all(eigs >= 0)
    assert np.all(np.diff(eigs) <= 1e-12)  # posortowane malejaco


def test_trace_equals_number_of_channels_after_zscore():
    # tr C = suma wariancji = D po standaryzacji (kontrola z par. 5 protokolu)
    rng = np.random.default_rng(12)
    Z, _ = zscore_channels(rng.standard_normal((100, 30)))
    eigs = gram_eigenvalues(Z)
    np.testing.assert_allclose(eigs.sum(), 30.0, rtol=1e-8)
