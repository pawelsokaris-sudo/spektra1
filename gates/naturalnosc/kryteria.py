"""Kryteria bramki naturalnosci SPEKTRY-2, wersja 3.

ZASADA NADRZEDNA: bramka sprawdza, czy wariant jest dobrze napisany JAK NA
SWOJ RODZAJ - a nie czy wszystkie warianty sa takie same. Wymog jednakowosci
zadalby zniesienia roznicy, ktora badanie ma zmierzyc.

SKAD BIORA SIE STALE: kazda jest kwantylem rozkladu ocen materialu dobrego.
Stala wyprowadzona z rozkladu jest osiagalna z konstrukcji; stala wymyslona
wymaga osobnego rachunku osiagalnosci - i to wlasnie ten rachunek pominieto
trzy razy (ANEKS-4, prog 5,0, rozstep 1,0).

BUDZET LICZY SIE LACZNIE, NIE NA KRYTERIUM. Pierwsza wersja tego modulu
dobierala kazda stala osobno na 10% ogona. Kryteriow jest trzynascie, wiec
ich suma odrzucala ponad polowe dobrego materialu - ten sam blad, ktory
kryteria maja eliminowac, tylko pietro wyzej. Teraz jeden wspolczynnik ogona
`alfa` jest dobierany tak, by ODRZUCENIE LACZNE zmiescilo sie w budzecie.
"""

from .prog import kwantyl

BUDZET = 0.10

WARIANTY = ["B", "C", "CprimG", "CprimComp", "CprimM", "CprimU"]

# K3: warianty, ktorych referent MUSI byc osadzony w rozmowie.
# Rozstrzyga o tym REGULA OKRESLNIKA ze specyfikacji autorskiej: referent
# obecny -> "ten/ta/to", referent nieobecny -> "tamten/tamta/tamto".
#   B, CprimG, CprimComp maja "ten"  -> referent obecny, jasnosc wymagana
#   CprimM, CprimU      maja "tamten"-> referent NIEOBECNY z zalozenia
#   C - referentem jest rozmowa, wiec skala jasnosci go nie opisuje
#
# POPRAWKA PO KALIBRACJI: pierwotnie CprimM byl w tej liscie. Pomiar pokazal
# jasnosc 2,78 (PL) i 2,69 (EN) - praktycznie tyle co CprimU (2,00). To nie
# jest wada wariantu zwyczajnego, tylko moj blad: wariant zwyczajny odsyla do
# przedmiotu codziennego SPOZA rozmowy, wiec jego referent jest nieobecny
# dokladnie tak samo jak referent nieosadzony. Roznia sie RODZAJEM referenta
# (codzienny konkret wobec technicznej abstrakcji), a nie osadzeniem - i to
# wlasnie mierzy H3.
MUSZA_BYC_OSADZONE = ["B", "CprimG", "CprimComp"]

# K4: warianty, ktorych referent ma byc NIEOBECNY. Zbyt wysoka jasnosc znaczy,
# ze autor przypadkiem osadzil referent i wariant przestal byc soba.
MUSZA_BYC_NIEOSADZONE = ["CprimM", "CprimU"]

# K5: warianty, ktore musza byc czytane jako ZEWNETRZNE wobec rozmowy.
MUSZA_BYC_ZEWNETRZNE = ["CprimComp", "CprimM"]


def _stale_przy_alfa(dobre, alfa):
    return {
        "alfa": alfa,
        "K1_prog_naturalnosci": kwantyl([s["B"]["naturalnosc"] for s in dobre], alfa),
        "K2_dopuszczalny_spadek": {
            w: kwantyl([s["B"]["naturalnosc"] - s[w]["naturalnosc"] for s in dobre],
                       1 - alfa)
            for w in WARIANTY if w != "B"},
        "K3_prog_jasnosci": {
            w: kwantyl([s[w]["jasnosc"] for s in dobre], alfa)
            for w in MUSZA_BYC_OSADZONE},
        "K4_sufit_jasnosci_nieosadzonego": {
            w: kwantyl([s[w]["jasnosc"] for s in dobre], 1 - alfa)
            for w in MUSZA_BYC_NIEOSADZONE},
        "K5_sufit_odczytu_samozwrotnego": {
            w: kwantyl([s[w]["samozwrotnosc"] for s in dobre], 1 - alfa)
            for w in MUSZA_BYC_ZEWNETRZNE},
    }


