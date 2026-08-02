# DEP — Zlecenie 09: PLLuM-4B, weryfikacja warstw i bramka pamięci

**Maszyna:** ta sama co w zleceniach 02–08.
**Katalog roboczy:** ten sam; ścieżki względne.
**Środowisko:** bez zmian, **nic nie instalować** — PLLuM jest architekturą Gemmy,
więc obecne biblioteki wystarczą.
**Czas:** pobranie ~20–40 min + sprawdzenia ~30 min.

## Po co

SPEKTRA-2 ma mierzyć na dwóch modelach: `google/gemma-3-4b-it` (jak dotąd)
i `CYFRAGOVPL/PLLuM-4B-instruct-2512`. PLLuM wyrasta z `gemma-3-4b-pt`, więc
**architektura powinna być tożsama** — 34 bloki, hidden 2560. To zlecenie ma
tego **dowieść, a nie założyć**, oraz zmierzyć, czy model mieści się w bramce
pamięci na 16 GB.

Bez tych dwóch liczb nie da się zapieczętować protokołu.

## Krok 1 — pobranie wag

Do pobrania: **`CYFRAGOVPL/PLLuM-4B-instruct-2512`, około 9 GB**, licencja
Apache 2.0, źródło HuggingFace. Same wagi i pliki modelu — **bez datasetów**.

Tokenizer masz już na maszynie ze zlecenia 07a.

## Krok 2 — weryfikacja indeksacji warstw hookami

To jest odpowiednik zadania T2 ze SPEKTRY-1. Materiałem testowym mogą być
**3–5 tekstów z korpusu SPEKTRY-1** — to badanie jest zamknięte i opublikowane,
więc nie ma tu żadnego zaślepienia do naruszenia. Korpus SPEKTRY-2 jeszcze
nie istnieje.

```
..\spektra1-env\Scripts\python.exe -m pipeline.layer_semantics --model CYFRAGOVPL/PLLuM-4B-instruct-2512
```

Jeśli moduł nie przyjmuje parametru `--model`, zgłoś to zamiast obchodzić —
dopiszę przełącznik.

**Do raportu:**
1. Liczba elementów `hidden_states` — oczekiwane **35** (embedding + 34 bloki).
2. Wymiar ukryty — oczekiwane **2560**.
3. **Który indeks jest już po normalizacji końcowej.** W Gemmie to indeks 34
   i był to realny problem, wykryty dopiero hookami. Jeśli w PLLuM wypadnie
   inaczej — to jest najważniejsza informacja z całego zlecenia.
4. Skład typów bloków w paśmie 14–27 (uwaga i attention wg raportu T2).
5. Czy nasz kod wyciągania stanów **w ogóle rusza** na tym modelu bez zmian.

## Krok 3 — bramka pamięci

Forward na najdłuższym z tekstów testowych, bf16, ten sam budżet okna co
w SPEKTRZE-1 (1024 tokeny), z włączoną bramką pamięci.

**Do raportu:**
- `max_memory_allocated` w GB. Odniesienie: Gemma dała **8,85 GB**.
- Czy bramka (próg 14 GB) się nie odezwała.
- Czy pojawiło się przelewanie do RAM (bramka na obce zużycie karty).

Jeśli PLLuM przekroczy 14 GB — **STOP i raport**, nie podnosić progu na własną
rękę. Próg jest zapieczętowany i jego zmiana wymaga aneksu.

## Krok 4 — pozycje insercji po szablonie

Domknięcie sprawy z raportu o tokenizerze: wiemy, że narzut szablonu jest stały
w obrębie scenariusza z dokładnością do jednego tokena. Zostaje pytanie, czy
**pozycje insercji** przesuwają się jednakowo we wszystkich wariantach.

Dla 5 tekstów SPEKTRY-1, po wyrenderowaniu szablonem każdego modelu, podaj
pozycję tokenową początku każdej insercji i różnicę między modelami. Jeśli
przesunięcie jest stałe — sprawa zamknięta. Jeśli zależy od wariantu — to jest
confound pozycyjny i musi trafić do protokołu.

## Raport

`ops/pllum-warstwy-i-pamiec.md`, konwencja bez nazw kont i hostów.

Zakres zmian: wyłącznie katalog roboczy plus pamięć podręczna HuggingFace.
Rollback: skasować model z pamięci podręcznej (~9 GB).

## Czego to zlecenie NIE robi

Zero pomiarów widma, zero metryk, zero perplexity. To jest wyłącznie
sprawdzenie, czy narzędzie działa na drugim modelu i czy się mieści.
Bramka manipulacji — czyli pytanie, **czy PLLuM w ogóle różni się od Gemmy
na naszym materiale** — to osobne zlecenie, po zamrożeniu kryteriów.
