# Przeliczenie korpusu dokładnym tokenizerem po poprawkach — raport wykonania

**Zlecenie:** `ops/DEP-zlecenie-04-przeliczenie-korpusu.md`
**Wykonał:** DEP (Claude Code w terminalu)
**Data:** 2026-07-30, 13:40–14:05
**Maszyna:** `maszyna-pomiarowa` (po nazwie hosta; środowisko i kod z zlecenia 03, nic nie stawiane od nowa)

## Odpowiedzi na trzy pytania, które zlecenie kazało podać jawnie

| Pytanie | Odpowiedź |
|---|---|
| Czy licznik był dokładny? | **TAK** — `licznik tokenow: DOKLADNY`, nagłówek raportu: „Licznik tokenów: **DOKŁADNY** (tokenizer Gemmy)". Tokenizer przeżył podmianę scenariuszy (sprawdzone przed i po). |
| Kryterium 1 — żaden scenariusz powyżej 2%? | **PRZESZŁO.** Zero wystąpień `⚠ ponad próg 2%` w całym raporcie, we wszystkich kontrastach i obu językach. Walidator: kod wyjścia **0**, „WSZYSTKIE SCENARIUSZE OK". Największa różnica w kontraście głównym to 0,89% (pl-04). |
| Kryterium 2 — brak przechyłu jednokierunkowego w C − C′-G? | **NIE PRZESZŁO — w obu replikach.** EN: 0 dodatnich, 6 ujemnych, 2 zera. PL: 0 dodatnich, 7 ujemnych, 1 zero. Oba dostały `⚠ PRZECHYŁ JEDNOKIERUNKOWY`. |
| **Średnia ze znakiem, kontrast główny** | **EN: −0,32%** · **PL: −0,48%** (policzone niezależnie przeze mnie z surowych liczb tokenów — zgadzają się z raportem co do drugiego miejsca) |

Zgodnie ze zleceniem **korpusu nie poprawiałem** — poniżej same liczby i wskazanie, których
scenariuszy dotyczy i w którą stronę.

---

## Dwie rzeczy, które wyszły w pre-flighcie i zmieniły przebieg zlecenia

### 1. Drift kodu: maszyna miała starą wersję `report.py`

Zlecenie mówi „zmieniły się **wyłącznie** pliki w `corpus/scenarios/`. Kod, konfiguracja
i środowisko zostają bez zmian" — ale jednocześnie opisuje **nową kolumnę „różnica ze znakiem"
i nowy detektor `⚠ PRZECHYŁ JEDNOKIERUNKOWY**". To się wyklucza: skoro raport zyskał nową
kolumnę, to `report.py` też się zmienił. Sprawdziłem sumy kontrolne:

```
                     LOKALNIE          NA MASZYNIE
corpus/report.py     77befc445deb6e21  67aa856eed8f3d8d   ← RÓŻNE
corpus/validate.py   b20f55f1b67cbf04  b20f55f1b67cbf04     zgodne
corpus/build.py      1e31b86cca4af9ce  1e31b86cca4af9ce     zgodne
```

Gdybym wysłał tylko scenariusze, jak literalnie każe zlecenie, maszyna wygenerowałaby raport
**starym** kodem — bez kolumny ze znakiem i bez detektora przechyłu. **Kryterium 2 byłoby
nieweryfikowalne**, a ja odesłałbym raport wyglądający poprawnie i nieświadomie zaraportował
„brak ostrzeżenia" jako sukces. Dlatego dołożyłem `report.py` do paczki. Odnotowuję to jawnie
jako wyjście poza literalny zakres zlecenia — uzasadnienie: bez tego jego własne kryterium
zaliczenia nie da się sprawdzić.

Po podmianie: `report.py` na maszynie = `77befc445deb6e21`, zgodny z lokalnym.

To ta sama klasa błędu, co awaria z 2026-04-27 (deploy konfiguracji bez sprawdzenia wersji
binarki). Dopisałem do inwentarza.

### 2. Warunek startu: korpus był poprawiany w trakcie moich kontroli

Zlecenie zawiera warunek startu: „to zlecenie ma sens dopiero, gdy autorzy skończą poprawki".
Pierwsza kontrola stanu repo o ~13:40 pokazała, że **zmieniony jest tylko jeden** z ośmiu
polskich scenariuszy (`pl-05`, niezacommitowany), i to **nie ten**, który oblał próg (`pl-06`).
Wyglądało to na pracę w połowie i byłem gotów zatrzymać zlecenie, żeby nie wydać werdyktu
o poprawce, której jeszcze nie ma.

Zanim to zrobiłem, sprawdziłem fakty do końca — i okazało się, że w trakcie moich kontroli
czat prowadzący **dokończył i zacommitował** całość:

```
f08fcf1 fix(T3): usunięcie systematycznego przechyłu C'-G w replice PL
  corpus/scenarios/pl/pl-01-deszczowka.json
  ... (wszystkie osiem plików PL)
