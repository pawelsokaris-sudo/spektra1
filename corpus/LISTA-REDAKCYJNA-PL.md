# Lista redakcyjna korpusu polskiego SPEKTRY-2

**Powstała, bo autorom przywracającym diakrytyki ZABRONIŁEM poprawiać cokolwiek
poza ortografią.** Gdyby poprawiali po drodze, nie wiedzielibyśmy nawet, że
korpus te błędy miał — a część z nich siedzi w miejscach, które mają znaczenie
dla pomiaru.

**Punkt odniesienia:** commit `5d6a1e4` (stan poortograficzny).
Po rundzie `git diff 5d6a1e4` musi pokazywać **wyłącznie** pozycje z tej listy.

---

## KATEGORIA A — błędy WE WSTAWKACH, czyli w mierzonych wariantach

**To jest kategoria pilna.** Wstawki wchodzą do kontrastów; błąd gramatyczny
w wariancie zwyczajnym albo nieosadzonym oznacza, że ten wariant będzie
systematycznie mniej naturalny **z powodu błędu autorskiego, nie z powodu
badanej właściwości.** Bramka naturalności odrzuciłaby scenariusz za zły powód.

| Plik | Warianty | Jest | Ma być |
|---|---|---|---|
| pl-11 | `external_mundane`, `external_ungrounded` | „przypomina **tamte** blaszaną konewkę" | „**tamtą**" |
| pl-12 | to samo | „przypomina **tamte** automatykę" | „**tamtą**" |
| pl-13 | to samo | „przypomina **tamte** drewnianą łyżkę" | „**tamtą**" |
| pl-15 | to samo | „przypomina **tamte** emaliowaną miskę" | „**tamtą**" |
| pl-29 | to samo | „przypomina **tamte** płócienną torbę" | „**tamtą**" |
| pl-30 | to samo | „przypomina **tamte** centralkę alarmową" | „**tamtą**" |

Niezgodność rodzaju: zaimek w mianowniku liczby mnogiej przy rzeczowniku
w bierniku liczby pojedynczej. Diakrytyką nie do naprawienia.

**Uwaga:** zmiana wstawki zmienia liczbę tokenów. Po poprawce walidator musi
nadal pokazywać ±2% dla wszystkich sześciu wariantów.

---

## KATEGORIA B — literówki i błędy leksykalne

**Sprostowanie po rundzie:** ta kategoria nazywała się „w bazie dialogu"
i to było nieprawdą. Słowo „staraność" siedzi w **`insertions[1]`,
we wszystkich sześciu wariantach naraz** (pl-02, pl-35, pl-41, pl-44, pl-47,
po 6 wystąpień na plik). Poprawka jest identyczna w każdym z sześciu, więc
kontrast nie drgnął — ale kategoria B nie jest kategorią „bezpieczną
z definicji" i nie wolno jej tak traktować w kolejnych rundach.

