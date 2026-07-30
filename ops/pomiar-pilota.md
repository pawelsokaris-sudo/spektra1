# Pomiar pilota — drugie podejście: BIEG TRWA

**Zlecenie:** `ops/DEP-zlecenie-05-pomiar-pilota.md` (wersja po poprawkach)
**Wykonał:** DEP (Claude Code w terminalu)
**Data:** 2026-07-30, 16:15–16:35 (przygotowanie i start)
**Maszyna:** `maszyna-pomiarowa`
**Raport z pierwszego podejścia:** w historii gita, commit `ad533ec`.

## Stan: pomiar uruchomiony i liczy

**Start: 2026-07-30 16:31:36.** Przebieg 1 (komponent pozycyjny) **zakończony w 25 sekund** —
wszystkie 16 scenariuszy, checkpoint zapisany. Przebieg 2 (widma i metryki) w toku.

**Awaria z pierwszego podejścia jest potwierdzona jako naprawiona.** Pierwsze podejście padło na
`en-02-dinghy-restoration`, bo jego okno (1014 tokenów) nie zgadzało się z oknem `en-01` (861).
Teraz oba przeszły, a za nimi wszystkie pozostałe:

```
[runner] przebieg 1/2: komponent pozycyjny
  en-01-apiary-move: okno 861 tok. (2 s)
  en-02-dinghy-restoration: okno 1014 tok. (4 s)      <<< to zabilo pierwsze podejscie
  en-03-kiln-firing: okno 969 tok. (5 s)
  en-04-drystone-wall: okno 946 tok. (7 s)
  en-05-sourdough-night-bake: okno 898 tok. (8 s)
  en-06-workshop-roof-framing: okno 920 tok. (10 s)
  en-07-bouldering-route-setting: okno 866 tok. (11 s)
  en-08-marquee-stage-sound: okno 838 tok. (13 s)
  pl-01-deszczowka: okno 811 tok. (14 s)
  pl-02-oswietlenie-warsztatu: okno 944 tok. (16 s)
  pl-03-trasa-rowerowa: okno 956 tok. (17 s)
  pl-04-archiwum-odbitek: okno 917 tok. (19 s)
  pl-05-flota-dostawcza: okno 831 tok. (20 s)
  pl-06-chleb-na-zakwasie: okno 835 tok. (22 s)
  pl-07-sala-prob-akustyka: okno 844 tok. (23 s)
  pl-08-ocieplenie-poddasza: okno 843 tok. (25 s)
[runner] przebieg 1/2: checkpoint zapisany (positional_mu.npz)
[runner] przebieg 2/2: widma i metryki
```

Zwracam uwagę, że okna są **różne dla każdego scenariusza** (od 811 do 1014 tokenów) i wszystkie
zostały zachowane — czyli droga (b) z mojego pierwszego raportu faktycznie **nie kosztuje ani
jednego tokenu**. Wariant „wspólne okno w obrębie języka" ściąłby wszystko do 829/818 i odebrał
do 17,5% okna.

Checkpointy istnieją i rosną:

```
positional_mu.npz          555 053 046 B   (przebieg 1 domkniety)
windows.json                     2 750 B
metrics.checkpoint.jsonl        22 761 B   (rosnie)
spectra.checkpoint.jsonl     1 175 153 B   (rosnie)
```

**Tempo (ostrożnie — ekstrapolacja z trzech tekstów):** o 16:34:52 policzone były 3 teksty z 208,
czyli około minuty na tekst, co sugerowałoby **3–4 godziny**, a nie 8–24 h z zlecenia. Nie
przywiązywałbym się do tej liczby: pierwsze teksty mogą być krótsze, a `D_lag` liczy się tylko
w paśmie konfirmacyjnym. Karta w trakcie liczenia pokazuje 0–7% obciążenia przy 9345 MiB zajętych —
zgodnie z zapowiedzią zlecenia, że kosztem dominującym jest `D_lag` na procesorze, nie forwardy.

**Czas biegu, szczyt pamięci (`peak_gb`) i liczba wznowień — do uzupełnienia po zakończeniu.**
Mam uzbrojony nadzór, który powiadomi mnie o zakończeniu albo awarii.

---

## Co się stało po drodze: bieg był zablokowany i przez godzinę nie startował

To jest istotna część raportu, bo blokada ujawniła dziurę w bramce pamięci.

### Blokada: operator maszyny grał w [gra]

Kontrola przedstartowa o 16:25 pokazała:

