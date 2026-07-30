"""Symulacja mocy dokladnej struktury testu (GATE 1, protokol par. 7).

Moc liczona przez SYMULACJE TEJ SAMEJ PROCEDURY, ktora bedzie uzyta w konfirmacji
(parowany test permutacyjny, jednostronny, alfa = 0.01) - nie wzorem zamknietym
dla testu t. Powod jest konkretny: przy malym n rozklad permutacyjny jest
dyskretny i ma twarda podloge 1/2^n na osiagalne p. Wzor dla testu t tej podlogi
nie widzi i przy n = 6 obiecywalby moc, ktorej fizycznie nie da sie osiagnac.

Standaryzacja: symulujemy roznice scenariuszowe ~ N(d_z, 1). Skala sie skraca,
bo d_z jest juz wielkoscia standaryzowana - dlatego SESOI protokolu jest podany
wlasnie w d_z, a wariancja z pilota sluzy do sprawdzenia, czy zalozenie
o rozkladzie roznic jest sensowne, nie do skalowania mocy.

Kontrast, dla ktorego liczymy M, to kontrast GLOWNY: C - C'-G (protokol v1.3 par. 7).
"""

import numpy as np

from power.permutation import paired_permutation_test


def min_n_for_alpha(alpha):
    """Najmniejsze n, przy ktorym test permutacyjny moze w ogole odrzucic H0.

    Przy n parach dokladny rozklad ma 2^n znakowan, wiec najmniejsze osiagalne
    p to 1/2^n. Ponizej tego progu zadna wielkosc efektu nie da istotnosci.
    """
    n = 1
    while 1 / (2 ** n) > alpha:
        n += 1
    return n


def power_at_n(n, d_z, alpha, n_sims=1000, rng=None):
    """Odsetek odrzucen H0 przy n scenariuszach i prawdziwym efekcie d_z."""
    if rng is None:
        rng = np.random.default_rng()
    if 1 / (2 ** n) > alpha:
        return 0.0  # podloga rozkladu dyskretnego - odrzucenie niemozliwe
    rejections = 0
    for _ in range(n_sims):
        diffs = rng.standard_normal(n) + d_z
        # compute_ci=False: przedzial ufnosci nie jest tu do niczego uzywany,
        # a jego bootstrap byl najdrozsza czescia petli. n_permutations=2000
        # daje rozdzielczosc p ~5e-4, w zupelnosci wystarczajaca przy alfa=0.01.
        res = paired_permutation_test(
            diffs, n_permutations=2000, compute_ci=False, rng=rng
        )
        if res["p_value"] <= alpha:
            rejections += 1
    return rejections / n_sims


def required_m(target_power, d_z, alpha, n_sims=1000, n_min=None, n_max=100, rng=None):
    """Najmniejsze M osiagajace zadana moc; zwraca (M, krzywa mocy).

    M is None, jesli w zakresie do n_max nie da sie osiagnac celu - to jest
    uczciwa odpowiedz, nie blad.
    """
    if rng is None:
        rng = np.random.default_rng()
    start = n_min if n_min is not None else min_n_for_alpha(alpha)
    curve, found = {}, None
    for n in range(start, n_max + 1):
        curve[n] = power_at_n(n, d_z, alpha, n_sims=n_sims, rng=rng)
        if found is None and curve[n] >= target_power:
            found = n
            break
    return found, curve
