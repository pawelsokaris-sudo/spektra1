# Pomiar pilota — raport wykonania (BIEG PADŁ, zero danych)

**Zlecenie:** `ops/DEP-zlecenie-05-pomiar-pilota.md`
**Wykonał:** DEP (Claude Code w terminalu)
**Data:** 2026-07-30, 14:30–15:05
**Maszyna:** `maszyna-pomiarowa` (po nazwie hosta)

## Wynik: STOP

Kroki 1 i 2 zaliczone. **Krok 3 padł po 12 sekundach** — nie na infrastrukturze, nie na pamięci
karty, a na **niespójności projektowej w samym runnerze**. Zgodnie ze zleceniem nie obchodziłem
problemu i nie tknąłem kodu; poniżej pełna diagnoza z liczbami.

```
ValueError: dlugosc 1014 != 861 - po wyrownaniu okna wszystkie teksty
            jezyka musza miec te sama dlugosc
```

**Czas biegu:** 12 s (14:50:32 → 14:50:44).
**Szczyt pamięci:** nie dotyczy — bieg padł w przebiegu 1, przed liczeniem metryk, więc kolumna
`peak_gb` nigdy nie powstała. **Bramka pamięci się nie uruchomiła** (nie było `MemoryGuardError`).
**Liczba wznowień:** 0 (nie ma czego wznawiać — patrz niżej).
**Wyprodukowane dane:** **żadne.** Katalog `measurements\` powstał i jest **pusty**, checkpointu nie ma.

---

## Krok 1 — synchronizacja kodu (pełna)

```
$ tar -czf spektra1-code.tar.gz --exclude=.venv --exclude=.git --exclude='*.npy' \
      --exclude=__pycache__ --exclude=.claude spektra1
rc=0 | rozmiar: 172870 B | plikow: 107
kontrola wykluczen: (pusto)
paczka zawiera tokenizer: brak - OK
```

**Rozmiar 172 KB przy wzorcu ~140 KB ze zlecenia** — sprawdziłem, czy to nie znak, że wykluczenia
nie zadziałały: nie jest. Filtr na `.git/`, `.npy`, `__pycache__`, `.venv`, `.claude` daje pustkę,
a liczba plików wzrosła z 90 (zlecenie 03) do 107. Różnica to realnie nowy kod, który powstał
w międzyczasie: `nulls/`, `power/`, `corpus/insertion_tokens.py` i pięć nowych plików testowych.

```
=== PRZED: tokenizer ===  TOKENIZER JEST
=== rozpakowanie ===      ROZPAKOWANO
=== usuniecie archiwum === usuniete
=== PO: tokenizer ===     tokenizer.json
```

**Weryfikacja sum kontrolnych — szerzej niż wymagało zlecenie.** Zlecenie prosi o dwa pliki
(`runner.py`, `metrics.py`); po nauce z driftu w zleceniu 04 porównałem **cały kod**: 35 plików
`.py` z `pipeline/`, `corpus/`, `nulls/`, `power/`, `tests/` plus `config.yaml`.

```
plikow do porownania: 35 | plikow na maszynie: 35
=== ROZNICE (pusto = kod identyczny) ===
>>> KOD NA MASZYNIE IDENTYCZNY Z LAPTOPEM <<<

