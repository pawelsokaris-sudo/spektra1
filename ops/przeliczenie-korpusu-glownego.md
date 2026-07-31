# Przeliczenie korpusu głównego dokładnym tokenizerem — raport wykonania

**Zlecenie:** `ops/DEP-zlecenie-06-przeliczenie-korpusu-glownego.md`
**Wykonał:** DEP (Claude Code w terminalu)
**Data:** 2026-07-31
**Maszyna:** `maszyna-pomiarowa` — **przez Tailscale** (`[adres-tailnet]`); przy okazji droga
zdalna została sprawdzona pod obciążeniem (transfer 364 KB, tokenizacja 320 tekstów), nie tylko
jednym poleceniem.

## Trzy kryteria — werdykt

| Kryterium | Werdykt |
|---|---|
| 1. Zero scenariuszy powyżej 2% w jakimkolwiek kontraście | **PRZESZŁO** — zero wystąpień `⚠ ponad próg 2%` w całym raporcie; walidator kod 0, „WSZYSTKIE SCENARIUSZE OK" |
| 2. Brak `⚠ PRZECHYŁ JEDNOKIERUNKOWY` w kontraście głównym, w obu replikach | **NIE PRZESZŁO dla EN. PRZESZŁO dla PL.** |
| 3. Średnia ze znakiem, kontrast główny, per język | **EN: −0,43%** · **PL: −0,26%** |

Licznik: **`licznik tokenow: DOKLADNY`** — potwierdzone w nagłówku walidatora i raportu.
64 scenariusze (32 EN + 32 PL).

Zgodnie ze zleceniem **korpusu nie poprawiałem.** Poniżej rozbicie, którego zlecenie wymaga przy
zapalonym ostrzeżeniu, plus dane per insercja gotowe do celowanej rundy autorskiej.

---

## Kryterium 2 — rozbicie pilot vs korpus główny

Zlecenie słusznie przewidziało, że detektor liczy po całej replice, a poprawki autorskie mogą
dotyczyć tylko nowych scenariuszy. Rozbicie pokazuje dwie różne historie w każdym języku:

| Replika | Grupa | n | dodatnich | ujemnych | zer | średnia ze znakiem | detektor |
|---|---|---|---|---|---|---|---|
| **EN** | pilot 01–08 | 8 | **0** | 6 | 2 | −0,32% | przechył |
| **EN** | główny 09–32 | 24 | **0** | 23 | 1 | −0,47% | przechył |
| **PL** | pilot 01–08 | 8 | **0** | 7 | 1 | −0,48% | przechył |
| **PL** | główny 09–32 | 24 | **9** | 13 | 2 | −0,19% | **bez przechyłu** |

**Interpretacja — to jest sedno raportu.** W polszczyźnie autorzy **nauczyli się i zastosowali
poprawkę do nowych scenariuszy**: w grupie 09–32 jest 9 różnic dodatnich i 13 ujemnych, czyli
znaki są mieszane, a średnia spadła do −0,19%. Cała replika PL przechodzi tylko dlatego, że te
24 zbalansowane scenariusze rozcieńczają nienaprawiony pilot.

W angielszczyźnie **nie naprawiono ani pilota, ani nowych scenariuszy** — obie grupy są
jednokierunkowe, a nowe są nawet nieco gorsze od pilota (−0,47% wobec −0,32%). To jest dokładnie
ta sytuacja, przed którą ostrzegałem w raporcie ze zlecenia 04: założenie, że „replika EN była
już zbalansowana", pochodziło z heurystycznego licznika i nie potwierdzało się pod dokładnym
tokenizerem. Nowe 24 scenariusze EN powstały z tym samym systematycznym przechyłem.

## Dane per insercja — dlaczego to nie jest problem językowy

Sumy `G − self` per scenariusz (dodatnie = wariant C′-G dłuższy od C, czyli źródło przechyłu),
pełne dane w `ops/insertion_tokens_glowny.txt`:

```
EN (n=32):  dodatnich 29 | zerowych 3 | UJEMNYCH 0    | suma delt +133 tokenow
            najgorsze: en-23 +8, en-30 +8, en-27 +7, en-29 +7, en-31 +7
            zerowe: en-04, en-06, en-18

PL (n=32):  dodatnich 20 | zerowych 3 | UJEMNYCH 9     | suma delt  +76 tokenow
            ujemne: pl-22 -11, pl-23 -9, pl-17 -5, pl-19 -4, pl-21 -4,
                    pl-24 -4, pl-20 -3, pl-12 -1, pl-15 -1
            zerowe: pl-05, pl-10, pl-18
```

