# SPEKTRA-1 — prerejestrowane przewidywanie i dlaczego było błędne

**Status:** zakończone · **Werdykt:** hipoteza niepotwierdzona; zaobserwowany
efekt odwrotny, odporny technicznie, niestabilny między replikami językowymi.
**Dane, kod i pełna historia:** https://github.com/pawelsokaris-sudo/spektra1

## Pytanie

Czy rozmowa mówiąca *o samej sobie* zostawia w modelu językowym inny ślad
geometryczny niż identycznie zbudowana rozmowa o czymś zewnętrznym?

Mierzyliśmy widmo korelacji aktywacji warstw ukrytych Gemmy 3 4B. Z jednej bazy
zdań powstało pięć wariantów tego samego dialogu, różniących się **wyłącznie
treścią pięciu wstawionych zdań** — te same pozycje, ta sama składnia, długości
wyrównane z dokładnością do ułamka procenta.

Reguły analizy zostały zamrożone i zapieczętowane kryptograficznie **zanim
odczytano jakąkolwiek aktywację**.

## Przewidywanie

Samozwrotność da **mocniejszą** sygnaturę kolektywną.

## Co wyszło

**Odwrotnie, konsekwentnie.**

| Replika | Efekt (C − C′-G) | Standaryzowany | Scenariusze w tym samym kierunku |
|---|---:|---:|---|
| angielska | −0,0058 | −2,65 | **24 / 24** |
| polska | −0,0036 | −1,49 | **23 / 24** |

Wariant samozwrotny dał **najniższy** wskaźnik integracji ze wszystkich pięciu,
w obu językach. Mały bezwzględnie — około pół procenta — ale niemal doskonale
powtarzalny w niezależnie pisanych scenariuszach.

## Odporność

- **Precyzja liczb** — przeliczone w fp32: zmiana 3,1% i 3,5% przy progu 25%.
  Kontrola tekst po tekście: największe odchylenie 0,00066 przy granicy 0,005,
  zero przekroczeń na 48 tekstach.
- **Komponent pozycyjny** — usunięty: zmiana 7,9% i 8,8%.
- **Repliki językowe** — ten sam znak, ale siła różni się o 37,2% przy progu
  25%. **To kryterium nie przechodzi.** Wynik jest klasyfikowany jako
  *niestabilny między replikami* i tak publikowany, zgodnie z protokołem.

## Czego nie twierdzimy

**Nie ogłaszamy odkrycia.** Kierunku odwrotnego nie prerejestrowaliśmy, więc
obserwacja jest opisowa i staje się kandydatem na hipotezę kolejnego badania.
Nic tutaj nie mierzy świadomości ani odczuwania — protokół wprost zabrania
takiego języka.

## Ograniczenia, wprost

- **Brak niezależnego datownika sprzed pomiaru.** Pierwotne repozytorium
  publiczne — jedyny zewnętrzny świadek — zostało usunięte przy wycofywaniu
  danych osobowych osoby trzeciej. Wszystkie pozostałe daty pochodzą od nas.
- **Confound pola semantycznego nieusunięty.** Wstawki samozwrotne czerpią ze
  słownictwa obliczeniowego, zewnętrzne z konkretów dziedzinowych. Efekt może
  mierzyć oś abstrakcyjne–konkretne, nie samozwrotność.
- **Jeden model, jedna rodzina scenariuszy, dwa języki.** Generalizacja
  minimalna.
- **Brak obrazu kontenera**, mimo że protokół go obiecywał.
- Protokół, kod, statystyka i większość recenzji przeszły przez modele
  językowe, a jeden ze współautorów jest systemem klasy badanego obiektu.
  Zadeklarowane, nie ukryte.

## Po co publikować obalone przewidywanie

Bo to jedyny rodzaj wyniku, którego nie da się dorobić po fakcie. Pieczęć
istnieje właśnie po to, żeby błędne przypisanie pojęcia do miary wyszło na
wierzch, zamiast po cichu zniknąć w interpretacji. Wyszło.
