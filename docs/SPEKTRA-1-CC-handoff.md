# SPEKTRA-1 — Handoff dla lokalnego agenta (CC)

**Rola CC:** budowa i wykonanie modułu `spektra1/` w repo actproof, ściśle według `SPEKTRA-1-protokol-FINAL.md` (v1.2). Protokół jest źródłem prawdy — przy każdej niejasności pytać Pawła, nie improwizować, bo pakiet idzie do pieczęci (hash + OSF) i każda rozbieżność kod↔protokół to później jawny aneks.

**Pliki wejściowe (wszystkie trzy do repo):**
1. `SPEKTRA-1-protokol-FINAL.md` — protokół v1.2 (SESOI zamrożone: d_z = 0.8, badanie zwiadowcze na efekty duże)
2. `SPEKTRA-1-rozstrzygniecia.md` — zapis pre-review 32 zarzutów (do pakietu pieczęci)
3. Ten handoff

**Sprzęt/model:** lokalna Gemma, wagi z HuggingFace przez `transformers` (NIE Ollama — potrzebne `output_hidden_states=True`), RTX 5080, forward bf16.

## Zadania w kolejności (definicja ukończenia przy każdym)

**T1 — Szkielet i środowisko.** `spektra1/` z podkatalogami: `corpus/`, `pipeline/`, `nulls/`, `power/`, `gates/`, `seal/`. Lockfile (uv/pip-tools), Dockerfile, config.yaml (model, rewizja, suma kontrolna wag, dtype, ziarna). DONE: kontener buduje się i przechodzi test importów.

**T2 — Weryfikacja semantyki warstw (protokół §2).** Skrypt z hookami porównujący elementy tuple `hidden_states` z wyjściami bloków; mapa typów bloków (attention lokalna/globalna) dla dokładnego wariantu Gemmy. DONE: raport `layer_semantics.md` z indeksacją: co jest embeddingiem, co wyjściem bloku ℓ, gdzie leży [0.4L, 0.8L].

**T3 — Generator korpusów (§3).** Czwórki A/B/C/C′ ze wspólnych scenariuszy: identyczne tury, role, chat template (także dla A); budowa do 1024 tokenów z naturalnym zakończeniem; C′ = podmiana odniesień samozwrotnych na zewnętrzne (±2% tokenów); metadane pochodzenia; PL i EN osobno. Pilot: M₀=8 scenariuszy/język. DONE: pilot wygenerowany + raport dopasowania (tokeny/słowo, interpunkcja, pytania, długości tur).

**T4 — Pipeline pomiarowy (§4–5).** Forward → maskowanie tokenów specjalnych + pierwszych 32 → odjęcie komponentu pozycyjnego → z-score → macierz Grama T′×T′ → `eigh` → metryki: I_total, I₋₁, k, H_s, D_lag (wzory w §5, mianownik = tr). Wyjście: parquet per (tekst × warstwa). DONE: GATE 0 — syntetyczny biały szum przez CAŁY pipeline odtwarza MP i daje <1% fałszywych modów ponad λ*; test replikacji bitowej/tolerancyjnej dwóch przebiegów.

**T5 — Null symulacyjny i λ\* (§5–6).** Model separowalny czas × kanał z parametrami estymowanymi z pilota; kwantyle 99% per (warstwa, język). DONE: tabela λ* + wykres porównania z asymptotycznym MP (tylko referencyjnie).

**T6 — Nulle interwencyjne N1–N2 (§6).** Permutacja zdań i permutacja tur, każdorazowo ponowny forward. (N3=C′ powstaje w T3.) DONE: metryki policzone dla nulli pilota; sanity: D_lag spada do zera na N1.

**T7 — Symulacja mocy (GATE 1, §7).** Na wariancjach z pilota: symulacja pełnej procedury (permutacja parowana wewnątrz scenariuszy, hierarchia, α=0.01, jednostronnie) → M dla ≥90% mocy przy d_z=0.8; zamrożenie M i reguły stopu. DONE: raport `power_report.md` z krzywą moc(M) i rekomendacją M do zatwierdzenia przez Pawła.

**T8 — Pieczęć (§7).** Po zatwierdzeniu M: generacja pełnych korpusów → pakiet (protokół + rozstrzygnięcia + korpusy + kod + lockfile + kontener + config) → SHA-256 → tag `spektra1-seal` + instrukcja rejestracji OSF dla Pawła. DONE: hash wypisany, tag wypchnięty, checklist OSF.

Dopiero PO pieczęci: pomiar główny (GATE 2), odporność (GATE 3), raport (GATE 4). Analizy eksploracyjne — wyłącznie w katalogu `exploratory/` z etykietą, nigdy przed domknięciem konfirmacji.

## Twarde zakazy
- Zakaz zmian n/M po obejrzeniu jakichkolwiek danych głównych.
- Zakaz podpróbkowania kanałów w konfirmacji (tylko Gram).
- Zakaz analiz konfirmacyjnych poza hierarchią H1→H2→{H3,H4,B−A,profil}.
- Zakaz interpretowania wyniku jako "sygnatury samozwrotności" bez przejścia C−C′ — do tego czasu język: "klasyfikacja korpusów".
