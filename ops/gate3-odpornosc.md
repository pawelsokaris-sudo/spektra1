# GATE 3 (wersja chuda) — raport wykonania biegów kontrolnych (zlecenie 08)

**Data:** 2026-08-01/02 (biegi nocne) · **Wykonawca:** DEP · **Maszyna:** maszyna pomiarowa
(konwencja po anonimizacji: bez kont, hostów i adresów; ścieżki względne)

## 1. Liczby tekstów i czasy

| Bieg | Teksty (oczekiwane) | Wiersze metryk / widm | Czas biegu (ok.) |
|---|---|---|---|
| **GATE 3a** (fp32, C + C′-G, 12/język) | **48 (48)** ✅ | 1632 / 1632 (48 × 34 warstwy) | **~45 min** (22:40–23:25) |
| **GATE 3b** (bez komp. pozycyjnego, 24/język) | **96 (96)** ✅ | 3264 / 3264 (96 × 34 warstwy) | **~40 min** (21:50–22:30) |

Oba biegi: warianty dokładnie `C, CprimG`, scenariusze wyłącznie z biegu głównego
(zgodność z `windows.json` sprawdzona przed startem: 48 kluczy ↔ 48 scenariuszy,
0 rozjazdów w obie strony).

## 2. max(peak_gb) osobno (wymóg ANEKS-2)

| Bieg | max(peak_gb) | Komentarz |
|---|---|---|
| GATE 3a (fp32) | **17.70 GB** (17.69791889190674) | zgodnie z przewidywaniem 17–18 GB; w progu kontroli fp32 (24 GB) z zapasem |
| GATE 3b (bf16) | **8.85 GB** (8.848422050476074) | praktycznie identyczny z biegiem głównym (8.85) |

## 3. Komunikaty protokolarne runnera

- GATE 3a: `[runner] GATE 3a: forward w fp32 (przelewa sie do RAM - zgodnie z protokolem kontrola zostaje na TYM SAMYM urzadzeniu)` — obecny ✅
- GATE 3b: `[runner] GATE 3b: komponent pozycyjny NIE jest odejmowany` — obecny ✅
- Oba biegi zakończone wpisem `[runner] zapisane: …` + oczekiwaną uwagą o placeholderze
  `lambda_star = inf` (progi przeliczy analiza po stronie laptopa — na maszynie nie liczono
  żadnych metryk z prawdziwym λ* ani kontrastów).

## 4. Co odbiegło (chronologicznie — wszystko rozwiązane w trakcie)

1. **Pierwsza próba GATE 3a zatrzymana przez bramkę pamięci** (17,65 GB > 14 GB,
   myląca etykieta `[bf16]`): błąd w kodzie — próg `fp32_control_limit_gb = 24.0`
   nie był podpięty przy dokładaniu `--dtype`. Naprawione przez czat prowadzący,
   bieg powtórzony na nowym kodzie. Sufit bezpieczeństwa pozostał (24 GB).
2. **Synchronizacja kodu przywróciła 16 scenariuszy pilota do korpusu** (paczka
   z laptopa niesie pełny korpus 32+32; przed biegiem głównym pilot był wyłączony).
   Skutek: fałszywy start GATE 3b (`KeyError` na scenariuszu pilota) i pierwsza próba
   GATE 3a na złym zestawie scenariuszy. Korpus przywrócono do stanu główno-biegowego
   (24+24) przed ważnymi biegami.
3. **Filtr scenariuszy po `windows.json` (pierwsza wersja poprawki) przykładany
   ZA PÓŹNO** — po wyborze per-language zostawało 8 scenariuszy zamiast 24
   („pominięto 16 … zostaje 8"). Start przerwany po ~30 s, korpus przycięty ręcznie,
   bieg ważny wykonany poprawnie. Kolejność naprawiona commitem `04e9859`
   (filtr PRZED `--limit`/`--per-language`, test odtwarza przypadek) — **od następnej
   synchronizacji korpus nie wymaga pilnowania**.
4. Poza powyższym: zero przerwań, wznowień i ostrzeżeń pamięci w ważnych biegach.

## 5. Sumy SHA-256 (zweryfikowane po transferze na laptop — zgodne 4/4)

| Plik | SHA-256 |
|---|---|
| `gate3-fp32/spectra.parquet` (11 517 783 B) | `8a677ccac90db1cb59545c52fc0ed65e8253e01927c5eeccbc781cbdb2e2dc98` |
| `gate3-fp32/metrics.parquet` (33 967 B) | `7db44ccb756e737ba63b0fbb067037b6efeba8076a513e075feab22b91e97a85` |
| `gate3-nopos/spectra.parquet` (22 497 273 B) | `bac648b006a27c773394ba14e3d9e48cca2949f09b4c1bf721771a02553a3f72` |
| `gate3-nopos/metrics.parquet` (58 724 B) | `4951dfede7f945e8765ce5dc54a15c698078b0e1678108420df849619f4d1664` |

Pliki leżą w `measurements-glowny/gate3-fp32/` i `measurements-glowny/gate3-nopos/`
(plus logi obu biegów). `positional_mu.npz` nie przesyłano (kopie z biegu głównego).

## Rollback / stan maszyny

Na maszynie pozostały katalogi `gate3-fp32/` i `gate3-nopos/` (do skasowania po
potwierdzeniu odbioru) oraz dwa zadania Harmonogramu w konwencji SPEKTRA1-*
(`-gate3a`, `-gate3b`, wyłączone po biegach — jak pozostałe cztery). Korpus na maszynie
jest w stanie główno-biegowym (24+24). Nic więcej nie zmieniano.
