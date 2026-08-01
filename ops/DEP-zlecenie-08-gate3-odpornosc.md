# DEP — Zlecenie 08: GATE 3, odporność wyniku (wersja chuda)

**Maszyna:** ta sama co w zleceniach 02–07, dostęp bez zmian.
**Katalog roboczy:** ten sam; dalej wyłącznie ścieżki względne.
**Środowisko:** bez zmian, **nic nie instalować**.
**Czas:** szacunkowo **3–4 h łącznie** (dwa biegi), całość wznawialna.

## Po co to jest — jedno zdanie

Pomiar główny dał efekt **odwrotny do przewidywanego**, ale niemal doskonale
zgodny (ujemny w 24/24 scenariuszach EN i 23/24 PL). To zlecenie odpowiada na
jedno pytanie: **czy ten efekt jest prawdziwy, czy jest artefaktem precyzji
liczb albo odejmowania komponentu pozycyjnego.** Nic poza tym nas tu nie
interesuje — dlatego biegi obejmują wyłącznie dwa warianty (C i C′-G), a nie
wszystkie pięć.

## Krok 0 — przygotowanie katalogów (KLUCZOWE, nie pomijać)

Okno pomiarowe to minimum po **wszystkich pięciu** wariantach, a komponent
pozycyjny liczy się ze wszystkich. Bieg ograniczony do dwóch wariantów
policzyłby **inne okno i inne mu**, czyli porównywałby dwa różne pomiary
zamiast izolować badaną zmianę — i nie byłoby tego widać w wynikach.

Dlatego oba biegi kontrolne startują na **gotowych plikach z biegu głównego**.
Runner **odmówi startu**, jeśli ich nie znajdzie (zabezpieczenie w kodzie).

```
mkdir gate3-fp32
mkdir gate3-nopos
copy measurements\windows.json gate3-fp32\
copy measurements\positional_mu.npz gate3-fp32\
copy measurements\windows.json gate3-nopos\
copy measurements\positional_mu.npz gate3-nopos\
```

(Na maszynie wyniki biegu głównego leżą w `measurements\` — potwierdzone
w Twoim raporcie ze zlecenia 07.)

**Najpierw zsynchronizuj kod** — runner dostał dziś przełączniki, których
poprzednia wersja nie ma. Bez nich polecenia niżej nie zadziałają. Po
rozpakowaniu sprawdź, że przełączniki istnieją:

```
..\spektra1-env\Scripts\python.exe -m pipeline.runner --help
```
Muszą się pojawić: `--dtype`, `--no-positional`, `--variants`, `--per-language`,
`--out`. Jeśli ich nie ma — paczka nie doszła, **STOP**.

## Krok 1 — GATE 3a: bf16 wobec fp32 (~2–3 h)

```
..\spektra1-env\Scripts\python.exe -m pipeline.runner --dtype fp32 --variants C,CprimG --per-language 12 --out gate3-fp32
```

- 48 tekstów (12 scenariuszy × 2 języki × 2 warianty).
- **fp32 przelewa się do RAM** — to jest zgodne z protokołem i zamierzone:
  kontrola ma izolować wyłącznie precyzję, więc zostaje na **tym samym
  urządzeniu**. Będzie wolniej niż zwykle; to nie jest awaria.
- Bramka pamięci może krzyknąć — jeśli zatrzyma bieg, podaj komunikat i STOP.

## Krok 2 — GATE 3b: bez odejmowania komponentu pozycyjnego (~1 h)

```
..\spektra1-env\Scripts\python.exe -m pipeline.runner --no-positional --variants C,CprimG --per-language 24 --out gate3-nopos
```

- 96 tekstów (24 scenariusze × 2 języki × 2 warianty), bf16, normalna prędkość.
- Runner wypisze `GATE 3b: komponent pozycyjny NIE jest odejmowany` — jeśli
  tego nie ma, uruchomiłeś złą wersję kodu.

## Krok 3 — co odesłać

Do `measurements-glowny\` na laptopie (jak przy zleceniu 07), w podkatalogach
`gate3-fp32\` i `gate3-nopos\`:

| Plik | Rozmiar ~ |
|---|---|
| `gate3-fp32/metrics.parquet` + `spectra.parquet` | ~6 MB |
| `gate3-nopos/metrics.parquet` + `spectra.parquet` | ~12 MB |

Sumy SHA-256 obu plików `spectra.parquet` w raporcie. **Nie odsyłać**
`positional_mu.npz` (kopie tego samego pliku co w biegu głównym).

**Nie licz metryk ani kontrastów** — tak samo jak przy zleceniu 07. Progi λ\*
do tych biegów zostaną wzięte z pomiaru głównego po stronie laptopa.

## Raport (`ops/gate3-odpornosc.md`)

1. Liczba tekstów w każdym biegu (oczekiwane: 48 i 96) i czas każdego.
2. `max(peak_gb)` **osobno dla obu biegów** — wymóg zamrożony w ANEKS-2;
   przy fp32 spodziewamy się wartości wyraźnie wyższej niż 8,85 GB z biegu
   głównego i to jest normalne.
3. Czy runner wypisał komunikaty `GATE 3a` / `GATE 3b`.
4. Cokolwiek odbiegło: ostrzeżenia pamięci, przerwania, wznowienia.
5. Sumy SHA-256.

Zakres zmian: wyłącznie wewnątrz katalogu roboczego. Rollback: skasować
`gate3-fp32\` i `gate3-nopos\`, nic więcej nie zostaje.

## Czego to zlecenie świadomie NIE robi

Progi λ\* **nie są przeliczane** dla biegów kontrolnych — to kosztowałoby
kolejny dzień, a kryterium GATE 3 dotyczy **znaku i względnej zmiany** efektu,
nie bezwzględnej wartości wskaźnika. Ograniczenie będzie jawnie napisane
w raporcie końcowym: kryterium znaku jest mocne, kryterium wielkości
przybliżone. Kryterium GATE 3c (obie repliki osobno) jest **już policzone**
z pomiaru głównego i nie wymaga maszyny.
