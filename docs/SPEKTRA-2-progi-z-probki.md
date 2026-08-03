# Progi bramki naturalności z próbki korpusu SPEKTRY-2

**Data:** 2026-08-03
**Materiał:** 12 scenariuszy na język × 6 wariantów = 144 elementy
**Panel:** 9 oceniających, 3 skale, ocena ślepa, losowa kolejność per oceniający
**Kod:** `gates/naturalnosc/probka_spektra2.py`, `gates/naturalnosc/progi_s2.py`

---

## 1. Warunek niekolistości — 24 scenariusze wypadają z badania

Progi policzone na materiale, który potem przesiewają, wykryłyby wyłącznie
scenariusze odstające — nigdy systematycznie słabego korpusu, bo słaby korpus
sam ustawiłby sobie niski próg. Dlatego próbka kalibracyjna jest **wyłączona
z badania**.

| Język | Wyłączone |
|---|---|
| PL | pl-05, pl-10, pl-12, pl-16, pl-18, pl-20, pl-22, pl-23, pl-24, pl-34, pl-41, pl-43 |
| EN | en-03, en-04, en-05, en-08, en-15, en-26, en-28, en-30, en-35, en-41, en-43, en-47 |

**Zostaje 36 na język, moc wymaga 48 → do dopisania 12 + 12.**

---

## 2. Wspólna rama zadziałała

| Wariant | naturalność PL | jasność PL | samozwrotny PL | naturalność EN |
|---|---:|---:|---:|---:|
| B — neutralny | 5,62 | 6,34 | 1,19 | 5,64 |
| **C — samozwrotny** | **2,87** | 2,64 | **5,70** | **3,15** |
| C′-G — zewnętrzny osadzony | 5,70 | 6,28 | 1,03 | 5,68 |
| C′-comp — obliczeniowy | 5,53 | 4,23 | 1,00 | 5,55 |
| C′-M — zwyczajny | 5,37 | 2,69 | 1,07 | 5,35 |
| C′-U — nieosadzony | 5,29 | 2,01 | 1,03 | 5,32 |

**Rozstęp naturalności bez wariantu C: 0,42 (PL) i 0,36 (EN).** Pięć wariantów
mieści się w pół punktu — wymóg wspólnej ramy ze specyfikacji autorskiej
działa dokładnie tak, jak miał.

Cały rozstęp bierze się z **jednego** wariantu: **85% (PL) i 92% (EN)**.

---

## 3. Znalezisko, które musi trafić do decyzji przed pieczęcią

**Wariant samozwrotny jest o 2,7 punktu mniej naturalny od pozostałych —
i przyczyną jest jedna fraza.**

| Fraza referenta w wariancie C | n | średnia naturalność |
|---|---:|---:|
| „to przetwarzanie" / „this processing" | 22 | **2,76** |
| „ten tok pytań", „this conversation" | 2 | **5,72** |

Dwa scenariusze użyły innej frazy samozwrotnej i wypadły **na poziomie
pozostałych wariantów** — przy zachowanym odczycie samozwrotnym 7/7.
Czyli: niska naturalność wariantu C **nie jest nieuchronną własnością
samoodniesienia**, tylko własnością konkretnego słowa.

### Dlaczego to jest groźne

**H1 = C − C′-comp.** Jeśli wariant C jest systematycznie mniej naturalny,
zmierzona różnica może pochodzić z płynności, a nie z samoodniesienia.
Wszystkich dziewięciu oceniających wskazało tę frazę niezależnie; po polsku
ostrzej niż po angielsku („to przetwarzanie" brzmi komputerowo w rozmowie
o kiszeniu ogórków).

### Decyzja do podjęcia

| Wariant | Za | Przeciw |
|---|---|---|
| **A. Przepisać frazę samozwrotną** na idiomatyczną | usuwa domieszkę płynności z H1; korpus pokazuje, że to wykonalne | zrywa ciągłość ze SPEKTRĄ-1, gdzie ramię replikacyjne (C − C′-G) używa „to przetwarzanie" |
| **B. Zostawić i zadeklarować** domieszkę, kontrolując perplexity | ciągłość ze SPEKTRĄ-1 zachowana | H1 pozostaje obciążone, a to hipoteza główna |

**Rekomendacja: A**, ale z zachowaniem starej frazy jako wariantu opisowego,
żeby ciągłość ze SPEKTRĄ-1 dała się policzyć osobno.

---

## 4. Trzecia skala się broni

Skala odczytu samozwrotnego rozdziela **czysto**: wariant C ma 5,70 (PL)
i 5,67 (EN), wszystkie pozostałe 1,00–1,19. Zgodność panelu r = 0,98.

To potwierdza sens K5: skala jasności odniesienia tej różnicy nie widziała
(w kalibracji SPEKTRY-1 wykryła 0 z 6 uszkodzeń samozwrotnych).

