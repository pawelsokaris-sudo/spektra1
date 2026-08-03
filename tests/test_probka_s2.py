"""Testy probki kalibracyjnej z korpusu SPEKTRY-2.

Probka decyduje, ktore scenariusze WYPADNA z badania. Blad tutaj kosztuje
tyle, ile napisanie brakujacych scenariuszy od nowa.
"""

from gates.naturalnosc.probka_spektra2 import (SCENARIUSZY_NA_JEZYK, WARIANT,
                                               kontekst, zbuduj)
from gates.naturalnosc.kryteria import WARIANTY


def test_probka_jest_odtwarzalna():
    """Ziarno zamrozone - dwa wywolania musza dac ten sam material,
    inaczej lista wykluczonych z badania nie znaczy nic."""
    a, wa = zbuduj()
    b, wb = zbuduj()
    assert wa == wb
    assert [x["id"] for x in a] == [x["id"] for x in b]
    assert [x["zdanie"] for x in a] == [x["zdanie"] for x in b]


def test_kazdy_scenariusz_ma_KOMPLET_szesciu_wariantow():
    """Kryteria K1-K5 porownuja warianty MIEDZY SOBA w obrebie scenariusza.
    Brakujacy wariant unieruchamia caly scenariusz."""
    elementy, _ = zbuduj()
    per_sc = {}
    for e in elementy:
        per_sc.setdefault((e["jezyk"], e["scenariusz"]), set()).add(e["wariant"])
    assert per_sc, "pusta probka"
    for klucz, warianty in per_sc.items():
        assert warianty == set(WARIANTY), f"{klucz}: {sorted(warianty)}"


def test_warianty_jednego_scenariusza_dziela_RAME():
    """Spec par. 2: warianty roznia sie wylacznie fraza referenta. Gdyby
    rozniły sie czyms wiecej, panel ocenialby dwie rzeczy naraz."""
    elementy, _ = zbuduj()
    per_sc = {}
    for e in elementy:
        per_sc.setdefault((e["jezyk"], e["scenariusz"]), []).append(e["zdanie"])
    for klucz, zdania in per_sc.items():
        dlugosci = [len(z.split()) for z in zdania]
        assert max(dlugosci) - min(dlugosci) <= 6, f"{klucz}: {dlugosci}"


def test_liczba_wykluczonych_z_badania_jest_JAWNA():
    """Wykluczenie musi byc policzalne - to sa scenariusze do dopisania."""
    _, wykluczone = zbuduj()
    for jezyk in ("pl", "en"):
        assert len(wykluczone[jezyk]) == SCENARIUSZY_NA_JEZYK
        assert len(set(wykluczone[jezyk])) == SCENARIUSZY_NA_JEZYK


def test_probki_jezykowe_sie_NIE_mieszaja():
    _, wykluczone = zbuduj()
    assert all(x.startswith("pl-") for x in wykluczone["pl"])
    assert all(x.startswith("en-") for x in wykluczone["en"])


def test_kontekst_konczy_sie_na_zdaniu_poprzedzajacym_wstawke():
    sc = {"turns": [{"base": ["A1.", "A2.", "A3."]},
                    {"base": ["B1.", "B2.", "B3.", "B4."]}]}
    k = kontekst(sc, {"turn": 1, "after_sentence": 1}, ile=4)
    assert k.endswith("B2.")
    assert "B3." not in k
    assert k.startswith("A")          # dobrane z poprzedniej tury


def test_kontekst_nie_siega_poza_pierwsza_ture():
    sc = {"turns": [{"base": ["A1.", "A2."]}]}
    assert kontekst(sc, {"turn": 0, "after_sentence": 0}, ile=4) == "A1."


def test_mapowanie_kluczy_pokrywa_wszystkie_warianty():
    assert set(WARIANT.values()) == set(WARIANTY)
