# SPEKTRA-2 — projekt badania (wersja 3, po dwóch rundach recenzji)

**Status:** projekt do uzgodnienia. Nic tu nie jest zamrożone.
**Poprzednik:** SPEKTRA-1 — hipoteza obalona, efekt odwrotny, wynik niestabilny
między replikami.

## 0. Rozstrzygnięcia recenzji

### Runda 1 (GPT, Grok, Gemini)

| Zmiana | Kto | Decyzja |
|---|---|---|
| **H1 była błędna** — C − C''-M miesza samozwrotność z rejestrem | GPT | **PRZYJĘTE.** H1 = C − C'-U |
| Ramię modelowe nie może bramkować gałęzi głównej | GPT, Grok | **PRZYJĘTE** |
| Ramię modelowe nie mierzy „dotrenowania na polskim" | GPT | **PRZYJĘTE.** Roszczenie zawężone do różnicy między checkpointami |
| H2 z nowym warunkiem musi być dwustronna | GPT | **PRZYJĘTE** |
| Naturalność nie może być tylko opisowa | GPT | **PRZYJĘTE.** Bramka konstrukcyjna przed pieczęcią |
| Referent zwyczajny miesza konkretność z rejestrem | GPT | **PRZYJĘTE.** Balans konkretny/procesowy zamrożony |
| Uzasadnienie ρ mieszało moc z SESOI | Grok | **PRZYJĘTE.** Wniosek ten sam, uzasadnienie poprawione |
| Permutacja etykiety modelu nieuprawniona | GPT | **PRZYJĘTE.** Bootstrap po scenariuszach |
| Wariant A niedopasowany | GPT | **PRZYJĘTE.** Usunięty |
| Obraz kontenera | Gemini | **PRZYJĘTE** |

### Runda 2 (GPT)

| Zmiana | Decyzja |
|---|---|
| MDE ≠ SESOI; podać poziom mocy, dla którego liczono MDE | **PRZYJĘTE** |
| M=64 to kosztowny półśrodek — albo 48, albo ~80 | **PRZYJĘTE co do logiki**, patrz §7 |
| Bramka naturalności potrzebuje progu bezwzględnego, nie tylko względnego | **PRZYJĘTE.** Dwa progi |
| Kalibracja na materiale SPEKTRY-1 z celowo uszkodzonymi wariantami | **PRZYJĘTE** |
| Nadmiarowa pula kandydatów + zamrożona losowa kolejność | **PRZYJĘTE** |
| Moc interakcji podać dla konkretnej wartości w jednostkach I_total | **PRZYJĘTE**, patrz §9 |
| Budżet 1600 wymaga wyjaśnienia mnożnika ×2 | **PRZYJĘTE** — to dwa przebiegi runnera |
| Pełna procedura ocen: 7 ocen/element, ~18 oceniających/język | **PRZYJĘTE CZĘŚCIOWO** — poza zasięgiem, patrz §6 |

### Wada znaleziona po recenzji, przez nikogo niezgłoszona

**Asymetryczne liczności (48 EN / 32 PL) były niespójne.** Uzasadniłem je tym,
że *spodziewany* efekt jest w polskim dwa razy silniejszy — ale SESOI to
najmniejszy efekt **wart wykrycia**, a ten jest taki sam dla obu replik.
Moc jest własnością M i SESOI, nie języka (d_z jest już standaryzowane).
Asymetria oznaczałaby **asymetryczną czułość**, przez co każde porównanie
replik mieszałoby się z różnicą mocy: przy SESOI 0,50 dawało 0,85 dla EN
i **0,65 dla PL**.

**Liczności są teraz symetryczne.**

## 1. Pytanie

Czy samozwrotność robi cokolwiek **ponad odniesienie do zewnętrznego układu
o tym samym rejestrze** — i osobno: ile w efekcie ze SPEKTRY-1 pochodziło
z samego przemieszczenia odniesienia, a ile z rejestru obliczeniowego.

## 2. Warianty (pięć)

Rama zdaniowa wspólna, zmienia się **jedna fraza rzeczownikowa**:

