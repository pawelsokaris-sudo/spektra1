# Wariant obliczeniowy — diagnoza

**Data:** 2026-08-03
**Materiał:** 24 scenariusze × 2 warianty, **pełny kontekst** (to, co widzi model)
**Panel:** 9 oceniających, parowanie w obrębie scenariusza, permutacja dokładna
**Kod:** `gates/naturalnosc/sonda_comp.py`, `sonda_comp_wynik.py`

---

## 1. Hipoteza, którą sprawdzałem — i która padła

Powtórzenie bramki dało wariantowi obliczeniowemu jasność 4,29 (PL) wobec 6,30
dla zewnętrznego osadzonego. Sprawdziłem, gdzie pada jego referent:

| gdzie referent | osadzony | obliczeniowy |
|---|---:|---:|
| w oknie 4 zdań pokazywanym oceniającym | 6,76 | 6,50 |
| poza oknem | 5,25 | 3,64 |

Referent obliczeniowy pada przed wstawką **we wszystkich 24 scenariuszach** —
nie brakuje go nigdy. Wyglądało to więc na artefakt procedury: oceniający
widział cztery zdania, model widzi cały dialog.

**Hipoteza: pokażmy oceniającym to, co widzi model, a różnica zniknie.**

## 2. Nie zniknęła — powiększyła się

| | okno 4 zdań | pełny kontekst | zmiana |
|---|---:|---:|---:|
| PL osadzony | 6,30 | 5,54 | −0,76 (p = 0,08) |
| PL **obliczeniowy** | 4,29 | **3,44** | **−0,85** (p = 0,012) |
| EN osadzony | 5,71 | 5,52 | −0,19 (n.s.) |
| EN **obliczeniowy** | 4,90 | **3,23** | **−1,67** (p = 0,011) |

**Luka przy pełnym kontekście: +2,10 (PL) i +2,29 (EN), p = 0,0005** — czyli
minimum osiągalne przy dwunastu parach. Wszystkie pary w obu językach w tę
samą stronę.

Pełny kontekst **pogorszył** wariant obliczeniowy, zamiast go uratować.

---

## 3. Właściwa przyczyna — podana zgodnie przez oceniających

Siedmiu z dziewięciu, niezależnie od siebie, opisało ten sam mechanizm.
Cytat reprezentatywny:

> „Przyrząd jest zawsze wskazywalny jako obiekt, więc referent istnieje —
> ale orzeczenie ramy («ta sama kolejność kroków», «drobny błąd na początku
> ciągnie się przez całą robotę») do miernika nie przystaje, więc *o czym*
> zdanie mówi robi się mgliste."

**Ramy SPEKTRY-2 orzekają o przebiegu:** „kolejność kroków", „pierwszy krok
decyduje o reszcie", „widać dopiero po czasie", „jedna część przejmuje pracę
za pozostałe". **Przyrząd pomiarowy nie ma etapów.** Porównanie nie ma się
do czego przyczepić.

Dlatego pełny kontekst pogorszył sprawę: przy urywku oceniający mógł jeszcze
przypisać niską jasność brakowi antecedensu i dać kredyt zaufania. Widząc
całą rozmowę widzi, że przyrząd **jest** wprowadzony i mimo to porównanie
nie działa — więc ocenia niżej.

> **Krótkie okno mieszało dwie przyczyny niskiej jasności. Pełny kontekst
> je rozdzielił — i to jest właściwy wynik tej sondy, nawet jeśli hipoteza
> padła.**

---

## 4. Co to znaczy dla pary głównej

Specyfikacja §1 wymaga, by `self` ↔ `external_computational` różniły się
**wyłącznie tym, na co wskazują**. Po przepisaniu wariantu samozwrotnego
`self` = „ta nasza rozmowa" — czyli **proces mający przebieg**.
`external_computational` = przyrząd — czyli **rzecz bez przebiegu**.

Para główna różni się więc nie tylko kierunkiem odniesienia, ale
**rodzajem ontologicznym referenta**. To jest dokładnie ten błąd, dla którego
naprawy dodano szósty wariant — tyle że na innym wymiarze niż obecność.

---

## 5. Propozycja naprawy

**Zamienić referent obliczeniowy z PRZYRZĄDU na PROCES, który ten przyrząd
wykonuje.** Nie „ten miernik ciągu", tylko „ten pomiar ciągu"; nie „this hive
scale", tylko „this weighing routine".

| Za | Przeciw |
|---|---|
| równa rodzaj ontologiczny z wariantem samozwrotnym („ta nasza rozmowa" też jest procesem) | 480 wstawek do przepisania, każda osobno — to praca autorska, nie podmiana mechaniczna |
| ramy zaczynają orzekać sensownie o obu członach pary | trzeba przeliczyć równanie tokenów ±2% i ±10% znaków |
| baza dialogu **nie wymaga zmian** — proces jest implikowany przez urządzenie, które już tam jest | referent procesowy grozi pułapką samozwrotną (spec §3): „to przetwarzanie" wpadło dokładnie w nią |
| poprawka mierzalna tym samym panelem i tą samą sondą | po zmianie trzeba powtórzyć bramkę po raz trzeci |

**Pułapka samozwrotna jest tu realnym ryzykiem** i wymaga uwagi: referent
procesowy w rozmowie łatwo czyta się jako „to, co teraz robimy". Zabezpieczenie
istnieje w specyfikacji — proces musi być jawnie zakotwiczony w urządzeniu
(„ten pomiar z czujnika"), nie sam w sobie. Walidator ma już kontrolę
`check_mundane` na tę pułapkę; trzeba ją rozszerzyć na wariant obliczeniowy.

---

## 6. Czego NIE robię i dlaczego

**Nie przepisuję korpusu bez decyzji.** To 480 wstawek pisanych ręcznie,
dotykających wariantu wchodzącego do hipotezy głównej, i wymagających
trzeciego przebiegu bramki. Zakres wykracza poza „wzmocnij wariant",
a diagnoza zmieniła się w trakcie: pytanie brzmiało „czy jest za słabo
osadzony" (nie jest), a odpowiedź brzmi „jest niewłaściwego rodzaju".

**Nie zmieniam ram.** Ramy są wspólne dla wszystkich sześciu wariantów
i działają dla pięciu z nich. Przerabianie ich pod jeden wariant zepsułoby
pozostałe.

---

## 7. Efekt uboczny wart odnotowania

Pełny kontekst **podniósł odczyt samozwrotny** wszystkich wariantów
(PL +0,4 do +1,0 wg oceniających). Powód: widząc całą rozmowę doradczą,
czytelnik widzi realną sekwencję udzielonych rad, więc „kolejność kroków"
daje się odczytać jako komentarz do **toku samej wymiany**.

To znaczy, że **długość pokazanego kontekstu jest zmienną eksperymentalną
bramki**, nie tłem. Trzeba ją zamrozić w protokole razem z resztą procedury
oceniania — dotąd nie była nigdzie zapisana.
