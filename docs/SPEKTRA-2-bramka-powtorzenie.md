# Bramka naturalności — powtórzenie po poprawce korpusu

**Data:** 2026-08-03
**Materiał:** te same 12 scenariuszy na język co w pierwszym przebiegu
**Panel:** 9 oceniających, 3 skale, ocena ślepa
**Jedyna różnica wobec pierwszego przebiegu:** fraza wariantu samozwrotnego
(23 z 24 zdań) plus jedna poprawka długości w `external_ungrounded`
**Kod:** `python -m gates.naturalnosc.progi_s2 --sufiks b --porownaj-z ""`

---

## 1. Poprawka zadziałała

| | PL | EN |
|---|---|---|
| naturalność C | 2,87 → **5,56** (+2,69) | 3,15 → **5,54** (+2,39) |
| jasność C | 2,64 → **6,67** (+4,03) | 2,77 → **6,67** (+3,90) |
| odczyt samozwrotny C | 5,70 → **7,00** (+1,30) | 5,67 → **7,00** (+1,33) |

**Odczyt samozwrotny 7,00 to maksimum skali osiągnięte przez wszystkie 24
zdania, u wszystkich dziewięciu oceniających.** Wariant samozwrotny jest teraz
bezdyskusyjnie samozwrotny — poprzednio wypadał 3,9 w sondzie parowanej
i 5,6 w izolacji, czyli jego kategoria zależała od zestawienia.

**Rozstęp naturalności między wariantami: 2,83 → 1,11 (PL), 2,53 → 1,07 (EN).**
Wariant samozwrotny przestał odstawać — leży teraz w górnej części profilu,
obok kotwicy i wariantu zewnętrznego osadzonego.

---

## 2. Rzecz, której nie zamawiałem: cały panel się przesunął

Nic poza wariantem samozwrotnym nie zmieniło się w materiale. Mimo to
**wszystkie pozostałe warianty spadły** — i to tym mocniej, im mniej
osadzony jest ich referent:

| wariant | Δ naturalność PL | Δ naturalność EN | Δ odczyt samozwrotny PL |
|---|---:|---:|---:|
| B — neutralny | −0,19 | −0,25 | **+0,70** |
| C′-G — zewnętrzny osadzony | −0,05 | −0,13 | +0,43 |
| C′-comp — obliczeniowy | −0,29 | −0,14 | +0,19 |
| C′-M — zwyczajny | −0,44 | −0,56 | +0,07 |
| C′-U — nieosadzony | **−0,74** | **−0,92** | −0,03 |

To jest **efekt kontrastu**, nie zmiana materiału. Kiedy wariant samozwrotny
stał się wyrazisty, oceniający przekalibrowali skalę: reszta wypada gorzej na
osadzeniu, a warianty najbliższe rozmowie zyskały na odczycie samozwrotnym.

Ten sam mechanizm złapałem wcześniej w sondzie parowanej — ta sama fraza
dostała 5,57 w izolacji i 3,92 obok wyrazistszej alternatywy. Teraz widać go
na poziomie całego panelu.

> **Wniosek twardy: bezwzględne wartości panelu NIE są porównywalne między
> zestawami bodźców. Porównywać wolno tylko w obrębie jednego przebiegu.**

To unieważnia pomysł zamrożenia progów z jednego przebiegu i stosowania ich
do materiału ocenianego w innym. Progi muszą powstawać z **tego samego
przebiegu**, w którym się je stosuje — a to wraca do warunku niekolistości
i wymaga puli kalibracyjnej ocenianej razem z materiałem badanym.

---

## 3. Druga rzecz: skala naturalności straciła moc rozdzielczą

Zgodność panelu na naturalności spadła z **r = 0,84 do r = 0,46**.

To nie jest pogorszenie ocen — to skutek tego, że **prawdziwa wariancja się
skurczyła**. Gdy wszystkie warianty leżą między 4,5 a 5,7, korelacja par musi
spaść. Naturalność przestała różnicować ten materiał; rozdzielają go teraz
**jasność odniesienia** (r = 0,95) i **odczyt samozwrotny** (r = 0,97).

Praktycznie: kryteria K1 i K2 pracują na skali, która na poprawionym korpusie
prawie nie odróżnia wariantów. Ciężar bramki przeniósł się na K3, K4 i K5.

---

## 4. Koszt, który przyjąłem świadomie

Fraza „tę naszą rozmowę" została wybrana **dlatego, że mieściła się w równaniu
tokenów** — 3 naruszenia wobec 38 dla „tego toku pytań". Sonda mierzyła jednak
„tok pytań", nie „naszą rozmowę". Rachunek dopasowania obecności do partnera
obliczeniowego wypada teraz tak:

| | jasność C | jasność C′-comp | niedopasowanie |
|---|---:|---:|---:|
| PL, przed poprawką | 2,64 | 4,23 | 1,59 |
| **PL, po poprawce** | 6,67 | 4,29 | **2,38** |
| EN, przed poprawką | 2,77 | 5,01 | 2,24 |
| **EN, po poprawce** | 6,67 | 4,90 | **1,77** |

**Po polsku para główna jest gorzej dopasowana niż przed poprawką.**
Znak niedopasowania odwrócił się dokładnie tak, jak zapowiadałem w sondzie:
z referenta zbyt mglistego zrobił się zbyt oczywisty.

Kierunek naprawy jest jednoznaczny i **nie prowadzi przez wariant samozwrotny**:
trzeba podnieść obecność **wariantu obliczeniowego**, czyli mocniej osadzić
urządzenie w rozmowie. Jego jasność (4,29 PL) leży wyraźnie poniżej wariantu
zewnętrznego osadzonego (6,30), mimo że oba mają referent obecny.

---

## 5. Nowy najsłabszy wariant — i dlaczego to nie jest wada

Najniżej leży teraz **C′-U (nieosadzony)**: 4,55 (PL) i 4,47 (EN), czyli
0,88–0,92 poniżej kotwicy.

To jest **własność konstrukcyjna, nie usterka**: referent nieosadzony ma
z definicji nie mieć zaczepienia w rozmowie, więc zdanie czyta się gorzej.
Dokładnie po to K2 ma osobny dopuszczalny spadek dla każdego rodzaju wariantu.

---

## 6. Progi — nadal nie do zamrożenia

Tryb **obwiedni** przy n = 12; sito percentylowe wymaga n ≥ 132 na język.
Po wyrównaniu wariantów stałe zrobiły się **nożowe**: dopuszczalny spadek
wariantu samozwrotnego wynosi 0,22 (PL) i **0,00** (EN) — czyli każdy
scenariusz, w którym C wypada choć minimalnie poniżej kotwicy, zostałby
odrzucony.

To artefakt trybu obwiedni przy małym n, nie sensowne kryterium.
**Progów z tego przebiegu nie zamrażam.**

---

## 7. Co z tego wynika dla planu

1. **Poprawka korpusu jest zamknięta i udana** — wariant samozwrotny działa.
2. **Wariant obliczeniowy wymaga wzmocnienia** — to teraz najsłabsze ogniwo
   pary głównej, i to po polsku bardziej niż po angielsku.
3. **Progi wymagają n ≥ 132 na język**, a przy 96 scenariuszach korpusu
   oznacza to albo więcej scenariuszy, albo więcej insercji na scenariusz
   w próbce kalibracyjnej.
4. **Ocena ludzka na 20% jest teraz ważniejsza niż była** — efekt kontrastu
   pokazał, że panel modelowy przesuwa całą skalę w reakcji na zmianę jednego
   warunku. Bez człowieka nie wiadomo, czy to własność ocenianego języka,
   czy własność oceniającego.