jawnie te dwa, o ktore prosi zlecenie:
lokalnie: c98e3023474aabd2 pipeline/metrics.py     maszyna: c98e3023474aabd2
lokalnie: 0a6151840dd230d7 pipeline/runner.py      maszyna: 0a6151840dd230d7
```

**Interpretacja:** zero driftu, tokenizer przeżył nadpisanie (nie ma go w paczce, a `tar` nie usuwa
plików nieobecnych w archiwum), archiwum transferowe usunięte.

## Krok 2 — kontrola przedstartowa

### Bramka pytest: `pytest` nie jest zainstalowany na maszynie pomiarowej

```
$ ...\spektra1-env\Scripts\python.exe -m pytest tests -q
C:\Users\operator\spektra1-env\Scripts\python.exe: No module named pytest
```

To nie jest „coś nie doszło w paczce", jak przewidywało zlecenie — **`pytest` nigdy nie był
instalowany**. Stos ze zlecenia 02 to `transformers accelerate numpy scipy pyarrow pandas
safetensors`, bez narzędzi testowych.

**Nie doinstalowałem go i chcę wyjaśnić dlaczego**, bo to nie jest lenistwo. Środowisko na tej
maszynie jest **zapieczętowane lockfile'em** (`requirements-lock.txt`, część pakietu pieczęci
z T1). Dorzucenie pakietów sprawiłoby, że środowisko, w którym poszedł pomiar, przestaje być tym
opisanym w lockfile'u. Ryzyko dla samego forwardu jest znikome, ale to jest **decyzja
protokolarna**, nie operacyjna — i nie moja.

Zamiast tego zrobiłem dwie rzeczy, które razem dają mocniejszy dowód niż uruchomienie pytesta
na maszynie:

**(a) Pełny zestaw testów na laptopie** (Python 3.13.14, pytest 9.0.2; żaden test nie importuje
`torch`, więc nie potrzebują środowiska pomiarowego):

```
$ python -m pytest tests -q
........................................................................ [ 72%]
............................                                             [100%]
100 passed in 17.72s
```

**Dokładnie 100 testów zielonych** — liczba zgodna z oczekiwaniem ze zlecenia. A skoro kod na
maszynie jest **bajtowo identyczny** (35/35 sum kontrolnych), to deklarowany cel tej bramki
(„czy coś nie doszło w paczce") jest spełniony **bardziej bezpośrednio** przez równość sum niż
przez przebieg testów.

**(b) Kontrola przedstartowa na maszynie**, sprawdzająca to, czego laptop potwierdzić nie może —
czy TO środowisko zaimportuje moduły, wczyta konfigurację i zobaczy tokenizer (bez ładowania modelu):

```
python: 3.14.4  |  cwd: C:\Users\operator\spektra1
--- import modulow ---   OK: pipeline.runner, pipeline.metrics, pipeline.memory_guard,
                             corpus.build, corpus.validate, nulls.interventional, power.permutation
--- biblioteki ---       OK: torch 2.9.1+cu128, transformers 5.14.1, numpy 2.5.1, scipy 1.18.0,
                             pyarrow 25.0.0, pandas 3.0.5, safetensors 0.8.0
--- config ---           token_window_mode = equalize   (nie TBD, start nie jest blokowany)
                         token_budget = 1024 | layer_band = [0.4, 0.8]
                         hf_name = google/gemma-3-4b-it
                         hf_revision = 093f9f388b31de276ce2de164bdc2081324b9767
