# Raport dopasowania korpusów SPEKTRA-1 (T3, protokół §3)

**Licznik tokenów: DOKŁADNY (tokenizer Gemmy)**
Scenariuszy: 64 (en: 32, pl: 32)

## Język: en

| Wariant | Tokeny | Słowa | Tokeny/słowo | Znaki/token | Zdania pytające | Tur |
|---|---|---|---|---|---|---|
| A | 868.97 ± 51.07 | 737.88 ± 26.72 | 1.18 ± 0.04 | 4.67 ± 0.20 | 7.19 ± 1.55 | 9.97 ± 0.18 |
| B | 959.41 ± 24.89 | 848.59 ± 22.83 | 1.13 ± 0.01 | 4.65 ± 0.10 | 7.56 ± 1.54 | 9.97 ± 0.18 |
| C | 955.62 ± 24.02 | 844.91 ± 22.49 | 1.13 ± 0.01 | 4.67 ± 0.10 | 7.56 ± 1.54 | 9.97 ± 0.18 |
| CprimG | 959.78 ± 24.63 | 848.28 ± 22.48 | 1.13 ± 0.02 | 4.65 ± 0.10 | 7.56 ± 1.54 | 9.97 ± 0.18 |
| CprimU | 959.47 ± 24.57 | 847.44 ± 22.05 | 1.13 ± 0.01 | 4.65 ± 0.10 | 7.56 ± 1.54 | 9.97 ± 0.18 |

### Profil interpunkcji (średnia liczba znaków na tekst)

| Wariant | `,` | `.` | `?` | `!` | `;` | `:` |
|---|---|---|---|---|---|---|
| A | 24.7 | 44.0 | 7.2 | 0.0 | 0.0 | 0.8 |
| B | 28.2 | 47.5 | 7.6 | 0.0 | 0.0 | 0.2 |
| C | 28.2 | 47.5 | 7.6 | 0.0 | 0.0 | 0.2 |
| CprimG | 28.2 | 47.5 | 7.6 | 0.0 | 0.0 | 0.2 |
| CprimU | 28.2 | 47.5 | 7.6 | 0.0 | 0.0 | 0.2 |

### Kontrasty prerejestrowane (wymóg §3: ±2% tokenów)

**C − CprimG** — GŁÓWNY — samozwrotność przy wyrównanym osadzeniu

| Scenariusz | C | CprimG | różnica ze znakiem |
|---|---|---|---|
| en-01-apiary-move | 972 | 978 | -0.61% |
| en-02-dinghy-restoration | 1005 | 1011 | -0.59% |
| en-03-kiln-firing | 960 | 966 | -0.62% |
| en-04-drystone-wall | 959 | 959 | +0.00% |
| en-05-sourdough-night-bake | 946 | 948 | -0.21% |
| en-06-workshop-roof-framing | 968 | 968 | +0.00% |
| en-07-bouldering-route-setting | 920 | 922 | -0.22% |
| en-08-marquee-stage-sound | 905 | 908 | -0.33% |
| en-09-cheese-cave-maturing | 989 | 991 | -0.20% |
| en-10-smokehouse-hams | 981 | 985 | -0.41% |
| en-11-cider-press-ferment | 967 | 973 | -0.62% |
| en-12-farmers-market-stall | 986 | 991 | -0.50% |
| en-13-garden-sauna-kit | 976 | 980 | -0.41% |
| en-14-wildlife-pond | 950 | 952 | -0.21% |
| en-15-root-cellar-shed | 941 | 944 | -0.32% |
| en-16-wood-fired-hot-tub | 946 | 951 | -0.53% |
| en-17-horse-trailer-refit | 968 | 974 | -0.62% |
| en-18-cargo-bike-conversion | 934 | 934 | +0.00% |
| en-19-vintage-tractor-service | 919 | 922 | -0.33% |
| en-20-kayak-trip-portages | 924 | 929 | -0.54% |
| en-21-leather-satchel-repair | 973 | 977 | -0.41% |
| en-22-floor-loom-setup | 957 | 963 | -0.62% |
| en-23-gold-leaf-shop-sign | 966 | 974 | -0.82% |
| en-24-longcase-clock-service | 935 | 940 | -0.53% |
| en-25-orchard-grafting | 977 | 978 | -0.10% |
| en-26-hedge-laying | 934 | 936 | -0.21% |
| en-27-shearing-day | 938 | 945 | -0.74% |
| en-28-coppice-firewood | 948 | 949 | -0.11% |
| en-29-village-chess-league | 993 | 1000 | -0.70% |
| en-30-allotment-rota | 971 | 979 | -0.82% |
| en-31-garden-railway-loop | 939 | 946 | -0.74% |
| en-32-brass-telescope-restoration | 933 | 940 | -0.74% |

