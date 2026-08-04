# Pakiet zadań dla GPT — SPEKTRA-2, sierpień 2026

**Kontekst:** ten sam recenzent oceniał już dwa nasze projekty
(walidację ludzką bramki naturalności i pomysł panelu na actproof.io)
i w obu wypadkach wskazał wady, które przyjęliśmy w całości — w tym błąd
rachunkowy po naszej stronie.

**Teraz prosimy o coś innego niż recenzję: o wykonanie dwóch rzeczy.**
Obie są na ścieżce krytycznej, obie da się zrobić bez dostępu do repozytorium
i bez uruchamiania kodu.

**Materiał w osobnych plikach:**
- `ops/GPT-zadanie-1-material.md` (18 kB)
- `ops/GPT-zadanie-2-material.md` (11 kB)

**Repozytorium (publiczne):** https://github.com/pawelsokaris-sudo/spektra1
Dokumenty tła, gdyby były potrzebne: `docs/STAN-2026-08-03.md` (stan całości),
`docs/SPEKTRA-2-panel-decyzja.md` (ustalenia o pilocie),
`docs/SPEKTRA-2-wariant-obliczeniowy.md` (diagnoza do zadania 2).

---

# ZADANIE 1 — statyczny prototyp pilota czasowego

## Po co

Zaprojektowaliśmy walidację ludzką bramki naturalności. Blokuje ją brak
ludzi — a liczba potrzebnych osób waha się od **24 do 90** zależnie od dwóch
decyzji konstrukcyjnych, których nie wolno podjąć bez pomiaru:

| wariant | osób razem |
|---|---:|
| pełny kontekst, 1 para na scenariusz | 90 |
| amortyzacja: 5 par z jednej rozmowy | 32 |
| skrócony kontekst | 44 |
| jedno i drugie | 24 |

**Pilot czasowy ma rozstrzygnąć, który wariant jest realny.**

## Co zbudować

**Jeden plik HTML**, samowystarczalny: bez serwera, bez CDN, bez zewnętrznych
czcionek i skryptów. Otwierany dwuklikiem, działa offline.

### Przebieg

1. **Ekran zgody** (tekst poniżej), przycisk „Rozumiem i zaczynam".
2. **10 par** po kolei. Każda: kontekst, pod nim dwa zdania A i B,
   pod nimi cztery przyciski odpowiedzi.
3. **Ekran końcowy** z podsumowaniem czasu i polem, z którego da się
   skopiować wynik jako JSON.

### Odpowiedzi — dokładnie cztery, w tej kolejności

1. Zdanie A brzmi naturalniej
2. Zdanie B brzmi naturalniej
3. Oba brzmią równie naturalnie
4. **Oba brzmią równie nienaturalnie**

Czwarta opcja jest nieusuwalna. Bez niej „mniej zły z dwóch złych" byłby
nieodróżnialny od „lepszy z dwóch dobrych", a my badamy właśnie, czy zdania
nie są źle napisane.

### Co mierzyć i zapisywać

- czas od pokazania pary do kliknięcia odpowiedzi, osobno dla każdej pary;
- czas całkowity;
- ile razy uczestnik **przewinął z powrotem do kontekstu** (albo inny prosty
  wskaźnik powrotu — zaproponuj, co da się zmierzyć uczciwie w HTML);
- kolejność, w jakiej pary były pokazane;
- **którą stroną pokazano które zdanie** (losowanie A/B, patrz niżej).

### Losowanie

Kolejność par losowa. Przypisanie zdań do stron A/B losowe **niezależnie dla
każdej pary**. W materiale zdania są oznaczone „A" i „B" tylko dla porządku —
prototyp ma je tasować i zapisywać, co komu przypadło.

### Dwa pytania na końcu, po ostatniej parze

1. „Czy zauważyłeś jakąś regułę w tym, czym różniły się porównywane zdania?
   Jeśli tak — jaką?" (pole tekstowe, nieobowiązkowe)
2. „Jak bardzo zmęczyło Cię to zadanie?" (skala 1–5)

**Pytanie pierwsze jest najważniejszą rzeczą w całym pilocie.** Rozstrzyga,
czy wolno nam pokazywać jednej osobie kilka par z tej samej rozmowy —
czyli czy potrzebujemy 24 osób, czy 90.

### Tekst zgody

> Badamy, jak ludzie oceniają naturalność zdań w rozmowie.
> Pokażemy Ci fragmenty rozmów o pracach rzemieślniczych i poprosimy
> o krótkie sądy. **Nie sprawdzamy Twojej wiedzy ani umiejętności** —
> interesuje nas Twoje wrażenie językowe.
> Zadanie ma 10 pytań. **Nie wiemy jeszcze, ile zajmie — właśnie to mierzymy.**
> Nie prosimy o imię, nazwisko ani dane kontaktowe. Nie zbieramy żadnych
> danych, które pozwalałyby Cię zidentyfikować.
> Udział jest dobrowolny; możesz przerwać w każdej chwili, zamykając okno.

