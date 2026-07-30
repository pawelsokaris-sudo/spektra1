"""Preprocessing aktywacji: maskowanie, komponent pozycyjny, z-score (protokol par. 4).

Kolejnosc w pipeline: mask_tokens -> positional_mean/subtract_positional -> zscore_channels.
Wykluczanie kanalow niskiej wariancji dziala na wariancji SUROWEJ (przed z-score),
zgodnie z par. 2 protokolu; liczba wykluczonych kanalow jest raportowana.
"""

import numpy as np


def mask_tokens(H, special_mask=None, skip_first=32):
    """Usuwa pierwsze `skip_first` tokenow oraz tokeny specjalne.

    H: (T, D) aktywacje; special_mask: (T,) bool, True = token specjalny.
    Zwraca (T', D).
    """
    T = H.shape[0]
    keep = np.ones(T, dtype=bool)
    keep[:skip_first] = False
    if special_mask is not None:
        keep &= ~np.asarray(special_mask, dtype=bool)
    return H[keep]


def positional_mean(texts):
    """Srednia aktywacji per pozycja po calym korpusie (protokol par. 4).

    texts: lista tablic (T_i, D) o wspolnej siatce pozycji od 0.
    Zwraca (T_max, D); na pozycji t usredniane sa tylko teksty siegajace t.
    """
    t_max = max(t.shape[0] for t in texts)
    d = texts[0].shape[1]
    sums = np.zeros((t_max, d), dtype=np.float64)
    counts = np.zeros(t_max, dtype=np.float64)
    for t in texts:
        n = t.shape[0]
        sums[:n] += t
        counts[:n] += 1.0
    return sums / counts[:, None]


def subtract_positional(texts, mu):
    """Odejmuje komponent pozycyjny mu od kazdego tekstu (po dlugosci tekstu)."""
    return [t - mu[: t.shape[0]] for t in texts]


def zscore_channels(H, eps=1e-6):
    """Z-score per kanal; kanaly o wariancji surowej < eps wykluczone.

    Zwraca (Z, n_excluded): Z (T, D_kept) o sredniej 0 i wariancji 1 per kanal
    (wariancja populacyjna), n_excluded = liczba wykluczonych kanalow.
    """
    H = np.asarray(H, dtype=np.float64)
    raw_var = H.var(axis=0)
    keep = raw_var >= eps
    Hk = H[:, keep]
    Z = (Hk - Hk.mean(axis=0)) / np.sqrt(Hk.var(axis=0))
    return Z, int((~keep).sum())
