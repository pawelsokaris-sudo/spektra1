# Pomiar pilota — ZAKOŃCZONY POMYŚLNIE

**Zlecenie:** `ops/DEP-zlecenie-05-pomiar-pilota.md` (wersja po poprawkach)
**Wykonał:** DEP (Claude Code w terminalu)
**Maszyna:** `maszyna-pomiarowa`
**Raport z pierwszego podejścia** (bieg padł po 12 s): w historii gita, commit `ad533ec`.

## Wynik

| Pozycja | Wartość |
|---|---|
| Start | 2026-07-30 **16:31:36** |
| Koniec | 2026-07-30 **19:16:38** |
| **Czas biegu** | **2 h 45 min 02 s** (zlecenie zakładało 8–24 h) |
| Kod wyjścia | **0** |
| **Szczyt pamięci (max `peak_gb`)** | **8,853 GB** przy progu bramki 14 GB — zapas 5,1 GB |
| **Liczba wznowień** | **0** — jeden start, bez przerwań |
| Błędy w logu | **0** (`Traceback`, `MemoryGuardError`: brak) |
| Wiersze metryk | **7 072** = 208 tekstów × 34 warstwy |
| Widma | **7 072** |

Ostatnie linie `runner.log`:

```
[runner] zapisane: 7072 wierszy metryk, 7072 widm
[runner] UWAGA: lambda_star = inf (placeholder). Metryki I_total, I_-1 i k sa policzone
         wzgledem nieskonczonego progu i beda PRZELICZONE w T5 z widm w spectra.parquet,
         po estymacji nullu symulacyjnego.
[DEP] proces zakonczony, kod wyjscia=0, czas: czw. 30.07.2026 19:16:38,79
```

Uwaga o `lambda_star` jest oczekiwana i zgodna ze zleceniem — nie jest sygnałem problemu.

## Zgodność liczb: wszystko domyka się co do sztuki

Trzy niezależne rachunki wychodzą dokładnie tak, jak przewiduje konstrukcja pomiaru. To jest
najmocniejszy dowód, że bieg policzył to, co miał policzyć, a nie coś przypadkiem podobnego.

- **7 072 wiersze = 208 tekstów × 34 warstwy.** Unikalnych tekstów w pliku: **208**
  (16 scenariuszy × 5 wariantów = 80 głównych + 128 nulli). Scenariuszy: 16, wariantów: 5,
  typów nullu: 2.
- **Braki w kolumnie `null`: 2 720 = 80 tekstów głównych × 34 warstwy.** Teksty główne nie mają
  etykiety nullu, więc dokładnie tyle powinno być pustych.
- **Braki w kolumnie `D_lag`: 4 160 = 208 tekstów × 20 warstw poza pasmem.** Pasmo
  konfirmacyjne to bloki 13–26, czyli 14 z 34 warstw; `D_lag` liczony jest tylko tam
  (to ~60% kosztu pomiaru). 34 − 14 = 20 warstw poza pasmem.

Żadnych innych braków w danych nie ma.

## Pliki wynikowe

| Plik | Rozmiar | Gdzie |
|---|---|---|
| `measurements/metrics.parquet` | 111 037 B | repo (wyjątek w `.gitignore`, wchodzi do commita) |
| `measurements/dropped_tokens.csv` | 705 B | repo |
| `measurements/spectra.parquet` | **50 795 478 B (48,4 MB)** | na laptopie, ale **ignorowany przez git** |
| `ops/runner.log` | 11 073 B | repo |
| `measurements/positional_mu.npz` | 555 053 046 B | tylko na maszynie (checkpoint przebiegu 1) |

**Uwaga do `spectra.parquet`:** zlecenie kazało zostawić go na maszynie tylko przy rozmiarze
>200 MB. Ma 48,4 MB, więc go skopiowałem — ale `.gitignore` ma regułę `*.parquet` z wyjątkiem
wyłącznie dla `metrics.parquet`. Plik leży więc na laptopie i jest dostępny do analizy, ale
**nie wejdzie do repo przez commit**. Skoro T5 ma z niego przeliczyć `I_total`, `I_-1` i `k`
po estymacji nullu, warto świadomie zdecydować, czy ma trafić do pakietu pieczęci inną drogą,
czy zostaje danymi roboczymi.

**Weryfikacja integralności — dwie niezależne ścieżki:**

