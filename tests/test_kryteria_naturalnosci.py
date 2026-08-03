"""Testy kryteriow bramki naturalnosci, wersja 3.

Kazdy test odpowiada jednemu sposobowi, w jaki dwie poprzednie wersje bramki
zawiodly. To nie sa testy dla samych testow - to zapis bledow, ktore juz
zostaly popelnione.
"""

import random

import pytest

from gates.naturalnosc.kryteria import (BUDZET, MUSZA_BYC_ZEWNETRZNE, WARIANTY,
                                        ocen_scenariusz, rachunek_osiagalnosci,
                                        stale_z_rozkladu)


def scenariusz(nat=None, jas=None, samo=None, rng=None):
    """Scenariusz o realistycznym profilu: warianty roznia sie Z ZALOZENIA."""
    rng = rng or random.Random(0)
    domyslne_nat = {"B": 6.0, "C": 3.5, "CprimG": 6.1, "CprimComp": 5.5,
                    "CprimM": 5.8, "CprimU": 4.5}
    domyslne_jas = {"B": 5.5, "C": 2.3, "CprimG": 6.5, "CprimComp": 5.6,
                    "CprimM": 5.4, "CprimU": 2.1}
    domyslne_samo = {"B": 1.5, "C": 6.5, "CprimG": 1.4, "CprimComp": 2.0,
                     "CprimM": 1.6, "CprimU": 1.3}
    n = {**domyslne_nat, **(nat or {})}
    j = {**domyslne_jas, **(jas or {})}
    s = {**domyslne_samo, **(samo or {})}
    return {w: {"naturalnosc": n[w] + rng.gauss(0, 0.25),
                "jasnosc": j[w] + rng.gauss(0, 0.25),
                "samozwrotnosc": s[w] + rng.gauss(0, 0.25)} for w in WARIANTY}


def korpus(n=48, ziarno=3):
    rng = random.Random(ziarno)
    return [scenariusz(rng=rng) for _ in range(n)]


def wzorcowy():
    """Scenariusz dokladnie o srednim profilu - bez szumu, wiec deterministyczny."""
    class Zero:
        def gauss(self, *_):
            return 0.0
    return scenariusz(rng=Zero())


# --- K6: sedno przeprojektowania -------------------------------------------

@pytest.mark.parametrize("ziarno", [3, 11, 29])
def test_odrzucenie_LACZNE_miesci_sie_w_budzecie(ziarno):
    """SEDNO WERSJI 3, i zarazem blad, ktory ta wersja sama popelnila w pierwszym
    podejsciu: kazda stala dobrana osobno na 10% ogona daje przy trzynastu
    kryteriach ponad 50% odrzucen lacznie. Budzet dotyczy CALEJ bramki."""
    dobre = korpus(ziarno=ziarno)
    stale = stale_z_rozkladu(dobre)
    odrzucone = rachunek_osiagalnosci(dobre, stale)
    assert odrzucone <= BUDZET + 1e-9, f"odrzucono {odrzucone:.0%} dobrego materialu"


def test_tryb_pracy_bramki_jest_JAWNY():
    """Przy 13 kryteriach i n=48 zaden dodatni ogon nie miesci sie w budzecie
    (rozdzielczosc probki 1/48 = 2,1%, potrzebne ~0,8%). Bramka schodzi wtedy
    do trybu obwiedni - i MUSI to zglosic, bo zmienia sie jej sens: przestaje
    byc sitem percentylowym, staje sie detektorem materialu gorszego niz
    cokolwiek uznanego za dobre."""
    stale = stale_z_rozkladu(korpus())
    assert stale["tryb"] in ("kwantylowy", "obwiednia")
    if stale["tryb"] == "obwiednia":
        assert stale["potrzebne_n"] > len(korpus())


def test_stale_sa_najostrzejsze_z_mieszczacych_sie_w_budzecie():
    """Bramka ma byc tak czula, jak pozwala budzet - luzniejsze stale
    przepuszczalyby uszkodzenia bez potrzeby."""
    dobre = korpus()
    stale = stale_z_rozkladu(dobre)
    from gates.naturalnosc.kryteria import _stale_przy_alfa
    ostrzejsze = _stale_przy_alfa(dobre, stale["alfa"] + BUDZET / 200)
    assert rachunek_osiagalnosci(dobre, ostrzejsze) > BUDZET