Znak różnicy: **0 razy dodatni, 29 razy ujemny**, 3 razy zero; średnia ze znakiem **-0.43%**. ⚠ **PRZECHYŁ JEDNOKIERUNKOWY** — przy kontraście parowanym taka różnica nie uśrednia się do zera i wchodzi wprost do wyniku.

**CprimG − CprimU** — diagnostyczny — sam efekt osadzenia referencyjnego

| Scenariusz | CprimG | CprimU | różnica ze znakiem |
|---|---|---|---|
| en-01-apiary-move | 978 | 972 | +0.61% |
| en-02-dinghy-restoration | 1011 | 1011 | +0.00% |
| en-03-kiln-firing | 966 | 960 | +0.62% |
| en-04-drystone-wall | 959 | 965 | -0.62% |
| en-05-sourdough-night-bake | 948 | 946 | +0.21% |
| en-06-workshop-roof-framing | 968 | 970 | -0.21% |
| en-07-bouldering-route-setting | 922 | 922 | +0.00% |
| en-08-marquee-stage-sound | 908 | 905 | +0.33% |
| en-09-cheese-cave-maturing | 991 | 988 | +0.30% |
| en-10-smokehouse-hams | 985 | 982 | +0.30% |
| en-11-cider-press-ferment | 973 | 974 | -0.10% |
| en-12-farmers-market-stall | 991 | 990 | +0.10% |
| en-13-garden-sauna-kit | 980 | 980 | +0.00% |
| en-14-wildlife-pond | 952 | 954 | -0.21% |
| en-15-root-cellar-shed | 944 | 943 | +0.11% |
| en-16-wood-fired-hot-tub | 951 | 954 | -0.31% |
| en-17-horse-trailer-refit | 974 | 973 | +0.10% |
| en-18-cargo-bike-conversion | 934 | 935 | -0.11% |
| en-19-vintage-tractor-service | 922 | 922 | +0.00% |
| en-20-kayak-trip-portages | 929 | 927 | +0.22% |
| en-21-leather-satchel-repair | 977 | 980 | -0.31% |
| en-22-floor-loom-setup | 963 | 964 | -0.10% |
| en-23-gold-leaf-shop-sign | 974 | 971 | +0.31% |
| en-24-longcase-clock-service | 940 | 944 | -0.42% |
| en-25-orchard-grafting | 978 | 977 | +0.10% |
| en-26-hedge-laying | 936 | 936 | +0.00% |
| en-27-shearing-day | 945 | 940 | +0.53% |
| en-28-coppice-firewood | 949 | 950 | -0.11% |
| en-29-village-chess-league | 1000 | 1001 | -0.10% |
| en-30-allotment-rota | 979 | 979 | +0.00% |
| en-31-garden-railway-loop | 946 | 947 | -0.11% |
| en-32-brass-telescope-restoration | 940 | 941 | -0.11% |

Znak różnicy: **13 razy dodatni, 13 razy ujemny**, 6 razy zero; średnia ze znakiem **+0.03%**.

**C − B** — wtórny — insercja meta wobec neutralnej

