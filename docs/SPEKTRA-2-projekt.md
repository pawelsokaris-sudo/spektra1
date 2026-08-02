# SPEKTRA-2 — projekt badania (wersja robocza, przed pieczęcią)

**Status:** projekt do uzgodnienia. Nic tu nie jest zamrożone.
**Poprzednik:** SPEKTRA-1 (hipoteza obalona, efekt odwrotny, wynik niestabilny
między replikami). Ten dokument wynika z tego, czego SPEKTRA-1 nauczyła.

## 1. Pytanie

SPEKTRA-1 pytała, czy samozwrotność zostawia mocniejszy ślad. Odpowiedź:
**nie, zostawia słabszy.** Analiza po fakcie pokazała jednak, że w angielskim
efekt jest w dużej mierze **zwykłym przemieszczeniem odniesienia** — samo
odesłanie do czegoś spoza dziedziny obniża wskaźnik mocniej niż dołożenie
metapoziomu. W polskim nie: tam liczy się wyłącznie przejście na desygnat
spoza opisywanego świata.

**Nowe pytanie: czy samozwrotność robi cokolwiek PONAD zwykłe przemieszczenie
odniesienia — i czy odpowiedź zależy od języka oraz od modelu.**

## 2. Warianty (sześć)

Rama zdaniowa wspólna, zmienia się **jedna fraza rzeczownikowa**:

| Wariant | Desygnat | Przykład (scenariusz o wędzeniu ryb) |
|---|---|---|
| **A** | brak insercji | — |
| **B** neutralny | sam temat | „ten sam dym" |
| **C'-G** zewnętrzny osadzony | inny obiekt w dziedzinie | „ten drugi piec" |
| **C''-M** zewnętrzny zwyczajny | **NOWY** — poza dziedziną, nietechniczny | „to ciasto" |
| **C'-U** zewnętrzny techniczny | poza dziedziną, rejestr techniczny | „tamto sterowanie" |
| **C** samozwrotny | rozmowa / przetwarzanie | „to przetwarzanie" |

**C''-M jest jedyną nowością i to on rozdziela dwie rzeczy, których SPEKTRA-1
nie rozdzielała:** przemieszczenie odniesienia od rejestru obliczeniowego.

Reguła doboru C''-M: **jeden referent na scenariusz, powtarzany we wszystkich
insercjach** — tak jak wszystkie pozostałe warianty. Pięć różnych referentów
różnicowałoby ten wariant także **spójnością odniesienia**, czyli ukrytym
confoundem, którego nikt by nie zauważył. Referent pochodzi z innej dziedziny
życia codziennego niż scenariusz i nie dzieli z nim żadnego słownictwa.

## 3. Wymóg wobec ram zdaniowych (nowy, wyciągnięty z błędu SPEKTRY-1)

Rama musi być **analogiczna i na tyle ogólna, żeby wszystkie sześć desygnatów
wchodziło w nią równie naturalnie.** Cała specyfika siedzi w podmienianej
frazie, nigdzie indziej.

