"""TOST rownowaznosci na parowanych roznicach scenariuszowych (ANEKS-2).

Dwa testy jednostronne przez te sama permutacje parowana co testy glowne
(zmiana znakow wewnatrz scenariuszy). Margines zamrozony jako |d_z| < 0.3,
alfa = 0.05 NA STRONE, per replika jezykowa osobno.

Dlaczego margines w d_z, a nie w jednostkach surowych: I_total jest udzialem
wariancji, wiec jego skala zalezy od warstwy i dlugosci okna. Margines
standaryzowany jest porownywalny miedzy replikami i spojny z H4, gdzie
zostal zamrozony jako pierwszy.

Uwaga interpretacyjna (ANEKS-2): brak istotnosci testu glownego przy
NIEzaliczonym TOST daje werdykt "niekonkluzywny", nie "efekt wykluczony".
Rownowaznosc potwierdza wylacznie zaliczony TOST.
"""

import numpy as np

from power.permutation import paired_permutation_test


def min_attainable_margin(n, alpha=0.05, n_permutations=10000, rng=None,
                          grid=np.arange(0.05, 2.01, 0.05)):
    """Najmniejszy margines, przy ktorym TOST moze przejsc dla efektu ZEROWEGO.

    Rzecz kluczowa dla uczciwosci raportu: przy malym n moze sie zdarzyc, ze
    zamrozony margines jest NIEOSIAGALNY - test rownowaznosci nie przejdzie
    nawet wtedy, gdy roznica jest dokladnie zerowa, bo rozklad permutacyjny
    przy n par ma zbyt gruby krok. Wtedy werdykt "efekt praktycznie wykluczony"
    nie istnieje w przestrzeni mozliwych wynikow badania i trzeba to napisac
    wprost, zamiast raportowac "nie wykazano rownowaznosci" jako wynik.

    Zwraca None, jesli zaden margines z siatki nie wystarcza.
    """
    if rng is None:
        rng = np.random.default_rng(0)
    z = np.zeros(int(n))
    z[0], z[1] = 1.0, -1.0          # d_z = 0 dokladnie, SD > 0
    z = z - z.mean()
    for m in grid:
        delta = float(m) * float(z.std(ddof=1))
        lo = paired_permutation_test(z + delta, n_permutations=n_permutations,
                                     compute_ci=False, rng=rng)["p_value"]
        hi = paired_permutation_test(delta - z, n_permutations=n_permutations,
                                     compute_ci=False, rng=rng)["p_value"]
        if lo < alpha and hi < alpha:
            return float(m)
    return None


def paired_tost_equivalence(diffs, margin_dz=0.3, alpha=0.05,
                            n_permutations=10000, rng=None):
    """Czy efekt miesci sie w marginesie rownowaznosci +/- margin_dz * SD.

    Zwraca dict z p obu stron i decyzja. Rownowaznosc = OBIE strony odrzucone.

    Konstrukcja: margines w jednostkach surowych to margin_dz * SD roznic.
    SD jest niezmiennicze wzgledem przesuniecia, wiec ten sam estymator sluzy
    do standaryzacji i do zbudowania obu hipotez brzegowych.
    """
    diffs = np.asarray(diffs, dtype=np.float64)
    if diffs.size < 2:
        raise ValueError("TOST wymaga co najmniej 2 scenariuszy")
    if rng is None:
        rng = np.random.default_rng()

    sd = float(diffs.std(ddof=1))
    if sd == 0.0:
        # Wszystkie roznice identyczne. Margines jest zdefiniowany wzgledem SD,
        # wiec przy SD = 0 jest zerowy i test bylby zdegenerowany. NIE orzekamy
        # rownowaznosci "bo efekt wyszedl dokladnie zero": w realnych danych to
        # sygnal bledu (ten sam plik policzony dwa razy), a nie wynik. Zwracamy
        # brak rozstrzygniecia z powodem, zamiast wywracac cala analize.
        return {"equivalent": None, "reason": "zerowe SD roznic - TOST nieokreslony",
                "p_lower": None, "p_upper": None, "p_tost": None,
                "margin_dz": float(margin_dz), "margin_raw": 0.0,
                "alpha_per_side": float(alpha),
                "observed_mean": float(diffs.mean()), "observed_d_z": None,
                "n_scenarios": int(diffs.size)}
    delta = margin_dz * sd

    # Strona dolna: H0: srednia <= -delta. Przesuwamy o +delta i testujemy > 0.
    lower = paired_permutation_test(diffs + delta, n_permutations=n_permutations,
                                    compute_ci=False, rng=rng)
    # Strona gorna: H0: srednia >= +delta. Testujemy (delta - roznice) > 0.
    upper = paired_permutation_test(delta - diffs, n_permutations=n_permutations,
                                    compute_ci=False, rng=rng)

    equivalent = bool(lower["p_value"] < alpha and upper["p_value"] < alpha)
    return {
        "min_attainable_margin_dz": min_attainable_margin(
            diffs.size, alpha=alpha, n_permutations=n_permutations, rng=rng),
        "equivalent": equivalent,
        "p_lower": lower["p_value"],
        "p_upper": upper["p_value"],
        "p_tost": float(max(lower["p_value"], upper["p_value"])),
        "margin_dz": float(margin_dz),
        "margin_raw": float(delta),
        "alpha_per_side": float(alpha),
        "observed_mean": float(diffs.mean()),
        "observed_d_z": float(diffs.mean() / sd),
        "n_scenarios": int(diffs.size),
    }