| Scenariusz | C | B | różnica ze znakiem |
|---|---|---|---|
| en-01-apiary-move | 972 | 978 | -0.61% |
| en-02-dinghy-restoration | 1005 | 1011 | -0.59% |
| en-03-kiln-firing | 960 | 966 | -0.62% |
| en-04-drystone-wall | 959 | 965 | -0.62% |
| en-05-sourdough-night-bake | 946 | 951 | -0.53% |
| en-06-workshop-roof-framing | 968 | 972 | -0.41% |
| en-07-bouldering-route-setting | 920 | 923 | -0.33% |
| en-08-marquee-stage-sound | 905 | 908 | -0.33% |
| en-09-cheese-cave-maturing | 989 | 992 | -0.30% |
| en-10-smokehouse-hams | 981 | 986 | -0.51% |
| en-11-cider-press-ferment | 967 | 972 | -0.51% |
| en-12-farmers-market-stall | 986 | 990 | -0.40% |
| en-13-garden-sauna-kit | 976 | 980 | -0.41% |
| en-14-wildlife-pond | 950 | 953 | -0.31% |
| en-15-root-cellar-shed | 941 | 940 | +0.11% |
| en-16-wood-fired-hot-tub | 946 | 950 | -0.42% |
| en-17-horse-trailer-refit | 968 | 973 | -0.51% |
| en-18-cargo-bike-conversion | 934 | 934 | +0.00% |
| en-19-vintage-tractor-service | 919 | 921 | -0.22% |
| en-20-kayak-trip-portages | 924 | 926 | -0.22% |
| en-21-leather-satchel-repair | 973 | 977 | -0.41% |
| en-22-floor-loom-setup | 957 | 963 | -0.62% |
| en-23-gold-leaf-shop-sign | 966 | 972 | -0.62% |
| en-24-longcase-clock-service | 935 | 938 | -0.32% |
| en-25-orchard-grafting | 977 | 979 | -0.20% |
| en-26-hedge-laying | 934 | 937 | -0.32% |
| en-27-shearing-day | 938 | 942 | -0.42% |
| en-28-coppice-firewood | 948 | 951 | -0.32% |
| en-29-village-chess-league | 993 | 998 | -0.50% |
| en-30-allotment-rota | 971 | 974 | -0.31% |
| en-31-garden-railway-loop | 939 | 942 | -0.32% |
| en-32-brass-telescope-restoration | 933 | 937 | -0.43% |

Znak różnicy: **1 razy dodatni, 30 razy ujemny**, 1 razy zero; średnia ze znakiem **-0.39%**.

## Język: pl

| Wariant | Tokeny | Słowa | Tokeny/słowo | Znaki/token | Zdania pytające | Tur |
|---|---|---|---|---|---|---|
| A | 864.19 ± 55.13 | 404.69 ± 25.29 | 2.14 ± 0.08 | 3.30 ± 0.15 | 3.97 ± 0.18 | 7.38 ± 0.55 |
| B | 962.38 ± 38.20 | 483.59 ± 23.14 | 1.99 ± 0.06 | 3.30 ± 0.12 | 3.97 ± 0.18 | 7.38 ± 0.55 |
| C | 957.81 ± 40.42 | 481.72 ± 23.47 | 1.99 ± 0.06 | 3.31 ± 0.12 | 3.97 ± 0.18 | 7.38 ± 0.55 |
| CprimG | 960.31 ± 39.37 | 483.34 ± 23.05 | 1.99 ± 0.06 | 3.30 ± 0.11 | 3.97 ± 0.18 | 7.38 ± 0.55 |
| CprimU | 962.22 ± 37.58 | 481.22 ± 22.40 | 2.00 ± 0.06 | 3.30 ± 0.12 | 3.97 ± 0.18 | 7.38 ± 0.55 |

### Profil interpunkcji (średnia liczba znaków na tekst)

| Wariant | `,` | `.` | `?` | `!` | `;` | `:` |
|---|---|---|---|---|---|---|
| A | 19.8 | 26.4 | 4.0 | 0.0 | 0.0 | 1.0 |
| B | 34.8 | 31.4 | 4.0 | 0.0 | 0.0 | 1.5 |
| C | 34.8 | 31.4 | 4.0 | 0.0 | 0.0 | 1.5 |
| CprimG | 34.8 | 31.4 | 4.0 | 0.0 | 0.0 | 1.5 |
| CprimU | 34.8 | 31.4 | 4.0 | 0.0 | 0.0 | 1.5 |

### Kontrasty prerejestrowane (wymóg §3: ±2% tokenów)

**C − CprimG** — GŁÓWNY — samozwrotność przy wyrównanym osadzeniu