def stale_z_rozkladu(dobre, budzet=BUDZET):
    """Komplet stalych o LACZNYM odrzuceniu <= budzet na materiale dobrym.

    dobre: lista scenariuszy, kazdy {wariant: {naturalnosc, jasnosc,
           samozwrotnosc}} - srednie panelu, jeden jezyk.
    """
    if not dobre:
        raise ValueError("brak materialu - stalych nie ma z czego wyprowadzic")

    # Od najluzniejszego dopuszczalnego ogona w dol. Pierwsze alfa, przy ktorym
    # odrzucenie laczne miesci sie w budzecie, jest najostrzejszym mozliwym
    # zestawem stalych - a wiec najbardziej czulym na uszkodzenia.
    krok = budzet / 200
    alfa = budzet
    while alfa > 1e-6:
        stale = _stale_przy_alfa(dobre, alfa)
        if rachunek_osiagalnosci(dobre, stale) <= budzet:
            stale["tryb"] = "kwantylowy"
            return stale
        alfa -= krok

    # TRYB OBWIEDNI. Zadne dodatnie alfa nie miesci sie w budzecie, bo trzynascie
    # kryteriow przy n scenariuszach wymaga ogona ~budzet/13 na kryterium, a
    # rozdzielczosc probki wynosi 1/n. Przy n=48 potrzeba ~0,8%, dostepne 2,1%.
    # Progi ladują wtedy na skrajnych obserwacjach: bramka przestaje byc sitem
    # percentylowym, a staje sie detektorem materialu GORSZEGO NIZ COKOLWIEK,
    # co uznano za dobre. To jest uczciwa granica tej probki, nie usterka -
    # ale trzeba ja raportowac, bo zmienia sens bramki.
    stale = _stale_przy_alfa(dobre, 0.0)
    stale["tryb"] = "obwiednia"
    stale["potrzebne_n"] = int(len(WARIANTY) * 2.2 / budzet)
    return stale


def ocen_scenariusz(sredni, stale):
    """Zwraca liste niespelnionych kryteriow. Pusta lista = scenariusz przechodzi."""
    braki = []

    # K1 - kotwica: wariant neutralny nie ma obciazenia konstrukcyjnego,
    # wiec jego slaby wynik znaczy po prostu zle napisany scenariusz
    if sredni["B"]["naturalnosc"] < stale["K1_prog_naturalnosci"]:
        braki.append(
            f"K1: wariant neutralny {sredni['B']['naturalnosc']:.2f} "
            f"< prog {stale['K1_prog_naturalnosci']:.2f} - scenariusz zle napisany")

    # K2 - spadek wobec kotwicy TEGO SAMEGO scenariusza; porownanie wewnatrz
    # scenariusza usuwa wplyw tematu, autora i trudnosci rzemiosla
    for w, dop in stale["K2_dopuszczalny_spadek"].items():
        spadek = sredni["B"]["naturalnosc"] - sredni[w]["naturalnosc"]
        if spadek > dop:
            braki.append(f"K2/{w}: spadek {spadek:.2f} > dopuszczalny {dop:.2f}")

    # K3 - osadzenie tam, gdzie jest wymagane
    for w, prog in stale["K3_prog_jasnosci"].items():
        if sredni[w]["jasnosc"] < prog:
            braki.append(f"K3/{w}: jasnosc {sredni[w]['jasnosc']:.2f} < prog {prog:.2f}")

    # K4 - wada odwrotna: referent, ktory mial byc NIEOBECNY, nie moze byc zbyt jasny
    for w, sufit in stale["K4_sufit_jasnosci_nieosadzonego"].items():
        if sredni[w]["jasnosc"] > sufit:
            braki.append(
                f"K4/{w}: jasnosc {sredni[w]['jasnosc']:.2f} > sufit {sufit:.2f} "
                f"- autor przypadkiem OSADZIL referent, ktory mial byc nieobecny")

    # K5 - pulapka samozwrotna, pytana wprost; skala jasnosci jej NIE wykrywa
    for w, sufit in stale["K5_sufit_odczytu_samozwrotnego"].items():
        if sredni[w]["samozwrotnosc"] > sufit:
            braki.append(f"K5/{w}: odczyt samozwrotny "
                         f"{sredni[w]['samozwrotnosc']:.2f} > sufit {sufit:.2f}")

    return braki


def rachunek_osiagalnosci(dobre, stale):
    """K6: udzial materialu DOBREGO, ktory te stale odrzucaja - LACZNIE."""
    if not dobre:
        return 0.0
    return sum(1 for s in dobre if ocen_scenariusz(s, stale)) / len(dobre)
