"""Test permutacyjny parowany wewnatrz scenariuszy (protokol par. 6).

Jednostka inferencji = SCENARIUSZ. Dla kontrastu dwoch wariantow (np. glownego
C - C'-G) liczymy roznice parowana d_s per scenariusz. Pod hipoteza zerowa
etykiety wariantow sa wewnatrz scenariusza wymienne, wiec rozklad zerowy
powstaje przez losowe ZMIANY ZNAKU roznic - to jest dokladny odpowiednik
permutacji etykiet w ukladzie parowanym.

Dla malego n rozklad jest wyliczany DOKLADNIE (2^n znakowan), nie probkowany:
przy n = 8 to 256 przypadkow, wiec probkowanie 10 000 razy byloby udawaniem
precyzji, ktorej i tak nie ma - najmniejsze osiagalne p to 1/256 = 0.0039.
To ma bezposrednie znaczenie dla planowania mocy przy alfa = 0.01.

Prog wyliczania dokladnego to 13 (2^13 = 8192 znakowan). Powyzej probkujemy:
przy n = 20 tablica wszystkich znakowan mialaby ponad milion wierszy, a i tak
byloby ich wiecej niz domyslnych 10 000 losowan, wiec dokladnosc nic nie daje.

Test jednostronny (H1 i H2 sa kierunkowe), alfa = 0.01, CI 99% dla decyzji
konfirmacyjnych (rozstrzygniecie #30 z rundy 1).
"""

import itertools

import numpy as np


def n_exact_permutations(n):
    """Liczba wszystkich znakowan przy n parach."""
    return 2 ** n


def _exact_null_means(diffs):
    """Wszystkie 2^n srednich pod zmiana znakow (dokladny rozklad zerowy)."""
    n = diffs.size
    signs = np.array(list(itertools.product([-1.0, 1.0], repeat=n)))
    return (signs * diffs).mean(axis=1)


def _sampled_null_means(diffs, n_permutations, rng):
    signs = rng.choice([-1.0, 1.0], size=(n_permutations, diffs.size))
    return (signs * diffs).mean(axis=1)


def paired_permutation_test(diffs, n_permutations=10000, ci_level=0.99,
                            exact_threshold=13, compute_ci=True, rng=None):
    """Jednostronny test permutacyjny dla parowanych roznic scenariuszowych.

    diffs: tablica roznic per scenariusz (np. Ī(C) - Ī(C'-G))
    Zwraca dict: p_value, d_z, mean, ci, exact, n_permutations.

    Alternatywa jest zawsze 'wieksze od zera' - hipotezy sa kierunkowe, wiec
    efekt o przeciwnym znaku ma z zalozenia dawac p bliskie 1, a nie istotnosc.
    """
    diffs = np.asarray(diffs, dtype=np.float64)
    if diffs.size == 0:
        raise ValueError("pusta tablica roznic - brak scenariuszy do testu")
    if rng is None:
        rng = np.random.default_rng()

    observed = float(diffs.mean())
    exact = diffs.size <= exact_threshold
    if exact:
        null_means = _exact_null_means(diffs)
        n_used = n_exact_permutations(diffs.size)
    else:
        null_means = _sampled_null_means(diffs, n_permutations, rng)
        n_used = n_permutations

    # p jednostronne z poprawka +1 (obserwowane znakowanie nalezy do rozkladu)
    p_value = float((np.sum(null_means >= observed) + (0 if exact else 1))
                    / (n_used + (0 if exact else 1)))

    sd = diffs.std(ddof=1) if diffs.size > 1 else 0.0
    d_z = float(observed / sd) if sd > 0 else float("inf") if observed else 0.0

    # CI przez bootstrap scenariuszy (jednostka inferencji = scenariusz).
    # Pomijane w symulacjach mocy: tam test wolany jest tysiace razy, a przedzial
    # nie jest do niczego uzywany - liczenie go bylo najdrozsza czescia petli.
    if compute_ci:
        n_boot = 10000
        boot = rng.choice(diffs, size=(n_boot, diffs.size), replace=True).mean(axis=1)
        a = 1.0 - ci_level
        ci = (float(np.quantile(boot, a / 2)), float(np.quantile(boot, 1 - a / 2)))
    else:
        ci = None

    return {
        "p_value": p_value,
        "mean": observed,
        "d_z": d_z,
        "sd": float(sd),
        "n_scenarios": int(diffs.size),
        "ci": ci,
        "ci_level": ci_level,
        "exact": bool(exact),
        "n_permutations": int(n_used),
        "min_attainable_p": float(1 / n_used) if exact else float(1 / (n_used + 1)),
    }