**To jest najważniejsza obserwacja tego raportu.** Przy pilocie napisałem, że `G − self` nie jest
ujemne w żadnym z 16 scenariuszy i że wygląda to na systematyczną właściwość konstrukcji —
rzeczownikowa fraza odniesienia zewnętrznego jest w tokenizerze Gemmy droższa od samozwrotnej.
**Polski korpus główny obala tę hipotezę: w dziewięciu scenariuszach udało się zejść poniżej zera**,
w jednym aż o 11 tokenów. Czyli ujemne delty są osiągalne, a brak ujemnych w EN nie wynika
z żadnego ograniczenia językowego ani z tokenizera — po prostu nikt tej repliki nie poprawiał.

### Ile trzeba poprawić, żeby średnia zeszła do zera

Zależność jest prosta i sprawdza się w obu językach: średnia ze znakiem ≈ − (średnia delta
`G − self`) ÷ ~950 tokenów tekstu. Dla EN: 133 ÷ 32 = 4,2 tokena średnio → 0,44%, zgadza się
z −0,43%. Dla PL: 76 ÷ 32 = 2,4 → 0,25%, zgadza się z −0,26%.

Praktycznie: **żeby średnia EN zeszła w okolice zera, trzeba usunąć około 133 tokenów netto**
z wariantu C′-G w replice angielskiej — najlepiej rozłożone tak, żeby część scenariuszy zeszła
poniżej zera.

### Ostrzeżenie: kryterium 2 da się spełnić pozornie

Detektor zapala się, gdy różnic niezerowych jest co najmniej 3 i **wszystkie** mają ten sam znak.
Dla EN wystarczyłoby więc, żeby **jeden jedyny** scenariusz z 32 stał się dodatni — ostrzeżenie
zgaśnie, a kryterium 2 formalnie przejdzie. Ale średnia ze znakiem zmieni się wtedy z −0,43%
na jakieś −0,41%, czyli praktycznie wcale. Skoro kryterium 3 idzie do pakietu pieczęci jako
liczba cytowana, warto mieć świadomość, że **spełnienie kryterium 2 pojedynczym odwróceniem
byłoby zgodne z literą, a puste co do treści**. Piszę to, bo bramka przed pieczęcią to ostatni
moment, żeby taką różnicę zauważyć.

## Kryterium 1 i pozostałe kontrasty

Zero przekroczeń progu 2% w całym raporcie. Dla porządku pełny obraz znaków:

| Kontrast | EN | PL |
|---|---|---|
| C − C′-G (główny) | 0 / 29 / 3 zera, **−0,43%** ⚠ | 9 / 20 / 3 zera, **−0,26%** czysto |
| C′-G − C′-U (diagnostyczny) | 13 / 13 / 6 zer, **+0,03%** czysto | 10 / 19 / 3 zera, **−0,20%** czysto |
| C − B (wtórny) | 1 / 30 / 1 zero, **−0,39%** ⚠ | 5 / 25 / 2 zera, **−0,48%** ⚠ |

Kontrast diagnostyczny w EN wychodzi wzorowo (13 na 13, średnia +0,03%) — co potwierdza, że
problem siedzi wyłącznie w wariancie **grounded**, nie w konstrukcji insercji jako takiej.
Kontrast wtórny C − B jest przechylony w obu językach; kryterium 2 go nie obejmuje, ale
odnotowuję, bo to ta sama choroba.

## Kontrola spójności: pilot odtworzył się co do sztuki

Zlecenie podpowiedziało darmową kontrolę — scenariusze 01–08 nie były ruszane od pomiaru pilota,
więc muszą dać identyczne liczby jak w raporcie ze zlecenia 04. Porównałem programowo wszystkie
16 (liczba tur + pięć wariantów):

```
KONTROLA SPOJNOSCI PILOTA: 16/16 zgodnych co do sztuki, 0 roznic
```

**Zgadza się wszystko**, łącznie z liczbą tur. To potwierdza trzy rzeczy naraz: pliki scenariuszy
pilota są nietknięte, tokenizer na maszynie jest ten sam co przy pomiarze, a cała ścieżka
liczenia jest deterministyczna.

