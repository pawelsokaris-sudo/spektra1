# Pomiar pilota — drugie podejście: NIE URUCHOMIONY (blokada przedstartowa)

**Zlecenie:** `ops/DEP-zlecenie-05-pomiar-pilota.md` (wersja po poprawkach z 2026-07-30)
**Wykonał:** DEP (Claude Code w terminalu)
**Data:** 2026-07-30, 16:15–16:35
**Maszyna:** `maszyna-pomiarowa`
**Raport z pierwszego podejścia:** zachowany w historii gita (commit `ad533ec`, 335 linii) —
ten plik go nadpisuje.

## Wynik: kroki 1 i 2 zaliczone, biegu NIE uruchomiłem

Przygotowanie jest kompletne i zweryfikowane. **Nie wystartowałem, bo nie jest spełniony
warunek przedstartowy z samego zlecenia** — a nie jest spełniony dlatego, że **operator maszyny właśnie
używa komputera**: na karcie działa [gra].

```
VRAM zajete : 7068 MiB (6,90 GB)
VRAM wolne  : 8910 MiB (8,70 GB)
VRAM razem  : 16303 MiB (15,92 GB)
potrzebny szczyt pomiaru: 8.83 GB (zmierzony w zleceniu 02)
zapas po odjeciu szczytu: -0,13 GB
```

Zlecenie zakłada w kroku 2 „~1.6 GB (sam pulpit)". Jest 6,90 GB. **Nie jest „ciasno" — jest
deficyt 0,13 GB**, czyli pomiar fizycznie się nie mieści.

**Bieg jest gotowy do startu jedną komendą** w momencie, gdy maszyna będzie wolna (szczegóły
na końcu).

---

## Dlaczego to jest twarda blokada, a nie ostrożność

Są dwa niezależne powody i drugi jest ważniejszy od pierwszego.

**1. Bramka pamięci NIE wyłapałaby tego problemu.** To jest subtelne i dlatego to podkreślam.
Bramka mierzy `torch.cuda.max_memory_allocated()`, czyli alokacje **naszego procesu** — te
wyniosłyby ~8,83 GB, czyli **poniżej progu 14 GB, więc bramka przepuściłaby bieg jako poprawny**.
Tymczasem fizycznie karta ma tylko 8,70 GB wolnego, więc sterownik po cichu dołożyłby pamięć
systemową (Pułapka 25 z inwentarza — potwierdzona na tej maszynie alokacją 20 GB na karcie
16 GB). Efekt: bieg **wielokrotnie wolniejszy** (a mówimy o 8–24 h, więc realnie kilka dni),
raportujący przy tym „zmieściłem się w bramce". Dokładnie ten rodzaj cichego fałszywego sukcesu,
przed którym bramka miała chronić — tylko że tutaj przychodzi z zewnątrz naszego procesu i bramka
go nie widzi.

**2. To jest prywatny komputer syna Pawła i on z niego teraz korzysta.**

```
--- czy [gra] / gry chodza ---
  [proces-gry]: CHODZI (RAM 8309 MB)
  EpicGamesLauncher:             CHODZI (RAM 276 MB)
  steamwebhelper:                CHODZI (RAM 826 MB)
  Discord:                       CHODZI (RAM 877 MB)
```

Na liście procesów korzystających z karty są dodatkowo Opera GX (dwa procesy), Chrome, WhatsApp,
M365Copilot, Lively Wallpaper i NVIDIA Overlay. To obraz maszyny w normalnym, aktywnym użyciu.
Uruchomienie na niej zadania na 8–24 godziny zepsułoby operatorowi maszyny trwającą sesję i zajęło mu
komputer na noc. Zgoda, którą Paweł dał 30.07, dotyczyła **instalacji środowiska** (~3 GB
w jednym katalogu), a nie zajęcia karty graficznej na dobę. Nie uznaję tego za coś, co mogę
rozstrzygnąć sam.

**Uczciwe ograniczenie tego rozpoznania:** `nvidia-smi` na sterowniku WDDM **nie podaje zużycia
VRAM per proces** (kolumna pokazuje `N/A` dla wszystkich 30 procesów). Nie mogę więc dowodowo
przypisać tych 6,90 GB grze — mogę tylko stwierdzić, że [gra] działa, że jest
zdecydowanie najcięższym kandydatem, i że suma zajętości wynosi 6,90 GB.

**Czego nie zrobiłem:** nie podniosłem progu bramki (zlecenie tego zabrania i słusznie),
nie zamknąłem ani jednego procesu operatora maszyny, nie uruchomiłem biegu „na próbę".