```
metrics.parquet     maszyna=6aeab4d314b0dc11  laptop=6aeab4d314b0dc11  ZGODNE
dropped_tokens.csv  maszyna=af931a4ce8f8b60f  laptop=af931a4ce8f8b60f  ZGODNE
spectra.parquet     maszyna=1946999c182a913b  laptop=1946999c182a913b  ZGODNE
```

Dodatkowo: `metrics.parquet` i `dropped_tokens.csv`, które pobrałem, są **bajtowo identyczne
z wersją już zacommitowaną** (commit `7239b44`) — czyli dwa niezależne transfery z maszyny dały
ten sam plik. To mocniejszy dowód integralności niż pojedyncze porównanie sum.

## Odrzucone tokeny (do pakietu pieczęci)

```
                   scenario_id  dropped_A  dropped_B  dropped_C  dropped_CprimG  dropped_CprimU
             en-01-apiary-move          0        122        116             122             116
      en-02-dinghy-restoration         14          6          0               6               6
             en-03-kiln-firing         20          6          0               6               0
           en-04-drystone-wall          0         28         22              22              28
    en-05-sourdough-night-bake          0         62         57              59              57
   en-06-workshop-roof-framing          0         61         57              57              59
en-07-bouldering-route-setting          0         66         63              65              65
     en-08-marquee-stage-sound          0         79         76              79              76
              pl-01-deszczowka          0         77         76              77              87
   pl-02-oswietlenie-warsztatu          0         14         11              19              22
          pl-03-trasa-rowerowa          0         11          8              14              14
        pl-04-archiwum-odbitek          0         84         83              92              86
         pl-05-flota-dostawcza          0        145        142             142             143
       pl-06-chleb-na-zakwasie          0        118        117             124             117
      pl-07-sala-prob-akustyka          0        111        102             106             104
     pl-08-ocieplenie-poddasza          0        122        112             114             110
```

**Interpretacja:** w 14 z 16 scenariuszy wariant A ma zero odrzuconych, bo jest najkrótszy
i to on wyznacza wspólne okno scenariusza. Wyjątki to `en-02` (A traci 14) i `en-03` (A traci 20),
gdzie okno wyznaczył inny wariant — w obu tych przypadkach wariant C nie stracił nic. Największe
odrzucenie to 145 tokenów (`pl-05`, wariant B). Warto odnotować, że **odrzucenia są bardzo
nierówne między scenariuszami** — od 8–22 tokenów w `pl-02` i `pl-03` do 110–145 w `pl-05`,
`pl-06` i `pl-08` — co przy analizie wariancji może mieć znaczenie i jest teraz zapisane liczbowo.

## Przebieg 1: naprawa z pierwszego podejścia potwierdzona

Przebieg 1 (komponent pozycyjny) zamknął się w **25 sekund** dla wszystkich 16 scenariuszy.
Pierwsze podejście padło tu na drugim scenariuszu; teraz przeszły wszystkie:

```
  en-01-apiary-move: okno 861 tok. (2 s)
  en-02-dinghy-restoration: okno 1014 tok. (4 s)      <<< to zabilo pierwsze podejscie
  en-03-kiln-firing: okno 969 tok. (5 s)
  ...
  pl-08-ocieplenie-poddasza: okno 843 tok. (25 s)
[runner] przebieg 1/2: checkpoint zapisany (positional_mu.npz)
```

Okna są **różne dla każdego scenariusza — od 811 do 1014 tokenów — i wszystkie zostały
zachowane**. To potwierdza w praktyce, że przyjęte rozwiązanie (akumulator z licznikiem per
pozycja) **nie kosztuje ani jednego tokenu**. Wariant alternatywny, czyli wspólne okno w obrębie
języka, ściąłby wszystko do 829 (EN) i 818 (PL), odbierając do 17,5% okna najdłuższego scenariusza.

## Bramka pamięci: zadziałała i nigdy nie musiała przerwać

Szczyt zużycia własnego procesu wyniósł **8,853 GB** przy progu 14 GB. Mediana po wszystkich
7 072 pomiarach to 8,810 GB, minimum 8,688 GB — czyli zużycie jest bardzo stabilne, bez skoków.
Zmierzony szczyt jest praktycznie identyczny z przewidywanym w zleceniu 02 (~8,8 GB), co
potwierdza, że oszacowanie sprzed pomiaru było trafne.