| Wariant | Desygnat | Rejestr | Przykład |
|---|---|---|---|
| **B** neutralny | sam temat scenariusza | dziedzinowy | „ten sam dym" |
| **C'-G** zewnętrzny osadzony | inny obiekt w dziedzinie | dziedzinowy | „ten drugi piec" |
| **C''-M** zewnętrzny zwyczajny | poza dziedziną, nietechniczny | zwyczajny | „tamto czekanie na pociąg" |
| **C'-U** zewnętrzny techniczny | poza dziedziną, techniczny | obliczeniowy | „tamto sterowanie" |
| **C** samozwrotny | rozmowa / przetwarzanie | obliczeniowy | „to przetwarzanie" |

### Dobór C''-M — cztery warunki obowiązkowe

1. **Poza dziedziną scenariusza**, zero wspólnego słownictwa.
2. **Nietechniczny** — kryterium zamrażane osobno przed pieczęcią.
3. **Dopasowany ontologicznie**: połowa scenariuszy z referentem konkretnym,
   połowa z procesowym; proporcja zamrożona. Inaczej C''-M różniłby się od C
   i C'-U także na osi konkretne–abstrakcyjne.
4. **Niemożliwy do odczytania jako samozwrotny.** Referent procesowy łatwo
   wpada w tę pułapkę: „to planowanie" w rozmowie może znaczyć „to, które
   teraz robimy". Musi być jawnie zakotwiczony poza rozmową — „tamto czekanie
   na pociąg", „to coroczne sprzątanie", nie „to planowanie".
   *(Warunek dodany przez nas; żaden recenzent go nie zgłosił.)*

**Jeden referent na scenariusz**, powtarzany we wszystkich insercjach — tak jak
pozostałe warianty. Pięć różnych różnicowałoby wariant także spójnością
odniesienia.

**Wariant A (bez insercji) usunięty:** różni się długością, liczbą zdań
i granic zdaniowych; w SPEKTRZE-1 nie przeszedł kontroli interpunkcyjnej i nie
wchodził do żadnej hipotezy konfirmacyjnej.

## 3. Wymóg wobec ram zdaniowych

Rama musi przyjmować **wszystkie pięć desygnatów równie naturalnie.** Cała
specyfika siedzi w podmienianej frazie. W SPEKTRZE-1 ramy pisano pod referenty
procesowe, przez co zwyczajny desygnat wpadałby w nie nienaturalnie.

## 4. Hipotezy

### Gałąź główna (Gemma, każda replika osobno)

| | Kontrast | Co mierzy | Kierunek |
|---|---|---|---|
| **H1** | C − C'-U | samozwrotność ponad odniesienie zewnętrzne **o tym samym rejestrze** | jednostronny ujemny — replikacja kierunku |
| **H2** | C''-M − C'-G | samo wyjście poza dziedzinę | **dwustronny** — warunek nowy |
| **H3** | C'-U − C''-M | wkład rejestru obliczeniowego | **dwustronny** |

Bramkowanie: H1 → {H2, H3}. H2 i H3 nie bramkują się nawzajem.


### Ograniczenie resztkowe: H2 miesza osadzenie z rejestrem

Trzy warianty zewnętrzne różnią się na **dwóch osiach naraz** — osadzenia
(czy referent był wcześniej w dialogu) i rejestru (dziedzinowy / zwyczajny /
techniczny). Pełne skrzyżowanie dwóch osi wymagałoby **czterech** wariantów
zewnętrznych; mamy trzy.

| Kontrast | Co różni | Czystość |
|---|---|---|
| **H1** C − C'-U | tylko samozwrotność (oba techniczne, oba nieosadzone) | **czysty** |
| **H3** C'-U − C''-M | tylko rejestr (oba nieosadzone) | **czysty** |
| **H2** C''-M − C'-G | osadzenie **oraz** rejestr | **mieszany** |

Świadoma decyzja: H2 jest hipotezą diagnostyczną, a szósty wariant (nieosadzony
o rejestrze dziedzinowym) kosztowałby 20% pomiaru na obu modelach. Zostaje jako
zadeklarowane ograniczenie i jako oczywisty kandydat na rozszerzenie, gdyby H2
okazała się interesująca.

### Gałąź replikacyjna (PLLuM) — osobna, **nie bramkuje głównej**

| | Test | Roszczenie |
|---|---|---|
| **R1** | H1 powtórzone na PLLuM | efekt replikuje się na drugim checkpoincie |
| **R2** | (C − C'-U)_PLLuM − (C − C'-U)_Gemma | **wyłącznie:** siła efektu różni się między checkpointami rodziny Gemma-3-4B |