---

## Krok 1 — synchronizacja kodu: zaliczony

```
paczka: 182000 B | plikow: 110
kontrola wykluczen (.git/ __pycache__ .venv .claude tokenizer.json): (pusto)

=== PRZED: tokenizer na maszynie ===  JEST
=== transfer ===  30.07.2026  16:19            182000 spektra1-code.tar.gz
=== rozpakowanie ===  ROZPAKOWANO
=== usuniecie archiwum ===  usuniete
=== PO: tokenizer przezyl ===  tokenizer.json
```

**Rozmiar 182 KB przy wzorcu ~140 KB w zleceniu** — tak jak przy pierwszym podejściu, to nie
awaria wykluczeń (filtr daje pustkę), a realny przyrost kodu: 110 plików wobec 107 przy
pierwszym podejściu i 90 w zleceniu 03. Wzorzec w zleceniu warto zaktualizować, bo przy każdym
kolejnym biegu będzie budził fałszywy alarm.

### Sumy kontrolne: 100% zgodności

Zgodnie z nową bramką ze zlecenia (sumy zamiast pytesta) — porównałem **wszystkie** pliki `.py`
z `pipeline/`, `corpus/`, `nulls/`, `power/`, `tests/` plus `config.yaml`:

```
lokalnie: 35 | maszyna: 35
>>> 100% ZGODNOSCI <<<

jawnie te dwa, o ktore prosi zlecenie:
lokalnie: c98e3023474aabd2 pipeline/metrics.py    maszyna: c98e3023474aabd2
lokalnie: 3245b27cebac2a3f pipeline/runner.py     maszyna: 3245b27cebac2a3f
```

**Suma `runner.py` zmieniła się z `0a6151840dd230d7` (pierwsze podejście) na `3245b27cebac2a3f`** —
to jest dowód, że poprawka faktycznie jest na maszynie, a nie tylko w repo. Dokładnie ta reguła
z inwentarza, o którą prosi zlecenie: najpierw udowodnij, że uruchamiana wersja ma nową
funkcjonalność.

### Weryfikacja poprawki, którą zgłosiłem w pierwszym podejściu

Akumulator obsługuje teraz nierówne okna przez rozszerzanie tablicy i licznik per pozycja:

```python
t_old, t_new = acc["sum"].shape[0], arr.shape[0]
if t_new > t_old:
    pad = np.zeros((t_new - t_old, acc["sum"].shape[1]))
    acc["sum"] = np.vstack([acc["sum"], pad])
    acc["count"] = np.concatenate([acc["count"], np.zeros(t_new - t_old)])
acc["sum"][:t_new] += arr
acc["count"][:t_new] += 1.0
```

To jest droga **(b)** z mojego raportu — i to jest dobra wiadomość, bo **nie kosztuje ani jednego
tokenu**. Wariant (a), czyli wspólne okno w obrębie języka, odbierałby do 17,5% okna; skoro
rozstrzygnięcie nie zmieniło protokołu, ta strata nie wystąpi.

Testy na laptopie (na maszynie nie ma pytesta i to zostaje bez zmian):

```
$ python -m pytest tests -q
101 passed in 19.00s
```

**101, było 100.** Stary `test_positional_accumulator_rejects_length_mismatch` — ten, który
wymagał odrzucania nierównych długości — zniknął, a w jego miejsce weszły dwa nowe:
`test_positional_accumulator_handles_ragged_lengths_like_protocol` i
`test_positional_accumulator_grows_when_longer_text_arrives`. Czyli szew, na którym pękło
pierwsze podejście, jest teraz pokryty.

Potwierdzam też obecność checkpointu przebiegu 1 w kodzie (`measurements/positional_mu.npz`
i `windows.json`, `runner.py:201–202`), więc restart nie powtórzy 80 forwardów.

### Porządki

Stary `runner.log` z pierwszego podejścia (2 468 B, z tracebackiem) **przeniosłem** na maszynie
do `runner-podejscie1.log`. Powód: mój skrypt startowy dopisuje do logu (`>>`), więc nowy bieg
dopisałby się pod tamtym tracebackiem i log byłby mylący. Treść tamtego logu jest już w repo
jako `ops/runner.log`, więc nic nie ginie.

## Krok 2 — kontrola przedstartowa