```

Żeby mieć pewność, że mierzę stan aktualny, a nie migawkę z połowy edycji, porównałem sumy
kontrolne wszystkich ośmiu plików PL między laptopem a maszyną — **wszystkie osiem zgadza się
bajt w bajt**:

```
pl-01 56d3596dbb6a | pl-02 cabc9a0cd143 | pl-03 67fe1121a19d | pl-04 5747f41b2a88
pl-05 482e20dcfd38 | pl-06 70cddfccb2ae | pl-07 43b3ca789897 | pl-08 5a6980b98c28
```

**Wniosek: wynik poniżej dotyczy kompletnego, zacommitowanego stanu korpusu po poprawkach.**
Zapisuję ten epizod, bo pokazuje realne ryzyko przy równoległej pracy: gdybym spakował kod
pięć minut wcześniej, zmierzyłbym stan częściowy i odesłał werdykt o niczym.

---

## Krok 1 — podmiana scenariuszy

```
=== KONTROLA PRZED: czy tokenizer jest na miejscu ===
TOKENIZER JEST

$ cd corpus && tar -czf scenarios.tar.gz scenarios report.py
rozmiar: 63721 B | plikow: 20
zawartosc: brak tokenizera w paczce - OK

$ (na maszynie) cd corpus && tar -xzf scenarios.tar.gz  =>  ROZPAKOWANO
$ del scenarios.tar.gz  =>  usuniete

=== KONTROLA PO: tokenizer przezyl podmiane? ===
TOKENIZER JEST
=== report.py na maszynie po podmianie ===
77befc445deb6e21   (zgodny z lokalnym)
```

**Interpretacja:** rozpakowanie archiwum zawierającego `scenarios/` i `report.py` nadpisało
tylko te dwie rzeczy, a katalog `corpus/.tokenizer/` został nietknięty — czyli ostrzeżenie ze
zlecenia zostało obsłużone. Sprawdziłem to **dwa razy**, przed i po, bo utrata tokenizera nie
zgłosiłaby się jako błąd, tylko cicho przestawiła licznik na heurystykę. Archiwum transferowe
usunąłem po rozpakowaniu.

## Krok 2 — przeliczenie

```
$ ...\python.exe -m corpus.validate
Scenariuszy: 16 | licznik tokenow: DOKLADNY
  en-01-apiary-move            en  tur= 9  A= 856 B= 978 C= 972 G= 978 U= 972  OK
  en-02-dinghy-restoration     en  tur=10  A=1019 B=1011 C=1005 G=1011 U=1011  OK
  en-03-kiln-firing            en  tur=10  A= 980 B= 966 C= 960 G= 966 U= 960  OK
  en-04-drystone-wall          en  tur=10  A= 937 B= 965 C= 959 G= 959 U= 965  OK
  en-05-sourdough-night-bake   en  tur=10  A= 889 B= 951 C= 946 G= 948 U= 946  OK
  en-06-workshop-roof-framing  en  tur=10  A= 911 B= 972 C= 968 G= 968 U= 970  OK
  en-07-bouldering-route-setting en  tur=10  A= 857 B= 923 C= 920 G= 922 U= 922  OK
  en-08-marquee-stage-sound    en  tur=10  A= 829 B= 908 C= 905 G= 908 U= 905  OK
  pl-01-deszczowka             pl  tur= 6  A= 818 B= 895 C= 894 G= 895 U= 905  OK
  pl-02-oswietlenie-warsztatu  pl  tur= 7  A= 947 B= 961 C= 958 G= 966 U= 969  OK
  pl-03-trasa-rowerowa         pl  tur= 7  A= 959 B= 970 C= 967 G= 973 U= 973  OK
  pl-04-archiwum-odbitek       pl  tur= 7  A= 920 B=1004 C=1003 G=1012 U=1006  OK
  pl-05-flota-dostawcza        pl  tur= 7  A= 834 B= 979 C= 976 G= 976 U= 977  OK
  pl-06-chleb-na-zakwasie      pl  tur= 7  A= 838 B= 956 C= 955 G= 962 U= 955  OK
  pl-07-sala-prob-akustyka     pl  tur= 7  A= 847 B= 958 C= 949 G= 953 U= 951  OK
  pl-08-ocieplenie-poddasza    pl  tur= 7  A= 846 B= 968 C= 958 G= 960 U= 956  OK
