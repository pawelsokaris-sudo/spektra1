"""Metryki widmowe: I_total, I_-1, k, H_s, D_lag (protokol par. 5, wzory zamrozone).

Mianownik wszystkich indeksow = tr (suma wszystkich wartosci wlasnych).
D_lag: sigma_1 macierzy korelacji z opoznieniem C(1) = Z_{+1}^T Z / T' vs null
permutacji kolejnosci wierszy Z; wynik = z-score wzgledem nullu.
"""

import numpy as np


def i_total(eigs, lambda_star):
    """I_total = suma{lambda_i : lambda_i > lambda*} / tr (z modem glownym)."""
    eigs = np.asarray(eigs, dtype=np.float64)
    tr = eigs.sum()
    return float(eigs[eigs > lambda_star].sum() / tr)


def i_minus1(eigs, lambda_star):
    """I_-1 = (I_total * tr - lambda_1 * 1[lambda_1 > lambda*]) / tr."""
    eigs = np.asarray(eigs, dtype=np.float64)
    tr = eigs.sum()
    lam1 = eigs.max()
    top = lam1 if lam1 > lambda_star else 0.0
    return float((i_total(eigs, lambda_star) * tr - top) / tr)


def k_modes(eigs, lambda_star):
    """k = liczba modow ponad lambda*."""
    eigs = np.asarray(eigs, dtype=np.float64)
    return int((eigs > lambda_star).sum())


def spectral_entropy(eigs):
    """H_s = -sum p_i ln p_i / ln r, p_i = lambda_i / tr, zera wykluczone.

    Dla r = 1 (jeden dodatni mod) entropia = 0 z definicji granicznej.
    """
    eigs = np.asarray(eigs, dtype=np.float64)
    p = eigs[eigs > 0.0]
    p = p / p.sum()
    r = p.size
    if r <= 1:
        return 0.0
    return float(-(p * np.log(p)).sum() / np.log(r))


def _sigma1_from_gram(G, order, t_prime, rng, max_iter=120, tol=1e-5):
    """sigma_1(C(1)) dla Z w kolejnosci wierszy `order`, z prekomputowanego G = Z Z^T.

    Trik 1: sigma_1(A^T B)^2 = lambda_max(G_A G_B), gdzie A = Z[order][1:],
    B = Z[order][:-1], a G_A, G_B sa podmacierzami G - bez ponownych iloczynow Z.
    Iloczyn PSD x PSD ma widmo rzeczywiste nieujemne (podobienstwo do
    GB^{1/2} GA GB^{1/2}), wiec iteracja potegowa jest poprawna.

    Trik 2 (wydajnosc): podmacierzy NIE materializujemy. Dla wektora v nosnego
    na indeksach `idx` zachodzi  G[idx][:,idx] @ v == (G @ rozproszony(v))[idx],
    bo rozproszony wektor ma zera poza `idx`. Dzieki temu jedna iteracja to dwa
    mnozenia macierz-wektor na pelnym G plus rozproszenia i zebrania, zamiast
    dwoch kopii podmacierzy T'xT' przy KAZDEJ z 500 permutacji.
    Trik 3 (wydajnosc): tolerancja 1e-5 przy limicie 120 iteracji zamiast 1e-8
    przy 300. Iloczyn G_A G_B dla losowych permutacji ma gesto upakowane
    najwieksze wartosci wlasne, wiec iteracja potegowa zbiega wolno i przy
    ciasnej tolerancji dobijala do limitu - to, a nie kopie podmacierzy, bylo
    faktycznym waskim gardlem (zmierzono: ~255 ms -> ~29-58 ms na permutacje).
    Kalibracja empiryczna 2026-07-30: niedomkniecie zbieznosci przesuwa
    sigma_1 o niemal STALA wartosc niezaleznie od danych (iid: -0.25 w z,
    AR(1) z z=89: -0.26), a obserwacja i null licza sie ta sama procedura,
    wiec przesuniecie skraca sie w z-score; ustawienie (120, 1e-5) wybrano,
    bo jest blizsze dokladnemu niz (60, 1e-4) przy tym samym koszcie.
    """
    idx_a = order[1:]
    idx_b = order[:-1]
    n = idx_a.size
    scratch = np.zeros(G.shape[0])

    v = rng.standard_normal(n)
    v /= np.linalg.norm(v)
    lam_prev = 0.0
    for _ in range(max_iter):
        scratch[:] = 0.0
        scratch[idx_b] = v
        u = (G @ scratch)[idx_b]          # G_B v
        scratch[:] = 0.0
        scratch[idx_a] = u
        w = (G @ scratch)[idx_a]          # G_A (G_B v)
        lam = np.linalg.norm(w)
        if lam == 0.0:
            return 0.0
        v = w / lam
        if abs(lam - lam_prev) <= tol * lam:
            break
        lam_prev = lam
    return np.sqrt(lam) / t_prime