--- tokenizer ---        corpus\.tokenizer\tokenizer.json | istnieje: True | 33384568 B
--- korpus ---           plikow scenariuszy: 16
--- GPU ---              cuda: True | RTX 5080 | compute capability (12, 0) | bf16: True
=== WYNIK: WSZYSTKO GOTOWE DO STARTU ===   (kod 0)
```

### Stan maszyny przed startem

```
$ ollama ps                    (pusto - zaden model w VRAM)
$ nvidia-smi memory.used        497 MiB / 16303 MiB
```

**Interpretacja:** warunek z „Uwagi operacyjnej" spełniony, karta praktycznie wolna (mniej niż
zakładane ~1,6 GB, bo pulpit był w tym momencie lekko obciążony).

## Krok 3 — uruchomienie

### Pierwsza próba nie przeżyła zamknięcia sesji SSH

Uruchomiłem runner przez `Start-Process -WindowStyle Hidden` (PID 35448, 14:46:20). Po rozłączeniu
i ponownym połączeniu:

```
--- procesy python ---   BRAK procesu python - bieg NIE przezyl
--- runner.log ---       rozmiar: 0 B
--- GPU ---              497 MiB, 1 %
```

**Interpretacja:** proces zginął razem z sesją SSH — serwer SSH na Windows sprząta drzewo procesów
sesji, a `Start-Process` tego nie omija. Dobrze, że sprawdziłem to empirycznie przez rozłączenie,
a nie założyłem, że „hidden = odczepiony": inaczej zameldowałbym uruchomiony bieg, którego nie ma.

### Druga próba: Harmonogram zadań Windows

Zlecenie dopuszcza wprost („zadanie w tle / `start /b` / harmonogram — wedle Twojego uznania"),
więc przeszedłem na harmonogram. Żeby uniknąć piekła cudzysłowów, wgrałem skrypt startowy
`run-pilot.cmd` **do środka `spektra1\`** (czyli w obrębie rollbacku):

```
POTWIERDZONE: run-pilot.cmd na miejscu
SUCCESS: The scheduled task "SPEKTRA1-pomiar-pilota" has successfully been created.
SUCCESS: Attempted to run the scheduled task "SPEKTRA1-pomiar-pilota".
SPEKTRA1-pomiar-pilota    N/A    Running
python.exe   34884   Console   2   585 836 K      (sesja konsolowa - ma dostep do karty)
```

Dwie decyzje, które podjąłem po drodze:

1. **Log dopisywany (`>>`), nie nadpisywany.** Zlecenie podaje `> runner.log`, ale przy wznawianiu
   nadpisanie zgubiłoby historię poprzednich podejść, a zlecenie każe raportować liczbę wznowień.
   Skrypt dopisuje znacznik czasu przy każdym starcie, więc wznowienia są widoczne w jednym pliku.
2. **Natychmiast wyłączyłem trigger zadania.** `schtasks /create` wymaga harmonogramu, więc zadanie
   dostało termin 23:59 tego samego dnia. Przy biegu planowanym na 8–24 h ten trigger odpaliłby
   **drugi runner na tym samym checkpointcie i tych samych plikach wyjściowych** w trakcie
   pierwszego. Po uruchomieniu zrobiłem `schtasks /change /disable` — zadanie pokazuje
   `Next Run Time: N/A`, a już działająca instancja nie została tym tknięta.

### Bieg padł po 12 sekundach

Pełny `runner.log` jest w `ops/runner.log`. Istotna część:

```
[runner] google/gemma-3-4b-it @ 093f9f388b31
Loading weights: 100%|##########| 883/883 [00:02<00:00, 398.05it/s]
[runner] przebieg 1/2: komponent pozycyjny
  en-01-apiary-move: okno 861 tok. (2 s)
