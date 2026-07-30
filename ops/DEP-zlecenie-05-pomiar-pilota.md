# DEP — Zlecenie 05: pomiar pilota (16 scenariuszy × 5 wariantów + nulle N1/N2)

**Maszyna:** `maszyna-pomiarowa` (po nazwie hosta).
**Środowisko i kod:** z zleceń 02–04. Kod na maszynie jest STARY — krok 1 go podmienia.
**Charakter:** pierwszy prawdziwy pomiar aktywacji w projekcie. **Bieg wielogodzinny**
(szacunek: 8–24 h, dominuje metryka porządku D_lag; forwardy to minuty). Runner ma
checkpoint per tekst i wznawianie — przerwanie NIE marnuje biegu.

> **To jest pomiar PILOTA (GATE 1), nie pomiar główny.** Pilot jest wyłączony
> z analizy głównej; służy do estymacji wariancji, ICC i parametrów nullu
> symulacyjnego (T5). Po nim: symulacja mocy → zamrożenie M → pieczęć.
> Kolejność zleceń 01→05 pozostaje ważna: po pieczęci ten sam runner zmierzy
> korpus główny bez zmiany ani jednej linii.

## Krok 1 — synchronizacja kodu (pełna, nie wybiórcza)

Nauka ze zlecenia 04 (drift `report.py`): tym razem podmieniamy **cały kod**, nie
wybrane pliki. Spakować na laptopie:

```
cd C:\Users\pawel\projects
tar -czf spektra1-code.tar.gz --exclude=.venv --exclude=.git --exclude=*.npy --exclude=__pycache__ --exclude=.claude spektra1
```

Rozmiar wzorcowy ~140 KB. Rozpakować do `C:\Users\operator\` nadpisując `spektra1\`.
**Po rozpakowaniu obowiązkowo:**

1. Sprawdzić, że tokenizer przeżył: `dir C:\Users\operator\spektra1\corpus\.tokenizer\`
   — plik `tokenizer.json` ma tam być. Jeśli zniknął, odtworzyć ze snapshotu
   (komenda w zleceniu 03) — **bez niego runner odmówi startu** (to celowe).
2. Zweryfikować sumą kontrolną, że `pipeline/runner.py` i `pipeline/metrics.py`
   na maszynie są identyczne z laptopem. Reguła z inwentarza: jeśli kryterium
   zakłada nową funkcjonalność, najpierw udowodnij, że uruchamiana wersja ją ma.
3. Usunąć archiwum transferowe.

## Krok 2 — kontrola przedstartowa

```
ollama ps                        # ma być pusto (żaden model w VRAM)
nvidia-smi --query-gpu=memory.used --format=csv    # ~1.6 GB (sam pulpit)
```

Plus test składni i konfiguracji bez modelu (sekundy):

```
cd C:\Users\operator\spektra1
C:\Users\operator\spektra1-env\Scripts\python.exe -m pytest tests -q
```

Oczekiwane: **100 testów zielonych**. Jeśli mniej — STOP, coś nie doszło w paczce.

## Krok 3 — pomiar (bieg długi, odporny na przerwanie)

```
cd C:\Users\operator\spektra1
C:\Users\operator\spektra1-env\Scripts\python.exe -m pipeline.runner --nulls > runner.log 2>&1
```

Uruchomić tak, żeby przeżyło zamknięcie sesji SSH (zadanie w tle / `start /b` /
harmonogram — wedle Twojego uznania, byle log szedł do pliku).

**Plan biegu:** 16 scenariuszy × 5 wariantów = 80 tekstów głównych + 128 tekstów
nulli (N1/N2 dla wariantów dialogowych) = **208 forwardów**. Metryki per warstwa
(34 warstwy, embedding i warstwa 34 wyłączone zgodnie z T2), D_lag liczony tylko
w paśmie konfirmacyjnym (bloki 13–26). Po każdym tekście dopisywany checkpoint —
**ponowne uruchomienie tej samej komendy wznawia od miejsca przerwania**.

**Bramka pamięci jest aktywna:** jeśli którykolwiek forward przekroczy 14 GB,
runner przerwie z jawnym błędem (sterownik przelewa nadmiar do RAM po cichu,
więc bez bramki nie byłoby sygnału). Oczekiwany szczyt: ~8.8 GB.

## Krok 4 — po zakończeniu

Sprawdzić ostatnie linie `runner.log`: ma być `[runner] zapisane: ... wierszy metryk`
oraz uwaga o placeholderze lambda_star (to jest OK — I_total/k przeliczamy w T5
z zachowanych widm).

Odesłać do repo na laptopa:
- `measurements/metrics.parquet` i `measurements/spectra.parquet` (widma są duże —
  jeśli >200 MB, zostawić na maszynie i odesłać tylko metrics + rozmiar spectra)
- `measurements/dropped_tokens.csv` (liczba odrzuconych tokenów per scenariusz
  i wariant — wchodzi do pakietu pieczęci)
- `runner.log`
- raport `ops/pomiar-pilota.md`: czas biegu, szczyt pamięci (max z kolumny peak_gb),
  liczba wznowień (jeśli były), wszystko co odbiegło od oczekiwań.

**NIE odsyłać** żadnych plików tokenizera ani wag.

## Awarie

- Runner odmawia startu z komunikatem o `token_window_mode` albo tokenizerze →
  paczka niekompletna, wróć do kroku 1.
- `MemoryGuardError` → STOP i raport z pełnym komunikatem; nie podnosić progu.
- Przerwanie/restart maszyny → po prostu uruchomić komendę z kroku 3 ponownie;
  wznowi od checkpointu. Liczba wznowień do raportu.

## Rollback

Jak dotąd: `Remove-Item -Recurse -Force C:\Users\operator\spektra1, C:\Users\operator\spektra1-env`.
Katalog `measurements\` jest wewnątrz `spektra1\`, więc rollback obejmuje też wyniki.
