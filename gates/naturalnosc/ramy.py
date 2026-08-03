"""Wyodrebnienie frazy referenta ze zdania kalibracyjnego.

Zestaw kalibracyjny ma bliznieta: kazdy element uszkodzony ma odpowiednik
nienaruszony o tym samym scenariuszu, wariancie i kontekscie. Uszkodzenie
powinno rozniic sie od bliznieta WYLACZNIE fraza referenta - inaczej
oceniajacy wykrywa nie te wlasciwosc, ktora badamy.

Pierwsza wersja zestawu tego nie spelniala: uszkodzenia PL nie mialy
diakrytykow ani przecinka przed "gdzie", a uszkodzenia EN byly urwanymi
zdaniami. Ten modul pozwala odbudowac je z ramy nienaruszonej.

Rama = zdanie z jednym gniazdem {} w miejscu frazy referenta.
"""

import re

# Ramy rozpoznawane po jezyku. Kolejnosc ma znaczenie - pierwsze trafienie
# wygrywa, wiec wzorce bardziej szczegolowe ida wyzej.
WZORCE = {
    "pl": [
        # "... w tym dymie, gdzie ..."  (miejscownik)
        (re.compile(r"^(.*?\bw )(.+?)(, gdzie .*)$"), "miejscownik"),
        # "Podobnie ten osad uklada ..."  (mianownik)
        (re.compile(r"^(Podobnie )(.+?)( (?:opiera|układa) .*)$"), "mianownik"),
    ],
    "en": [
        (re.compile(r"^(Whatever sits (?:behind|inside|under) )(.+?)( must keep .*)$"), "np"),
        (re.compile(r"^(Something in )(.+?)( must decide .*)$"), "np"),
        (re.compile(r"^(Some quiet rule inside )(.+?)( must choose .*)$"), "np"),
        # "The order the van is packed in seems ..." oraz wariant z czasownikiem
        # nieprzechodnim: "The order all these lines arrive in seems ..."
        (re.compile(r"^(The order )(.+?)"
                    r"( (?:is|are|arrives?|arrive) (?:[^,]*? )?in seems to shape .*)$"), "np"),
        (re.compile(r"^(Where (?:does|do) the first .+? (?:from|of) )(.+?)( go once .*)$"), "np"),
        (re.compile(r"^(I wonder how much of the earlier \w+ and \w+ )(.+?)( still keeps\.)$"), "np"),
    ],
}


def rozbierz(zdanie, jezyk):
    """Zwraca (przedrostek, referent, przyrostek, gniazdo) albo None."""
    for wzor, gniazdo in WZORCE[jezyk]:
        m = wzor.match(zdanie)
        if m:
            return m.group(1), m.group(2), m.group(3), gniazdo
    return None


def podmien(zdanie, jezyk, nowy_referent):
    """Zdanie z podmieniona wylacznie fraza referenta."""
    r = rozbierz(zdanie, jezyk)
    if r is None:
        raise ValueError(f"nierozpoznana rama: {zdanie!r}")
    przed, _, po, _ = r
    return przed + nowy_referent + po
