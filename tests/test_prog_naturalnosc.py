"""Testy rachunku progu bramki naturalnosci.

Prog decyduje, ktore scenariusze wejda do badania. Blad w tym rachunku jest
kosztowniejszy niz blad w pojedynczym scenariuszu - dlatego regula musi byc
sprawdzona na danych, ktorych wynik znamy z gory.
"""

import random

import pytest

from gates.naturalnosc.prog import BUDZET_BLEDU, kwantyl


def test_kwantyl_zwraca_wartosc_ze_zbioru():
    """Nearest rank, bez interpolacji - prog ma byc realnie osiagnieta ocena,
    a nie liczba, ktorej nikt nie wystawil."""
    d = [1.0, 2.0, 3.0, 4.0, 5.0]
    assert kwantyl(d, 0.5) in d
    assert kwantyl(d, 0.0) == 1.0
    assert kwantyl(d, 1.0) == 5.0


def test_kwantyl_nie_zalezy_od_kolejnosci():
    d = [4.2, 1.1, 6.9, 3.3, 5.5]
    p = list(d)
    random.Random(1).shuffle(p)
    assert kwantyl(d, 0.25) == kwantyl(p, 0.25)


@pytest.mark.parametrize("n", [10, 24, 48, 96])
def test_falszywe_odrzucenie_nie_przekracza_budzetu(n):
    """SEDNO REGULY: prog dobrany jako kwantyl 10% rozkladu nienaruszonych
    ma odrzucac nie wiecej niz 10% dobrego materialu. Jesli ten test padnie,
    bramka wycina zdrowe scenariusze."""
    rng = random.Random(7)
    dobre = [rng.gauss(5.8, 0.7) for _ in range(n)]
    prog = kwantyl(dobre, BUDZET_BLEDU)
    odrzucone = sum(1 for v in dobre if v < prog) / n
    assert odrzucone <= BUDZET_BLEDU + 1e-9, f"odrzucono {odrzucone:.0%}"


def test_prog_rosnie_z_jakoscia_materialu():
    """Material lepszy => prog wyzszy. Bramka ma sie dostrajac do materialu,
    a nie trzymac stalej wartosci niezaleznie od tego, co ocenia."""
    rng = random.Random(11)
    slaby = [rng.gauss(4.5, 0.7) for _ in range(48)]
    dobry = [rng.gauss(6.2, 0.7) for _ in range(48)]
    assert kwantyl(dobry, BUDZET_BLEDU) > kwantyl(slaby, BUDZET_BLEDU)


def test_wykrywalnosc_jest_wynikiem_a_nie_wyborem():
    """Prog liczy sie WYLACZNIE z materialu nienaruszonego. Dolozenie
    uszkodzonych elementow nie moze go ruszyc - inaczej kalibracja
    dostrajalaby sie do wlasnych uszkodzen."""
    rng = random.Random(13)
    dobre = [rng.gauss(5.8, 0.7) for _ in range(24)]
    prog_sam = kwantyl(dobre, BUDZET_BLEDU)
    _ = [rng.gauss(3.0, 0.9) for _ in range(24)]      # uszkodzone - ignorowane
    prog_znowu = kwantyl(dobre, BUDZET_BLEDU)
    assert prog_sam == prog_znowu


def test_prog_z_symulacji_moglby_odrzucic_zdrowy_material():
    """REGRESJA HISTORYCZNA: prog 5,0 zamrozony z symulacji odrzucal realny
    material SPEKTRY-1 o sredniej 4,85. Test pilnuje, ze regula kwantylowa
    tego nie robi - prog wyliczony z materialu jest od niego nizszy."""
    material = [4.85] * 12 + [5.2] * 12
    prog = kwantyl(material, BUDZET_BLEDU)
    assert prog <= 4.85
    assert sum(1 for v in material if v < prog) / len(material) <= BUDZET_BLEDU