# --- czego wersja 2 nie potrafila ------------------------------------------

def test_wariant_nieosadzony_NIE_jest_karany_za_nieosadzenie():
    """WADA WERSJI 2: 'jasnosc kazdego wariantu >= 5,0' odrzucalaby wariant
    nieosadzony za wlasnosc, ktora jest jego DEFINICJA (zmierzone: 2,09)."""
    stale = stale_z_rozkladu(korpus())
    s = scenariusz(jas={"CprimU": 2.0})
    assert not [b for b in ocen_scenariusz(s, stale) if "CprimU" in b and "K3" in b]


def test_wariant_samozwrotny_NIE_jest_karany_za_niska_naturalnosc_typowa():
    """WADA WERSJI 2: 'rozstep miedzy wariantami <= 1,0' przy realnym rozstepie
    3,27 odrzucalby kazdy scenariusz. Tutaj wariant samozwrotny lezy 2,5 pkt
    ponizej kotwicy i scenariusz przechodzi, bo taki jest JEGO RODZAJ."""
    stale = stale_z_rozkladu(korpus())
    assert ocen_scenariusz(wzorcowy(), stale) == []


# --- czego wersja 2 nie wykrywala ------------------------------------------

def test_przypadkowo_OSADZONY_wariant_nieosadzony_jest_wykryty():
    """K4 - wada odwrotna, dotad niesprawdzana. Wariant nieosadzony, ktory
    wypada zbyt jasno, przestal byc tym, czym mial byc."""
    stale = stale_z_rozkladu(korpus())
    braki = ocen_scenariusz(scenariusz(jas={"CprimU": 6.5}), stale)
    assert any("K4" in b for b in braki), braki


@pytest.mark.parametrize("wariant", MUSZA_BYC_ZEWNETRZNE)
def test_pulapka_samozwrotna_jest_wykryta_przez_PYTANIE_WPROST(wariant):
    """K5. Skala jasnosci tej pulapki NIE wykrywa - zmierzone 0/6 po polsku:
    referent (rozmowa) istnieje i jest jasny, wada jest to, ze nie o nim mowa.
    Dlatego pyta sie o nia wprost."""
    stale = stale_z_rozkladu(korpus())
    s = scenariusz(samo={wariant: 6.0}, jas={wariant: 6.5})   # jasny, ale samozwrotny
    braki = ocen_scenariusz(s, stale)
    assert any("K5" in b and wariant in b for b in braki), braki


def test_zle_napisana_kotwica_odrzuca_scenariusz():
    """K1. Wariant neutralny nie ma zadnego obciazenia konstrukcyjnego,
    wiec jego slaby wynik znaczy po prostu zle napisany scenariusz."""
    stale = stale_z_rozkladu(korpus())
    braki = ocen_scenariusz(scenariusz(nat={"B": 2.0}), stale)
    assert any("K1" in b for b in braki), braki


def test_spadek_liczony_wobec_kotwicy_TEGO_SAMEGO_scenariusza():
    """K2. Porownanie wewnatrz scenariusza usuwa wplyw tematu i autora.
    Scenariusz slabszy w calosci, ale o zachowanych proporcjach, przechodzi."""
    stale = stale_z_rozkladu(korpus())
    s = wzorcowy()
    przesuniety = {w: {**v, "naturalnosc": v["naturalnosc"] - 0.4} for w, v in s.items()}
    assert not [b for b in ocen_scenariusz(przesuniety, stale) if b.startswith("K2")]


def test_wariant_zapadajacy_sie_wzgledem_kotwicy_jest_wykryty():
    stale = stale_z_rozkladu(korpus())
    braki = ocen_scenariusz(scenariusz(nat={"CprimM": 1.5}), stale)
    assert any("K2/CprimM" in b for b in braki), braki


def test_brak_materialu_to_blad_a_nie_domyslne_stale():
    """Stale nie moga powstac znikad - to bylby powrot do wymyslania."""
    with pytest.raises(ValueError):
        stale_z_rozkladu([])
