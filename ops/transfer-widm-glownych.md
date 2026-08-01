# Transfer widm i progów korpusu głównego — raport wykonania (zlecenie 07)

**Data:** 2026-08-01 · **Wykonawca:** DEP · **Maszyna:** maszyna pomiarowa (ścieżki względne wg konwencji po anonimizacji)

## Warunek startu

`pipeline.t5_null_run` zakończony w trakcie dnia. Pierwsza kontrola (17:07) zastała
bieg w toku — **625/672 progów** — zgodnie ze zleceniem wykonanie wstrzymano (STOP,
odesłano liczbę). Czujka automatyczna wykryła komplet o ~18:04; log kończy się wpisem
`[t5] zapisane: 672 progow`. Dopiero wtedy ruszyły kroki 1–3.

## 1. Kontrola kompletności — wszystkie wartości zgodne z wymaganymi

| Wielkość | Wymagane | Zmierzone | Status |
|---|---|---|---|
| wierszy `t5_lambda_star` | 672 (48 × 14) | **672** | ✅ |
| scenariuszy | 48 | **48** | ✅ |
| warstwy pasma | 14–27 | **14–27 (komplet)** | ✅ |
| języki | en, pl | **en, pl** | ✅ |
| wierszy `spectra` | 21216 (624 × 34) | **21216** | ✅ |
| braków `lambda_star` | 0 | **0** | ✅ |

Uwaga porządkowa: na maszynie pomiarowej wyniki biegu głównego leżą w katalogu
`measurements/` (nie `measurements-glowny/`, jak zakładało zlecenie). Dane kompletne —
różnica dotyczy wyłącznie nazwy katalogu; po stronie laptopa pliki trafiły do
`measurements-glowny/` zgodnie z uzupełnieniem zlecenia.

## 2. Podział widm per język i sumy SHA-256

Podział: `spectra-en.parquet` **10608** wierszy (73 585 628 B), `spectra-pl.parquet`
**10608** wierszy (73 565 020 B) — oba poniżej limitu 100 MB.

| Plik | SHA-256 |
|---|---|
| `spectra-en.parquet` | `34c6be1bf4edab2bfd336ebb9bda8eb7998abe1a4e17429f6121ce098520f13b` |
| `spectra-pl.parquet` | `d813d5deab15ca27424434d898a4a3232fdd2d526417acc2fd4b5540513c4a1c` |
| `t5_lambda_star.parquet` | `256679cf0fe5a92e0869bb41863413569c9a83cf6aed8758f2b325e17b438278` |
| `t5_phi.json` | `53ba68386eec46ada503fd816756de0b96bd482786febaeb117d5ddfd901924d` |

## 3. Transfer

Przeniesione do `measurements-glowny/` w repozytorium na laptopie (nazwy bez zmian):
`spectra-en.parquet`, `spectra-pl.parquet`, `t5_lambda_star.parquet`, `t5_phi.json`
oraz log biegu `t5.log`. **Sumy SHA-256 przeliczone po stronie laptopa: zgodne 4/4**
z wartościami z maszyny (tabela wyżej). Wag modelu, tokenizera ani `positional_mu.npz`
nie przesyłano.

## 4. GATE 0 powtórzony na maszynie pomiarowej (po transferze, sam procesor)

**Werdykt: PASS** we wszystkich kryteriach, czas **275,4 s**
(odniesienie laptopowe: 816 s — maszyna ~3× szybsza, nic nie zjada procesora w tle).

| Kryterium | Maszyna pomiarowa | Odniesienie z laptopa | Status |
|---|---|---|---|
| A. Marchenko–Pastur | KS = **0.0014** | KS = 0.0014 | PASS (identyczne) |
| B. Kalibracja λ* | λ*=6.8400; fałszywe mody **21/1000 (2.10%)**, próg q0.995=26 | 2.10% przy progu 26/1000 | PASS (identyczne) |
| C. Replikacja | **BITOWA** (8 realizacji × 2 przebiegi) | bitowa | PASS — zero różnic sprzętowych |
| D. D_lag (porządek) | iid \|z\|<3, AR(1) z>5 | — | PASS |

Pełny raport wygenerowany na maszynie: `ops/gate0_report-maszyna.md` (kopia
`gates/gate0_report.md` z maszyny).

## Do raportu GATE 3

**max(peak_gb) z całego biegu głównego = 8,85 GB** (dokładnie 8.85239315032959,
kolumna `peak_gb` w `metrics.parquet`) — zgodne z wartością odniesienia z ANEKS-2.

## Nieoczekiwane zdarzenia w trakcie T5

**Brak.** Bez przerwań, wznowień i ostrzeżeń pamięci; log ciągły od załadowania wag do
`[t5] zapisane: 672 progow`, czas biegu ~43 715 s (~12,1 h). Automatyczny przegląd
ostrzeżeń dał 15 pozornych trafień — wszystkie to nazwa scenariusza *floor-loom*
(zawiera ciąg „oom") — fałszywe dopasowania, nie zdarzenia.

## Higiena ślepej próby

Na maszynie nie liczono żadnych metryk z prawdziwym λ* ani kontrastów między
wariantami — wyłącznie kontrola kompletności, podział plików i sumy. Endpoint główny
pozostaje nieotwarty.

## Rollback / sprzątanie

Zmiany wyłącznie wewnątrz katalogu roboczego maszyny: dołożone `spectra-{en,pl}.parquet`
(do skasowania po potwierdzeniu odbioru przez czat prowadzący); skrypty pomocnicze
wykonawcy usunięte. Nic poza tym nie ruszano.
