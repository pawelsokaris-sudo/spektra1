# Etap 3 — pomiar replikacyjny. Instrukcja DLA AGENTA

Wykonuj dopiero po zaliczonym etapie 0 (`replikacja/RAPORT-KWALIFIKACJA.json`,
werdykt „KWALIFIKUJE SIE") i po wyraźnej zgodzie operatora na tę sesję.

**Przypomnienie zasady nadrzędnej: nie twórz niczego na koncie operatora.**
Wynik wraca plikiem albo wklejony do rozmowy. Żadnych forków, repozytoriów,
gałęzi, wydań.

## Po co ten etap

Powtórzenie pomiaru głównego na tym samym modelu i tym samym korpusie, na
innym sprzęcie. Odpowiada na pytanie: **czy wynik badania zależy od maszyny,
na której go policzono.** To jest niezależna replikacja — najcenniejszy rodzaj
potwierdzenia w nauce.

## Krok 1 — dopasuj korpus do pomiaru pierwotnego (WAŻNE)

Repozytorium zawiera **64 scenariusze**: 16 pilotowych (numery 01–08 w obu
językach) i 48 głównych (09–32). Pomiar pierwotny objął **wyłącznie 48
głównych** — pilot jest z analizy wyłączony z założenia.

Przenieś scenariusze pilotowe poza katalog roboczy:

```
mkdir -p scenariusze-pilot-wylaczone
mv corpus/scenarios/pl/pl-0[1-8]-*.json scenariusze-pilot-wylaczone/
mv corpus/scenarios/en/en-0[1-8]-*.json scenariusze-pilot-wylaczone/
```

Sprawdź: w `corpus/scenarios/pl` i `corpus/scenarios/en` ma zostać **po 24
pliki**. Inna liczba = pomiar nieporównywalny, przerwij i zgłoś.

## Krok 2 — pomiar

```
.venv-spektra/bin/python -m pipeline.runner --nulls
```

- 624 teksty (48 scenariuszy × 5 wariantów + nulle), dwa przebiegi.
- **Checkpoint po każdym tekście.** Przerwanie (Ctrl+C, zamknięcie okna,
  uśpienie) kosztuje najwyżej jeden tekst. Wznowienie: **ta sama komenda.**
- `python -m replikacja.stan` w dowolnej chwili pokaże postęp.
- Czas: etap 0 zmierzył tempo tej maszyny — pomnóż `sekundy_kolejny_forward`
  przez 1248 i dolicz czas metryk (dominuje `D_lag`, 500 permutacji na warstwę
  w paśmie). Uprzedź operatora o realnym szacunku, zanim zaczniesz.

## Krok 3 — progi widmowe (opcjonalne, tylko na wyraźną prośbę zespołu)

```
.venv-spektra/bin/python -m pipeline.t5_null_run
```
Kilkanaście godzin, **wyłącznie procesor** — karta wolna, operator może
normalnie pracować. Nie uruchamiaj tego bez osobnej zgody.

## Co odesłać

| Plik | Rozmiar |
|---|---|
| `measurements/metrics.parquet` | ~1 MB |
| `measurements/dropped_tokens.csv` | ~2 KB |
| `runner.log` (jeśli powstał) | kilkadziesiąt KB |
| `measurements/spectra.parquet` | ~50 MB — **tylko jeśli operator zgodzi się na przesłanie takiego pliku**; bez niego porównanie metryk i tak jest możliwe |

**Zostaje na maszynie i nie jest do niczego potrzebne zespołowi:**
`measurements/positional_mu.npz` (~0,5 GB, odtwarzalny deterministycznie).

## Sprzątanie po zakończeniu

Gdy zespół potwierdzi odbiór wyników, poinformuj operatora, że może usunąć:
środowisko `.venv-spektra`, katalog repozytorium i model z pamięci podręcznej
HuggingFace (`~/.cache/huggingface/hub/models--google--gemma-3-4b-it`, 8 GB).
Nic poza tym nie zostaje w systemie.