**R2 nie licencjonuje twierdzenia o dotrenowaniu na polskim** — modele różnią
się także ścieżką dostrajania instrukcyjnego, zbiorem instrukcji i formatem
dialogu.

### Opisowe

C − C''-M, C − C'-G (replikacja SPEKTRY-1), C − B, entropia widmowa, I₋₁,
profil warstwowy, perplexity, oceny naturalności.

## 5. Endpoint

Ī = średnia I_total po zamrożonym paśmie warstw, jeden skalar na tekst,
parowanie wewnątrz scenariusza, permutacja etykiet wariantów.

**Definicja dziedziczona wchodzi do pieczęci jako wersjonowany załącznik**, nie
jako odwołanie do SPEKTRY-1: wzór I_total, metoda ustalania λ*, normalizacja,
pasmo warstw, tokeny specjalne, tokenizer, dopasowanie długości, test
permutacyjny, liczba permutacji, ziarna, obsługa braków.

**Test R2:** model nie jest przypisywany losowo do tekstu, więc permutacja
etykiety modelu jest nieuprawniona. Statystyka: różnica scenariuszowych Δ
między modelami, **bootstrap po scenariuszach**, CI 99%, osobno per replika.

Entropia widmowa i I₋₁ **nie są endpointami**.

## 6. Naturalność — bramka konstrukcyjna, wersja hybrydowa

**Pełna procedura zalecana przez recenzenta (7 ocen na element, ~18 native
speakerów na język) oznacza ponad 3000 ocen na język. To jest zlecenie na
platformie badawczej, kilkaset euro i koordynacja 36 osób — poza zasięgiem
tego projektu.** Zapisujemy to jako świadomy kompromis, nie jako przeoczenie.

### Co robimy

1. **Przesiew modelowy na całości.** Dwa modele **spoza badanej pary** (nigdy
   Gemma ani PLLuM — byłoby koliste). Oceniają ślepo: możliwe odczytanie
   samozwrotne, brak osadzenia referencyjnego, zgrzyt w ramie, odstępstwo
   konkretne–abstrakcyjne.
2. **Ocena ludzka na losowej próbce 20%** — sprawdza, czy oceny modelowe
   w ogóle zgadzają się z ludzkimi. Bez tego przesiew jest niesprawdzalny.
3. **Kalibracja na materiale SPEKTRY-1** (zbiór ofiarny, nie wchodzi do
   SPEKTRY-2), z **celowo uszkodzonymi wariantami**: referent nieosadzony,
   połączenie gramatyczne ale nienaturalne, referent czytelny jako samozwrotny,
   fraza niedopasowana ontologicznie. Jeśli bramka nie odrzuca znanych błędów —
   skala albo instrukcja nie działa.

### Progi — **przeliczone, wersja na medianach ODRZUCONA**

Pierwotna specyfikacja (7 ocen, mediany, rozstęp ≤ 1) **nie przechodzi rachunku
osiągalności**:

| Reguła | Fałszywe odrzucenie dobrego scenariusza | Wykrycie uszkodzenia 1,5 pkt |
|---|---:|---:|
| mediany, n=7, rozstęp ≤1 | **24%** | 73% |
| **średnie, n=9, rozstęp ≤1,0** | **9%** | **96%** |

Powód porażki wersji medianowej jest konstrukcyjny: **mediana nieparzystej
liczby ocen całkowitych jest liczbą całkowitą**, więc rozstęp też. Reguła
„więcej niż 1" znaczy w praktyce „co najmniej 2" — czyli z definicji przepuszcza
uszkodzenie o dokładnie ten rozmiar, który miała łapać (wykrywalność
uszkodzenia 1,0 pkt spada z rosnącym n: 0,49 przy n=7, 0,25 przy n=15).

**Specyfikacja zamrażana:**
- **9 ocen na element**, statystyka: **średnia**, nie mediana;
- średnia naturalności **każdego** wariantu ≥ 5,0 / 7;
- średnia jasności referenta **każdego** wariantu ≥ 5,0 / 7;
- **rozstęp średnich naturalności między wariantami ≤ 1,0 punktu**;
- żaden referent zwyczajny nie daje się rozsądnie odczytać jako odniesienie
  do rozmowy albo do czynności właśnie wykonywanej.

