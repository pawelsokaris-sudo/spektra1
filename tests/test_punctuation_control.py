"""Testy kontroli interpunkcyjnej - na tekstach o znanej konstrukcji."""

import numpy as np

from gates.punctuation_control import (balanced_accuracy, feature_diagnostics,
                                       features, leave_one_scenario_out, text_of)


def test_cechy_sa_znormalizowane_dlugoscia():
    """Tekst sklejony sam ze soba ma dawac te same cechy - inaczej klasyfikator
    uczylby sie DLUGOSCI, a dlugosc jest wyrownana osobnym mechanizmem."""
    t = "Czy tak? Tak, tak."
    assert np.allclose(features(t), features(t + t), atol=1e-9)


def test_dokladnosc_zbalansowana_nie_nagradza_wiekszosciowego():
    """1 do 4 jak w kontroli A vs dialogowe: 'zawsze klasa 1' ma dac 0.5."""
    y = np.array([0] + [1] * 4)
    zawsze_jeden = np.array([True] * 5)
    assert balanced_accuracy(y, zawsze_jeden) == 0.5


def test_klasyfikator_wykrywa_realna_roznice_interpunkcyjna():
    teksty0 = ["Krok - jeden. Krok - dwa. Krok - trzy."] * 8
    teksty1 = ["Czy to dziala? Tak, dziala. Na pewno?"] * 8
    X = np.array([features(t) for t in teksty0 + teksty1])
    y = np.array([0] * 8 + [1] * 8)
    groups = np.array([f"s{i}" for i in range(8)] * 2)
    acc, _ = leave_one_scenario_out(X, y, groups)
    assert acc > 0.9


def test_klasyfikator_nie_wykrywa_roznicy_ktorej_nie_ma():
    rng = np.random.default_rng(3)
    baza = ["Czy to dziala? Tak, dziala, oczywiscie."] * 16
    X = np.array([features(t) for t in baza])
    X = X + rng.normal(0, 1e-6, X.shape)
    y = np.array([0] * 8 + [1] * 8)
    groups = np.array([f"s{i}" for i in range(8)] * 2)
    acc, _ = leave_one_scenario_out(X, y, groups)
    assert acc < 0.75


def test_diagnostyka_wskazuje_wlasciwe_znaki():
    """Diagnostyka ma wskazac OBA znaki, ktore realnie roznicuja klasy.

    Nie testujemy, ktory z nich wyladuje pierwszy: oba separuja idealnie,
    wiec kolejnosc zalezy od skali, a nie od sily dowodu."""
    X = np.array([features("Krok - jeden - dwa - trzy.")] * 6
                 + [features("Krok jeden, dwa, trzy.")] * 6)
    y = np.array([0] * 6 + [1] * 6)
    top2 = {r["znak"] for r in feature_diagnostics(X, y)[:2]}
    assert top2 == {"-", ","}


def test_text_of_sklada_tury_w_jeden_tekst():
    turns = [{"role": "user", "sentences": ["A.", "B."]},
             {"role": "model", "sentences": ["C."]}]
    assert text_of(turns) == "A. B. C."