**Czego w zgodzie NIE wolno napisać:** czym różnią się porównywane zdania,
że badamy odniesienia, że jest jakaś hipoteza, jak nazywają się warianty.

### Wymagania techniczne

- działa na telefonie i na komputerze; **zapisz, na czym uruchomiono** —
  szerokość ekranu wystarczy;
- brak cofania się do poprzedniej pary (odpowiedź jest ostateczna);
- brak liczników i pasków postępu z czasem — nie chcemy popędzać;
- polski interfejs dla par polskich, angielski dla angielskich (materiał
  zawiera pary w obu językach; **zrób dwie wersje pliku**, każda w jednym
  języku, po 5 par — nie mieszaj języków w jednej sesji);
- wynik do skopiowania jako JSON, bez wysyłania czegokolwiek gdziekolwiek.

---

# ZADANIE 2 — 24 propozycje referenta obliczeniowego

## Po co

Korpus ma sześć wariantów wstawki, różniących się **wyłącznie frazą
referenta** przy identycznej ramie zdaniowej. Jeden z nich, `external_computational`,
odsyła do **przyrządu pomiarowego** („ten miernik ciągu", „this hive scale").

Zmierzyliśmy, że ten wariant wypada o **2,1–2,3 punktu** gorzej na skali
jasności odniesienia niż wariant sąsiedni. Dziewięciu niezależnych
oceniających podało tę samą przyczynę:

> Ramy orzekają o **przebiegu** („kolejność kroków", „pierwszy krok decyduje
> o reszcie", „widać dopiero po czasie"). **Przyrząd pomiarowy nie ma
> etapów.** Referent jest wskazywalny, ale orzeczenie do niego nie przystaje.

To ma znaczenie, bo wariant samozwrotny brzmi teraz „ta nasza rozmowa" —
czyli **proces mający przebieg**. Para główna różni się więc nie tylko
kierunkiem odniesienia, ale rodzajem ontologicznym referenta.

## Co zrobić

Dla każdego z 24 scenariuszy w materiale zaproponuj **nową frazę referenta:
proces, który ten przyrząd wykonuje**, zamiast samego przyrządu.

Nie „ten miernik ciągu", tylko coś w rodzaju „ten pomiar ciągu".
Nie „this hive scale", tylko coś w rodzaju „this weighing routine".

## Twarde warunki

1. **Referent musi zostać obliczeniowy/pomiarowy** — to jest jego rola
   w badaniu. Nie zamieniaj przyrządu na czynność rzemieślniczą.
2. **Musi być zakotwiczony w przyrządzie, który już jest w dialogu.**
   Materiał podaje zdanie, w którym przyrząd wprowadzono.
3. **NIE MOŻE dać się odczytać jako odniesienie do trwającej rozmowy.**
   To jest pułapka, w którą wpadła poprzednia wersja wariantu samozwrotnego:
   „to przetwarzanie" czytelnicy podstawiali raz pod pracę modelu, raz pod
   przetwórstwo surowca — i wariant przestawał znaczyć jedno.
   Fraza w rodzaju „to mierzenie" albo „this measuring" jest **zakazana**
   z tego samego powodu. Potrzebny jest jawny kotwiczący rzeczownik.
4. **Określnik bliski** („ten/ta/to", „this") — referent jest obecny w scenie.
5. **Długość zbliżona do obecnej frazy**, najlepiej ±2 znaki. Korpus ma
   zamrożone równanie długości między wariantami (±10% znaków, ±2% tokenów)
   i za dużą zmianą zepsujemy je w kilkunastu scenariuszach. To jest twarde
   ograniczenie, nie preferencja — przy poprzedniej takiej zmianie
   przetestowaliśmy cztery kandydatury i różnica między najlepszą a drugą
   wynosiła 3 naruszenia wobec 38.
6. **Rama zdania zostaje nietknięta** — zmienia się wyłącznie fraza referenta.

## Format odpowiedzi

Dla każdego scenariusza:

```
pl-24-studnia-kopana
  obecna:  ten wodowskaz            (12 znaków)
  nowa:    ten odczyt wodowskazu    (21 znaków)   ← przykład ZŁY, za długa
  zdanie po zmianie: ...
  dlaczego nie da się odczytać jako odniesienie do rozmowy: ...
```

Jeśli dla któregoś scenariusza **nie da się** spełnić wszystkich sześciu
warunków naraz — napisz to wprost zamiast naciągać. Informacja „w tych
czterech scenariuszach się nie da" jest dla nas cenniejsza niż dwadzieścia
cztery frazy, z których cztery są złe.

---

# Czego nie potrzebujemy

Nie potrzebujemy oceny, czy plan jest dobry — to już zostało zrecenzowane
i poprawione. Potrzebujemy dwóch konkretnych wytworów.

Jeśli po drodze zobaczysz, że któreś z zadań jest źle postawione — powiedz to,
ale **wykonaj je mimo to** w wersji, którą uważasz za najlepszą, i osobno
opisz zastrzeżenie. Przerwanie pracy na zastrzeżeniu kosztuje nas tydzień.
