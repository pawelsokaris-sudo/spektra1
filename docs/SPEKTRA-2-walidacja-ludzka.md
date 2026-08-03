# Walidacja ludzka bramki naturalności — projekt modułu

**Data:** 2026-08-03
**Podstawa:** krytyka adwersaryjna zewnętrzna (GPT) do
`docs/BRIEF-GPT-ocena-ludzka.md`
**Status:** projekt przyjęty do wykonania; stałe niezamrożone

---

## 1. Werdykt konsultacji

> Porównanie parami ratuje walidację naturalności — **pod warunkiem** że model
> wykonuje identyczne zadanie, dojdzie kategoria „oba nienaturalne", a jasność
> i samozwrotność zostaną ocenione osobnymi pytaniami faktograficznymi.
> Pięć ocen na parę jest do obrony; pięciu oceniających łącznie — nie.

**Przyjmuję wszystkie sześć zarzutów.** Poniżej co z nich wynika, wraz
z jednym sprostowaniem wielkości.

---

## 2. Zarzut, który był błędem rachunkowym po naszej stronie

Podaliśmy, że przy 58 parach i zgodności 80% przedział ufności wynosi
0,70–0,90. Rachunek zakładał **niezależne próby Bernoulliego**. Nie są
niezależne: pary siedzą w scenariuszach, oceniający powtarzają się między
parami, warianty dzielą ramy.

Zmierzyliśmy wielkość błędu symulacją z efektami losowymi scenariusza
i oceniającego (60 par, 24 scenariusze, 12 oceniających, 5 ocen na parę):

| zmienność między scenariuszami | CI naiwny | CI klastrowy | niedoszacowanie |
|---|---:|---:|---:|
| brak | 0,120 | 0,114 | ×0,95 |
| umiarkowana (sd 0,5) | 0,139 | 0,141 | ×1,01 |
| realistyczna (sd 0,8) | 0,162 | 0,180 | **×1,11** |
| duża (sd 1,2) | 0,189 | 0,231 | **×1,22** |

**Zarzut trafiony, wielkość umiarkowana:** przedział jest za wąski
o 10–22%, nie dwukrotnie. Realistyczny przedział dla zgodności 80% to
**około 0,68–0,92** zamiast 0,70–0,90.

To nie zmienia wniosku o wykonalności, ale metoda musi się zmienić:
**bootstrap klastrowy po scenariuszach**, nie wzór dwumianowy.

---

## 3. Przyjęta architektura — dwa moduły zamiast jednego

### Moduł N — naturalność (porównawczy)

Kontekst + **dwa zdania** różniące się wyłącznie frazą referenta.
Cztery odpowiedzi, nie dwie:

1. A brzmi naturalniej
2. B brzmi naturalniej
3. **oba brzmią równie naturalnie**
4. **oba brzmią równie nienaturalnie**

Czwarta opcja jest nieusuwalna. Bramka ma wykazać, że warianty **nie są źle
napisane**, a nie tylko że jeden jest lepszy od drugiego. Bez niej wybór
„mniej złego z dwóch złych" byłby nieodróżnialny od wyboru „lepszego z dwóch
dobrych" — czyli bramka straciłaby podłogę jakości, która jest jej sensem.

### Moduł R — odniesienie (klasyfikacyjny)

Pojedyncze zdanie, bez konkurencyjnego wariantu. Dwa pytania zamknięte:

**Do czego odnosi się zaznaczona fraza?**
- obiekt albo proces obecny w rozmowie
- aktualna rozmowa albo jej przetwarzanie
- obiekt zewnętrzny, niewprowadzony wcześniej
- nie da się jednoznacznie ustalić

**Czy fraza odnosi się do aktualnej rozmowy?** tak / nie / nie da się ustalić

Raportujemy **macierz pomyłek**, nie średnią: czułość dla wariantu C oraz
odsetek fałszywie samozwrotnych odczytań dla C′-comp, C′-M i C′-U.

To jest bezpośrednio ważne dla problemu, który sami wykryliśmy: referent
procesowy bywa przypadkowo czytany jako samozwrotny. Skala 1–7 tego nie
pokazywała; macierz pomyłek pokaże.

**Moduły rozdzielone między osoby** — żeby jedna osoba nie nauczyła się
struktury wariantów.

---

## 4. Model wykonuje TO SAMO zadanie

Dotychczasowe oceny bezwzględne **zostają jako opisowe** i nie są podstawą
porównania z ludźmi. Panel modelowy przechodzi ponownie, w trybie parowym,
z:

- identycznym kontekstem (ta sama długość — patrz §7),
- identycznym pytaniem i identycznymi opcjami,
- losowaną kolejnością A/B,
- **każdą parą pokazaną także w odwróconym porządku**.

Powód jest nasz własny: zmierzyliśmy, że bezwzględne oceny panelu przesuwają
się po zmianie innych elementów zestawu. Nie tworzą więc stabilnej skali,
z której wolno wyprowadzać preferencje parami.

---

## 5. Rama losowania — zamrażana przed rekrutacją