| Scenariusz | C | CprimG | różnica ze znakiem |
|---|---|---|---|
| pl-01-deszczowka | 894 | 895 | -0.11% |
| pl-02-oswietlenie-warsztatu | 958 | 966 | -0.83% |
| pl-03-trasa-rowerowa | 967 | 973 | -0.62% |
| pl-04-archiwum-odbitek | 1003 | 1012 | -0.89% |
| pl-05-flota-dostawcza | 976 | 976 | +0.00% |
| pl-06-chleb-na-zakwasie | 955 | 962 | -0.73% |
| pl-07-sala-prob-akustyka | 949 | 953 | -0.42% |
| pl-08-ocieplenie-poddasza | 958 | 960 | -0.21% |
| pl-09-wedzenie-ryb | 897 | 900 | -0.33% |
| pl-10-kiszenie-w-beczkach | 1008 | 1008 | +0.00% |
| pl-11-sery-podpuszczkowe | 1011 | 1016 | -0.49% |
| pl-12-nalewki-klarowanie | 1017 | 1016 | +0.10% |
| pl-13-studnia-poglebianie | 903 | 908 | -0.55% |
| pl-14-rekuperacja-stary-dom | 996 | 1007 | -1.09% |
| pl-15-piec-chlebowy-ogrod | 985 | 984 | +0.10% |
| pl-16-odgromowka-stodola | 924 | 931 | -0.75% |
| pl-17-przyczepa-kempingowa | 1008 | 1003 | +0.50% |
| pl-18-lodz-wioslowa | 968 | 968 | +0.00% |
| pl-19-garaz-organizacja | 928 | 924 | +0.43% |
| pl-20-taczki-wozki | 967 | 964 | +0.31% |
| pl-21-staw-kapielowy | 1007 | 1003 | +0.40% |
| pl-22-kurnik-przydomowy | 947 | 936 | +1.16% |
| pl-23-pieczarki-w-piwnicy | 981 | 972 | +0.92% |
| pl-24-szczepienie-drzewek | 979 | 975 | +0.41% |
| pl-25-oprawa-ksiazek | 906 | 912 | -0.66% |
| pl-26-kucie-narzedzi | 903 | 915 | -1.31% |
| pl-27-szycie-owerlok | 1013 | 1021 | -0.78% |
| pl-28-kolo-garncarskie | 964 | 967 | -0.31% |
| pl-29-plan-polmaratonu | 910 | 923 | -1.41% |
| pl-30-smarowanie-nart-biegowych | 895 | 898 | -0.33% |
| pl-31-wywazanie-szybowcow | 904 | 909 | -0.55% |
| pl-32-akwarium-roslinne | 969 | 973 | -0.41% |

Znak różnicy: **9 razy dodatni, 20 razy ujemny**, 3 razy zero; średnia ze znakiem **-0.26%**.

**CprimG − CprimU** — diagnostyczny — sam efekt osadzenia referencyjnego

| Scenariusz | CprimG | CprimU | różnica ze znakiem |
|---|---|---|---|
| pl-01-deszczowka | 895 | 905 | -1.10% |
| pl-02-oswietlenie-warsztatu | 966 | 969 | -0.31% |
| pl-03-trasa-rowerowa | 973 | 973 | +0.00% |
| pl-04-archiwum-odbitek | 1012 | 1006 | +0.59% |
| pl-05-flota-dostawcza | 976 | 977 | -0.10% |
| pl-06-chleb-na-zakwasie | 962 | 955 | +0.73% |
| pl-07-sala-prob-akustyka | 953 | 951 | +0.21% |
| pl-08-ocieplenie-poddasza | 960 | 956 | +0.42% |
| pl-09-wedzenie-ryb | 900 | 900 | +0.00% |
| pl-10-kiszenie-w-beczkach | 1008 | 1005 | +0.30% |
| pl-11-sery-podpuszczkowe | 1016 | 1014 | +0.20% |
| pl-12-nalewki-klarowanie | 1016 | 1016 | +0.00% |
| pl-13-studnia-poglebianie | 908 | 919 | -1.20% |
| pl-14-rekuperacja-stary-dom | 1007 | 1012 | -0.49% |
| pl-15-piec-chlebowy-ogrod | 984 | 991 | -0.71% |
| pl-16-odgromowka-stodola | 931 | 938 | -0.75% |
| pl-17-przyczepa-kempingowa | 1003 | 999 | +0.40% |
| pl-18-lodz-wioslowa | 968 | 973 | -0.51% |
| pl-19-garaz-organizacja | 924 | 925 | -0.11% |
| pl-20-taczki-wozki | 964 | 966 | -0.21% |
| pl-21-staw-kapielowy | 1003 | 1005 | -0.20% |
| pl-22-kurnik-przydomowy | 936 | 942 | -0.64% |
| pl-23-pieczarki-w-piwnicy | 972 | 970 | +0.21% |
| pl-24-szczepienie-drzewek | 975 | 974 | +0.10% |
| pl-25-oprawa-ksiazek | 912 | 917 | -0.55% |
| pl-26-kucie-narzedzi | 915 | 920 | -0.54% |
| pl-27-szycie-owerlok | 1021 | 1022 | -0.10% |
| pl-28-kolo-garncarskie | 967 | 979 | -1.23% |
| pl-29-plan-polmaratonu | 923 | 917 | +0.65% |
| pl-30-smarowanie-nart-biegowych | 898 | 904 | -0.66% |
| pl-31-wywazanie-szybowcow | 909 | 914 | -0.55% |
| pl-32-akwarium-roslinne | 973 | 977 | -0.41% |

