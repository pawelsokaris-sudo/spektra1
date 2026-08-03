"""Testy sondy dwoch fraz samozwrotnych.

Ta sonda ma rozstrzygnac, co znaczy wariant samozwrotny w hipotezie glownej.
Blad w podmianie frazy albo w tescie parowanym przenosi sie wprost na
definicje H1 - dlatego oba sa sprawdzone osobno.
"""

import pytest

from gates.naturalnosc.sonda_self import kontrola, przelicz, roznica_dlugosci
from gates.naturalnosc.sonda_wynik import permutacja_parowana


# --- podmiana frazy --------------------------------------------------------

@pytest.mark.parametrize("zdanie,oczekiwana_r", [
    ("Coś takiego zdarza się przy tym przetwarzaniu, kiedy jedno ustępuje drugiemu.",
     "Coś takiego zdarza się przy tym toku pytań, kiedy jedno ustępuje drugiemu."),
    ("To trochę przypomina to przetwarzanie, jeśli patrzeć na kolejność.",
     "To trochę przypomina ten tok pytań, jeśli patrzeć na kolejność."),
    ("Z tym przetwarzaniem jest chyba podobnie, bo decyduje pierwszy krok.",
     "Z tym tokiem pytań jest chyba podobnie, bo decyduje pierwszy krok."),
    ("That resembles this processing a little, provided you look only at order.",
     "That resembles this conversation a little, provided you look only at order."),
])
def test_podmiana_zachowuje_przypadek_gramatyczny(zdanie, oczekiwana_r):
    p, r = przelicz(zdanie)
    assert p == zdanie
    assert r == oczekiwana_r


def test_podmiana_dziala_w_OBIE_strony():
    """Dwa scenariusze korpusu uzywaja juz frazy 'tok pytan' - dla nich trzeba
    wytworzyc wersje z 'przetwarzaniem', nie odwrotnie."""
    p, r = przelicz("Ten sam układ widać przy tym toku pytań, gdzie proporcje znaczą więcej.")
    assert "przetwarzaniu" in p
    assert "toku pytań" in r


def test_fraza_nierozpoznana_daje_None():
    """Cicha akceptacja nieznanej frazy wprowadzilaby do sondy trzeci referent."""
    assert przelicz("Coś takiego zdarza się przy tym drugim piecu, kiedy stygnie.") is None


# --- kontrola pary ---------------------------------------------------------

def _para(a, b, jezyk="pl", sc="pl-01"):
    return [{"jezyk": jezyk, "scenariusz": sc, "wersja": "przetwarzanie", "zdanie": a},
            {"jezyk": jezyk, "scenariusz": sc, "wersja": "rozmowa", "zdanie": b}]


def test_rozna_dlugosc_frazy_NIE_jest_bledem():
    """'ten tok pytan' jest o slowo dluzsze niz 'to przetwarzanie'. Pierwsza
    wersja kontroli odrzucala z tego powodu wszystkie 12 par polskich -
    kryterium bylo zle, nie material."""
    assert kontrola(_para(
        "To trochę przypomina to przetwarzanie, jeśli patrzeć na kolejność.",
        "To trochę przypomina ten tok pytań, jeśli patrzeć na kolejność.")) == []


def test_roznica_w_DWOCH_miejscach_jest_wykryta():
    """Wersje maja sie roznic jedna fraza. Dwie zmiany znaczylyby, ze mierzymy
    dwie rzeczy naraz."""
    problemy = kontrola(_para(
        "To trochę przypomina to przetwarzanie, jeśli patrzeć na kolejność.",
        "To bardzo przypomina ten tok pytań, jeśli patrzeć na kolejność."))
    assert problemy


def test_wersje_identyczne_sa_wykryte():
    z = "To trochę przypomina to przetwarzanie, jeśli patrzeć na kolejność."
    assert any("IDENTYCZNE" in p for p in kontrola(_para(z, z)))


def test_niepelna_para_jest_wykryta():
    assert kontrola(_para("a b c", "a d c")[:1]) != []


def test_koszt_tokenowy_jest_raportowany_per_jezyk():
    el = (_para("To przypomina to przetwarzanie dzisiaj.",
                "To przypomina ten tok pytań dzisiaj.", "pl", "pl-01")
          + _para("That resembles this processing today.",
                  "That resembles this conversation today.", "en", "en-01"))
    d = roznica_dlugosci(el)
    assert d["pl"] == [1], "polska fraza jest o slowo dluzsza"
    assert d["en"] == [0], "angielska ma te sama dlugosc"


# --- test parowany ---------------------------------------------------------

def test_permutacja_wykrywa_efekt_jednorodny():
    """Wszystkie pary w te sama strone - przy 12 parach p = 2/4096."""
    p = permutacja_parowana([1.0] * 12)
    assert p == pytest.approx(2 / 4096)


def test_permutacja_nie_widzi_efektu_gdy_go_nie_ma():
    assert permutacja_parowana([1.0, -1.0] * 6) > 0.5


def test_permutacja_jest_dwustronna():
    """Znak efektu nie moze zmieniac wartosci p - inaczej kierunek decydowalby
    o istotnosci."""
    d = [0.8, 1.2, -0.3, 0.9, 1.1, 0.4, 0.7, 1.3, 0.2, 0.6, 1.0, 0.5]
    assert permutacja_parowana(d) == pytest.approx(
        permutacja_parowana([-x for x in d]))


def test_permutacja_odmawia_gdy_enumeracja_niewykonalna():
    with pytest.raises(ValueError):
        permutacja_parowana([1.0] * 20)