Traceback (most recent call last):
  File "C:\Users\operator\spektra1\pipeline\runner.py", line 282, in <module>
    sys.exit(main())
  File "C:\Users\operator\spektra1\pipeline\runner.py", line 210, in main
    pos_acc[lang][li] = accumulate_positional(pos_acc[lang][li], arr[:n])
  File "C:\Users\operator\spektra1\pipeline\runner.py", line 77, in accumulate_positional
    raise ValueError(
ValueError: dlugosc 1014 != 861 - po wyrownaniu okna wszystkie teksty jezyka
            musza miec te sama dlugosc
[DEP] proces zakonczony, kod wyjscia=1
```

Model wczytał się poprawnie z lokalnego cache, właściwa rewizja, pierwszy scenariusz policzony
(okno 861 tokenów) — i awaria na **drugim** scenariuszu tego samego języka.

---

## Diagnoza: okno liczone per scenariusz, komponent pozycyjny akumulowany per język

To nie jest błąd losowy ani problem środowiska. To niespójność między dwiema decyzjami
projektowymi, które osobno są poprawne:

- **Okno wyrównywane jest w obrębie scenariusza.** `runner.py:202` liczy `n = min(lengths.values())`,
  gdzie `lengths` to długości pięciu **wariantów jednego scenariusza**. Docstring `equalize_scenario`
  mówi to wprost: „wspólne okno = min T′ **po wariantach scenariusza** (protokół §4, aneks)".
- **Komponent pozycyjny akumulowany jest per język.** `runner.py:207–210` wrzuca `arr[:n]` do
  `pos_acc[lang]`, wspólnego dla **wszystkich scenariuszy danego języka**.

Skoro każdy scenariusz ma własne `n`, to drugi scenariusz przynosi tablicę innej długości
i akumulator ją odrzuca.

**Bramka w akumulatorze jest zamierzona, nie przypadkowa.** Sprawdziłem testy — istnieje
`tests/test_runner.py::test_positional_accumulator_rejects_length_mismatch`, który **wymaga**
tego wyjątku:

```python
def test_positional_accumulator_rejects_length_mismatch():
    acc = accumulate_positional(None, np.ones((10, 3)))
    with pytest.raises(ValueError, match="dlugosc"):
        accumulate_positional(acc, np.ones((9, 3)))
```

Czyli to nie akumulator jest do naprawy „bo za surowy" — to **strona wywołująca łamie jego
kontrakt**. Rozstrzygnięcie należy do kierownika badania, bo zmienia definicję komponentu
pozycyjnego, a ta wchodzi do pieczęci.

### Dlaczego 100 testów przeszło, a runner padł na drugim scenariuszu

Testy sprawdzają `accumulate_positional` i `equalize_scenario` **osobno** i oba są poprawne.
Nie ma testu integracyjnego, który przepuściłby przez przebieg 1 **dwa scenariusze tego samego
języka o różnych oknach** — a to jest dokładnie ten szew, na którym pękło. Zielony zestaw testów
nie był tu fałszywy; był po prostu niekompletny w jednym konkretnym miejscu.

### Skala kompromisu, jeśli wybrana będzie droga „wspólne okno całego języka"

Policzyłem, ile tokenów kosztowałoby ujednolicenie okna w obrębie języka. Podstawa: dokładne
liczby tokenów z `corpus.validate` (zlecenie 04). Runner raportuje okna o kilka tokenów większe
(861 wobec 856 dla en-01, 1014 wobec 1005 dla en-02) — różnica to maskowanie tokenów specjalnych —
więc traktować poniższe jako bardzo dobre przybliżenie, nie wartości dokładne.

**Wariant obecny (okno = min po wszystkich pięciu wariantach, czyli z wariantem A):**

| Język | okno per scenariusz | wspólne okno języka | największa strata |
|---|---|---|---|
| EN | od 829 (en-08) do 1005 (en-02) | **829** | **176 tok. = 17,5%** okna en-02 |
| PL | od 818 (pl-01) do 959 (pl-03) | **818** | **141 tok. = 14,7%** okna pl-03 |

**Gdyby wariant A nie brał udziału w wyrównywaniu okna** (A z definicji nie ma insercji i jest
krótszy, a kontrast C−A jest w protokole i tak wtórny):

| Język | okno per scenariusz | wspólne okno języka | największa strata |
|---|---|---|---|
| EN | od 905 (en-08) do 1005 (en-02) | **905** | 100 tok. = 10,0% |
| PL | od 894 (pl-01) do 1003 (pl-04) | **894** | 109 tok. = 10,9% |

Czyli wyłączenie wariantu A z wyrównywania odzyskuje ~76 tokenów w EN i ~76 w PL i redukuje
najgorszą stratę z ~17% do ~10%. Czy to jest dopuszczalne, zależy od tego, czy komponent pozycyjny
ma być liczony na tym samym zestawie wariantów, co metryki — na to nie umiem odpowiedzieć i nie
próbuję.

### Ostrzeżenie o wznawianiu: przebieg 1 nie ma checkpointu

Zlecenie zapewnia, że „przerwanie NIE marnuje biegu", i to prawda **dla przebiegu 2** — tam
checkpoint jest po każdym tekście (`runner.py:217–224`). Ale **przebieg 1 (komponent pozycyjny)
checkpointu nie ma w ogóle**: to 80 forwardów liczonych od zera przy każdym starcie. Awaria
wystąpiła właśnie w przebiegu 1, dlatego nie ma czego wznawiać i katalog `measurements\` jest pusty.
Warto o tym wiedzieć przy planowaniu kolejnych podejść: dopóki przebieg 1 się nie domknie, każde
przerwanie kosztuje pełne 80 forwardów (kilka minut, więc nie jest to dramat — ale nie jest to
też „wznawianie od miejsca przerwania").

---

## Co odesłane do repo

| Plik | Rozmiar | Uwaga |
|---|---|---|
| `ops/runner.log` | 2 426 B | pełny log biegu z tracebackiem |
| `ops/pytest-laptop.log` | 184 B | dowód 100/100 z laptopa |

**Nie odesłano** `metrics.parquet`, `spectra.parquet` ani `dropped_tokens.csv` — **nie powstały**.
Żaden plik tokenizera ani wag nie trafił na laptopa.

## Co zostało na maszynie (i jak to usunąć)

| Artefakt | Gdzie | Objęty rollbackiem? |
|---|---|---|
| `run-pilot.cmd` | `C:\Users\operator\spektra1\` | tak |
| pusty katalog `measurements\` | `C:\Users\operator\spektra1\` | tak |
| `runner.log` | `C:\Users\operator\spektra1\` | tak |
| **zadanie `SPEKTRA1-pomiar-pilota`** | Harmonogram zadań Windows | **NIE — to obiekt systemowy** |

Zadanie jest **wyłączone** (`Disabled`, `Next Run Time: N/A`), więc samo nie wystartuje.
Zostawiam je świadomie, bo kolejne podejście po poprawce kodu będzie go potrzebowało —
uruchomienie to `schtasks /run /tn SPEKTRA1-pomiar-pilota` (i pamiętać o ponownym
`/disable` po starcie, jeśli trigger zostanie włączony). Usunięcie, jeśli zapadnie inna decyzja:

```
schtasks /delete /tn SPEKTRA1-pomiar-pilota /f
```

Odnotowuję to jawnie, bo jest to jedyna rzecz, jaką ten pomiar zostawił **poza** katalogiem
objętym rollbackiem.

Nie instalowano niczego, nie zmieniano sterownika, nie ruszano Ollamy ani cache HuggingFace.

**Rollback:** `Remove-Item -Recurse -Force C:\Users\operator\spektra1, C:\Users\operator\spektra1-env`
plus powyższe `schtasks /delete`.

## Rzecz, którą zrobiłem źle

W trakcie pracy maszyna na moment zniknęła z sieci (`Connection timed out` — przejściowy zanik
Wi-Fi; po chwili i nazwa, i adres działały normalnie). Trafiło to w moment wysyłania skryptu
startowego, a **mój skrypt wypisał „POTWIERDZONE: skrypt wgrany" bezwarunkowo**, mimo że `scp`
właśnie padł. Zauważyłem to przy następnym kroku i powtórzyłem transfer z prawdziwą weryfikacją
(`if exist` na maszynie). Zgłaszam, bo przez kilkadziesiąt sekund miałem w logu nieprawdziwe
potwierdzenie — dokładnie ten rodzaj komunikatu, który przy dłuższym biegu mógłby wprowadzić
w błąd.

## Co czeka na czat prowadzącego

1. **Rozstrzygnąć niespójność okno-per-scenariusz vs komponent-pozycyjny-per-język.** Trzy widoczne
   drogi: (a) wspólne okno w obrębie języka (koszt do 17,5% okna, tabela wyżej), (b) akumulator
   pozycyjny tolerujący różne długości z licznikiem per pozycja — struktura `count` jest już
   wektorem, więc zmiana jest niewielka, ale trzeba wtedy zmienić też test, który obecnie wymaga
   odrzucenia, (c) wyłączenie wariantu A z wyrównywania okna, co samo w sobie nie naprawia
   problemu, ale zmniejsza koszt drogi (a) z ~17% do ~10%.
2. **Dodać test integracyjny przebiegu 1 na dwóch scenariuszach jednego języka o różnych oknach** —
   bez tego ta sama klasa błędu wróci przy pomiarze głównym, już po pieczęci.
3. **Zdecydować w sprawie `pytest` na maszynie pomiarowej.** Bramka ze zlecenia jest nieuruchamialna
   w obecnym środowisku. Albo świadomie dopuścić rozejście się środowiska z zapieczętowanym
   lockfile'em o pakiety testowe, albo trwale zmienić bramkę na „testy na laptopie + równość sum
   kontrolnych", jak zrobiłem tutaj.
4. **Rozważyć checkpoint dla przebiegu 1**, jeśli docelowy pomiar główny ma być dłuższy niż pilot.