Przy okazji: zgłosiłem po drodze fałszywy alarm, że `en-01` zmienił się strukturalnie z 9 tur
na 7. Czat prowadzący wyprostował przesłankę — **liczba tur zależy od licznika tokenów**, bo
generator tnie scenariusz do budżetu 1024 tokenów na granicy pełnej tury, a heurystyka na
laptopie zawyża znaki na token w angielskim. Powyższa kontrola 16/16 potwierdza to empirycznie.
Zapisuję, bo wniosek jest ogólny: **liczby tur i tokenów porównywać wyłącznie w obrębie tego
samego licznika.**

## Krok 1 — synchronizacja i kontrole

```
paczka: 364534 B | plikow: 171
kontrola wykluczen (.git/ __pycache__ .venv .claude measurements/ tokenizer.json .parquet .npz): (pusto)
scenariuszy w paczce: pl 32 | en 32

PRZED: tokenizer JEST → transfer 364534 B → ROZPAKOWANO-I-USUNIETO → PO: tokenizer.json
liczba scenariuszy na maszynie: pl 32 | en 32
```

**Rozmiar 364 KB przy wzorcu 200–250 KB ze zlecenia** — sprawdziłem, co go napędza, zamiast
uznać za normę: **64 scenariusze to 847 KB nieskompresowane, czyli 74% paczki**. To korpus
urósł czterokrotnie wobec pilota, a nie śmieci — wykluczenia dają pustkę, w szczególności
`measurements/` z 48 MB widm nie weszło.

**Sumy kontrolne: 40/40 zgodnych** (wszystkie `.py` z `pipeline/`, `corpus/`, `nulls/`, `power/`,
`tests/` plus `config.yaml`). Cztery pliki wymagane wprost przez zlecenie:

```
corpus/build.py             1e31b86cca4af9ce
corpus/insertion_tokens.py  7b54b6a7a0cb4fb2
corpus/report.py            77befc445deb6e21
corpus/validate.py          b20f55f1b67cbf04
```

## Warunek startu — zweryfikowany, nie przyjęty na słowo

Zanim cokolwiek wysłałem, sprawdziłem sam (własna lekcja ze zlecenia 04, gdzie omal nie
zmierzyłem stanu częściowego): repo czyste, **64 scenariusze zacommitowane**, numeracja ciągła
01–32 w obu językach, żaden plik scenariusza nie jest zmodyfikowany ani nieśledzony. Lokalny
walidator przechodzi na komplecie (kod 0, licznik heurystyczny), testy **114 zielonych**.

## Co odesłane do repo

| Plik | Rozmiar |
|---|---|
| `corpus/matching_report.md` | 14 444 B (nadpisany, komplet 64, licznik DOKŁADNY) |
| `ops/insertion_tokens_glowny.txt` | 47 839 B (dane per insercja, 64 scenariusze) |
| `ops/validate-glowny.txt` | 5 336 B (pełne wyjście `corpus.validate`, 66 linii) |

Żaden plik tokenizera ani wag nie trafił na laptopa. Zakres zmian na maszynie: wyłącznie
wewnątrz `C:\Users\operator\spektra1`, archiwum transferowe usunięte.

## Co czeka na czat prowadzącego

1. **Replika EN wymaga rundy poprawkowej — pilot i korpus główny razem.** 29 z 32 scenariuszy
   ma wariant C′-G dłuższy od C, żaden nie ma krótszego. Cel liczbowy: około **133 tokeny netto**
   do usunięcia, rozłożone tak, żeby część scenariuszy zeszła poniżej zera. Lista per scenariusz
   i per insercja jest w `ops/insertion_tokens_glowny.txt`.
2. **PL pilot (01–08) też jest jednokierunkowy** — dziś nie zapala ostrzeżenia tylko dlatego, że
   24 nowe scenariusze go rozcieńczają. Do decyzji, czy zostawić, czy dociągnąć przy okazji EN.
3. **Czy kontrast wtórny C − B ma być wyrównywany** — przechylony w obu językach, poza
   kryterium 2.
4. **Świadomość co do kryterium 2:** jedno odwrócenie znaku w EN wyłączy ostrzeżenie, nie
   zmieniając praktycznie średniej cytowanej w pieczęci.
