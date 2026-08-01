# Etapy replikacji i co wraca do repo

Dokument dla agenta prowadzącego replikację, dla zespołu badawczego i dla
osób trzecich chcących powtórzyć badanie. Każdy etap kończy się **jednym plikiem wyników** przekazanym dowolnym kanałem.
**Na koncie właściciela maszyny nie powstaje nic** — żadnych forków, repozytoriów
ani gałęzi. Wyniki dołącza do repozytorium zespół badawczy.

**Zasada przepływu:** z maszyny replikującej wychodzą **wyłącznie wyniki
liczbowe i raporty**. Nigdy: wagi modelu, pliki tokenizera, dane operatora,
zawartość jego dysku. Kierunek do maszyny: publiczny kod i korpus, nic więcej.

---

## Etap 0 — kwalifikacja sprzętu (jest zbudowany)

| | |
|---|---|
| Co robi | 6 testów: środowisko, GATE 0 numeryczny, powtarzalność forwardu co do bitu, zgodność struktury modelu, sumy kontrolne wag, tempo |
| Model | `gemma-3-4b-it` (8 GB) — ten sam, na którym zmierzono badanie główne |
| Czas | ~30 min łącznie z pobraniem |
| **Wraca do repo** | `replikacja/RAPORT-KWALIFIKACJA.md` + `.json` (~10 KB) |
| Decyzja po etapie | zespół: pomiar na akceleratorze czy na procesorze |

## Etap 1 — kalibracja krzyżowa (nasz wzorzec + jego pomiar)

| | |
|---|---|
| Co robi | liczy widmo dla **ustalonego tekstu z zapieczętowanego korpusu**, na ustalonej warstwie, i porównuje z wzorcem policzonym na maszynie odniesienia |
| Po co | dowód, że wynik badania **nie jest artefaktem jednej karty graficznej** — wzmacnia SPEKTRA-1, nie tylko przygotowuje replikację |
| Czas | minuty (model już pobrany) |
| **Wraca do repo** | `replikacja/RAPORT-KALIBRACJA.md` + `.json` (~10 KB) |

## Etap 2 — semantyka warstw nowego modelu (dopiero przy modelu 27B)

| | |
|---|---|
| Co robi | hookami odkrywa architekturę: który stan jest embeddingiem, gdzie kończy się blok, mapa uwagi, skład pasma pomiarowego |
| Po co | protokół **zabrania zakładać** cokolwiek o architekturze — każdy nowy model musi zostać zbadany przed pomiarem |
| Czas | ~15 min |
| **Wraca do repo** | `docs/layer_semantics-<model>.md` + `.json` (~20 KB) |

## Etap 3 — pomiar główny

| | |
|---|---|
| Co robi | 624 teksty (48 scenariuszy × 5 wariantów + nulle) przez wszystkie warstwy, dwa przebiegi |
| Czas | zależny od modelu i sprzętu — **etap 0 podaje szacunek**; rozkłada się na kilka sesji, checkpoint po każdym tekście |
| **Wraca do repo** | `metrics.parquet` (1–3 MB), `dropped_tokens.csv` (2 KB), `runner.log`, raport etapu |
| **Wraca jako załącznik wydania** | `spectra.parquet` — pełne widma; przy modelu 27B rzędu 150–300 MB, więc dzielone per język |
| **Zostaje na maszynie** | `positional_mu.npz` (~1,4 GB) — odtwarzalny deterministycznie, nie ma sensu przesyłać |

## Etap 4 — progi widmowe

| | |
|---|---|
| Co robi | symuluje szum o statystyce zmierzonej w etapie 3 i wyznacza poprzeczkę, powyżej której struktura jest realna |
| Czas | kilkanaście godzin, **wyłącznie procesor** — nie blokuje karty, właściciel może normalnie pracować |
| **Wraca do repo** | `t5_lambda_star.parquet` (~50 KB), `t5_phi.json` |

## Etap 5 — analiza (po naszej stronie, bez maszyny replikującej)

Konfirmacja wg zamrożonej hierarchii, porównanie z wynikiem pierwotnym,
raport replikacji. Maszyna replikująca jest już wtedy wolna.

---

## Podsumowanie przepływu

| Kierunek | Co | Rozmiar |
|---|---|---|
| do maszyny | publiczny kod + korpus (repo) | ~400 KB |
| do maszyny | wagi modelu z HuggingFace (nie od nas) | 8 GB / 54 GB |
| **z maszyny** | raporty etapów 0–2 | ~40 KB |
| **z maszyny** | metryki i progi (etapy 3–4) | ~3 MB |
| **z maszyny** | widma (etap 3) | 50–300 MB, jako załącznik wydania |
| nigdy z maszyny | wagi, tokenizer, dane operatora, cokolwiek prywatnego | — |

Każdy etap jest **niezależnie przerywalny i wznawialny**. Zakończenie etapu
= jeden plik wyników = punkt, w którym można przerwać współpracę bez straty.
Duże pliki (widma) przekazywane kanałem wskazanym przez właściciela maszyny.
