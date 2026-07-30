# Raport dopasowania korpusów SPEKTRA-1 (T3, protokół §3)

**Licznik tokenów: HEURYSTYCZNY — raport WSTĘPNY**; ostateczny raport wymaga tokenizera z T2.
Scenariuszy: 14 (en: 8, pl: 6)

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
| A | 808.33 ± 57.36 | 371.67 ± 10.78 | 2.18 ± 0.19 | 3.21 ± 0.00 | 3.50 ± 0.55 | 6.50 ± 0.55 |
| B | 831.83 ± 48.44 | 389.00 ± 16.42 | 2.14 ± 0.06 | 3.21 ± 0.00 | 3.50 ± 0.55 | 6.50 ± 0.55 |
| C | 969.00 ± 54.32 | 453.33 ± 16.71 | 2.14 ± 0.06 | 3.21 ± 0.00 | 3.50 ± 0.55 | 6.50 ± 0.55 |
| Cprim | 968.50 ± 54.69 | 453.33 ± 16.71 | 2.14 ± 0.06 | 3.21 ± 0.00 | 3.50 ± 0.55 | 6.50 ± 0.55 |

### Profil interpunkcji (średnia liczba znaków na tekst)

| Wariant | `,` | `.` | `?` | `!` | `;` | `:` |
|---|---|---|---|---|---|---|
| A | 21.2 | 24.5 | 3.5 | 0.0 | 0.0 | 1.3 |
| B | 26.5 | 24.5 | 3.5 | 0.0 | 0.0 | 0.3 |
| C | 32.2 | 29.5 | 3.5 | 0.0 | 0.0 | 0.8 |
| Cprim | 32.2 | 29.5 | 3.5 | 0.0 | 0.0 | 0.8 |

### Kontrast C vs C′ (wymóg §3: ±2% tokenów)

| Scenariusz | C | C′ | różnica |
|---|---|---|---|
| pl-01-deszczowka | 917 | 917 | 0.00% |
| pl-02-oswietlenie-warsztatu | 896 | 895 | 0.11% |
| pl-05-flota-dostawcza | 956 | 954 | 0.21% |
| pl-06-chleb-na-zakwasie | 1024 | 1024 | 0.00% |
| pl-07-sala-prob-akustyka | 1017 | 1017 | 0.00% |
| pl-08-ocieplenie-poddasza | 1004 | 1004 | 0.00% |

## Uwagi metodologiczne

1. **Przecinki w wariancie A.** Wariant A jest z definicji wyliczeniowy (listy, kroki, liczby), więc jego profil przecinków jest strukturalnie wyższy niż w wariantach dialogowych. Protokół §3 wymaga *raportowania* rozkładu interpunkcji — jest on tutaj jawny; wyrównanie liczby przecinków wymagałoby wypaczenia natury wariantu A. Decyzja kierownika badania przed pieczęcią.
2. **Długości tur A vs B.** Wariant C zawiera insercje, więc jest z definicji dłuższy od B; kluczowa parowość dotyczy C vs C′ (tabela wyżej).
3. Raport wygenerowany automatycznie: `python -m corpus.report`.