Charakterystyka reguły przy założeniu SD ocen = 1,0 i prawdziwej średniej 6,0:
fałszywe odrzucenie **9%**, wykrycie uszkodzenia 1,0 pkt **70%**,
1,5 pkt **96%**, 2,0 pkt **100%**.

Niezaliczenie → poprawa albo odrzucenie **całego scenariusza**, nie
pojedynczego wariantu. Maksymalnie **dwie** rundy poprawek, ocenia świeży panel.

### Nadmiarowa pula

Przygotować **~20% więcej kandydatów** (58 na język przy celu 48). Losowa
kolejność zamrożona **przed** ocenami; do badania wchodzą pierwsze scenariusze
z tej kolejności, które przejdą bramkę. **Zakaz wybierania „najładniejszych"
spośród zaliczonych.**

### Ograniczenie do zadeklarowania

Oceny modelowe wnoszą własne preferencje stylistyczne i nie zastępują panelu
ludzkiego. Próbka 20% jest sprawdzeniem zgodności, nie pełną walidacją.

## 7. Liczność — **48 na język, symetrycznie**

Moc jest własnością M i SESOI, nie języka.

| SESOI d_z | M=32 | M=40 | **M=48** | M=56 |
|---:|---:|---:|---:|---:|
| 0,70 | 0,93 | 0,97 | **0,99** | 1,00 |
| 0,60 | 0,81 | 0,91 | **0,96** | 0,98 |
| **0,55** | 0,74 | 0,85 | **0,91** | 0,95 |
| 0,50 | 0,65 | 0,76 | **0,85** | 0,90 |
| 0,40 | 0,42 | 0,54 | **0,65** | 0,71 |

**SESOI = d_z 0,55** (≈ 0,0013 w jednostkach I_total). Uzasadnienie: poniżej
tego progu efekt mieści się w zakresie, w którym **udokumentowana niestabilność
naszego przyrządu — 37% różnicy amplitud między replikami w SPEKTRZE-1** —
mogłaby go zdominować. To jest argument ze **zmierzonej właściwości przyrządu**,
nie z konwencji ani z tego, co akurat umiemy wykryć.

**M = 48 na język, 96 scenariuszy.** Moc 0,91 przy SESOI; 0,92 przy efekcie
zdyskontowanym o 25% wobec SPEKTRY-1 (d_z 0,56).

**MDE = 0,00127 (EN) i 0,00155 (PL) przy mocy 0,90** — raportowane jako
własność projektu, **nie jako definicja istotności naukowej.**

Zamrożone: **liczności nie zwiększa się po poznaniu wyników.**

## 8. Modele

| Ramię | Model | Rola |
|---|---|---|
| główne | `google/gemma-3-4b-it` | H1, H2, H3 |
| replikacyjne | `CYFRAGOVPL/PLLuM-4B-instruct-2512` | R1, R2 |

**Zweryfikowane empirycznie:** architektura tożsama (34 bloki, hidden 2560);
tokenizacja korpusu SPEKTRY-1 identyczna co do tokena (240/240); narzut
szablonu stały w scenariuszu ±1 token; słownik PLLuM = słownik Gemmy plus
`[INST]` i `[/INST]`.

**Różni się format dialogu.** Sprawdzić przed pieczęcią, czy różnica narzutu
przesuwa pozycje insercji w oknie T′ jednakowo we wszystkich wariantach.

## 9. Budżet obliczeniowy

| Pozycja | Liczba | Uwaga |
|---|---:|---|
| scenariusze | 96 | 48 EN + 48 PL |
| teksty (5 wariantów) | 480 | bez nulli, bez wariantu A |
| forwardy **na model** | 960 | **480 × 2 przebiegi runnera** — przebieg 1 liczy okno i komponent pozycyjny, przebieg 2 widma i metryki |
| forwardy razem | **1920** | dwa modele |
| czas karty | **~18 h** | przy 34 s/forward, tempo SPEKTRY-1 |
| progi λ* | **2688** | 1344 na model (96 × 14 warstw) |
| czas procesora | **~4 doby** | w tle; **najdłuższy odcinek całości** |

Mnożnik ×2 przy forwardach to dwa przebiegi runnera, nie replikacja.

