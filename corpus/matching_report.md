# Raport dopasowania korpusów SPEKTRA-1 (T3, protokół §3)

**Licznik tokenów: HEURYSTYCZNY — raport WSTĘPNY**; ostateczny raport wymaga tokenizera z T2.
Scenariuszy: 16 (en: 8, pl: 8)

## Język: en

| Wariant | Tokeny | Słowa | Tokeny/słowo | Znaki/token | Zdania pytające | Tur |
|---|---|---|---|---|---|---|
| A | 889.50 ± 46.19 | 642.62 ± 24.87 | 1.38 ± 0.07 | 4.01 ± 0.00 | 0.00 ± 0.00 | 8.38 ± 0.52 |
| B | 842.88 ± 31.46 | 646.62 ± 35.92 | 1.31 ± 0.04 | 4.01 ± 0.00 | 5.50 ± 1.51 | 8.38 ± 0.52 |
| C | 960.88 ± 35.32 | 728.38 ± 44.84 | 1.32 ± 0.04 | 4.01 ± 0.00 | 5.50 ± 1.51 | 8.38 ± 0.52 |
| Cprim | 960.88 ± 35.32 | 728.38 ± 44.84 | 1.32 ± 0.04 | 4.01 ± 0.00 | 5.50 ± 1.51 | 8.38 ± 0.52 |

### Profil interpunkcji (średnia liczba znaków na tekst)

| Wariant | `,` | `.` | `?` | `!` | `;` | `:` |
|---|---|---|---|---|---|---|
| A | 39.9 | 44.6 | 0.0 | 0.0 | 0.0 | 3.9 |
| B | 23.2 | 36.4 | 5.5 | 0.0 | 0.4 | 0.1 |
| C | 24.1 | 41.9 | 5.5 | 0.0 | 0.4 | 0.1 |
| Cprim | 24.1 | 41.9 | 5.5 | 0.0 | 0.4 | 0.1 |

### Kontrast C vs C′ (wymóg §3: ±2% tokenów)

| Scenariusz | C | C′ | różnica |
|---|---|---|---|
| en-01-apiary-move | 1002 | 1002 | 0.00% |
| en-02-dinghy-restoration | 930 | 930 | 0.00% |
| en-03-kiln-firing | 1008 | 1008 | 0.00% |
| en-04-drystone-wall | 977 | 977 | 0.00% |
| en-05-sourdough-night-bake | 946 | 946 | 0.00% |
| en-06-workshop-roof-framing | 922 | 922 | 0.00% |
| en-07-bouldering-route-setting | 922 | 922 | 0.00% |
| en-08-marquee-stage-sound | 980 | 980 | 0.00% |

## Język: pl

| Wariant | Tokeny | Słowa | Tokeny/słowo | Znaki/token | Zdania pytające | Tur |
|---|---|---|---|---|---|---|
| A | 795.00 ± 68.77 | 372.38 ± 14.85 | 2.14 ± 0.18 | 3.21 ± 0.00 | 3.25 ± 0.46 | 6.25 ± 0.46 |
| B | 814.75 ± 39.58 | 381.12 ± 14.55 | 2.14 ± 0.06 | 3.21 ± 0.00 | 3.25 ± 0.46 | 6.25 ± 0.46 |
| C | 948.62 ± 44.00 | 444.25 ± 15.80 | 2.14 ± 0.06 | 3.20 ± 0.00 | 3.25 ± 0.46 | 6.25 ± 0.46 |
| Cprim | 948.38 ± 44.09 | 444.25 ± 15.80 | 2.13 ± 0.06 | 3.21 ± 0.00 | 3.25 ± 0.46 | 6.25 ± 0.46 |

### Profil interpunkcji (średnia liczba znaków na tekst)

| Wariant | `,` | `.` | `?` | `!` | `;` | `:` |
|---|---|---|---|---|---|---|
| A | 20.9 | 24.8 | 3.2 | 0.0 | 0.0 | 1.1 |
| B | 24.5 | 24.8 | 3.2 | 0.0 | 0.0 | 0.2 |
| C | 30.5 | 29.8 | 3.2 | 0.0 | 0.0 | 0.6 |
| Cprim | 30.5 | 29.8 | 3.2 | 0.0 | 0.0 | 0.6 |

### Kontrast C vs C′ (wymóg §3: ±2% tokenów)

| Scenariusz | C | C′ | różnica |
|---|---|---|---|
| pl-01-deszczowka | 916 | 916 | 0.00% |
| pl-02-oswietlenie-warsztatu | 908 | 907 | 0.11% |
| pl-03-trasa-rowerowa | 944 | 944 | 0.00% |
| pl-04-archiwum-odbitek | 920 | 920 | 0.00% |
| pl-05-flota-dostawcza | 963 | 962 | 0.10% |
| pl-06-chleb-na-zakwasie | 912 | 912 | 0.00% |
| pl-07-sala-prob-akustyka | 1022 | 1022 | 0.00% |
| pl-08-ocieplenie-poddasza | 1004 | 1004 | 0.00% |

## Uwagi metodologiczne

1. **Przecinki w wariancie A.** Wariant A jest z definicji wyliczeniowy (listy, kroki, liczby), więc jego profil przecinków jest strukturalnie wyższy niż w wariantach dialogowych. Protokół §3 wymaga *raportowania* rozkładu interpunkcji — jest on tutaj jawny; wyrównanie liczby przecinków wymagałoby wypaczenia natury wariantu A. Decyzja kierownika badania przed pieczęcią.
2. **Długości tur A vs B.** Wariant C zawiera insercje, więc jest z definicji dłuższy od B; kluczowa parowość dotyczy C vs C′ (tabela wyżej).
3. Raport wygenerowany automatycznie: `python -m corpus.report`.