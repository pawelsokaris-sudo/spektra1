# SPEKTRA-1 — Zapis rozstrzygnięć recenzji adwersaryjnej (do pakietu pieczęci)

**Recenzent:** GPT (rola: wrogi recenzent metodologiczny), 30.07.2026. Werdykt recenzji: WARUNKOWO.
**Rozstrzygający:** Paweł (decyzja) + Claude (implementacja). Konwencja: Multi-Model Pre-Review Protocol v2.2 (ActProof).
**Zasada:** każdy zarzut ma status PRZYJĘTY / PRZYJĘTY CZĘŚCIOWO / ODRZUCONY z lokalizacją naprawy w protokole v1.1.

| # | Zarzut (skrót) | Status | Rozstrzygnięcie → v1.1 |
|---|---|---|---|
| 1 | Podpróbkowanie kanałów estymuje inny obiekt; pełne widmo przez Grama | **PRZYJĘTY** | Konfirmacja wyłącznie na pełnym niezerowym widmie przez macierz Grama T′×T′; podpróbkowanie zdegradowane do eksploracji. §4. Uznane jako błąd matematyczny autorów v1.0. |
| 2 | Asymptotyczne λ⁺ MP nie jest właściwym nullem dla aktywacji transformera | **PRZYJĘTY** | MP tylko referencyjnie; λ* z empirycznego nullu symulacyjnego (separowalny czas × kanał, parametry z pilota) przez pełny pipeline; inferencja główna permutacyjna. §5–6. |
| 3 | Korpusy mieszają kilkanaście osi; A–C nie izoluje samozwrotności | **PRZYJĘTY** | Dopasowane czwórki scenariuszowe A/B/C/C′, identyczne tury/role/template, układ czynnikowy ze scenariuszem jako blokiem. §3. |
| 4 | Statystyka ślepa na porządek; język "pętli" bez narzędzia | **PRZYJĘTY** | Metryka porządku D_lag (σ₁ korelacji z opóźnieniem vs null permutacji kolejności) prerejestrowana w SPEKTRA-1 jako H4; język roszczeń zawężony (§0); pełna dynamika = SPEKTRA-2. |
| 5 | "Null mieszany" niejednoznaczny i nietrafny | **PRZYJĘTY** | Usunięty. Zastąpiony nullami interwencyjnymi N1–N3 (permutacja zdań, permutacja tur, kontrfaktyczny C′), każdy ponownie przez model, z osobnym pytaniem i kryterium. §6. |
| 6 | Brak analizy mocy; GATE 1 pozwalał dosypywać n po odślepieniu | **PRZYJĘTY** | Pilot M₀=8/język poza analizą główną → symulacja mocy dokładnej struktury → M dla ≥90% mocy przy SESOI d_z=0.8 *(korekta redakcyjna 2026-07-30: pierwotny zapis 0.5 był reliktem wersji roboczej; obowiązuje 0.8 zgodnie z protokołem v1.2-FINAL, decyzja kierownika badania)*; M i reguła stopu zamrożone przed pieczęcią; zakaz zmian po odślepieniu. Uznane jako błąd projektowy v1.0. §7. |
| 7 | Wykluczenie λ₁ może usuwać szukany efekt; konstrukcja kołowa | **PRZYJĘTY** | Endpoint główny = I_total (z λ₁); I₋₁ wyłącznie jako dekompozycja; zakaz wyboru post hoc. §5. |
| 8 | Brak jednoznacznej reguły rozstrzygnięcia H1 | **PRZYJĘTY** | H1 = jeden skalar Ī (średnia I_total po zamrożonym paśmie [0.4L, 0.8L]), jeden parowany kontrast C−A, test jednostronny, permutacja, α=0.01. Pasma z v1.0 tylko opisowo. §6. |
| 9 | Krawędź MP ≠ test istotności pojedynczej wartości własnej (Tracy–Widom) | **PRZYJĘTY** | λ* = empiryczne kwantyle 99% z nullu symulacyjnego per (warstwa, język). §5. |
| 10 | 50 podzbiorów ≠ 50 replikacji | **PRZYJĘTY** (bezprzedmiotowy po #1) | Jednostką inferencji scenariusz/tekst; podzbiorów brak w konfirmacji. §6. |
| 11 | Komponent pozycyjny nie znika po 32 tokenach | **PRZYJĘTY** | Estymacja i odejmowanie średniej per pozycja; wariant bez odejmowania jako prerejestrowana analiza wrażliwości (GATE 3b); identyczna struktura pozycyjna wariantów scenariusza. §3–4, §7. |
| 12 | PL/EN niekontrolowane "stałymi proporcjami"; "Gemma" niedookreślona | **PRZYJĘTY** | Języki jako osobne repliki prerejestrowane; dopasowanie tokeny/słowo i znaki/token raportowane; dokładny wariant modelu + rewizja + suma kontrolna w pieczęci. §2–3. |
| 13 | Model mieszany niedookreślony, prawdopodobnie antykonserwatywny | **PRZYJĘTY** | Konfirmacja permutacyjna (wiersz tabeli = scenariusz, kontrast parowany); modele parametryczne tylko opisowo z pełną specyfikacją zagnieżdżenia. §6. |
| 14 | Jeden model gaussowski nie pasuje do metryk | **PRZYJĘTY** | Rodziny per metryka (beta/logit, NB); konfirmacja permutacyjna niezależna od tych założeń. §6. |
| 15 | Wielokrotność drastycznie niedoszacowana | **PRZYJĘTY** | Zamknięta hierarchia gatekeeping: H1 → H2 → {H3, H4, B−A, profil}; profil warstwowy przez klastrową permutację; nic poza hierarchią nie jest konfirmacyjne. §6. |
| 16 | H3 wymaga testu równoważności, nie braku istotności | **PRZYJĘTY** | TOST z marginesem \|d\| < 0.3. §1. |
| 17 | "Falsyfikacja przez brak istotności" sprzeczna wewnętrznie | **PRZYJĘTY** | Werdykt trójwartościowy: wykryty / praktycznie wykluczony / niekonkluzywny; każdy publikowany. §0. |
| 18 | fp16 może tworzyć/tłumić korelacje; brak reguł numerycznych | **PRZYJĘTY** | bf16 główne + fp32 na 10% tekstów z zamrożoną tolerancją; reguła kanałów niskiej wariancji; determinizm środowiska w pieczęci. §2. |
| 19 | Semantyka hidden_states niezdefiniowana | **PRZYJĘTY** | Weryfikacja hookami przed pomiarem; embedding poza pasmami; indeksacja w pieczęci. §2. |
| 20 | Pasma mogą aliasować typy bloków (attention lokalna/globalna) | **PRZYJĘTY** | Mapa typów bloków przed pomiarem; skład pasma raportowany; typ bloku jako kowariancja wtórna. §2, §6. |
| 21 | Chat template i tokeny specjalne mogą wyjaśnić wynik | **PRZYJĘTY** | Identyczny template dla wszystkich wariantów włącznie z A; tokeny specjalne maskowane w korelacji; wariant z nimi = eksploracja. §3. |
| 22 | Przycinanie do 1024 nieneutralne | **PRZYJĘTY** | Teksty budowane do budżetu z naturalnym zakończeniem; zakaz przycinania. §3. |
| 23 | Niezależność 40 tekstów niewykazana | **PRZYJĘTY** | Metadane pochodzenia zamrożone; ≤2 teksty/szablon; scenariusz jako blok; jednostka inferencji = scenariusz. §3, §6. |
| 24 | GATE 3 nieoperacyjny | **PRZYJĘTY** | Kryteria ilościowe: identyczny znak Δ₁ i \|zmiana\| ≤ 25% w trzech zdefiniowanych wariantach; niepowodzenie = werdykt "niestabilny", publikowany. §7. |
| 25 | Wynik dodatni ma wiele wyjaśnień; roszczenia wymagają matched counterfactual | **PRZYJĘTY** | Hierarchia roszczeń w §0: bez przejścia C−C′ wynik nazywany wyłącznie klasyfikacją korpusów. To ograniczenie wpisane, nie obchodzone. |
| 26 | Mianownik I i traktowanie λ₁ niespójne | **PRZYJĘTY** | Wzory jawne: mianownik = tr; I_total i I₋₁ zdefiniowane osobno. §5. |
| 27 | Entropia widmowa niezdefiniowana | **PRZYJĘTY** | Wzór z pᵢ=λᵢ/tr, zera wykluczone, normalizacja ln r. §5. |
| 28 | PR₁ zależne od bazy | **PRZYJĘTY** | Zdegradowane do charakterystyki pomocniczej parametryzacji. §5. |
| 29 | Cohen d niezdefiniowany dla struktury mieszanej | **PRZYJĘTY** | d_z na poziomie parowanych różnic scenariuszowych, zdefiniowane w §6. |
| 30 | 95% CI niespójne z α=0.01 | **PRZYJĘTY** | 99% CI dla decyzji konfirmacyjnych; 95% tylko dodatkowo. §6. |
| 31 | Pieczęć bez środowiska nie gwarantuje odtwarzalności | **PRZYJĘTY** | Lockfile + obraz kontenera + tokenizer + ustawienia deterministyczne + test replikacji w pieczęci. §2, §7. |
| 32 | "Dane surowe" niejednoznaczne | **PRZYJĘTY** | Poziomy publikowanych danych i formaty wymienione w §8. |

**Bilans:** 32/32 przyjęte (dwa — #1 i #6 — uznane wprost jako błędy autorów v1.0, odnotowane dla uczciwości zapisu). Zarzutów odrzuconych: 0. Jedna świadoma granica utrzymana wbrew duchowi zarzutu 4: pełna analiza dynamiczna pozostaje w SPEKTRA-2, ale SPEKTRA-1 otrzymała minimalną metrykę porządku (D_lag), więc centralny język teorii ma narzędzie już teraz.

**Wniosek:** warunki werdyktu "WARUNKOWO" spełnione w v1.1. Dokument dołączany do pakietu pieczęci jako dowód procesu pre-review.
