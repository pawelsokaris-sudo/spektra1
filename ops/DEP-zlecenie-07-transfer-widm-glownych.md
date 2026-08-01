# DEP — Zlecenie 07: transfer widm i progów korpusu głównego (odblokowanie GATE 2)

**Maszyna:** ta sama co w zleceniach 02–06, dostęp bez zmian (LAN albo Tailscale).
**Katalog roboczy:** ten sam co w zleceniach 02–06 — w komendach niżej wołany
przez `cd`, dalej wyłącznie ścieżki względne.
**Środowisko i kod:** ze zleceń 02–05, **nic nie instalować**.
**Charakter:** wyłącznie weryfikacja kompletności i transfer plików. Zero
obliczeń modelu, zero dotykania karty. To ostatni krok przed analizą
konfirmacyjną — po nim otwiera się zamknięta szuflada wyników.

> **UWAGA O ŚCIEŻKACH (ważne przy czytaniu starszych zleceń).** Repozytorium
> przeszło 2026-08-01 anonimizację danych osobowych, która podmieniła nazwę
> konta w treści **wszystkich** plików, w tym w zleceniach 02–06. Ścieżki
> widoczne dziś w tamtych dokumentach **nie są dosłowne** — realny katalog
> roboczy jest niezmieniony od zlecenia 02 i znasz go ze swojej sesji.
> To zlecenie celowo nie zawiera żadnej nazwy konta: instrukcje operacyjne
> i dane osobowe nie mogą mieszkać w tym samym pliku.

> **WARUNEK STARTU:** `pipeline.t5_null_run` zakończone. Sprawdzenie poniżej
> jest częścią zlecenia — jeśli progów jest mniej niż 672, **STOP**, odeślij
> samą liczbę i czekaj. Analiza na częściowych progach policzyłaby endpoint
> różną miarą dla różnych scenariuszy, co jest gorsze niż brak wyniku.

## Krok 0 — wejście do katalogu roboczego

```
cd <katalog roboczy spektra1 z zleceń 02-06>
```
Dalsze komendy zakładają, że jesteś w nim, i używają wyłącznie ścieżek
względnych: interpreter to `..\spektra1-env\Scripts\python.exe` (katalog
środowiska jest rodzeństwem katalogu repozytorium, tak jak od zlecenia 02).

## Krok 1 — kontrola kompletności (nic nie przesyłaj przed nią)

```
..\spektra1-env\Scripts\python.exe -c "import pandas as pd; t=pd.read_parquet('measurements-glowny/t5_lambda_star.parquet'); s=pd.read_parquet('measurements-glowny/spectra.parquet'); print('lambda* wierszy:', len(t)); print('scenariuszy:', t.scenario_id.nunique()); print('warstw pasma:', sorted(t.hidden_state_index.unique())); print('jezyki:', sorted(t.language.unique())); print('widm wierszy:', len(s)); print('braki lambda*:', t.lambda_star.isna().sum())"
```

Wartości **wymagane** (inne = STOP i raport):

| Wielkość | Wartość |
|---|---|
| wierszy `t5_lambda_star` | **672** (48 scenariuszy × 14 warstw pasma) |
| scenariuszy | **48** |
| warstwy pasma | **14–27** |
| języki | **en, pl** |
| wierszy `spectra` | **21216** (624 teksty × 34 warstwy) |
| braków `lambda_star` | **0** |

## Krok 2 — podział widm per język (limit rozmiaru)

Widma korpusu głównego to ~145 MB (pilot: 50,8 MB przy 208 tekstach, główny ma
624). Pojedynczy plik przekracza limit 100 MB na plik, więc **dzielimy per
język** — tak jak przewidywał rachunek z listy kontrolnej pieczęci:

```
..\spektra1-env\Scripts\python.exe -c "import pandas as pd; s=pd.read_parquet('measurements-glowny/spectra.parquet'); [s[s.language==l].to_parquet(f'measurements-glowny/spectra-{l}.parquet', index=False) or print(l, len(s[s.language==l])) for l in sorted(s.language.unique())]"
certutil -hashfile measurements-glowny\spectra-en.parquet SHA256
certutil -hashfile measurements-glowny\spectra-pl.parquet SHA256
certutil -hashfile measurements-glowny\t5_lambda_star.parquet SHA256
```

Każdy plik per język ma mieć **10608** wierszy. Sumy SHA-256 podaj w raporcie —
posłużą do sprawdzenia transferu po drugiej stronie.

## Krok 3 — co odesłać

| Plik | Rozmiar ~ |
|---|---|
| `measurements-glowny/spectra-en.parquet` | ~72 MB |
| `measurements-glowny/spectra-pl.parquet` | ~72 MB |
| `measurements-glowny/t5_lambda_star.parquet` | ~40 KB |
| `measurements-glowny/t5_phi.json` | ~3 KB |
| log biegu T5, jeśli powstał | kilkadziesiąt KB |

**NIE odsyłać:** wag modelu, tokenizera, `positional_mu.npz` (~0,5 GB,
odtwarzalny deterministycznie i do niczego niepotrzebny w analizie).

## Raport (`ops/transfer-widm-glownych.md`)

1. Komplet liczb z kroku 1 — jawnie, obok wartości wymaganych.
2. Sumy SHA-256 z kroku 2.
3. `max(peak_gb)` z całego biegu głównego — wchodzi do raportu GATE 3
   (wymóg zamrożony w ANEKS-2). Dla porównania: pomiar główny dał 8,85 GB.
4. Czy w trakcie T5 pojawiło się cokolwiek nieoczekiwanego (przerwania,
   wznowienia, ostrzeżenia pamięci).

**Konwencja pisania raportów po anonimizacji:** w raportach trafiających do
repozytorium nie umieszczaj nazwy konta, nazwy hosta w sieci lokalnej ani
adresu w sieci prywatnej. Pisz „maszyna pomiarowa" i ścieżki względne.

Zakres zmian: wyłącznie wewnątrz katalogu roboczego. Rollback: bez zmian; nowe
pliki `spectra-{en,pl}.parquet` można skasować po potwierdzeniu odbioru.

## Po zaliczeniu

Czat prowadzący uruchamia lokalnie `python -m gates.gate2`. Kod jest gotowy
i przetestowany (130 testów) **od 2026-08-01, przed istnieniem tych progów** —
kolejność ma znaczenie i jest udokumentowana w historii repozytorium.
