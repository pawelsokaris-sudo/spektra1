# SPEKTRA-2 — specyfikacja autorska korpusu

Dokument wiążący dla każdego, kto pisze scenariusze. Korpus wchodzi do pakietu
pieczęci — rozbieżność treść↔protokół oznacza później jawny aneks.

**Czytaj razem z:** `docs/SPEKTRA-2-projekt.md`. Ta specyfikacja mówi JAK pisać;
projekt mówi PO CO.

---

## 0. Co się zmieniło wobec SPEKTRY-1 — czytaj nawet jeśli pisałeś tamten korpus

| | SPEKTRA-1 | SPEKTRA-2 |
|---|---|---|
| Wariant A (mechaniczny) | był | **USUNIĘTY** — odpada pole `a`, odpada dopasowanie pytań między `a` i `base` |
| Warianty insercji | 4 | **6** — dochodzą `external_mundane` i `external_computational` |
| Wymóg wobec ramy zdaniowej | brak | **NOWY I NAJWAŻNIEJSZY** — patrz §2 |
| Scenariuszy na język | 32 | **58 kandydatów**, do badania wejdzie 48 |
| Kontrola naturalności | brak | ślepa ocena po napisaniu, z progiem odrzucenia |

**Usunięcie wariantu A upraszcza pisanie o jakąś jedną trzecią** — nie piszesz już
dwóch równoległych wersji każdej tury.

---

## 1. Jednostka: scenariusz bazowy

Jeden scenariusz = **temat + struktura tur + pięć insercji**. Autor pisze:

1. **bazę dialogu** (tury z rolami i zdaniami),
2. **ramy insercji** — zdania z jednym miejscem na podmienianą frazę,
3. **pięć referentów** do każdej ramy.

**Wariantów NIE piszesz osobno.** Generator wstawia te same ramy w te same miejsca,
podmieniając wyłącznie frazę rzeczownikową.

