# SPEKTRA-2 — projekt badania (wersja 2, po recenzji trzech modeli)

**Status:** projekt do uzgodnienia. Nic tu nie jest zamrożone.
**Poprzednik:** SPEKTRA-1 — hipoteza obalona, efekt odwrotny, wynik niestabilny
między replikami.

## 0. Co zmieniła recenzja (rozstrzygnięcia)

| Zmiana | Kto wskazał | Decyzja |
|---|---|---|
| **H1 była błędna** — C − C''-M miesza samozwrotność z rejestrem | GPT | **PRZYJĘTE.** H1 = C − C'-U (rejestr dopasowany) |
| H3 nie może bramkować H1/H2 | GPT, Grok | **PRZYJĘTE.** Ramię modelowe jest osobną gałęzią |
| H3 nie mierzy „dotrenowania na polskim" — modele różnią się całą ścieżką dostrajania | GPT | **PRZYJĘTE.** Roszczenie: moderacja przez wariant modelu w rodzinie |
| H2 z nowym wariantem musi być dwustronna | GPT | **PRZYJĘTE** |
| Naturalność nie może być tylko opisowa | GPT | **PRZYJĘTE.** Ślepa ocena przed pieczęcią, reguła konstrukcyjna |
| Referent zwyczajny miesza konkretność z rejestrem | GPT | **PRZYJĘTE z poprawką** (patrz §2) |
| Uzasadnienie ρ mieszało moc z SESOI | Grok | **PRZYJĘTE.** Wniosek ten sam, uzasadnienie poprawione |
| Test interakcji wymaga definicji; permutacja etykiety modelu nieuprawniona | GPT | **PRZYJĘTE.** Bootstrap po scenariuszach |
| Wariant A nie jest dopasowany | GPT | **PRZYJĘTE.** A usunięty z SPEKTRY-2 |
| Endpoint dziedziczony musi być załącznikiem, nie odwołaniem | GPT | **PRZYJĘTE** |
| Obraz kontenera musi powstać | Gemini | **PRZYJĘTE** |

**Błąd własny do odnotowania:** dwa dni przed napisaniem wersji 1 sam zauważyłem,
że C'-U jest dopasowany rejestrem do C — i mimo to postawiłem H1 na C''-M.
Nowy wariant miał rozdzielić trzy czynniki, a hipoteza główna z powrotem
skleiła dwa z nich.

**Rozbieżność między recenzentami:** uzasadnienie ρ zostało przez Gemini
entuzjastycznie potwierdzone, a przez Groka obalone. Grok miał rację.

## 1. Pytanie

Czy samozwrotność robi cokolwiek **ponad odniesienie do zewnętrznego układu
o tym samym rejestrze** — i osobno: ile w efekcie ze SPEKTRY-1 pochodziło
z samego przemieszczenia odniesienia, a ile z rejestru obliczeniowego.

## 2. Warianty (pięć — A usunięty)

Rama zdaniowa wspólna, zmienia się **jedna fraza rzeczownikowa**:

| Wariant | Desygnat | Rejestr | Przykład |
|---|---|---|---|
| **B** neutralny | sam temat scenariusza | dziedzinowy | „ten sam dym" |
| **C'-G** zewnętrzny osadzony | inny obiekt w dziedzinie | dziedzinowy | „ten drugi piec" |
| **C''-M** zewnętrzny zwyczajny | **NOWY** — poza dziedziną, nietechniczny | zwyczajny | „tamto czekanie na pociąg" |
| **C'-U** zewnętrzny techniczny | poza dziedziną, techniczny | obliczeniowy | „tamto sterowanie" |
| **C** samozwrotny | rozmowa / przetwarzanie | obliczeniowy | „to przetwarzanie" |

### Dobór C''-M — trzy warunki, wszystkie obowiązkowe

1. **Poza dziedziną scenariusza**, zero wspólnego słownictwa.
2. **Nietechniczny** — kryterium zamrażane osobno przed pieczęcią (lista
   wykluczeń plus ocena ślepa), żeby granica C''-M wobec C'-U nie była miękka.
3. **Dopasowany ontologicznie** do C i C'-U — nie zawsze przedmiot konkretny.
   **Połowa scenariuszy z referentem konkretnym, połowa z procesowym**, proporcja
   zamrożona przed badaniem. Inaczej C''-M różniłby się od C i C'-U także na osi
   konkretne–abstrakcyjne i wymienialibyśmy jeden confound na drugi.

**Ostrzeżenie własne, którego recenzent nie zgłosił:** referent procesowy
i abstrakcyjny łatwo daje się przeczytać jako samozwrotny. „To planowanie"
w rozmowie może znaczyć „to planowanie, które teraz robimy" — i wtedy wariant
kontrolny zaraża się tym, co ma kontrolować. **Referent procesowy musi być
jawnie zakotwiczony poza rozmową**: „tamto czekanie na pociąg", „to coroczne
sprzątanie", nie „to planowanie".