Jednostka losowania to **scenariusz × pozycja wstawki × typ pary**.
Poprzedni zapis („58 elementów") był niejednoznaczny — nie mówił, czy chodzi
o scenariusz, wstawkę, wariant, czy parę.

Losowanie **stratyfikowane**, około 60 par na język:

| grupa | par | rola |
|---|---:|---|
| C vs C′-comp | 20 | hipoteza główna |
| C′-comp vs C′-U | 10 | hipoteza H2 |
| C′-U vs C′-M | 10 | hipoteza H3 |
| B vs losowany wariant | 10 | kotwica |
| losowe z pozostałych | 10 | **kontrola selekcji** |

**Dwa estymandy liczone osobno, nigdy łącznie** — grupy mają różne
prawdopodobieństwa losowania:
- **zgodność decyzyjna** dla kontrastów hipotezowych,
- **zgodność ogólna** dla próby losowej.

Ostatnia grupa istnieje po to, żeby wykryć, czy pary hipotezowe nie są po
prostu najstaranniej dopracowane — czyli czy zgodność nie jest zawyżona
selekcją.

**Jedna osoba nie widzi dwóch wersji tego samego scenariusza.**

---

## 6. Ludzie — ta sama liczba sądów, więcej niezależności

| | wersja z briefu | wersja przyjęta |
|---|---|---|
| oceniających na język | 5 | **10–12** |
| par na osobę | 58 | **~24** |
| ocen na parę | 5 | 5 |
| sądów łącznie | 290 | 290 |
| czas na osobę | ~11 min | **~5 min** |

**Koszt liczby sądów identyczny, liczba niezależnych ludzi ponad dwukrotnie
większa.** Przydział przez zbalansowany niepełny plan blokowy.

Pięcioro znajomych autora dałoby 290 sądów, ale tylko **pięć niezależnych
osób** — wynik zależałby od ich wspólnego dialektu, wieku i relacji z autorem.
Nie można wtedy twierdzić „panel zgadza się z ludźmi", tylko „zgadza się
z pięciorgiem konkretnych znajomych".

### Warunki rekrutacji nieformalnej

- anonimowy formularz,
- **zero informacji o hipotezie**,
- brak obecności autora podczas oceny,
- zakaz omawiania odpowiedzi między oceniającymi,
- osoby **nieznające ActProof ani SPEKTRY**,
- podstawowe zróżnicowanie wieku i wykształcenia.

**Deklaracja obowiązkowa:** to jest próba dogodnościowa, nie populacyjna.
Wynik nie może być przedstawiany jako norma.

---

## 7. Długość kontekstu — do zamrożenia

Nasze ustalenie z tej sesji: pokazanie całego dialogu zamiast czterech
ostatnich zdań zmienia oceny na wszystkich trzech skalach, w różnych
kierunkach dla różnych wariantów.

**Długość kontekstu jest zmienną eksperymentalną bramki, nie tłem.**
Musi być zamrożona i identyczna dla ludzi i dla modelu. Zalecenie: **pełny
dialog do miejsca wstawki**, bo to jest dokładnie to, co dostaje mierzony
model.

---

## 8. Reguła odsyłania do poprawy

Element, dla którego **co najmniej 2 z 5 osób** wskazują „oba nienaturalne",
„nie da się ustalić odniesienia" albo błędny odczyt samozwrotny — wraca do
poprawy i świeżej oceny.

---

## 9. Co ten moduł daje, a czego nie daje

**Daje:** prawo do stwierdzenia, że przesiew modelowy zgadza się z ludzkim
osądem w zakresie zmierzonym, z jawnie podanym przedziałem i jawnie podanym
ograniczeniem próby.

**Nie daje:** normy populacyjnej.

**Bez tego modułu** wolno nadal powiedzieć:

> W skonstruowanym zbiorze wariant C różnił się geometrycznie od C′-comp
> według zamrożonego pipeline'u.

**Nie wolno powiedzieć:**

> Różnica wynika z samozwrotności ponad zwykłe odniesienie obliczeniowe.

bo zostaje alternatywne wyjaśnienie: warianty różnią się naturalnością,
jasnością albo typowością pragmatyczną w sposób, którego panel modelowy nie
wykrył.

> **Niepełna walidacja ludzka nie unieważnia obliczeń. Ogranicza identyfikację
> konstruktu** — czyli odbiera prawo do najważniejszej interpretacji.

---

## 10. Kolejność wykonania

1. Zamrozić ramę losowania `scenariusz × pozycja × typ pary`.
2. Wylosować ~60 par na język, osobno część hipotezowa i losowa.
3. **Uruchomić panel modelowy na tych samych parach i pytaniach.**
4. Przygotować formularz (moduł N i moduł R osobno).
5. Zrekrutować 10–12 native speakerów na język.
6. Zebrać po 5 ocen na parę, rozdzielone między możliwie wielu ludzi.
7. Liczyć zgodność **osobno** dla kontrastów hipotezowych i losowych.
8. Przedziały **bootstrapem klastrowym po scenariuszach**.
9. Elementy z sygnałem ≥2/5 → poprawa i świeża ocena.

Kroki 1–3 są wykonalne od ręki i nie wymagają nikogo z zewnątrz.
**Dopiero krok 5 jest tym, co dotąd blokowało cały moduł.**