**Moc R2 dla konkretnej alternatywy** (nie dla słowa „zrównanie"): jeśli PLLuM
da Δ = 0 przy Gemmie na poziomie historycznym, interakcja wynosi **0,00175
(EN)** i **0,00314 (PL)** w jednostkach I_total. Przy M = 48 i ρ = 0,3 moc
przekracza 0,94 w obu replikach.

## 10. Do policzenia przed pieczęcią — pozostałe

1. ✅ Moc H1 — policzona (§7).
2. ✅ Moc R2 z krzywą ρ — policzona.
3. ✅ MDE — policzone, z podanym poziomem mocy.
4. ✅ Brak testu równoważności — nie zamrażamy żadnego.
5. ✅ **Bramka manipulacji PLLuM** — specyfikacja niżej.
6. ⬜ Weryfikacja warstw PLLuM hookami — **zlecenie DEP-09**.
7. ⬜ Bramka pamięci PLLuM na 16 GB — **zlecenie DEP-09**.
8. ✅ Budżet — policzony (§9).
9. ✅ **Progi naturalności — przeliczone i ZMIENIONE** (§6): wersja medianowa
   odrzuca 24% dobrych scenariuszy i nie wykrywa uszkodzenia, dla którego
   powstała. Zastąpiona wersją na średnich z 9 ocenami.

### Bramka manipulacji PLLuM — specyfikacja

**Konstrukcja:** manipulacja ma być **specyficzna dla polskiego**, nie ogólna.
Sam spadek perplexity nic nie mówi — dwa modele różnią się całą ścieżką
dostrajania. Pytanie brzmi, czy PLLuM zyskuje **po polsku bardziej niż po
angielsku**.

**Statystyka:** dla każdego scenariusza poprawa log-perplexity PLLuM wobec
Gemmy, liczona na wariantach neutralnych. Porównanie dwóch prób (48 scenariuszy
polskich wobec 48 angielskich — repliki są rozłączne), jednostronnie, α = 0,01.

**Moc, policzona:**

| Efekt (w SD) | n=24 | n=32 | **n=48** | n=64 |
|---:|---:|---:|---:|---:|
| 0,50 | 0,26 | 0,37 | 0,54 | 0,67 |
| 0,60 | 0,38 | 0,51 | 0,72 | 0,85 |
| 0,80 | 0,64 | 0,79 | **0,93** | 0,98 |

**MDE przy n = 48 i mocy 0,90: d = 0,75 odchylenia standardowego.**

**Interpretacja i świadoma decyzja:** bramka jest **konserwatywna** — zażąda
wyraźnej, specyficznej dla polskiego poprawy. Manipulacja umiarkowana
(d ≈ 0,5) przejdzie tylko w 54% przypadków. Zostawiamy to tak celowo:
**fałszywe zaliczenie bramki jest gorsze niż fałszywe niezaliczenie**, bo
pierwsze pozwala twierdzić coś o interakcji przy manipulacji, której nie ma.
Niezaliczenie tylko zawęża roszczenie do R1.

**Próg bezwzględny w jednostkach log-PPL wymaga zmierzenia rozrzutu** — ale
kryterium jest zamrożone **w jednostkach standaryzowanych już teraz**, więc
zmierzenie rozrzutu nie jest decyzją po wyniku.

## 11. Rejestracja

Niezależny datownik **przed pierwszym forwardem obu modeli na korpusie.**
Pakiet: hash korpusu, kodu, konfiguracji, sumy wag obu modeli, wersje
tokenizerów, **obraz kontenera** (brak w SPEKTRZE-1), lockfile, log czasu
pierwszego forwardu.

**Zakaz uruchamiania czegokolwiek — łącznie z testami sanity — na
zapieczętowanym korpusie przed datownikiem.** Sanity wyłącznie na sztucznym
zestawie.

## 12. Czego nie będziemy twierdzić

- Że mierzymy świadomość albo odczuwanie.
- Że R2 dowodzi wpływu dotrenowania na polskim.
- Że confound abstrakcyjne–konkretne jest usunięty — jest **zbalansowany
  i zmierzony**.
- Że bramka naturalności ma moc pełnego panelu ludzkiego.
- Że jeden model i jedna rodzina scenariuszy pozwalają na generalizację.