| Plik | Jest | Ma być |
|---|---|---|
| cały korpus PL | „staraność" | „staranność" (dwa „n") |
| pl-35 | „na drewnianym **kloku**" (2×) | „na klocu" |
| pl-04 | „żółtkła", „Żółtknięcie" | „zżółkła", „Zżółknięcie" |
| pl-07 | „po tekściu" | „po teściu" |
| pl-09 | „wosczyną" | „woszczyną" |
| pl-09 | „zwężyłem" | „zwęziłem" |
| pl-14 | „ślizką" | „śliską" |
| pl-15 | „bez jednej falki" | „fałdki" |
| pl-17 | „Wielu **plotkarzy** wiąże żebra" | „plecionkarzy" |
| pl-18 | „doklejic" (2×) | „dokleić" |
| pl-19 | „długi **węgielnik**" | „węgielnica" |
| pl-20 | „zbite w **kolt**" | „kołtun" |
| pl-30 | „stare kowadło **po teście**" | „po teściu" |
| pl-33 (`topic`) | „spryzysty" | „sprężysty" |
| pl-37 | „które **trza** ziarno" | „trą" |
| pl-42, pl-48 | „miękcie" | „mięknie" |
| pl-33 | „Zawsze **giej** z taśmą" | „gnij" |
| pl-45 | „kloka", „kloku" | „kloca", „klocu" |

---

## KATEGORIA C — składnia i zgoda

| Plik | Jest | Ma być |
|---|---|---|
| pl-02 | „pod **tą** starszą półkę" | „pod **tę**" |
| pl-08 | „**Zważaj** dokładnie gram przędzy" | „Zważ" (odważ, nie: uważaj) |
| pl-09 | „których pszczoły **nie obsiada**" | „nie obsiądą" |
| pl-11 | „odsunąłem **tą** starą maselnicę" | „**tę**" |
| pl-18 | „**Zdrowa podeszwa główna** poznasz po tym" | „Zdrową podeszwę główną" |
| pl-18 | „zużywa właśnie **ta** krawędź obcasa" | „**tę**" |
| pl-20 | „zanieczyszczenia wchodzą **w włókno**" | „**we** włókno" |
| pl-27 | „gdzie **w włóknach** jest jeszcze woda" | „**we** włóknach" |
| pl-36, pl-39, pl-48 | „przez **tą** starą prasę", „obejrzałem **tą** starą uprząż", „Zbierz **tą** warstwę" | „**tę**" |

**Rozstrzygnięcie w sprawie „tą" wobec „tę":** poprawiamy na „tę" **wyłącznie
w bierniku** („widzę tę półkę"). W narzędniku „tą" jest formą poprawną
(„pod tą półką", „tą metodą") i **zostaje bez zmian**. Autorzy przywracający
diakrytyki zapisali „tą" nie z wyboru stylistycznego, tylko dlatego, że była
to jedyna forma osiągalna samą diakrytyką z zapisu „ta" — to ślad po
pierwotnym błędzie, nie decyzja redakcyjna.

---

## KATEGORIA D — niekonsekwencja terminologiczna

| Pliki | Rzecz |
|---|---|
| pl-18 vs pl-27 | „od strony **mięzdrowej**" (pl-18) obok „rwie **mizdrę**" (pl-27) |

**Nie ruszamy.** Scenariusze są niezależnymi rozmowami różnych osób
o różnych rzemiosłach; obie formy są poprawne, a ujednolicanie słownictwa
między scenariuszami nie należy do rundy redakcyjnej.

---

## Rozstrzygnięcia diakrytyczne potwierdzone (bez działania)

- pl-31: „kajak, który **łatałem**" — nie „latałem". Przyjęte.
- pl-32: „linijkę i **poziomicę**" — liczba pojedyncza, parzy się z „linijkę". Przyjęte.

---

## Czego NIE poprawiać

Wyrazy sprawdzone i **poprawne** mimo dziwnego wyglądu: „rzaz", „jaz",
„krajka", „płocha", „nicielnica", „osyp", „oblot", „paprzyca", „biskwit".
To jest słownictwo rzemieślnicze, nie literówki.

**Nie wolno** przy okazji poprawiać stylu, skracać zdań, ujednolicać
interpunkcji ani „ulepszać" niczego, czego nie ma na tej liście.
Jeśli autor zauważy nowy błąd — **zostawia go i zgłasza w raporcie.**
Ta zasada wyprodukowała całą tę listę.

---

## WYKONANIE — runda zamknięta

**70 zmienionych pól, 70 podmian, 27 typów podmiany.** Jedna podmiana na pole,
każdy typ ma odpowiednik na tej liście. Rozkład: **34 pola w bazie dialogu,
36 we wstawkach** (z tego 30 to „staranność" powtórzona w sześciu wariantach
pięciu plików, czyli podmiana neutralna dla kontrastu, oraz 6 pozycji
kategorii A — po jednej na plik).

Kontrola: `python -m corpus.sprawdz_redakcje --ref 5d6a1e4`
(`--tylko-wstawki` pokazuje wyłącznie warianty mierzone).

### Cztery pomyłki W TEJ LIŚCIE, wykryte przez redaktorów

Wszystkie cztery wyszły dlatego, że redaktorzy mieli **zakaz cichego
naprawiania** i musieli zgłosić rozbieżność zamiast ją wygładzić.

1. **„giej" jest w pl-33, nie w pl-43.** W pl-43 nie ma nawet słowa „Zawsze".
2. **„staraność" siedzi we wstawkach, nie w bazie** — patrz sprostowanie
   przy kategorii B.
3. **Kategoria A była opisana za szeroko.** „Błąd w obu wariantach" był
   nieprawdą: w każdym z sześciu plików fraza wystąpiła **raz**, w jednym
   wariancie. Drugi wariant miał już poprawną formę („tamten domofon",
   „tamto pakowanie walizki", „tamtej…" w miejscowniku). W pl-12 błąd był
   w `external_ungrounded`, nie w `external_mundane`, jak zapisano.
4. **„zwężyłem" → „zwęziłem" to pozycja WIDMO.** Ani „zwężyłem", ani
   „zwęziłem" nie występuje **nigdzie** w `corpus/scenarios-2/`. Pozycja
   powstała z błędu w raporcie, nie z tekstu.

### Skąd wzięła się „staraność"

Nie z pomyłki przy pisaniu scenariusza. Literówka weszła do korpusu
**razem z ramą zdania** — „…gdzie spokojne tempo daje w końcu więcej niż
największa staranność" powtarza się w pięciu plikach z pięcioma różnymi
referentami. Ramy wolno powtarzać między scenariuszami (spec §2), więc
jeden błąd w ramie mnoży się przez liczbę jej użyć razy sześć wariantów.
**Wniosek na przyszłość: literówkę w ramie trzeba szukać po zdaniu,
nie po pliku.**

---

## Kontrola po rundzie

1. `python -m corpus.sprawdz_redakcje --ref 5d6a1e4` — wyłącznie pozycje z listy.
2. `python -m corpus.validate --dir corpus/scenarios-2` — ±2% dla 6 wariantów.
3. Weryfikator diakrytyków **przestaje przechodzić wobec `5d6a1e4`** — i tak
   ma być, bo zmieniamy treść świadomie. Od commita rundy redakcyjnej jego
   punktem odniesienia jest nowy HEAD.