def lag_sigma1(Z):
    """sigma_1 macierzy C(1) = Z_{+1}^T Z / T' (obserwowana, bez permutacji)."""
    Z = np.asarray(Z, dtype=np.float64)
    t_prime = Z.shape[0]
    G = Z @ Z.T
    rng = np.random.default_rng(0)  # tylko wektor startowy iteracji potegowej
    return float(_sigma1_from_gram(G, np.arange(t_prime), t_prime, rng))


def d_lag_sentence(Z, sentence_ids, n_permutations=500, rng=None):
    """D_lag z nullem ZDANIOWYM: permutacja blokow zdan zamiast tokenow.

    Powstala z sanity N1 pilota (2026-07-30): tokenowy null nie spadl na
    przetasowanych zdaniach (43.1 vs 42.5), bo sygnal dominuje lokalna
    ciaglosc skladniowa wewnatrz zdania, ktorej N1 nie narusza. Null blokowy
    tasuje cale zdania (kolejnosc wierszy WEWNATRZ bloku nietknieta), wiec
    metryka mierzy porzadek DYSKURSU, na ktory tokenowa jest slepa.

    sentence_ids: tablica dlugosci T' - identyfikator zdania per wiersz Z po
    maskowaniu; tokeny szablonu miedzy zdaniami maja id -1 i tworza wlasne
    bloki podlegajace permutacji. Blok = maksymalny spojny przedzial rownych id.
    """
    from nulls.interventional import _derangement_indices

    if rng is None:
        rng = np.random.default_rng()
    Z = np.asarray(Z, dtype=np.float64)
    sentence_ids = np.asarray(sentence_ids)
    t_prime = Z.shape[0]

    # bloki = spojne przedzialy rownych id
    boundaries = np.flatnonzero(np.diff(sentence_ids) != 0) + 1
    starts = np.concatenate([[0], boundaries])
    ends = np.concatenate([boundaries, [t_prime]])
    n_blocks = starts.size
    if n_blocks < 2:
        raise ValueError(
            f"permutacja blokow niemozliwa: {n_blocks} blok(ow) zdan - metryka "
            f"zdaniowa wymaga co najmniej 2"
        )

    G = Z @ Z.T
    observed = _sigma1_from_gram(G, np.arange(t_prime), t_prime, rng)
    null = np.empty(n_permutations)
    for i in range(n_permutations):
        block_order = _derangement_indices(n_blocks, rng)
        order = np.concatenate([np.arange(starts[b], ends[b]) for b in block_order])
        null[i] = _sigma1_from_gram(G, order, t_prime, rng)
    return float((observed - null.mean()) / null.std(ddof=1))


def d_lag(Z, n_permutations=500, rng=None):
    """D_lag = z-score sigma_1(C(1)) wzgledem nullu permutacji kolejnosci wierszy."""
    if rng is None:
        rng = np.random.default_rng()
    Z = np.asarray(Z, dtype=np.float64)
    t_prime = Z.shape[0]
    G = Z @ Z.T
    observed = _sigma1_from_gram(G, np.arange(t_prime), t_prime, rng)
    null = np.empty(n_permutations)
    for i in range(n_permutations):
        null[i] = _sigma1_from_gram(G, rng.permutation(t_prime), t_prime, rng)
    return float((observed - null.mean()) / null.std(ddof=1))