Druga bramka — na **obce** zużycie karty, dodana dziś po blokadzie — nie przerwała biegu ani
razu, co znaczy, że przez całe 2 h 45 min nikt nie obciążył karty czymś innym.

## Przebieg zlecenia: blokada i drugie podejście

Bieg nie wystartował od razu. Kontrola przedstartowa o 16:25 pokazała **6,90 GB zajętej pamięci
karty przy 8,70 GB wolnych i potrzebnym szczycie 8,83 GB — deficyt 0,13 GB**. Powód: operator
maszyny korzystał z niej w tym momencie (gra + Discord, Steam, Epic, dwie przeglądarki).
Nie wystartowałem, nie zamknąłem żadnego jego procesu i nie podniosłem progu bramki.

Ta blokada ujawniła **dziurę w bramce pamięci**: `check_peak_memory` mierzy alokacje własnego
procesu, więc przepuściłaby bieg, który fizycznie się nie mieści, a sterownik po cichu dołożyłby
pamięć systemową. Czat prowadzący zaimplementował poprawkę (`check_foreign_vram`, commit
`9478e3c`) wywoływaną przed każdym forwardem, więc obciążenie karty w trakcie biegu zatrzymuje
pomiar czysto na checkpointcie. Po tej poprawce zsynchronizowałem kod ponownie i wystartowałem
o 16:31, gdy karta się zwolniła (1,32 GB obcego zużycia przy progu 3 GB, 14,60 GB wolnych).

Pełen opis tej części — łącznie z uzasadnieniem, dlaczego zmieniłem decyzję i wystartowałem —
jest w historii gita w poprzedniej wersji tego pliku.

## Synchronizacja kodu i kontrole

Kod synchronizowany **dwa razy** (16:19 i 16:30, po commicie z bramką), za każdym razem
**35/35 sum kontrolnych zgodnych** dla wszystkich plików `.py` z `pipeline/`, `corpus/`,
`nulls/`, `power/`, `tests/` plus `config.yaml`. Ślad wersji `runner.py` przez całe zlecenie:

```
0a6151840dd230d7  (1. podejscie, z awaria)
3245b27cebac2a3f  (po naprawie akumulatora)
64435df0665d0450  (po dodaniu bramki na obcy VRAM — ta wersja policzyla pomiar)
```

Testy na laptopie: **104 zielone** (na maszynie nie ma pytesta i to zostaje bez zmian — lockfile
jest częścią pieczęci). Sonda przedstartowa na maszynie: `SONDA OK`.

Tokenizer przeżył obie synchronizacje, archiwa transferowe usunięte.

## Stan maszyny po biegu

Katalog `C:\Users\operator\spektra1` zawiera kod, wyniki i checkpointy (w tym
`positional_mu.npz`, 555 MB). Poza katalogiem objętym rollbackiem nadal jest **jeden obiekt
systemowy**: zadanie `SPEKTRA1-pomiar-pilota` w Harmonogramie, stan `Disabled`.

Rollback: `Remove-Item -Recurse -Force C:\Users\operator\spektra1, C:\Users\operator\spektra1-env`
plus `schtasks /delete /tn SPEKTRA1-pomiar-pilota /f`.

Skoro pomiar się zakończył, zadanie w Harmonogramie **nie jest już potrzebne** — do usunięcia,
chyba że planowany jest kolejny bieg (np. pomiar główny po pieczęci, który ma iść tym samym
runnerem).

## Co czeka na czat prowadzącego

1. **T5: przeliczenie `I_total`, `I_-1` i `k`** z `spectra.parquet` po estymacji nullu
   symulacyjnego — dziś są policzone względem `lambda_star = inf` (placeholder).
2. **Decyzja o `spectra.parquet`** (48,4 MB): jest ignorowany przez `.gitignore`, więc nie
   trafi do repo przez commit. Jeśli ma być częścią pakietu pieczęci, potrzebna inna droga.
3. **Usunięcie zadania z Harmonogramu** albo świadome zostawienie go pod pomiar główny.
4. **Zaktualizować wzorzec rozmiaru paczki w zleceniach** ze ~140 KB na ~180 KB (dziś 181 KB /
   110 plików — wykluczenia czyste, to realny przyrost kodu).