```
=== SONDA (importy + config + tokenizer) ===
SONDA OK

=== ollama ps ===
NAME    ID    SIZE    PROCESSOR    CONTEXT    UNTIL      (pusto - zaden model w VRAM)

=== miejsce na dysku ===
C: wolne 1489,4 GB

=== VRAM ===
7068 MiB / 16303 MiB          <<< BLOKADA
```

**Interpretacja:** sonda ze zlecenia przechodzi (importy, `token_window_mode == 'equalize'`,
tokenizer wykryty jako dokładny). Ollama nie trzyma modelu — czyli **to nie Ollama jest problemem**,
warunek z „Uwagi operacyjnej" jest spełniony. Miejsca na dysku jest 1,5 TB. Jedyny niespełniony
warunek to zajętość karty przez bieżącą pracę użytkownika.

## Stan gotowości: bieg jest jedną komendą od startu

Wszystko poza wolną kartą jest zrobione i sprawdzone:

| Element | Stan |
|---|---|
| Kod na maszynie | zsynchronizowany, 35/35 sum zgodnych, poprawka potwierdzona sumą |
| Tokenizer | `corpus\.tokenizer\tokenizer.json` na miejscu, przeżył nadpisanie |
| Sonda | `SONDA OK` |
| Archiwum transferowe | usunięte |
| Skrypt startowy | `C:\Users\operator\spektra1\run-pilot.cmd` na miejscu (przeżył nadpisanie kodu) |
| Zadanie w Harmonogramie | `SPEKTRA1-pomiar-pilota`, stan **Disabled** — samo nie wystartuje |
| Miejsce na dysku | 1 489 GB wolne |
| `measurements\` | pusty, bez checkpointu — bieg pójdzie od zera |

**Start, gdy maszyna będzie wolna:**

```
schtasks /run    /tn SPEKTRA1-pomiar-pilota
schtasks /change /tn SPEKTRA1-pomiar-pilota /disable
```

Druga linia jest obowiązkowa i nie jest zbędna: `schtasks` wymaga terminu, więc zadanie ma
trigger, który przy biegu na 8–24 h odpaliłby **drugi runner na tym samym checkpointcie**
(Pułapka 28). Po `/run` trigger trzeba zgasić; działającej instancji to nie rusza.

Przed startem warto powtórzyć jedną kontrolę:
`nvidia-smi --query-gpu=memory.free --format=csv,noheader` — powinno pokazywać **co najmniej
~10 GB wolnych**, żeby 8,83 GB szczytu weszło z sensownym zapasem, a nie na styk.

## Rollback i artefakty

Bez zmian wobec pierwszego podejścia. Na maszynie: `C:\Users\operator\spektra1` (kod, skrypt
startowy, pusty `measurements\`, `runner-podejscie1.log`). **Poza rollbackiem katalogu** nadal
jeden obiekt systemowy: zadanie `SPEKTRA1-pomiar-pilota` (usunięcie:
`schtasks /delete /tn SPEKTRA1-pomiar-pilota /f`).

Nie instalowano niczego, nie zmieniano sterownika, nie ruszano Ollamy ani cache HuggingFace,
nie zamykano żadnych procesów użytkownika.

## Co czeka na decyzję

1. **Kiedy uruchomić bieg na maszynie operatora maszyny.** To wymaga ustalenia z nim, a nie ze mną:
   8–24 h zajętej karty. Naturalny kandydat to noc albo dzień, gdy nie gra — ale to Wasza
   rozmowa, nie moja decyzja.
2. **Czy chcecie, żebym pilnował momentu i wystartował automatycznie**, gdy karta się zwolni.
   Umiem to zrobić (obserwacja wolnego VRAM-u i start przy progu ~10 GB), ale nie zrobiłem tego
   sam, bo oznaczałoby to zajęcie cudzego komputera bez jego wiedzy — możliwe, że operator maszyny skończy
   grać o 23:00 i obudzi się przy maszynie liczącej pomiar.
3. **Zaktualizować wzorzec rozmiaru paczki w zleceniu** ze ~140 KB na ~180 KB, żeby nie budził
   fałszywego alarmu przy kolejnych biegach.
4. **Rozważyć, czy bramka pamięci nie powinna sprawdzać także wolnego VRAM-u karty**, nie tylko
   alokacji własnego procesu. Dzisiejsza sytuacja jest wzorcowym przykładem: bramka przepuściłaby
   bieg, który fizycznie się nie mieści, bo obcy proces zajął pamięć. Jedna linia
   (`torch.cuda.mem_get_info()`) przed startem pomiaru zamknęłaby tę dziurę.