Znak różnicy: **10 razy dodatni, 19 razy ujemny**, 3 razy zero; średnia ze znakiem **-0.20%**.

**C − B** — wtórny — insercja meta wobec neutralnej

| Scenariusz | C | B | różnica ze znakiem |
|---|---|---|---|
| pl-01-deszczowka | 894 | 895 | -0.11% |
| pl-02-oswietlenie-warsztatu | 958 | 961 | -0.31% |
| pl-03-trasa-rowerowa | 967 | 970 | -0.31% |
| pl-04-archiwum-odbitek | 1003 | 1004 | -0.10% |
| pl-05-flota-dostawcza | 976 | 979 | -0.31% |
| pl-06-chleb-na-zakwasie | 955 | 956 | -0.10% |
| pl-07-sala-prob-akustyka | 949 | 958 | -0.94% |
| pl-08-ocieplenie-poddasza | 958 | 968 | -1.03% |
| pl-09-wedzenie-ryb | 897 | 903 | -0.66% |
| pl-10-kiszenie-w-beczkach | 1008 | 1008 | +0.00% |
| pl-11-sery-podpuszczkowe | 1011 | 1022 | -1.08% |
| pl-12-nalewki-klarowanie | 1017 | 1019 | -0.20% |
| pl-13-studnia-poglebianie | 903 | 914 | -1.20% |
| pl-14-rekuperacja-stary-dom | 996 | 1001 | -0.50% |
| pl-15-piec-chlebowy-ogrod | 985 | 987 | -0.20% |
| pl-16-odgromowka-stodola | 924 | 936 | -1.28% |
| pl-17-przyczepa-kempingowa | 1008 | 1004 | +0.40% |
| pl-18-lodz-wioslowa | 968 | 968 | +0.00% |
| pl-19-garaz-organizacja | 928 | 931 | -0.32% |
| pl-20-taczki-wozki | 967 | 968 | -0.10% |
| pl-21-staw-kapielowy | 1007 | 1005 | +0.20% |
| pl-22-kurnik-przydomowy | 947 | 939 | +0.84% |
| pl-23-pieczarki-w-piwnicy | 981 | 979 | +0.20% |
| pl-24-szczepienie-drzewek | 979 | 977 | +0.20% |
| pl-25-oprawa-ksiazek | 906 | 919 | -1.41% |
| pl-26-kucie-narzedzi | 903 | 915 | -1.31% |
| pl-27-szycie-owerlok | 1013 | 1023 | -0.98% |
| pl-28-kolo-garncarskie | 964 | 969 | -0.52% |
| pl-29-plan-polmaratonu | 910 | 921 | -1.19% |
| pl-30-smarowanie-nart-biegowych | 895 | 907 | -1.32% |
| pl-31-wywazanie-szybowcow | 904 | 912 | -0.88% |
| pl-32-akwarium-roslinne | 969 | 978 | -0.92% |

Znak różnicy: **5 razy dodatni, 25 razy ujemny**, 2 razy zero; średnia ze znakiem **-0.48%**.

## Uwagi metodologiczne

1. **Przecinki w wariancie A.** Wariant A jest z definicji wyliczeniowy (listy, kroki, liczby), więc jego profil przecinków jest strukturalnie wyższy niż w wariantach dialogowych. Protokół §3 wymaga *raportowania* rozkładu interpunkcji — jest on tutaj jawny; wyrównanie liczby przecinków wymagałoby wypaczenia natury wariantu A. Decyzja kierownika badania przed pieczęcią.
2. **Wariant A nie zawiera insercji z definicji**, więc jest krótszy od pozostałych czterech — kontrast C−A jest z tego powodu wtórny, nie główny (protokół v1.3 §1). Wszystkie warianty z insercjami (B, C, C′-G, C′-U) są parowane co do tokenów.
3. Raport wygenerowany automatycznie: `python -m corpus.report`.