### Reguła powtarzalności

Jeden referent na scenariusz, powtarzany we wszystkich insercjach — tak jak
pozostałe warianty. Pięć różnych referentów różnicowałoby wariant także
spójnością odniesienia, czyli ukrytym confoundem.

### Dlaczego A wypadł

A nie ma insercji, więc różni się od pozostałych długością, liczbą zdań,
liczbą granic zdaniowych i pozycją dalszych fragmentów. W SPEKTRZE-1 nie
przeszedł kontroli interpunkcyjnej i nie wchodził do żadnej hipotezy
konfirmacyjnej. W SPEKTRZE-2 nie odpowiada na żadne pytanie. **Usunięty** —
to zarazem 1/5 mniej pomiaru.

## 3. Wymóg wobec ram zdaniowych

Rama musi przyjmować **wszystkie pięć desygnatów równie naturalnie.** Cała
specyfika siedzi w podmienianej frazie.

W SPEKTRZE-1 ramy pisano pod referenty procesowe („czy X ma podobny próg"),
przez co zwyczajny desygnat wpadałby w nie nienaturalnie — mierzylibyśmy
dziwność zdania zamiast przemieszczenia odniesienia.

## 4. Hipotezy

### Gałąź główna (Gemma, każda replika językowa osobno)

| | Kontrast | Co mierzy | Kierunek |
|---|---|---|---|
| **H1** | C − C'-U | samozwrotność ponad zewnętrzne odniesienie **o tym samym rejestrze** | **jednostronny ujemny** — replikacja kierunku ze SPEKTRY-1 |
| **H2** | C''-M − C'-G | samo wyjście poza dziedzinę | **dwustronny** — warunek nowy, brak obserwacji |
| **H3** | C'-U − C''-M | wkład rejestru obliczeniowego ponad przemieszczenie | **dwustronny** |

Bramkowanie: H1 → {H2, H3}. H2 i H3 są mechanistyczne i **nie bramkują się
nawzajem.**

### Gałąź replikacyjna (PLLuM) — **osobna, nie bramkuje gałęzi głównej**

| | Test | Roszczenie |
|---|---|---|
| **R1** | H1 powtórzone na PLLuM, per replika | efekt replikuje się na drugim checkpoincie |
| **R2** | interakcja: (C − C'-U)_PLLuM − (C − C'-U)_Gemma | **wyłącznie:** siła efektu różni się między checkpointami rodziny Gemma-3-4B |

**R2 NIE licencjonuje twierdzenia o dotrenowaniu na polskim.** Modele różnią
się także całą ścieżką dostrajania instrukcyjnego, zbiorem instrukcji
i formatem dialogu. To jest porównanie dwóch checkpointów, nie eksperyment
przyczynowy nad językiem treningu.

### Kontrasty opisowe

C − C''-M (szeroki), C − C'-G (replikacja SPEKTRY-1), C − B, entropia widmowa,
I₋₁, profil warstwowy, perplexity i oceny naturalności.

## 5. Endpoint

Ī = średnia I_total po zamrożonym paśmie warstw, jeden skalar na tekst,
parowanie wewnątrz scenariusza, permutacja etykiet wariantów.

**Definicja dziedziczona wchodzi do pieczęci jako wersjonowany załącznik**, nie
jako odwołanie „bez zmian wobec SPEKTRY-1": wzór I_total, metoda ustalania λ*,
normalizacja aktywacji, pasmo warstw, traktowanie tokenów specjalnych,
tokenizer, dopasowanie długości, test permutacyjny, liczba permutacji, ziarna,
obsługa braków.

**Test interakcji R2 — zamrożony jawnie.** Model nie jest przypisywany losowo
do tekstu, więc permutacja etykiety modelu jest nieuprawniona. Statystyka:
różnica scenariuszowych Δ między modelami, **bootstrap po scenariuszach**
(jednostka = scenariusz), CI 99%, osobno per replika językowa. Bez łączenia p
między językami.

Entropia widmowa i I₋₁ **nie są endpointami** — to funkcje tego samego widma.

## 6. Naturalność — kontrola konstrukcyjna, nie inferencyjna

Przed **jakimkolwiek** forwardem na zapieczętowanym korpusie:

1. Ślepa ocena każdej insercji — oceniający nie zna nazw warunków.
2. Wymiary: poprawność gramatyczna, spójność odniesienia, zaskoczenie
   semantyczne, dopasowanie do ramy.
3. **Reguła konstrukcyjna** (nie próg inferencyjny): żaden wariant nie może
   mieć mediany naturalności niższej o więcej niż 1 punkt w skali 1–7 od
   pozostałych wariantów **tego samego scenariusza**. Scenariusz odstający —
   poprawiany albo odrzucany **przed** pieczęcią.
4. Próg 1 punktu **sprawdzić na istniejącym materiale SPEKTRY-1**, zanim
   zostanie zamrożony. To jest ta sama lekcja co ANEKS-4.

Perplexity raportowana, ale **nie jako jedyna kontrola** — każdy model inaczej
ocenia naturalność tego samego zdania.

## 7. Liczność

Wiążący jest **angielski**: efekt w kontraście C − C'-U wynosi tam d_z −0,74
wobec −1,35 po polsku.

Moc przy dyskoncie 75% (klątwa zwycięzcy):

| | M=32 | M=40 | M=48 |
|---|---:|---:|---:|
| EN | 0,76 | 0,86 | **0,93** |
| PL | **1,00** | 1,00 | 1,00 |

**EN = 48, PL = 32.** Repliki są osobnymi badaniami, więc wolno im mieć różne
liczności — i powinny, skoro wymagają różnej mocy.

Przed pieczęcią policzyć moc także dla **SESOI ustalonego merytorycznie**, nie
tylko dla dyskontowanego efektu historycznego. Wiążący jest **większy** z dwóch
wymogów. Zamrozić regułę: **liczności nie zwiększa się po poznaniu wyników.**

## 8. Modele

| Ramię | Model | Rola |
|---|---|---|
| główne | `google/gemma-3-4b-it` | H1, H2, H3 |
| replikacyjne | `CYFRAGOVPL/PLLuM-4B-instruct-2512` | R1, R2 |

**Zweryfikowane empirycznie, nie założone:** architektura tożsama (34 bloki,
hidden 2560); tokenizacja korpusu SPEKTRY-1 identyczna co do tokena
(240/240 tekstów); narzut szablonu stały w scenariuszu ±1 token; słownik PLLuM
to słownik Gemmy plus `[INST]` i `[/INST]`.

**Różni się format dialogu** — ograniczenie do zadeklarowania. Sprawdzić przed
pieczęcią, czy różnica narzutu przesuwa **pozycje insercji w oknie T′** i czy
to jest jednakowe we wszystkich wariantach.

## 9. Do policzenia PRZED pieczęcią

1. Moc H1 przy M dla dyskonta 100%, 75%, 50% **oraz dla SESOI**.
2. Moc R2 z jawnym ρ — **zamrożenie na ρ = 0,3, bo ρ jest nieznane
   i planujemy konserwatywnie.** (Uzasadnienie poprawione: to jest argument
   o niepewności, nie o tym, że wysokie ρ „nie warto".) Krzywa mocy dla
   ρ ∈ {0,3, 0,5, 0,7, 0,9} w protokole.
3. MDE dla H1 i R2 — granica strefy niekonkluzywnej w zbiorze werdyktów.
4. **Żadnego testu równoważności**, dopóki symulacja nie wykaże osiągalności
   marginesu (ANEKS-4).
5. **Bramka manipulacji PLLuM — z liczbami.** Kryteria, testy i reguła
   odrzucenia zamrożone. Niezaliczenie → R2 wypada, zostaje R1.
6. Weryfikacja warstw PLLuM hookami — sprawdzenie znanej odpowiedzi.
7. Bramka pamięci PLLuM na karcie 16 GB, przy 5 wariantach i M=48/32.
8. **Budżet obliczeniowy** — 80 scenariuszy × 5 wariantów × 2 modele,
   z czasem i szczytem pamięci, przed zobowiązaniem.
9. Próg naturalności (1 punkt) sprawdzony na materiale SPEKTRY-1.

## 10. Rejestracja

Niezależny datownik **przed pierwszym forwardem obu modeli na korpusie.**
Pakiet: hash korpusu, kodu, konfiguracji, identyfikatory i sumy wag obu modeli,
wersje tokenizerów, **obraz kontenera** (brak w SPEKTRZE-1, do nadrobienia),
lockfile, log czasu pierwszego forwardu.

**Zakaz uruchamiania czegokolwiek — łącznie z testami sanity — na zapieczętowanym
korpusie przed datownikiem.** Sanity techniczne wyłącznie na sztucznym zestawie.

## 11. Czego nie będziemy twierdzić

- Że mierzymy świadomość albo odczuwanie.
- Że R2 dowodzi wpływu **dotrenowania na polskim** — dowodzi różnicy między
  dwoma checkpointami.
- Że confound abstrakcyjne–konkretne jest usunięty — jest **zbalansowany
  i zmierzony**, nie usunięty.
- Że jeden model i jedna rodzina scenariuszy pozwalają na generalizację.