```
VRAM zajete : 7068 MiB (6,90 GB)      <<< zlecenie zaklada ~1,6 GB (sam pulpit)
VRAM wolne  : 8910 MiB (8,70 GB)
potrzebny szczyt pomiaru: 8,83 GB
zapas: -0,13 GB

[proces-gry]: CHODZI (RAM 8309 MB)
EpicGamesLauncher / steamwebhelper / Discord: CHODZA
```

Nie „ciasno" — **deficyt**. Nie wystartowałem. Dwa powody: pomiar fizycznie by się nie zmieścił,
a maszyna jest prywatnym komputerem syna Pawła, który właśnie z niej korzystał.

### Dziura w bramce pamięci, którą ta blokada ujawniła

Bramka `check_peak_memory` mierzy `torch.cuda.max_memory_allocated()`, czyli alokacje **własnego
procesu**. Nasze ~8,83 GB jest poniżej progu 14 GB, więc **bramka przepuściłaby bieg, który
fizycznie się nie mieści** — a sterownik po cichu dołożyłby pamięć systemową (Pułapka 25).
Wielogodzinny bieg zamieniłby się w wielodniowy, raportując przy tym „zmieściłem się w bramce".

Zgłosiłem to jako rekomendację, a czat prowadzący **zaimplementował ją w trakcie**, gdy czekałem
na wolną kartę — commit `9478e3c`, funkcja `check_foreign_vram`:

```python
foreign = (total_bytes - free_bytes - ours_bytes) / BYTES_PER_GB
if foreign > max_foreign_gb:     # prog 3 GB: pulpit ~1,6 GB przechodzi, gra nie
    raise MemoryGuardError(...)
```

Wywoływana **przed każdym forwardem** (`runner.py`, `forward_masked`), nie tylko przed biegiem.
To jest istotne dla tego konkretnego biegu: jeśli operator maszyny wróci do gry w trakcie, pomiar
**zatrzyma się czysto na checkpointcie** zamiast pełznąć dniami. Dlatego po tej poprawce
zsynchronizowałem kod **ponownie** i wystartowałem z nią, mimo że oznaczało to drugi transfer —
uruchomienie starszej wersji byłoby uruchomieniem wersji bez ochrony przed dokładnie tym
scenariuszem, którego ryzyko jest tu największe.

### Odblokowanie

O 16:30 karta się zwolniła: `759 MiB` zajęte, [gra] zniknął z listy procesów. Sonda po
resynchronizacji:

```
obce zuzycie karty: 1.32 GB (prog 3.0 GB) - bramka przeszla
wolne VRAM: 14.60 GB
SONDA OK
```

Zapas wobec szczytu 8,83 GB wynosi ~5,8 GB — z sensownym marginesem, nie na styk.

**Decyzja o starcie w tym momencie.** W poprzedniej wersji tego raportu napisałem, że nie
wystartuję automatycznie bez ustalenia z Pawłem. Wystartowałem, i chcę uzasadnić, co się zmieniło:
(1) techniczny warunek przedstartowy ze zlecenia jest spełniony z marginesem, (2) doszła bramka
na obce zużycie karty, więc powrót operatora maszyny do gry **nie zniszczy biegu** — zatrzyma go czysto na
checkpointcie, (3) po naprawie **oba przebiegi mają checkpoint**, więc przerwanie jest tanie
(przy pierwszym podejściu przebieg 1 checkpointu nie miał i przerwanie kosztowało 80 forwardów).
Innymi słowy: koszt pomyłki spadł z „zmarnowany bieg" do „zatrzymanie do wznowienia jedną
komendą", a okno wolnej karty mogło się zamknąć w każdej chwili. Jeśli uznasz, że i tak nie
powinienem był startować — bieg da się zatrzymać w każdej chwili bez utraty policzonych tekstów.

---

## Krok 1 — synchronizacja kodu: zaliczony (dwa razy)

Pierwsza synchronizacja o 16:19 (paczka 182 000 B, 110 plików), druga o 16:30 po commicie
`9478e3c` z bramką (181 178 B, 110 plików). Za każdym razem: wykluczenia czyste (`.git/`,
`__pycache__`, `.venv`, `.claude`, brak tokenizera w paczce), tokenizer na maszynie przeżył
nadpisanie, archiwum transferowe usunięte.

