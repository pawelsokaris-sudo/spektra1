# Uwagi zewnętrzne (Gemini, 30.07.2026, noc) — ocena i rozstrzygnięcia

*Nie jest to formalna runda recenzji; trzy uwagi techniczne przed pieczęcią,
ocenione wobec istniejącej konstrukcji. Dołączane do pakietu dla kompletności.*

## 1. „Czy nowa miara nie jest proxy entropii tokenów / n-gramów?"

**Ocena: w przeważającej mierze obsłużone konstrukcyjnie — silniej, niż uwaga
zakłada.** Główny test walidacyjny D_discourse to parowany kontrast oryginał
vs N1 po nowym forwardzie, a N1 zachowuje **dokładnie ten sam multizbiór
tokenów**, długości zdań i statystyki n-gramowe wewnątrz zdań (zmieniają się
wyłącznie bigramy na J−1 granicach zdań). Proxy powierzchniowe jest więc
w tym kontraście wyzerowane z konstrukcji.
**Przyjęte dodatkowo:** raport opisowy korelacji D_discourse z prostymi
statystykami powierzchniowymi (entropia unigramowa, długość zdań) per tekst —
jako kontrola jawna, poza hierarchią konfirmacyjną.

## 2. „Wariancja I_total może różnić się między PL i EN (gęstość tokenizacji)"

**Ocena: trafna i wnosi robotę do T5/GATE 1.** Już w konstrukcji: języki są
osobnymi replikami z osobną analizą, λ* liczone per (warstwa, JĘZYK), a różnicę
gęstości tokenizacji zmierzyliśmy wprost (PL ~3,2 znaki/token vs EN ~4,0;
to ona wymusiła rundę poprawek korpusu).
**Przyjęte do wdrożenia:**
- **T5:** null symulacyjny generowany dla T′ KAŻDEGO scenariusza (parametry
  per język) — kwantyle λ* efektywnie per (warstwa, język, T′ scenariusza),
  bo T′ waha się 811–1014 i wspólna podłoga szumu dla różnych T′ byłaby
  niedokładna. Kontrasty parowane są na to odporne (wspólne okno w scenariuszu),
  ale poziomy I_total między scenariuszami — nie.
- **GATE 1:** wariancje i ICC liczone OSOBNO per język; jeśli się rozjadą,
  M = maksimum z dwóch języków (reguła zamrażana przy pieczęci).

## 3. „Attention sink / dryf pozycyjny w małych modelach"

**Ocena: obsłużone potrójnie, przyjęte jako uwaga interpretacyjna.** Konstrukcja
już zawiera: (a) odrzucenie pierwszych 32 tokenów (protokół §4 — dokładnie
przeciw efektowi pierwszych pozycji), (b) odjęcie komponentu pozycyjnego
(średnia per pozycja po korpusie języka; wariant bez odejmowania = prerejestrowana
analiza wrażliwości GATE 3b), (c) parowanie wariantów na wspólnym oknie.
Przy analizie profilu per warstwa dryf pozycyjny będzie miany „z tyłu głowy"
zgodnie z uwagą — widma per warstwa publikujemy w całości.