W SPEKTRZE-1 ramy pisano pod referenty procesowe („czy X ma podobny próg"),
przez co zwyczajny desygnat wpadałby w nie nienaturalnie — a wtedy mierzylibyśmy
**dziwność zdania** zamiast przemieszczenia odniesienia. Tego warunku tam nie
było i to jest błąd do niepowtórzenia.

## 4. Hipotezy — hierarchia zamknięta

| | Kontrast | Pytanie | Bramkuje |
|---|---|---|---|
| **H1 GŁÓWNA** | C − C''-M | czy samozwrotność robi cokolwiek ponad zwykłe przemieszczenie | tak |
| **H2** | C''-M − C'-G | czy samo przemieszczenie w ogóle działa | tak |
| **H3** | interakcja H1 × model (PLLuM wobec Gemmy) | czy odpowiedź zależy od dotrenowania na polskim | tak |
| rodzina po H3 | C'-U − C''-M (rejestr), C − C'-G (replikacja SPEKTRY-1), C − B, B − A, profil warstwowy | opisowe | — |

Kierunek H1 i H2: **ujemny**, jednostronnie, α = 0,01. Kierunek pochodzi ze
SPEKTRY-1, więc jest to prerejestrowana replikacja kierunku na świeżym
materiale, a nie zgadywanie.

Repliki językowe: **osobne badania**, osobna hierarchia, osobne α.
Meta-porównanie wyłącznie opisowe.

## 5. Endpoint

Bez zmian wobec SPEKTRY-1: Ī = średnia I_total po zamrożonym paśmie warstw,
jeden skalar na tekst, parowanie wewnątrz scenariusza, permutacja etykiet
wariantów.

**Interakcja modelowa liczona na surowej Δ, nie na d_z** — d_z standaryzuje
wariancją wewnątrzmodelową i mieszałoby wielkość efektu z jednorodnością
reprezentacji (rozstrzygnięcie recenzenta zewnętrznego, przyjęte).

Entropia widmowa i I₋₁ **nie są osobnymi endpointami** — to funkcje tego samego
widma. Wchodzą wyłącznie opisowo.

## 6. Liczność

Wiążącym ograniczeniem jest **angielski**: tam efekt samozwrotności ponad
przemieszczenie jest dwa razy słabszy niż po polsku (d_z −0,74 wobec −1,35
w najbliższym odpowiedniku ze SPEKTRY-1, kontraście C − C'-U).

Moc przy dyskoncie 75% (klątwa zwycięzcy — hipotezę podsunęły te same dane):

| | M=32 | M=40 | M=48 |
|---|---:|---:|---:|
| EN | 0,76 | 0,86 | **0,93** |
| PL | **1,00** | 1,00 | 1,00 |

**Propozycja: EN = 48, PL = 32.** Razem 80 scenariuszy. Repliki są osobnymi
badaniami, więc wolno im mieć różne liczności — i powinny, skoro wymagają
różnej mocy.

## 7. Modele

| Ramię | Model | Rola |
|---|---|---|
| główne | `google/gemma-3-4b-it` | test H1 i H2, porównywalny ze SPEKTRĄ-1 |
| replikacyjne | `CYFRAGOVPL/PLLuM-4B-instruct-2512` | replikacja H1 + interakcja H3 |

PLLuM wyrasta z `gemma-3-4b-pt`: architektura tożsama (34 bloki, hidden 2560),
tokenizacja korpusu **identyczna co do tokena** (240/240 tekstów SPEKTRY-1),
narzut szablonu stały w obrębie scenariusza z dokładnością do 1 tokena.

**Różni się format dialogu** (`[INST]` wobec `<start_of_turn>`) — ograniczenie
do zadeklarowania, nie do wyrównania.

Dotrenowanie: ~30 mld tokenów polskich (modele na w pełni otwartej licencji).
Siła manipulacji **mierzona bramką**, nie zakładana.

## 8. Do policzenia PRZED pieczęcią — lista obowiązkowa

Trzy razy w SPEKTRZE-1 zamroziliśmy kryterium, którego osiągalności nikt nie
sprawdził. Ta lista istnieje po to, żeby czwartego razu nie było.

1. **Moc H1** przy proponowanym M, dla dyskonta 100%, 75% i 50%.
2. **Moc H3 (interakcja)** z jawnym założeniem ρ — **zamrozić na ρ
   konserwatywnym (0,3), nie optymistycznym.** Wysokie ρ jest przesłanką
   *przeciwko* istnieniu dużej interakcji, więc planowanie na nie oznacza
   planowanie mocy pod przypadek, w którym nie ma czego znaleźć.
3. **Minimalny wykrywalny efekt** dla H1 i H3 — wchodzi do zbioru werdyktów
   jako granica strefy niekonkluzywnej.
4. **Żadnego testu równoważności** przy tych licznościach, dopóki symulacja nie
   wykaże, że margines jest osiągalny (lekcja ANEKSU 4).
5. **Bramka manipulacji PLLuM** — kryteria i reguła odrzucenia zamrożone przed
   pomiarem. Niezaliczenie → brak roszczenia o interakcji, zostaje sama
   replikacja kierunku.
6. **Weryfikacja warstw PLLuM hookami** — sprawdzenie znanej odpowiedzi
   (architektura tożsama), nie wyprowadzanie od zera. Ale sprawdzenie.
7. **Bramka pamięci** dla PLLuM na karcie 16 GB.

## 9. Rejestracja

**Niezależny datownik przed pierwszym forwardem na korpusie.** To jest
największy brak SPEKTRY-1 — jedyny zewnętrzny świadek zniknął razem z usuniętym
repozytorium. Tutaj rejestracja jest **pierwszym krokiem, nie ostatnim.**

## 10. Czego nie będziemy twierdzić

- Że mierzymy świadomość albo odczuwanie. Protokół tego zabrania.
- Że wynik dotyczy „polskocentryczności w ogóle" — dotyczy **dotrenowania
  w obrębie rodziny Gemma-3-4B**.
- Że replikacja modelowa usuwa confound abstrakcyjne–konkretne. Nie usuwa;
  częściowo usuwa go dopiero wariant C''-M.
- Że jeden model i jedna rodzina scenariuszy pozwalają na generalizację.

## 11. Otwarte

- **Naturalność wstawek:** zmierzymy perplexity wstawionego zdania per wariant
  i zaraportujemy **opisowo**. Progu nie zamrażamy, bo nie umiemy go dziś
  skalibrować, a zamrażanie kryterium bez rachunku osiągalności jest błędem,
  który popełniliśmy już trzy razy.
- **Nazwa:** SPEKTRA-2 (nowe pytanie, nowy korpus), nie 1b.
