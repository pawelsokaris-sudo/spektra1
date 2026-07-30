"""Widmo macierzy korelacji przez macierz Grama (protokol par. 4).

Niezerowe wartosci wlasne C = Z^T Z / T' (D x D) sa identyczne z niezerowymi
wartosciami wlasnymi G = Z Z^T / T' (T' x T'). Konfirmacja liczy WYLACZNIE pelne
niezerowe widmo przez Grama - zero podprobkowania kanalow (rozstrzygniecie #1).
"""

import numpy as np


def gram_eigenvalues(Z, rtol=1e-10):
    """Niezerowe widmo korelacji przez Grama, malejaco.

    Z: (T', D) po z-score. Zwraca lambda_1 >= ... >= lambda_r > 0.
    Wartosci ponizej lambda_1 * rtol traktowane jako numeryczne zero (rank cutoff).
    Uzywa symetrycznego solvera LAPACK (eigvalsh == sciezka wartosci wlasnych eigh).
    """
    Z = np.asarray(Z, dtype=np.float64)
    t_prime = Z.shape[0]
    G = (Z @ Z.T) / t_prime
    w = np.linalg.eigvalsh(G)[::-1]
    w = np.clip(w, 0.0, None)
    if w.size == 0:
        return w
    cutoff = w[0] * rtol
    return w[w > cutoff]