---

## 5. Poprawka w kryteriach — mój błąd, wykryty przez pomiar

K3 wymagało osadzenia referenta od **czterech** wariantów, w tym C′-M.
Pomiar: jasność C′-M = 2,69 (PL) i 2,69 (EN), praktycznie tyle co C′-U (2,01).

To nie jest wada wariantu zwyczajnego. **Wariant zwyczajny odsyła do
przedmiotu codziennego spoza rozmowy** — jego referent jest nieobecny
dokładnie tak samo jak referent nieosadzonego, co widać w regule określnika
(„tamten", nie „ten"). Różnią się **rodzajem** referenta, nie osadzeniem —
i to właśnie mierzy H3.

Poprawione: K3 obejmuje B, C′-G, C′-comp; K4 (sufit) obejmuje C′-M i C′-U.

---

## 6. Progi

Tryb: **obwiednia** — przy 12 scenariuszach żaden dodatni ogon nie mieści się
w budżecie 10%. Sito percentylowe wymaga **n ≥ 132 na język**.

| Stała | PL | EN |
|---|---:|---:|
| K1 próg naturalności (kotwica B) | 4,44 | 4,89 |
| K2 dopuszczalny spadek C′-G | 0,22 | 0,44 |
| K2 dopuszczalny spadek C′-comp | 0,33 | 0,44 |
| K2 dopuszczalny spadek C′-M | 0,44 | 0,56 |
| K2 dopuszczalny spadek C′-U | 1,22 | 0,56 |
| K2 dopuszczalny spadek C | 3,56 | 3,22 |
| K3 próg jasności B | 5,00 | 5,44 |
| K3 próg jasności C′-G | 3,67 | 3,67 |
| K3 próg jasności C′-comp | 2,44 | 3,11 |
| K4 sufit jasności C′-M | 3,00 | 2,33 |
| K4 sufit jasności C′-U | 2,11 | 2,00 |
| K5 sufit odczytu samozwrotnego C′-comp | 1,00 | 1,00 |
| K5 sufit odczytu samozwrotnego C′-M | 1,11 | 1,11 |

**Dopuszczalny spadek 3,56 dla wariantu C jest miarą problemu z §3, nie
własnością konstrukcji.** Po przepisaniu frazy samozwrotnej ta stała powinna
spaść do rzędu pozostałych. Jeśli nie spadnie — znaczy, że samoodniesienie
rzeczywiście kosztuje naturalność, i to samo w sobie jest wynikiem.

**K6 — sprawdzenie osiągalności:** próg ze SPEKTRY-1 (3,22 PL / 3,78 EN)
odrzuciłby 0 z 12 kotwic w obu językach. Progi z materiału o luźniejszej
konstrukcji są więc **za niskie**, zgodnie z przewidywaniem.

---

## 7. Znaleziska redakcyjne w korpusie

**Pleonazm w ramie: „kolejność kolejnych / kolejno wykonywanych kroków".**
36 wstawek w 6 scenariuszach (pl-01, pl-02, pl-08, pl-11, pl-20, pl-22).
Ośmiu oceniających zgłosiło to niezależnie jako stałe obniżenie naturalności
o ~1 punkt.

Rzecz działa tak samo jak literówka „staraność" z rundy redakcyjnej:
**błąd wszedł razem z ramą i mnoży się przez liczbę jej użyć razy sześć
wariantów.** Ponieważ jest identyczny we wszystkich sześciu, **kontrastu nie
obciąża** — obniża tylko sufit.

Drugie: **porównania okrężne** — „To trochę przypomina to runo" w rozmowie
o czesaniu runa. Referent jest maksymalnie jasny, ale porównanie puste.
Żadna z trzech skal tego nie mierzy; zgłosili to oceniający 5, 8 i 9.

---

## 8. Panel — to samo ograniczenie co poprzednio

| Skala | korelacja par | SD elementu |
|---|---:|---:|
| naturalność | 0,84 | 0,51 |
| jasność odniesienia | 0,94 | 0,41 |
| odczyt samozwrotny | 0,98 | 0,20 |

Dziewięciu oceniających to dziewięć wywołań tego samego modelu. Zgoda dowodzi
**podobieństwa, nie trafności**. Ocena ludzka na 20% pozostaje nierozwiązana
i jest najsłabszym ogniwem bramki.

Wszyscy oceniający zgłosili też, że **rozdzielenie naturalności od dopasowania
tematycznego** było najtrudniejszą decyzją — i że rozstrzygali je zgodnie
z instrukcją, przenosząc karę na skalę jasności. Inny panel mógłby rozłożyć
to inaczej, co przesunęłoby progi K1 i K3 w przeciwnych kierunkach.