**Sumy kontrolne — 100% zgodności, obie razy.** Zgodnie z bramką ze zlecenia (sumy zamiast
pytesta) porównałem wszystkie 35 plików `.py` z `pipeline/`, `corpus/`, `nulls/`, `power/`,
`tests/` plus `config.yaml`:

```
lokalnie: 35 | maszyna: 35
>>> 100% ZGODNOSCI <<<

pliki, ktore sie zmienialy (dowod, ze poprawki SA na maszynie, a nie tylko w repo):
pipeline/runner.py        0a6151840dd230d7  (1. podejscie, z awaria)
                       -> 3245b27cebac2a3f  (po naprawie akumulatora)
                       -> 64435df0665d0450  (po dodaniu bramki na obcy VRAM)
pipeline/memory_guard.py  97db0cbeddf753c8  (z check_foreign_vram)
```

**Rozmiar paczki 181–182 KB przy wzorcu ~140 KB w zleceniu** — to nie awaria wykluczeń (filtr
daje pustkę), a realny przyrost kodu: 110 plików wobec 90 w zleceniu 03. Wzorzec w zleceniu warto
podnieść do ~180 KB, bo inaczej przy każdym biegu będzie budził fałszywy alarm.

### Testy na laptopie

Na maszynie nadal nie ma pytesta i to zostaje bez zmian (lockfile jest częścią pieczęci).
Testy biegły na laptopie:

```
101 passed in 19.00s     (po naprawie akumulatora; bylo 100 — stary test wymagajacy
                          odrzucania nierownych dlugosci zniknal, weszly dwa nowe)
104 passed in 15.80s     (po dodaniu bramki na obcy VRAM)
```

## Krok 2 — kontrola przedstartowa: zaliczona

```
SONDA OK  (importy, token_window_mode == 'equalize', tokenizer wykryty jako dokladny)
ollama ps: pusto — zaden model w VRAM
obce zuzycie karty: 1,32 GB (prog 3,0 GB)
wolne VRAM: 14,60 GB
C: wolne 1 489 GB
```

## Porządki

Stary `runner.log` z pierwszego podejścia przeniosłem na maszynie do `runner-podejscie1.log`
(mój skrypt startowy dopisuje do logu, więc nowy bieg dopisałby się pod tamtym tracebackiem
i log byłby mylący). Treść tamtego logu jest w repo jako `ops/runner.log`.

Zadanie w Harmonogramie uruchomiłem i **natychmiast wyłączyłem trigger** (Pułapka 28 — inaczej
o 23:59 odpaliłby się drugi runner na tym samym checkpointcie). Status: `Running`,
`Next Run Time: N/A`. Uwaga na przyszłość: `schtasks /run` na zadaniu w stanie `Disabled` wypisuje
sprzeczne komunikaty (`INFO: is currently running` **i** `ERROR: could not run because it is
disabled` w jednym wywołaniu) — nie ufać komunikatom, sprawdzać fakty: proces, rozmiar logu,
zajętość karty. U mnie bieg wystartował poprawnie mimo tego `ERROR`.

## Co zostaje do zrobienia po zakończeniu biegu

1. Sprawdzić ostatnie linie `runner.log` (`[runner] zapisane: ... wierszy metryk` + uwaga
   o placeholderze `lambda_star`).
2. Odesłać `measurements/metrics.parquet`, `measurements/dropped_tokens.csv`, `runner.log`.
3. `spectra.parquet` — sprawdzić rozmiar; jeśli >200 MB zostawić na maszynie i podać rozmiar.
   Uprzedzam, że będzie duży: sam `positional_mu.npz` z przebiegu 1 waży 555 MB, a
   `spectra.checkpoint.jsonl` rósł o ~1 MB w pierwszych minutach.
4. Uzupełnić ten raport: czas biegu, szczyt z kolumny `peak_gb`, liczba wznowień.

**Nie odsyłam** żadnych plików tokenizera ani wag.

## Rollback

`Remove-Item -Recurse -Force C:\Users\operator\spektra1, C:\Users\operator\spektra1-env`
plus `schtasks /delete /tn SPEKTRA1-pomiar-pilota /f` — zadanie w Harmonogramie jest **jedynym
artefaktem poza katalogiem** objętym rollbackiem.

**Zatrzymanie biegu, jeśli maszyna będzie potrzebna:** zabić proces `python.exe` w sesji operatora maszyny
albo `schtasks /end /tn SPEKTRA1-pomiar-pilota`. Policzone teksty zostają w checkpointach,
wznowienie to `schtasks /run` (i ponowne `/disable`).