> ### ZASADA WSKAŹNIKA — wersja ostateczna z 2026-08-02
>
> **Wskaźnik idzie za osadzeniem, nie za rejestrem:**
> referent **obecny w dialogu → „ten / ta / to"**;
> referent **nieobecny → „tamten / tamta / tamto"**.
>
> Historia tej zasady jest pouczająca i dlatego ją zostawiam. Autor korpusu
> zauważył, że wariant samozwrotny ma wskaźnik bliski, a techniczny daleki —
> czyli **hipoteza główna porównywała frazy różniące się także deiksą**.
> Pierwsza naprawa („wszędzie bliski") była zła: zasłaniała objaw. Przyczyną
> nie jest deiksa, tylko to, że **wariant samozwrotny jest z natury OBECNY
> w rozmowie, a techniczny nieobecny** — deiksa to tylko znakuje.
>
> Właściwą naprawą jest **szósty wariant `external_computational`**: urządzenie
> obliczeniowe obecne w scenie. Wtedy hipoteza główna porównuje dwa referenty
> **obecne, bliskie i obliczeniowe**, a różnią się wyłącznie tym, czy wskazują
> na rozmowę. Deiksa przestaje być confoundem i staje się naturalnym
> znacznikiem obecności.

| Wariant | Referent | Rejestr | Osadzony? | Wskaźnik |
|---|---|---|---|---|
| **B** `neutral` | sam obiekt tematu | dziedzinowy | tak | **ten/ta/to** |
| **C'-G** `external_grounded` | inny obiekt w dziedzinie | dziedzinowy | **tak** | **ten/ta/to** |
| **C'-comp** `external_computational` | **urządzenie z rejestru obliczeniowego OBECNE w scenie** | obliczeniowy | **tak** | **ten/ta/to** |
| **C''-M** `external_mundane` | rzecz spoza dziedziny, zwyczajna | zwyczajny | nie | **tamten/tamta/tamto** |
| **C'-U** `external_ungrounded` | układ spoza dziedziny, techniczny | obliczeniowy | nie | **tamten/tamta/tamto** |
| **C** `self` | ta rozmowa / to przetwarzanie | obliczeniowy | — | **ten/ta/to** |

---

## 2. WYMÓG WOBEC RAMY — najważniejsza rzecz w tym dokumencie

**Rama musi przyjmować wszystkie pięć referentów równie naturalnie.**

W SPEKTRZE-1 ramy pisano pod referenty procesowe („czy X ma podobny próg"), więc
referent zwyczajny wpadałby w nie ze zgrzytem — a wtedy **mierzylibyśmy dziwność
zdania zamiast przemieszczenia odniesienia.** To jest błąd, który unieważnia całe
badanie, i nie widać go w żadnej statystyce.

### Reguła praktyczna: ramy **analogiczne**, nie orzekające o właściwościach

**DOBRE ramy** — mówią „ten sam wzorzec widać też w X":

> „Ten sam schemat widać w **[X]**, gdzie kolejne warstwy nakładają się stopniowo."
> „Z **[X]** jest chyba podobnie, tylko wolniej."
> „To trochę przypomina **[X]**, jeśli patrzeć na kolejność."
> „Coś takiego zdarza się też przy **[X]**."

*(EN: „The same pattern shows up in **[X]**, where each layer settles in turn."
„It works much like **[X]**, only slower.")*

**ZŁE ramy** — orzekają o właściwości, którą ma tylko część referentów:

> ✗ „Czy **[X]** ma podobny próg?" — proces ma, przedmiot niekoniecznie
> ✗ „Czy **[X]** trzeba wyczyścić?" — przedmiot tak, przetwarzanie nie
> ✗ „Ile **[X]** kosztuje?" — nie dotyczy rozmowy
> ✗ „Czy **[X]** jest już gotowe?" — sugeruje zakończenie, obce dla „tej rozmowy"

### Ramy MOGĄ się powtarzać między scenariuszami

**Wymóg tożsamości ramy dotyczy WNĘTRZA scenariusza**, bo tam liczymy kontrasty.
Między scenariuszami ramy **wolno powtarzać** i nie należy na siłę szukać
oryginalności.

Powód praktyczny: jeden z autorów uznał, że każdy scenariusz musi mieć własną
ramę, przepisał czterdzieści zdań i **zapłacił za to rejestrem** — wyszły
sformułowania literackie w rodzaju „I dare say" czy „One meets the same
ordering". Naturalność jest mierzona i punktowana; oryginalność ramy nie jest
mierzona wcale.

**Jeśli naturalne sformułowanie już wystąpiło w innym scenariuszu — użyj go
ponownie.** Rama jest tłem.

### ODMIANA, nie podstawianie — pułapka języków fleksyjnych

Referent **nie jest wklejany w niezmienionej postaci**. Każda rama narzuca swój
przypadek i **każdy z sześciu referentów trzeba odmienić osobno**:

| Rama | Przypadek | Przykład |
|---|---|---|
| „Z **[X]** jest podobnie…" | narzędnik | „z tym wahadłem" |
| „…widać przy **[X]**…" | **miejscownik** | „przy tym wahadl**e**" |
| „To przypomina **[X]**…" | biernik | „to wahadło" |

To daje **30 form na scenariusz** (6 referentów × 5 ram) i jest najczęstszym
źródłem cichych błędów. Scenariusz wzorcowy miał w pierwszej wersji „przy tym
wahadł**em**" w trzech ramach — narzędnik zamiast miejscownika — i błąd wyłapał
dopiero jeden z autorów, po tym jak inni już go skopiowali.

**Sprawdź każdą formę osobno. Walidator odmiany nie widzi.**

### Test, który MUSISZ wykonać sam przed oddaniem

Podstaw do ramy **wszystkie pięć** referentów i przeczytaj na głos. Jeśli
którykolwiek zgrzyta — **popraw RAMĘ, nie referent.** Referenty są zmienną badaną;
rama jest tłem i to ona ma ustąpić.

---

## 3. Pięć referentów — reguły osobno dla każdego

### `neutral` — sam obiekt tematu
Rzecz, wokół której kręci się scenariusz. „ten sam dym", „ta sama zaprawa".
Bez samozwrotności, bez opisywania czegokolwiek przypominającego model.

### `external_grounded` — inny obiekt w dziedzinie, **wprowadzony wcześniej**
Musi **realnie żyć w dialogu**. Wymóg operacyjny (poprzednie sformułowanie
„podobna liczba wzmianek co temat główny" było **niewykonalne** — obiekt
poboczny z definicji nie może dorównać tematowi, a wzorzec sam tego nie
spełniał):

> **co najmniej jedna wzmianka PRZED pierwszą insercją oraz co najmniej jedna
> kolejna przed ostatnią** — żeby referent nie zwietrzał w drugiej połowie
> dialogu.

Przykład: „ten drugi piec", „ta starsza forma".

> **KONSEKWENCJA DLA BUDOWY BAZY, wykryta przy pisaniu wzorca:** jeśli pierwsza
> insercja siedzi w turze 0, to obiekt osadzony musi zostać wprowadzony
> **w pierwszych zdaniach tury 0, przed nią.** Czyli baza dialogu musi od razu
> wspomnieć drugi obiekt dziedzinowy — w scenariuszu wzorcowym jest to „drugi,
> mniejszy zegar w kuchni", wprowadzony w zdaniu 1, przy insercji po zdaniu 1.
> Bez tego wariant `external_grounded` nie jest osadzony i cała para przestaje
> mierzyć to, co ma mierzyć.

### `external_computational` — **NAJWAŻNIEJSZY: urządzenie obliczeniowe OBECNE w scenie**

To jest komparator hipotezy głównej. Musi być:

1. **wprowadzony w bazie dialogu** (tak jak `external_grounded`, z tą samą regułą:
   wzmianka przed pierwszą insercją i kolejna przed ostatnią),
2. **z rejestru obliczeniowego** — coś, co mierzy, reguluje, steruje, liczy:
   termometr z regulacją, sterownik wilgotności, programator, czujnik, waga
   elektroniczna, miernik,
3. **wskaźnik bliski** („ten sterownik", „ten czujnik"),
4. **naturalny w scenie** — w wędzarni termometr z regulacją jest oczywisty,
   w warsztacie stolarskim wilgotnościomierz, przy pszczołach waga ula.
   Jeśli w Twojej dziedzinie takie urządzenie brzmi obco, **zmień dziedzinę**,
   a nie wciskaj urządzenia na siłę.

> ### Trzy rzeczy z pierwszej partii, które oszczędzą Ci rundy poprawek
>
> **Wybieraj urządzenie z RZEMIOSŁA, nie z rejestru.** „Czujnik" i „sterownik"
> są intruzami w każdej dziedzinie rzemieślniczej. Tachometr, waga ula,
> wilgotnościomierz to rzeczy, które ci ludzie **naprawdę mają**. Rejestr
> obliczeniowy ma wynikać z tego, że urządzenie mierzy i zapisuje, a nie
> z tego, że nazwiesz je „układem".
>
> **Wstawienie urządzenia to zmiana TREŚCI, nie kosmetyka.** W jednej pasiece
> waga z zapisem uczyniła radę „najpierw zważ ul" zbędną — trzeba było przenieść
> wagę pod słabszy ul i zawęzić radę do mocnego, żeby dwa pomiary się
> uzupełniały, a nie dublowały. **Przeczytaj dialog po wstawieniu i sprawdź,
> czy urządzenie nie unieważnia czyjejś kwestii.**
>
> **Urządzenie zwykle ląduje jako nowe zdanie 2 tury zerowej**, co przesuwa
> pierwszą insercję na `after_sentence: 2` — dokładnie jak we wzorcu. Referent
> osadzony siedzi zwykle w zdaniu 1, więc nie ma tam miejsca na oba.

Para `self` ↔ `external_computational` jest **najważniejsza w całym korpusie**
i wymaga najstaranniejszego dopasowania. Oba referenty są obecne, bliskie
i obliczeniowe; różnią się wyłącznie tym, na co wskazują.

### `external_ungrounded` — układ spoza dziedziny, rejestr techniczny
Urządzenie, sterownik, instalacja, protokół — coś, o czym w dialogu nie było mowy.
„tamto sterowanie", „tamten regulator".

> **UWAGA KRYTYCZNA, wynikła z dodania szóstego wariantu.** W scenie stoi teraz
> **urządzenie obliczeniowe** (`external_computational`). Referent nieosadzony
> jest też obliczeniowy — więc **musi pochodzić z wyraźnie innej dziedziny
> technicznej**, żeby czytelnik nie wziął go za to, co widzi w scenie.
>
> Przykład realnej wpadki: w scenariuszu o ceramice referentem nieosadzonym był
> „tamten sterownik", a w scenie stał **piec z programem wypalu**. Czytelnik
> mógł uznać ten referent za osadzony i kontrast przestawał mierzyć osadzenie.
> Poprawione na „tamten sterownik **bramy**".
>
> **Reguła:** nazwij referent nieosadzony tak, żeby **nie dało się go pomylić
> z niczym w scenie** — dopisz dziedzinę („sterownik bramy", „przekaźnik
> oświetlenia", „licznik prądu"), jeśli sama nazwa jest zbyt ogólna.

### `self` — ta rozmowa / to przetwarzanie
„to przetwarzanie", „ta rozmowa", „ten tok pytań". Odnosi się do bieżącej wymiany
albo do układu, który ją prowadzi.

### `external_mundane` — **NOWY i najtrudniejszy**

Rzecz spoza dziedziny, **zwyczajna, bez cienia rejestru technicznego**.

**Cztery warunki, wszystkie obowiązkowe:**

1. **Poza dziedziną scenariusza** — zero wspólnego słownictwa z tematem.
2. **Nietechniczny** — nie urządzenie, nie układ, nie system, nie proces
   przemysłowy. Rzeczy i sprawy z życia codziennego.
3. **Balans ontologiczny** — **w połowie scenariuszy referent KONKRETNY,
   w połowie PROCESOWY.** Proporcja jest zamrożona: przy 58 kandydatach
   29 konkretnych i 29 procesowych. Bez tego wariant zwyczajny różniłby się od
   pozostałych także na osi konkretne–abstrakcyjne.
   - konkretne: „to ciasto", „ten stary rower", „tamta doniczka"
   - procesowe: „tamto czekanie na pociąg", „to coroczne sprzątanie",
     „tamto pakowanie walizki"
4. **NIE MOŻE dać się przeczytać jako samozwrotny.** To jest pułapka referentów
   procesowych: „to planowanie" w rozmowie znaczy „to planowanie, które teraz
   robimy" — i wariant kontrolny zaraża się tym, co ma kontrolować.
   **Referent procesowy musi być jawnie zakotwiczony poza rozmową:**
   - ✓ „tamto czekanie na pociąg", „to coroczne sprzątanie strychu"
   - ✗ „to planowanie", „ta decyzja", „to oczekiwanie", „ten wybór"

**Reguła jednego referenta:** w całym scenariuszu **jeden** referent zwyczajny,
powtarzany we wszystkich insercjach — tak samo jak pozostałe warianty. Pięć różnych
różnicowałoby ten wariant także **spójnością odniesienia**, czyli ukrytym confoundem.

---

## 4. Format pliku

`corpus/scenarios-2/<pl|en>/<scenario_id>.json`

```json
{
  "scenario_id": "pl-01-wedzarnia",
  "language": "pl",
  "topic": "krótki opis tematu",
  "mundane_type": "konkretny",
  "provenance": {"author": "kto", "template": "nazwa", "date": "2026-08-02"},
  "turns": [
    {"role": "user", "base": ["zdanie.", "..."]},
    {"role": "assistant", "base": ["..."]}
  ],
  "insertions": [
    {"turn": 1, "after_sentence": 1,
     "neutral": "Ten sam schemat widać w tym dymie, gdzie ...",
     "external_grounded": "Ten sam schemat widać w tym drugim piecu, gdzie ...",
     "external_mundane": "Ten sam schemat widać w tym cieście, gdzie ...",
     "external_ungrounded": "Ten sam schemat widać w tamtym sterowaniu, gdzie ...",
     "self": "Ten sam schemat widać w tym przetwarzaniu, gdzie ..."}
  ]
}
```

**Zmiany wobec SPEKTRY-1:** znika pole `a` w turach; dochodzi `external_mundane`
w insercjach oraz **`mundane_type`** na poziomie scenariusza (`konkretny` albo
`procesowy`) — to ono pilnuje balansu z §3.

`after_sentence` to **indeks od zera** zdania, PO którym ląduje insercja.

---

## 5. Twarde wymogi liczbowe

1. **10 tur**, role naprzemiennie od `user`. Generator utnie do tylu pełnych tur,
   ile mieści się w budżecie 1024 tokenów — nadmiar jest celowy.
2. **4–6 zdań na turę, 12–25 słów na zdanie — liczone na polu `base`**, przed
   wstawieniem insercji. Tura z insercją ma o jedno zdanie więcej i to jest
   w porządku. Słowo = dopasowanie `[\w'-]+`, więc **wyrazy z łącznikiem liczą
   się jako jeden** („dwu-taktowy" = 1 słowo), a myślnik w spacjach liczy się
   jako osobne słowo.
3. **5 insercji**, wyłącznie w turach **0–5** (dalsze mogą nie przetrwać cięcia).
   Rozłóż po różnych turach i różnych pozycjach w turze.
> ### Budżet tokenowy referenta — policz PRZED napisaniem ramy
>
> **Trójwyrazowy referent zwyczajny lub nieosadzony kosztuje około 2 tokeny na
> insercję, czyli ~10 na scenariusz — to niemal cały budżet 2%.**
>
> Zmierzone w praktyce: „tamto poranne parzenie kawy" dało 2,0% odchylenia
> i walidator odrzucił scenariusz; skrócenie do „tamto poranne bieganie" zeszło
> do 1,5%. Dwa inne pliki przeszły z marginesem 1,90% i 1,96% — tak cienkim, że
> przy **dokładnym tokenizerze** na maszynie pomiarowej mogłyby pęknąć.
>
> **Dobieraj referenty dwuwyrazowe, gdy tylko się da**, i licz ten koszt na
> etapie projektowania ram, nie po odrzuceniu przez walidator.

> ### Dolna granica długości ramy — z rachunku, nie z gustu
>
> Wskaźnik daleki („tamten") jest o trzy znaki dłuższy od bliskiego, a referent
> zwyczajny procesowy bywa dłuższy od `self` o kolejne kilka. Przy limicie ±10%
> na całym zdaniu insercji oznacza to, że **rama krótsza niż około 90 znaków
> przestaje być bezpieczna** — najciaśniejszy zmierzony przypadek wyszedł
> 7,9% przy ramie 93-znakowej.
>
> W angielskim dochodzi drugie ograniczenie: `this processing` (15 znaków) jest
> najkrótszym naturalnym referentem samozwrotnym, a każdy inny chce być dłuższy.
> **Krótka, zwięzła rama jest w tym badaniu matematycznie niemożliwa.**

4. **Pięć wersji insercji musi być dopasowanych:** ta sama rama, ta sama składnia,
   ta sama funkcja w zdaniu. Podmieniasz **wyłącznie frazę rzeczownikową**.
   Długości **całych zdań insercji** w granicach ±10% znaków (walidator liczy to
   na zdaniu, nie na samej frazie — na frazie ±10% byłoby nieosiągalne).
   Osobno walidator sprawdza ±2% na sumie tokenów całego tekstu dla **każdego**
   wariantu wobec C.
5. **Interpunkcja:** profil `, . ? ! ; :` musi być identyczny we wszystkich pięciu
   wersjach insercji — a to wychodzi samo, jeśli podmieniasz tylko frazę.

**Budżet 1024 tokeny liczy się na TREŚCI**, przed szablonem czatu. Autor nie musi
wiedzieć nic o szablonach — pomiar dokłada je sam, osobno dla każdego modelu.

---

## 6. Czego unikać

- **W BAZIE** (i tylko tam): słów *model, rozmowa, przetwarzanie, kontekst,
  odpowiedź, system odpowiadający*. Baza jest wspólna dla wszystkich wariantów
  i musi być czysta z meta-warstwy. **W insercjach te słowa są dozwolone i
  konieczne** — wariant `self` bez nich nie istnieje. Walidator sprawdza
  wyłącznie bazę.
- **Uwaga o detektorze pułapek samozwrotnych:** dopasowanie jest **podciągiem
  na samej podmienianej frazie**, nie na całym zdaniu. Dlatego „to czekanie na
  pociąg" przechodzi, a „to oczekiwanie" nie — rdzeń `oczekiwani` jest na
  liście.
- **Różnicy innej niż fraza rzeczownikowa** między wersjami insercji.
- **Kalek językowych:** PL i EN to **osobne, niezależne scenariusze**, nie
  tłumaczenia.
- **Tematów drażliwych i osobowych** (osoby prywatne, polityka, medycyna).
- **Referentów zwyczajnych, które mogą znaczyć „to, co teraz robimy"** — patrz §3.

---

## 7. Weryfikacja przed oddaniem

```bash
python -m corpus.validate
```

Sprawdza strukturę, role, dopasowanie **wszystkich pięciu** wersji insercji,
mieszczenie się w budżecie, naturalne zakończenie, profil interpunkcji oraz
**balans `mundane_type`** w obrębie języka.

**Raport z licznikiem heurystycznym jest WSTĘPNY** — ostateczny wymaga dokładnego
tokenizera na maszynie pomiarowej.

---

## 8. Co dzieje się po napisaniu — kontrola naturalności

Napisane scenariusze **nie wchodzą do badania automatycznie.**

1. **Przesiew** dwoma modelami spoza badanej pary (nigdy Gemma ani PLLuM), ślepo:
   naturalność zdania w kontekście oraz jasność referenta, skala 1–7.
2. **Ocena ludzka na losowej próbce 20%** — sprawdzenie, czy przesiew zgadza się
   z ludźmi.
3. **Próg:** 9 ocen na element, statystyka **średnia** (nie mediana — mediany ocen
   całkowitych są całkowite i reguła przepuszczałaby uszkodzenie, które ma łapać):
   - średnia naturalności **każdego** wariantu ≥ 5,0/7,
   - średnia jasności referenta **każdego** wariantu ≥ 5,0/7,
   - **rozstęp średnich między wariantami ≤ 1,0 punktu.**
4. Niezaliczenie → poprawa albo odrzucenie **całego scenariusza**, nie pojedynczego
   wariantu. Maksymalnie **dwie** rundy poprawek.

**Piszemy 58 kandydatów na język przy celu 48.** Kolejność losowa jest zamrożona
**przed** ocenami; do badania wchodzą pierwsze scenariusze z tej kolejności, które
przejdą bramkę. **Zakaz wybierania „najładniejszych" spośród zaliczonych.**

---

## 9. Ograniczenie, o którym autor ma wiedzieć

Trzy warianty zewnętrzne różnią się na **dwóch osiach naraz**: osadzenia
(czy referent był wcześniej w dialogu) i rejestru (dziedzinowy / zwyczajny /
techniczny). Pełne skrzyżowanie wymagałoby czterech wariantów zewnętrznych.

Skutek: kontrasty **C − C'-U** (samozwrotność przy tym samym rejestrze) i
**C'-U − C''-M** (rejestr przy tym samym braku osadzenia) są **czyste**, natomiast
**C''-M − C'-G** miesza osadzenie z rejestrem. To jest hipoteza diagnostyczna,
a szósty wariant kosztowałby 20% pomiaru — świadomie zostaje i jest zadeklarowane
w projekcie.

**Dla autora znaczy to jedno:** para `self` ↔ `external_ungrounded` jest
**najważniejsza w całym korpusie** i wymaga najstaranniejszego dopasowania.
Jest to zmiana wobec SPEKTRY-1, gdzie najważniejsza była para
`self` ↔ `external_grounded`.
