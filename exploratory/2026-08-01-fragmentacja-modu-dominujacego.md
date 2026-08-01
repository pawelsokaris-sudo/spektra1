# EKSPLORACJA — trzy sygnatury „drugiego magnesu"

> **STATUS: analiza post hoc. ZERO mocy konfirmacyjnej.** Hipoteza powstała
> PO zobaczeniu wyniku głównego. Metryki (λ₁/tr, k, H_s) są zamrożone
> w protokole §5, ale ich zestawienie w tę hipotezę — nie. Nie wolno tego
> cytować jako potwierdzenia czegokolwiek. Miejsce docelowe: sekcja
> interpretacji preprintu oraz kandydat na prerejestrowaną hipotezę SPEKTRA-1b
> na ŚWIEŻYCH korpusach.

## Hipoteza (Paweł + Claude z rozmowy źródłowej, 2026-08-01)

Wstawka samozwrotna nie obniża „porządku" — **fragmentuje mod dominujący**.
Zamiast jednego dużego modu powstają dwa mniejsze („dwa magnesy zamiast
jednego"). Przewidywania: (a) λ₁/tr niższe w C niż w C′-G, (b) k równe lub
wyższe, (c) H_s wyższe w C.

## Wynik (48 scenariuszy, pasmo 14–27, parowanie po scenariuszu)

| Sygnatura | EN | PL |
|---|---|---|
| (a) λ₁/tr niższe w C | −0,00045 · **18/24** | −0,00047 · **22/24** |
| (b) k równe lub wyższe w C | −0,235 · **7/24** ✗ | +0,161 · 18/24 |
| (c) H_s wyższe w C | +0,00220 · **24/24** | +0,00192 · **24/24** |

Dla odniesienia efekt główny: I_total niższe w C — 24/24 (EN), 23/24 (PL).

## Ocena krytyczna — trzy rzeczy, które osłabiają prostą interpretację

**1. Sygnatura (c) jest częściowo pociągnięta przez wynik główny, nie
niezależna od niego.** H_s i I_total są funkcjami tego samego widma. Spłaszczone
widmo z definicji ma mniej masy skupionej powyżej progu. Zgodność 48/48 robi
wrażenie, ale jest bliższa przeformułowaniu efektu głównego niż jego
niezależnemu potwierdzeniu.

**2. Sygnatura (a) jest WYRAŹNIE SŁABSZA niż efekt główny** (18/24 i 22/24
wobec 24/24 i 23/24). Gdyby mechanizmem była fragmentacja modu dominującego,
λ₁ powinno przesuwać się co najmniej tak konsekwentnie jak cały wskaźnik.
Nie przesuwa się. **To jest argument przeciwko obrazowi „jeden mod pęka na dwa".**

**3. Sygnatura (b) zawodzi w angielskim** (7/24 — k jest tam w większości
scenariuszy NIŻSZE, nie wyższe). Gdyby mod pękał na dwa liczone mody, k
rosłoby. Rośnie tylko w polskim.

## Wniosek: hipoteza w lepiej postawionej wersji

Dane układają się nie w **pęknięcie modu dominującego**, tylko w
**rozproszenie energii po całym widmie**: mniej masy w modach kolektywnych,
płaskie widmo, przy czym mod czołowy uczestniczy w tym słabiej niż reszta.
Obraz „dwóch magnesów" pasuje, ale to nie jest „jeden magnes pękł na dwa" —
bliżej mu do „część układu przestała nadążać za wspólnym rytmem".

To jest **ostrzejsza i bardziej ryzykowna** hipoteza kierunkowa dla 1b niż
pierwotna, bo wprost przewiduje, że λ₁ zmieni się SŁABIEJ niż I_total —
czyli daje się obalić inaczej niż przez sam znak.

## Czego z tych danych NIE wolno użyć jako poparcia

Wariant A ma najwyższe I_total i najniższe H_s, co ładnie pasuje do odczytania
„I_total mierzy synchronizację". **Ale A jest zanieczyszczony** — kontrola
interpunkcyjna wykazała, że odróżnia się od wariantów dialogowych samym stylem
zapisu (55% EN, 58% PL przy przypadku 50%). Jego wartości nie mogą być
argumentem za niczym.

---

# Dopisek: dwie rzeczy sprawdzone na prośbę rozmowy źródłowej

## 1. Czy k jest hałaśliwe? TAK, i to rozstrzygająco

W pasie 5% nad progiem λ\* siedzi **średnio 3,68 modu na warstwę** (mediana 4,
maksimum 8). Obserwowana różnica k między C i C′-G to **0,16–0,24**.

Czyli: przesunięcie progu o 5% zmienia k o rząd wielkości bardziej niż wynosi
mierzony efekt. **Sygnatura (b) nie jest „mniej wiarygodna" — jest
nieinformatywna.** Nie świadczy ani za hipotezą, ani przeciw niej, w żadnym
z języków. Rozjazd EN/PL na k nie wymaga wyjaśnienia, bo nie jest zjawiskiem.

## 2. Czy dysocjacja λ₁/tr wobec I₋₁ jest obecna w danych?

Test: parowany bootstrap różnicy |d_z(λ₁/tr)| − |d_z(I₋₁)|, 10 000 losowań
po scenariuszach, CI 99%.

| Replika | d_z(λ₁/tr) | d_z(I₋₁) | d_z(I_total) | Różnica | CI 99% | Wynik |
|---|---:|---:|---:|---:|---|---|
| EN | −0,704 | −2,574 | −2,650 | **−1,870** | [−3,658; −0,662] | **dysocjacja obecna** |
| PL | −1,478 | −1,307 | −1,494 | +0,171 | [−0,509; +0,953] | brak rozstrzygnięcia |

**W angielskim dysocjacja jest wyraźna i przedział wyklucza zero.** Mod czołowy
uczestniczy w efekcie znacznie słabiej niż reszta widma — dokładnie tak, jak
przewiduje obraz rozproszenia, a wbrew obrazowi pęknięcia.

**W polskim jej nie ma** — oba efekty są tej samej siły, różnica nieodróżnialna
od zera i z przeciwnym znakiem. To jest **ten sam rozjazd między replikami**,
który już zaklasyfikował wynik główny jako niestabilny.

## Konsekwencja dla prerejestracji 1b — ostrzeżenie z ANEKSU 4

Zanim ten test zostanie zamrożony, trzeba **policzyć, jaką różnicę da się przy
planowanym M w ogóle wykryć.** Przy M = 24 przedział ufności miał tu połowę
szerokości około **1,5 jednostki d_z**. Czyli:

- dysocjacja rzędu obserwowanej w EN (1,87) — wykrywalna;
- dysocjacja umiarkowana, rzędu 0,5 — **niewykrywalna**; potrzeba około
  **9× więcej scenariuszy** (M ≈ 216 na język), bo przedział zwęża się jak
  pierwiastek z liczności.

To jest **dokładnie ta sama pułapka co margines równoważności z ANEKSU 4**:
kryterium zamrożone bez sprawdzenia, czy istnieją dane, które je spełnią.
Drugi raz w tym projekcie nie powinien się zdarzyć.

## Uwaga do porządku endpointów

Zgoda, że H_s nie może stać obok I_total. Ale **I₋₁ też nie może** — z tego
samego powodu, bo to znowu funkcja tego samego widma. Endpointem dysocjacyjnym
musi być **różnica efektów** (λ₁/tr wobec I₋₁), nie I₋₁ samo w sobie.
Sformułowanie z rozmowy źródłowej już to robi poprawnie; zapisuję to wprost,
żeby przy redakcji nikt tego nie uprościł.
