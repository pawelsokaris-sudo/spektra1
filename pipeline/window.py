"""Okno pomiarowe: wyrownanie dlugosci wariantow (kandydat na aneks do par. 4).

PROBLEM, KTORY TO ROZWIAZUJE. Pomiar dokladnym tokenizerem wykazal (DEP-04,
2026-07-30), ze wariant C'-G jest co najmniej tak dlugi jak C we WSZYSTKICH
16 scenariuszach, w obu replikach - roznica G-self nie jest ujemna nigdzie,
najlepsze osiagniete to dokladne zero. To nie jest niedbalosc autorow tylko
wlasnosc tokenizera: samoodniesienie uzywa czestych slow deiktycznych ("ta
rozmowa", "to przetwarzanie"), a odniesienie osadzone wymaga rzadszego
rzeczownika dziedzinowego, ktory tokenizer rozbija na wiecej czastek.

Dlaczego to grozne: widmo macierzy korelacji zalezy od proporcji T'/D. Prog
odciecia lambda* liczymy per (warstwa, jezyk), NIE per dlugosc tekstu, wiec
systematyczna roznica dlugosci nie zostaje przez niego pochloniete. Przy
roznicy jednokierunkowej w 16 scenariuszach nie usrednia sie do zera - wchodzi
wprost do kontrastu glownego.

Wyrownanie okna usuwa CALA zaleznosc od dlugosci, nie tylko te czesc, ktora
lapie lambda*: proporcja T'/D staje sie identyczna z konstrukcji, wiec I_total,
k, H_s i D_lag przestaja byc porownywane miedzy tekstami roznej dlugosci.

WYBOR TRYBU WCHODZI DO PIECZECI i nalezy do kierownika badania. Dopoki nie
zapadnie, `mode` w config.yaml ma wartosc TBD-DECISION, a pipeline odmawia
uruchomienia - zeby nie podjac tej decyzji milczaco przez wartosc domyslna.
"""

import numpy as np

MODES = {
    "equalize": "wspolne okno = minimum T' po wariantach scenariusza",
    "none": "bez wyrownania; roznice dlugosci raportowane jako ograniczenie",
}


class WindowNotDecidedError(RuntimeError):
    """Tryb okna nie zostal wybrany - wybor wchodzi do pieczeci."""


def common_window(lengths):
    """Wspolna dlugosc okna dla wariantow jednego scenariusza."""
    return int(min(lengths.values()))


def apply_window(activations, mode, report_dropped=False):
    """Ucina warianty do wspolnego okna (albo zostawia bez zmian).

    activations: dict wariant -> tablica (T', D) po maskowaniu.
    mode: 'equalize' | 'none' | 'TBD-DECISION'
    Zwraca dict wariant -> tablica; z report_dropped takze liczbe odrzuconych
    tokenow per wariant (raportowana w pakiecie pieczeci).
    """
    if mode not in MODES:
        raise WindowNotDecidedError(
            f"tryb okna pomiarowego = {mode!r}. Wybor wchodzi do pieczeci i musi "
            f"byc podjety jawnie przez kierownika badania; dopuszczalne: "
            f"{sorted(MODES)}. Pipeline nie uruchomi sie z TBD-DECISION, zeby nie "
            f"rozstrzygnac tego milczaco wartoscia domyslna."
        )

    lengths = {k: v.shape[0] for k, v in activations.items()}
    if mode == "none":
        out, dropped = dict(activations), {k: 0 for k in activations}
    else:
        n = common_window(lengths)
        out = {k: v[:n] for k, v in activations.items()}
        dropped = {k: lengths[k] - n for k in activations}
    return (out, dropped) if report_dropped else out
