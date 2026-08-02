"""Testy walidatora dla korpusu SPEKTRY-2 (5 wariantow, bez wariantu A)."""

import copy

import pytest

from corpus.build import spec_version, variants_for
from corpus.validate import (check_insertion_pairs, check_mundane,
                             check_mundane_balance, check_structure,
                             validate_scenario)

ZDANIE = "Ta czynnosc wymaga rownego tempa oraz spokojnej uwagi przez caly czas jej trwania."
RAMA = "Ten sam schemat widac w {}, gdzie kolejne warstwy nakladaja sie stopniowo."


def scenariusz(sid="pl-01-test", lang="pl", mundane_type="konkretny",
               mundane_fraza="tym ciescie"):
    """Poprawny scenariusz SPEKTRY-2: 10 tur, 5 insercji, piec wariantow."""
    turns = [{"role": "user" if i % 2 == 0 else "assistant",
              "base": [ZDANIE] * 5} for i in range(10)]
    ins = []
    for k in range(5):
        ins.append({
            "turn": k, "after_sentence": 1,
            "neutral": RAMA.format("tym samym dymie"),
            "external_grounded": RAMA.format("tym drugim piecu"),
            "external_mundane": RAMA.format(mundane_fraza),
            "external_ungrounded": RAMA.format("tamtym sterowaniu"),
            "self": RAMA.format("tym przetwarzaniu"),
        })
    return {"scenario_id": sid, "language": lang, "topic": "test",
            "mundane_type": mundane_type,
            "provenance": {"author": "test", "template": "t", "date": "2026-08-02"},
            "turns": turns, "insertions": ins}


# --- rozpoznanie wersji ----------------------------------------------------

def test_pole_mundane_type_rozpoznaje_spektre_2():
    assert spec_version(scenariusz()) == 2
    assert spec_version({"scenario_id": "x", "turns": []}) == 1


def test_spektra_2_nie_ma_wariantu_A():
    assert "A" not in variants_for(scenariusz())
    assert "CprimM" in variants_for(scenariusz())


# --- poprawny scenariusz przechodzi ---------------------------------------

def test_poprawny_scenariusz_spektry_2_przechodzi():
    assert validate_scenario(scenariusz()) == []


def test_brak_pola_a_NIE_jest_bledem_w_spektrze_2():
    """W SPEKTRZE-1 brak 'a' byl bledem. Tu wariantu A nie ma."""
    sc = scenariusz()
    assert all("a" not in t for t in sc["turns"])
    assert check_structure(sc) == []


# --- kontrole wariantu zwyczajnego ----------------------------------------

def test_brak_mundane_type_jest_wykryty():
    sc = scenariusz()
    del sc["mundane_type"]
    # bez tego pola scenariusz jest czytany jako SPEKTRA-1 i wtedy brakuje 'a'
    assert spec_version(sc) == 1
    assert check_structure(sc) != []


def test_zly_mundane_type_jest_wykryty():
    sc = scenariusz(mundane_type="jakis")
    problemy = check_mundane(sc)
    assert any("mundane_type" in p for p in problemy)


@pytest.mark.parametrize("fraza", ["tym planowaniu", "tej decyzji", "tym oczekiwaniu"])
def test_referent_zwyczajny_czytelny_jako_samozwrotny_jest_wykryty(fraza):
    """Pulapka ze specyfikacji par. 3: 'to planowanie' w rozmowie znaczy
    'to, ktore teraz robimy' - wariant kontrolny zarazilby sie tym, co ma
    kontrolowac."""
    sc = scenariusz(mundane_type="procesowy", mundane_fraza=fraza)
    problemy = check_mundane(sc)
    assert any("SAMOZWROTNY" in p for p in problemy), fraza


def test_referent_zakotwiczony_poza_rozmowa_przechodzi():
    sc = scenariusz(mundane_type="procesowy",
                    mundane_fraza="tamtym czekaniu na pociag")
    assert check_mundane(sc) == []


# --- brakujacy piaty wariant ----------------------------------------------

def test_brak_piatego_wariantu_insercji_jest_wykryty():
    sc = scenariusz()
    del sc["insertions"][0]["external_mundane"]
    problemy = check_insertion_pairs(sc)
    assert any("external_mundane" in p for p in problemy)


# --- balans konkretny/procesowy -------------------------------------------

def test_balans_zachowany_przechodzi():
    korpus = ([scenariusz(f"pl-{i:02d}", mundane_type="konkretny") for i in range(4)]
              + [scenariusz(f"pl-{i:02d}", mundane_type="procesowy") for i in range(4, 8)])
    assert check_mundane_balance(korpus) == []


def test_balans_zlamany_jest_wykryty():
    korpus = ([scenariusz(f"pl-{i:02d}", mundane_type="konkretny") for i in range(6)]
              + [scenariusz(f"pl-{i:02d}", mundane_type="procesowy") for i in range(6, 8)])
    problemy = check_mundane_balance(korpus)
    assert any("balans" in p for p in problemy)


def test_balans_liczony_OSOBNO_dla_kazdego_jezyka():
    """Repliki sa osobnymi badaniami - balans musi zachodzic w kazdej z osobna,
    a nie tylko w sumie."""
    korpus = ([scenariusz(f"pl-{i:02d}", lang="pl", mundane_type="konkretny")
               for i in range(4)]
              + [scenariusz(f"en-{i:02d}", lang="en", mundane_type="procesowy")
                 for i in range(4)])
    problemy = check_mundane_balance(korpus)
    assert len(problemy) == 2, "obie repliki sa jednorodne - obie powinny zglosic"


def test_balans_ignoruje_scenariusze_spektry_1():
    korpus = [{"scenario_id": "stary", "language": "pl", "turns": []}]
    assert check_mundane_balance(korpus) == []


def test_roznica_wieksza_niz_sama_fraza_jest_wykryta():
    """Spec par. 2: warianty dziela RAME i roznia sie wylacznie fraza
    rzeczownikowa. Jesli rozni sie wiecej, mierzylibysmy dwie rzeczy naraz."""
    sc = scenariusz()
    sc["insertions"][0]["external_mundane"] = (
        "Zupelnie inne zdanie o czyms calkiem innym, napisane od nowa bez ramy.")
    problemy = check_mundane(sc)
    assert any("WIECEJ niz sama fraza" in p for p in problemy)


def test_wariant_zwyczajny_identyczny_z_neutralnym_jest_wykryty():
    sc = scenariusz()
    sc["insertions"][0]["external_mundane"] = sc["insertions"][0]["neutral"]
    problemy = check_mundane(sc)
    assert any("IDENTYCZNY" in p for p in problemy)
