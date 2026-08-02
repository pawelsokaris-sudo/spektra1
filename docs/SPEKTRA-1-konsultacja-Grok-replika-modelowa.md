# Konsultacja zewnętrzna: replika modelowa na polskim modelu (Bielik)

**Data:** 2026-08-02. Recenzent ten sam, który przy poprzedniej konsultacji
wykrył lukę zamrożoną potem jako ANEKS-2 (brak marginesu równoważności dla H1).
**Charakter:** prosimy o krytykę adwersaryjną, nie o potwierdzenie.

## Kontekst w pięciu zdaniach

SPEKTRA-1 to prerejestrowane badanie na Gemma 3 4B. Z jednej bazy zdań powstaje
pięć wariantów tej samej rozmowy, różniących się **wyłącznie treścią pięciu
wstawionych zdań** (te same pozycje, ta sama składnia, długości w tokenach
wyrównane do ±0,2%): A mechaniczny, B wstawka neutralna, C samozwrotna,
C′-G odniesienie zewnętrzne osadzone, C′-U zewnętrzne nieosadzone. Endpoint:
I_total = udział wartości własnych macierzy korelacji aktywacji powyżej progu
λ\* z symulowanego nulla, uśredniony po paśmie warstw [0.4L, 0.8L]. Test główny
H1 = C − C′-G, jednostronny dodatni, α = 0.01, permutacja parowana wewnątrz
scenariusza, 24 scenariusze na język, PL i EN jako **osobne repliki**.

## Wynik

H1 **niepotwierdzona**; efekt istotnie w przeciwną stronę:

| Replika | Δ₁ = C − C′-G | d_z | zgodność |
|---|---:|---:|---|
| EN | −0,0058 | −2,65 | 24/24 scenariuszy |
| PL | −0,0036 | −1,49 | 23/24 |

GATE 3 (odporność): precyzja bf16→fp32 zmienia Δ₁ o 3,1% / 3,5%; usunięcie
komponentu pozycyjnego o 7,9% / 8,8% (próg 25%) — **oba spełnione**.
Kryterium replik **niespełnione**: znak zgodny, ale amplitudy różnią się
o **37,2%** przy progu 25%. Wynik klasyfikowany jako niestabilny.

## Problem do rozstrzygnięcia

Rozjazd 37% ma co najmniej trzy konkurencyjne wyjaśnienia i nie umiemy ich
rozdzielić: (1) Gemma jest anglocentryczna, więc polskie reprezentacje są
słabsze; (2) różnica jest własnością języka (fleksja); (3) różnica wynika
z autorstwa dwóch korpusów.

## Proponowany układ

Ten sam korpus, oba języki, **dwa modele**: Gemma 3 4B (anglocentryczna)
i Bielik 4,5B (polskocentryczny, Apache 2.0, mieści się w 16 GB VRAM,
prawie identyczna wielkość — więc porównanie nie miesza skali z językiem).
PLLuM odpada: najmniejszy wariant 8B nie mieści się na dostępnej karcie.

Przewidywanie: jeśli winna jest anglocentryczność, Bielik pokaże **przecięcie**
— efekt silniejszy po polsku niż po angielsku.

## Pytania — prosimy o odpowiedź punkt po punkcie

1. **Czy układ 2×2 rzeczywiście rozdziela te trzy wyjaśnienia?** Jeżeli nie —
   które z nich pozostaje splątane i z czym?

2. **Czy porównywanie d_z między modelami jest w ogóle uprawnione?** d_z to
   efekt standaryzowany wariancją międzyscenariuszową, a ta może się różnić
   między modelami z powodów niemających nic wspólnego z językiem. Czy
   endpointem powinno być przecięcie (różnica różnic) liczone na surowej skali,
   czy na standaryzowanej — i jak wtedy uzasadnić wybór?

3. **λ\* jest estymowane per (scenariusz, warstwa) z nulla dopasowanego do
   danych.** Przy dwóch modelach progi będą inne z definicji. Czy I_total
   pozostaje porównywalne między modelami, czy wolno porównywać wyłącznie
   kontrasty wewnątrz modelu?

4. **Jak zaplanować liczność dla przecięcia?** Nasza lekcja z ANEKSU 4: przy
   M = 24 margines |d_z| < 0,3 okazał się nieosiągalny nawet dla efektu
   dokładnie zerowego. Nie chcemy powtórzyć tego błędu. Interakcja jest z
   reguły znacznie mniej mocna niż efekt główny — jakiego M realnie potrzeba,
   przy obserwowanych wielkościach (−2,65 i −1,49)?

5. **Kompetencja językowa jako confound.** Jeśli Bielik jest po prostu słabszy
   w angielskim, dostaniemy różnicę z niewłaściwego powodu. Jak to
   zoperacjonalizować **przed** pomiarem — jakim niezależnym testem i jakim
   kryterium odrzucenia?

6. **Pasmo warstw.** [0.4L, 0.8L] wyprowadziliśmy dla Gemmy, z weryfikacją
   hookami, który indeks jest już po normalizacji końcowej. Czy przenoszenie
   tej samej reguły proporcjonalnej na inną architekturę jest uzasadnione, czy
   wymaga osobnego uzasadnienia empirycznego?

7. **Czy Bielik 4,5B jest właściwym wyborem?** Jeśli nie — jaki model
   polskocentryczny do 16 GB VRAM byłby lepszy i dlaczego?

8. **Czego w tym planie nie widzimy?** Prosimy w szczególności o wskazanie
   błędu typu „kryterium zamrożone bez sprawdzenia osiągalności" — ten sam
   błąd popełniliśmy trzykrotnie w SPEKTRZE-1 i zakładamy, że popełnimy go
   znowu.

## Ograniczenia, o których recenzent powinien wiedzieć

- Brak niezależnego datownika sprzed pomiaru SPEKTRY-1 (pierwotne repozytorium
  publiczne usunięto przy wycofywaniu danych osobowych osoby trzeciej).
- Confound pola semantycznego nieusunięty: wstawki samozwrotne czerpią ze
  słownictwa obliczeniowego, zewnętrzne z konkretów dziedzinowych.
- Protokół, kod i większość recenzji przeszły przez modele językowe; jeden
  ze współautorów jest systemem klasy badanego obiektu.
- Sprzęt: pojedyncza karta 16 GB. To jest twarde ograniczenie, nie preferencja.