=== WSZYSTKIE SCENARIUSZE OK ===

KOD WYJSCIA: 0
```

```
$ ...\python.exe -m corpus.report
Raport zapisany: ...\corpus\matching_report.md (16 scenariuszy, licznik dokladny)
KOD WYJSCIA: 0
```

**Interpretacja:** kryterium 1 zaliczone z zapasem — walidator nie zgłasza już żadnego problemu
(w zleceniu 03 zgłaszał `pl-06` na 2,15%). Poprawka autorów zadziałała w tym zakresie, do
którego była celowana.

### Poprawka pomogła wyraźnie — ale nie odwróciła kierunku

Porównanie kontrastu głównego dla polskiego, przed poprawką (zlecenie 03) i po:

| Scenariusz | przed | po | zmiana |
|---|---|---|---|
| pl-01-deszczowka | −1,00% | **−0,11%** | poprawa |
| pl-02-oswietlenie-warsztatu | −1,03% | **−0,83%** | poprawa |
| pl-03-trasa-rowerowa | −1,02% | **−0,62%** | poprawa |
| pl-04-archiwum-odbitek | −1,09% | **−0,89%** | poprawa |
| pl-05-flota-dostawcza | −0,61% | **0,00%** | wyrównane do zera |
| **pl-06-chleb-na-zakwasie** | **−2,15% ⚠** | **−0,73%** | próg przestał być łamany |
| pl-07-sala-prob-akustyka | −1,15% | −0,42% | poprawa |
| pl-08-ocieplenie-poddasza | −1,34% | −0,21% | poprawa |
| **średnia ze znakiem** | **≈ −1,05%** | **−0,48%** | **poprawa ponad dwukrotna** |

Każdy scenariusz poszedł w dobrą stronę, jeden trafił dokładnie w zero, a złamanie progu 2%
zniknęło. **Ale znak nie zmienił się w żadnym scenariuszu** — wariant C′-G nadal jest
w każdym przypadku co najmniej tak długi jak C.

### Sprostowanie założenia ze zlecenia: replika EN nigdy nie była zbalansowana

Zlecenie mówi: „Dla repliki EN warunek był spełniony już wcześniej (4 dodatnie, 4 ujemne) —
sprawdź, czy poprawki go nie zepsuły". **Poprawki EN nie zepsuły, bo commit `f08fcf1` w ogóle
nie tknął plików angielskich** — liczby dla EN są dziś **identyczne** jak w zleceniu 03
(en-01 972/978, en-02 1005/1011, en-03 960/966, en-04 959/959, en-05 946/948, en-06 968/968,
en-07 920/922, en-08 905/908 — bit w bit to samo).

Skąd wtedy „4 dodatnie, 4 ujemne"? Z **heurystycznego** licznika, czyli z tego samego szacunku,
który zlecenie 03 zdemaskowało jako zawodny. Pod dokładnym tokenizerem replika EN była
jednokierunkowa **już w zleceniu 03** — po prostu nikt tego wtedy nie policzył pod kątem znaku,
bo detektora przechyłu jeszcze nie było. Praktyczny wniosek: **replika EN wymaga poprawek
dokładnie tak samo jak PL**, a nie tylko „sprawdzenia, czy się nie zepsuła".

### Kontrast wtórny C − B ma tę samą patologię, i to w pełnej skali

Nie jest objęty kryterium 2, ale odnotowuję, bo to ta sama choroba i pewnie ta sama przyczyna:

| Kontrast | EN | PL |
|---|---|---|
| C − C′-G (główny) | 0 dodatnich / 6 ujemnych / 2 zera, **−0,32%** ⚠ | 0 / 7 / 1, **−0,48%** ⚠ |
| C′-G − C′-U (diagnostyczny) | 4 / 2 / 2, **+0,12%** — czysto | 4 / 3 / 1, **+0,05%** — czysto |
| C − B (wtórny) | **0 / 8 / 0**, **−0,51%** ⚠ | **0 / 8 / 0**, **−0,40%** ⚠ |

Kontrast diagnostyczny jest jedynym, który wychodzi zbalansowany — i to w obu językach.
Kontrast wtórny jest przechylony **w komplecie 8 na 8** w obu replikach, mocniej niż główny.

## Krok 3 — kalibracja dla autorów

Pełne wyjście w `ops/insertion_tokens.txt` (164 linie, wszystkie 16 scenariuszy, per insercja).
Poniżej to, co z niego wynika.

**Sumy `G − self` per scenariusz** (dodatnie = wariant C′-G dłuższy od C, czyli źródło przechyłu):

| EN | delta | PL | delta |
|---|---|---|---|
| en-01-apiary-move | **+6** | pl-01-deszczowka | +1 |
| en-02-dinghy-restoration | **+6** | pl-02-oswietlenie-warsztatu | **+8** |
| en-03-kiln-firing | **+6** | pl-03-trasa-rowerowa | **+6** |
| en-04-drystone-wall | 0 | pl-04-archiwum-odbitek | **+9** |
| en-05-sourdough-night-bake | +2 | pl-05-flota-dostawcza | 0 |
| en-06-workshop-roof-framing | 0 | pl-06-chleb-na-zakwasie | **+6** |
| en-07-bouldering-route-setting | +2 | pl-07-sala-prob-akustyka | +4 |
| en-08-marquee-stage-sound | +3 | pl-08-ocieplenie-poddasza | +2 |

**Kluczowa obserwacja: `G − self` nie jest ujemne w ŻADNYM z szesnastu scenariuszy.**
Najlepsze, co udało się osiągnąć, to dokładne zero (pl-05, en-04, en-06). To nie jest szum —
to systematyczna właściwość konstrukcji: rzeczownikowa fraza odniesienia zewnętrznego
(„ten rejestrator", „ten zapis pokładowy") jest w tokenizerze Gemmy zawsze co najmniej tak
droga, jak fraza samozwrotna („to przetwarzanie", „ta wymiana zdań").

Trzy szczegóły, które mogą oszczędzić autorom pracy:

1. **`en-01`, `en-02`, `en-03` mają dokładnie `+1` na KAŻDEJ insercji** (6 insercji, 6 razy +1).
   To jedna powtarzająca się fraza, nie sześć niezależnych problemów — poprawka w jednym
   miejscu załatwia cały scenariusz.
2. **W EN wariant `U − self` bardzo często wynosi dokładnie 0** (en-01, en-03, en-08). Czyli
   problem jest specyficznie w wariancie **grounded**, nie w samej konstrukcji insercji.
   To zgadza się z tym, że kontrast diagnostyczny C′-G − C′-U wychodzi zbalansowany.
3. **`neutral` (wariant B) jest niemal zawsze dłuższy od `self`** — stąd komplet 8/8 w kontraście
   wtórnym. Największe: pl-08 `+10`, pl-07 `+9`.

### Co dokładnie musi się stać, żeby detektor zamilkł

Przeczytałem logikę detektora w `corpus/report.py`, żeby autorzy nie celowali ponownie na oślep.
Warunek zapalenia ostrzeżenia:

```python
n_nonzero = n_pos + n_neg
skew = n_nonzero >= 3 and (n_pos == 0 or n_neg == 0)
```

Czyli ostrzeżenie gaśnie na **dwa** sposoby, i drugi jest chyba łatwiejszy:

- **Droga A — mieszane znaki:** wystarczy, żeby w danym języku **co najmniej jeden** scenariusz
  miał różnicę dodatnią, a co najmniej jeden ujemną. Wymaga, żeby gdzieś fraza grounded była
  **krótsza** od samozwrotnej — dziś nie zdarza się to nigdzie, ale pl-05 pokazuje, że zero jest
  osiągalne, więc minus też powinien być.
- **Droga B — prawie wszystko na zero:** jeśli różnic niezerowych będzie **co najwyżej 2**
  (czyli 6 z 8 scenariuszy trafi dokładnie w zero), ostrzeżenie nie zapali się nawet przy
  jednakowym znaku. Trzy scenariusze już są na zerze, więc do drogi B brakuje trzech kolejnych
  na język.

Uwaga: droga B daje średnią ze znakiem bliższą zeru, a to jest ta liczba, która ma być cytowana
w pakiecie pieczęci — więc prawdopodobnie jest też lepsza merytorycznie, nie tylko łatwiejsza.

## Co odesłane do repo

| Plik | Rozmiar | Uwaga |
|---|---|---|
| `corpus/matching_report.md` | 7 487 B | nadpisany, licznik DOKŁADNY, z kolumną ze znakiem i detektorem przechyłu |
| `ops/insertion_tokens.txt` | 12 195 B | wyjście kroku 3, dokładne tokeny per insercja i wariant |

Pełne wyjście `corpus.validate` jest w tym raporcie wyżej, w całości.

**Kontrola wycieku:** sprawdzone — ani `tokenizer.json`, ani żaden plik wag nie trafił na
laptopa Pawła. Tokenizer został na maszynie pomiarowej.

## Zakres zmian i rollback

Na maszynie: nadpisane `corpus/scenarios/` i `corpus/report.py`, dosłany `corpus/insertion_tokens.py`,
wygenerowane `corpus/matching_report.md` i `insertion_tokens.txt` — wszystko wewnątrz istniejącego
`C:\Users\operator\spektra1`. Archiwum transferowe usunięte. Nie instalowano niczego, nie tworzono
nowych katalogów, nie ruszano środowiska, cache HuggingFace, Ollamy ani sterownika.

Rollback: `Remove-Item -Recurse -Force C:\Users\operator\spektra1, C:\Users\operator\spektra1-env`.

## Co czeka na czat prowadzącego

1. **Kryterium 2 nie przeszło w obu replikach.** Kierunek: wariant C′-G jest wszędzie co najmniej
   tak długi jak C. Dotyczy 6 z 8 scenariuszy EN i 7 z 8 PL (lista z deltami wyżej).
2. **Replika EN wymaga poprawek na równi z PL** — założenie o jej zbalansowaniu pochodziło
   z heurystycznego licznika i nie potwierdza się pod dokładnym tokenizerem.
3. **Do rozważenia, czy kontrast wtórny C − B też ma być wyrównywany** — jest przechylony
   w komplecie 8/8 w obu językach, mocniej niż główny, ale kryterium 2 go nie obejmuje.
4. **Wybór drogi wyjścia (A czy B)** — próg detektora jest teraz znany dokładnie, więc następna
   iteracja może być celowana, a nie zgadywana. Dane per insercja są w `ops/insertion_tokens.txt`.
