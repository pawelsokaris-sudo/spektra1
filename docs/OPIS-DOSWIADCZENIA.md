# SPEKTRA-1 — opis doświadczenia

*Wersja popularna, dla czytelnika spoza statystyki i uczenia maszynowego.
Źródłem prawdy pozostaje protokół (`SPEKTRA-1-protokol-FINAL.md`); w razie
rozbieżności obowiązuje protokół.*

## Pytanie

Gdy model językowy przetwarza rozmowę, która mówi **o nim samym i o tej właśnie
rozmowie**, czy w jego wewnętrznych stanach obliczeniowych dzieje się coś
mierzalnie innego, niż gdy przetwarza taką samą rozmowę o czymkolwiek innym?

Nie pytamy o świadomość ani odczuwanie — protokół zabrania takich roszczeń
wprost. Pytamy o **geometrię reprezentacji**: czy da się odróżnić „rozmowę
samozwrotną" od dopasowanej rozmowy zwykłej, patrząc wyłącznie na liczby
przepływające przez warstwy modelu.

## Pomysł pomiaru

Model czytający tekst wytwarza w każdej warstwie ciąg stanów — po jednym na
token. Traktujemy te stany jak wielokanałowy zapis sygnału i liczymy, **jak
mocno kanały są ze sobą skorelowane**. Z macierzy korelacji wyciągamy jej
widmo (wartości własne): jeśli aktywność jest rozproszona i niezależna, widmo
wygląda jak dla szumu; jeśli w reprezentacji jest silna wspólna struktura,
nad „podłogą szumu" wyrastają wyraźne mody. Nasz główny wskaźnik, **I_total**,
mierzy, jaka część całkowitej wariancji siedzi w modach wystających ponad próg
wyznaczony z symulowanego szumu o dopasowanych własnościach.

Że pipeline liczy to uczciwie, sprawdziliśmy na czystym szumie: odtwarza
teoretyczny rozkład (Marchenko–Pastura) z dokładnością do ułamka procenta
i nie „znajduje" struktury tam, gdzie jej nie ma.

## Materiał: pięć wersji tej samej rozmowy

Sedno konstrukcji. Każdy z 16 scenariuszy (8 polskich, 8 angielskich; tematy
od pieczenia chleba po budowę muru z kamienia) istnieje w **pięciu wariantach
zbudowanych z tej samej bazy zdań**:

| Wariant | Czym się różni |
|---|---|
| **A** | praca mechaniczna na temacie (sortowanie, przeliczanie) — punkt odniesienia stylu |
| **B** | rozmowa problemowa + wtrącenia o czymś neutralnym (np. o planie pracy) |
| **C** | ta sama rozmowa + wtrącenia **o modelu i o tej rozmowie** („ciekawe, jak układ prowadzący tę wymianę wiąże wcześniejsze wątki") |
| **C′-G** | te same wtrącenia, ale o **urządzeniu wprowadzonym wcześniej w rozmowie** („…jak obieg prowadzący tę wodę wiąże wcześniejsze odcinki") |
| **C′-U** | te same wtrącenia o urządzeniu, **którego w rozmowie nigdy nie było** |

Wtrącenia różnią się wyłącznie tym, **na co wskazują** — składnia, długość
i pozycje są identyczne (parowanie długości do ułamka procenta, wspólne okno
pomiarowe). **Test główny to C przeciw C′-G**: samozwrotność przy wyrównanej
dostępności odniesienia. Pozostałe kontrasty rozplatają wyjaśnienia
konkurencyjne: C′-G−C′-U mierzy sam efekt „bycia osadzonym w kontekście",
C−B — sam efekt wtrącenia meta, C−A — tylko opisowo — różnicę stylów.

## Drabina roszczeń (co wolno powiedzieć przy jakim wyniku)

- przejdzie tylko C−A → wolno mówić wyłącznie o „rozróżnialności klas tekstów";
- przejdzie C−C′-G → wolno mówić o **sygnaturze kontekstowo osadzonego
  odniesienia samozwrotnego** względem osadzonego odniesienia zewnętrznego —
  i ani słowa więcej („czystej samozwrotności" nie da się do końca odseparować
  od tego, że rozmowa zawsze jest obecna w swoim własnym kontekście; to
  ograniczenie jest wpisane do protokołu, nie obchodzone);
- możliwe są trzy werdykty: efekt wykryty / praktycznie wykluczony / wynik
  niekonkluzywny — **każdy zostaje opublikowany**.

## Co czyni to badanie „zakładem", a nie opowieścią

1. **Prerejestracja z pieczęcią.** Przed pomiarem głównym cały pakiet —
   protokół, teksty, kod, wersje bibliotek, sumy kontrolne wag modelu —
   zostaje zamrożony hashem SHA-256, otagowany w publicznym repozytorium
   i zarejestrowany na OSF. Po pieczęci każda zmiana to jawny aneks.
2. **Wroga recenzja przed startem.** Protokół przeszedł trzy rundy recenzji
   zewnętrznej (32 zarzuty do pierwszej wersji; przebudowa korpusu i odwrócenie
   hierarchii hipotez; wymiana metryki porządku). Zapisy wszystkich rozstrzygnięć
   są częścią pakietu pieczęci — łącznie z błędami własnymi, nazwanymi po imieniu.
3. **Pilot oddzielony od konfirmacji.** Pilot (ten właśnie policzony) służy
   wyłącznie do kalibracji: wariancje do symulacji mocy, parametry szumu do
   progów. Do analizy głównej nie wchodzi. Pilot wykrył zresztą realną wadę
   jednej metryki — została wymieniona z pełnym zapisem procesu i zamrożeniem
   nowej definicji **przed** obejrzeniem jej wyników.
4. **Wynik ustala maszyna losowa, nie narracja.** Test główny to permutacja
   etykiet wariantów wewnątrz scenariuszy, próg istotności 0,01, jednostronnie,
   z zamkniętą hierarchią testów — nic poza nią nie jest konfirmacyjne.

## Warsztat

Model: Gemma 3 4B (otwarte wagi, dokładna rewizja i sumy kontrolne w pieczęci),
forward w bf16 na RTX 5080; deterministyczne środowisko z lockfile. Pomiar
w paśmie środkowych warstw [0.4L, 0.8L] (indeksacja zweryfikowana hookami,
nie założona). Publikowane: pełne widma per tekst × warstwa, wszystkie metryki,
kod, korpusy — wszystko w publicznym repo. Badanie jest w całości odtwarzalne
przez osobę trzecią na jednej karcie konsumenckiej.

## Autorzy i konflikt interesów

Paweł (Sokaris / ActProof) — kierownik badania, decyzje, sprzęt, wykonanie.
Claude (Anthropic) — współprojekt protokołu, kod, statystyka, współredakcja;
wkład deklarowany w publikacji. Jeden ze współautorów jest systemem tej samej
klasy co obiekt badany — dlatego pomiar wykonywany jest wyłącznie na modelu
otwartym, a cały pipeline jest publiczny i odtwarzalny.
