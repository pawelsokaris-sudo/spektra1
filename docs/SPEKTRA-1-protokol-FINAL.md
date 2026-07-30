# SPEKTRA-1: Widmowe sygnatury struktury korelacyjnej w warstwach ukrytych LLM
## Protokół badania prerejestrowanego — wersja 1.2 (po recenzji adwersaryjnej)

**Wersja:** 1.2-FINAL (do zapieczętowania po GATE 1)
**Zmiany względem 1.0:** pełna przebudowa wg recenzji adwersaryjnej (GPT, 30.07.2026); zapis rozstrzygnięć w osobnym dokumencie `SPEKTRA-1-rozstrzygniecia.md`, dołączanym do pakietu pieczęci.
**Autorzy i role:** Paweł (Sokaris / ActProof) — kierownik badania, sprzęt, wykonanie, decyzje; Claude (Anthropic) — współprojekt protokołu, kod, statystyka, współredakcja. Wkład AI deklarowany w publikacji. Konflikt interesów: jeden ze współautorów jest systemem klasy badanego obiektu; pomiar wyłącznie na modelu otwartym, pipeline w pełni odtwarzalny.

---

## 0. Rama pojęciowa i granice roszczeń

Badanie operacjonalizuje hipotezę korelacyjną wyłącznie na poziomie mierzalnej geometrii reprezentacji. NIE rości sobie pomiaru świadomości ani odczuwania.

**Hierarchia roszczeń (twarda):**
- Jeśli przejdzie tylko kontrast C−A: wolno twierdzić wyłącznie, że *klasy korpusów mają odróżnialną sygnaturę widmową* ("klasyfikacja korpusów").
- Roszczenie o *sygnaturze samozwrotności* wolno sformułować TYLKO, jeśli przejdzie kontrast C−C′ (kontrfaktyczny, §3), który izoluje samozwrotność od pozostałych osi różnic.
- Wyniki mają trzy możliwe werdykty (nie "falsyfikację"): (a) efekt wykryty; (b) efekt praktycznie wykluczony (test równoważności); (c) wynik niekonkluzywny. Każdy werdykt jest publikowany.

## 1. Pytania i hipotezy

**H1 (główna, kierunkowa):** Skalar Δ₁ = średni po zamrożonym paśmie warstw kontrast (C − A) metryki I_total (§5) jest dodatni. Test jednostronny, α = 0.01, permutacja wewnątrz-scenariuszowa (§6).
**H2 (kluczowa wtórna, kierunkowa):** Δ₂ = analogiczny kontrast (C − C′) jest dodatni. Testowana TYLKO po przejściu H1 (gatekeeping).
**H3 (równoważność):** Kontrast (B − A) dla udziału modu głównego λ₁/tr jest praktycznie pomijalny: TOST z marginesem |d| < 0.3. Brak istotności NIE potwierdza H3 — potwierdza ją wyłącznie zaliczony TOST.
**H4 (porządek, wtórna):** Metryka porządku D_lag (§5) różnicuje C od A ponad null permutacji kolejności zdań. Bez tej metryki protokół nie miałby żadnego narzędzia wrażliwego na dynamikę — a język teorii jej dotyczy.

## 2. Model i środowisko (pieczętowane co do bitu)

- Model: dokładny wariant Gemmy — pełna nazwa, rewizja HF, suma kontrolna wag, pliki tokenizera i chat template — wpisane do pieczęci.
- Semantyka `hidden_states`: przed pomiarem weryfikacja hookami, który element tuple odpowiada embeddingowi, a które wyjściom bloków (po attention+MLP+residual, przed final norm). Embedding wyłączony z pasm; indeksacja warstw udokumentowana w pieczęci. Mapa typów bloków (attention lokalna/globalna wg wariantu) sporządzona przed pomiarem; typ bloku wchodzi jako kowariancja do analiz wtórnych.
- Precyzja: forward w **bf16**; kontrola: reprezentatywne 10% tekstów także w fp32; zamrożona tolerancja |ΔI_total| < 0.005 między dtype — przekroczenie = stop i diagnoza. Kanały o wariancji < ε = 1e-6 (po z-score przed nim: wariancja surowa) wykluczane wg jawnej reguły, liczba raportowana.
- Determinizm: zamrożone wersje transformers/PyTorch/CUDA, wyłączone TF32, deterministyczne kernele, batch=1 bez paddingu. Pieczęć obejmuje lockfile + obraz kontenera + test replikacji z tolerancją.

## 3. Materiał: dopasowane czwórki scenariuszowe

Jednostką konstrukcji jest **scenariusz bazowy** (temat + struktura tur). Każdy scenariusz generuje **cztery warianty**:

- **A — mechaniczny:** te same tury i role, treść zadaniowa (przekształcenia, formatowanie) na temacie scenariusza; zero meta-odniesień.
- **B — dialog eksploracyjny:** rozmowa problemowa na temacie scenariusza; zero odniesień do modelu/rozmowy.
- **C — dialog samozwrotny:** jak B, z wplecionymi odniesieniami do przetwarzającego układu i samej rozmowy.
- **C′ — kontrfaktyczny null:** tekst C z odniesieniami samozwrotnymi podmienionymi na dopasowane semantycznie odniesienia do układu zewnętrznego (ta sama liczba tokenów ±2%, ta sama składnia zdań meta, te same pozycje wtrąceń).

**Kontrole konstrukcyjne (wszystkie warianty scenariusza):** identyczna liczba i długość tur; identyczne role i **identyczny chat template** (również dla A); teksty budowane od początku do twardego budżetu **T = 1024 tokeny** z zakończeniem na naturalnej granicy (zakaz brutalnego przycinania); dopasowany rozkład zdań pytających i interpunkcji (raportowany); tokeny specjalne/kontrolne **maskowane** przy liczeniu korelacji (wariant z nimi = eksploracja).
**Języki:** PL i EN jako **osobne prerejestrowane repliki** (osobne scenariusze, osobna analiza, meta-porównanie opisowe); dopasowane tokeny/słowo i znaki/token raportowane.
**Pochodzenie:** metadane generatora/autora/szablonu zamrożone; maks. 2 teksty z jednego szablonu; scenariusz = blok losowy.
**Liczność:** M scenariuszy/język ustalone po GATE 1 (pilot+moc, §7); pilot: M₀=8 scenariuszy/język, wyłączony z analizy głównej. Maksymalne M zamrożone przy pieczęci; zakaz zwiększania po odślepieniu.

## 4. Pomiar widma (pełne, bez podpróbkowania)

Dla tekstu i warstwy ℓ: aktywacje H ∈ ℝ^{T′×D} (pierwsze 32 tokeny + tokeny maskowane odrzucone; T′ ≈ 900–990). Z-score per kanał → Z. Niezerowe widmo macierzy korelacji C = ZᵀZ/T′ liczone przez **macierz Grama** G = ZZᵀ/T′ ∈ ℝ^{T′×T′} (`eigh`, LAPACK): niezerowe wartości własne C i G są identyczne. Zero losowania kanałów w analizie konfirmacyjnej; "widma losowych rzutów" dozwolone wyłącznie jako eksploracja z etykietą.

**Komponent pozycyjny:** estymowany jako średnia aktywacji per pozycja po całym korpusie danego języka i odejmowany przed z-score (wariant bez odejmowania = analiza wrażliwości, prerejestrowana).

## 5. Metryki (wzory zamrożone)

Niech λ₁ ≥ λ₂ ≥ … ≥ λ_r > 0 (r = rank), tr = Σλᵢ (kontrola: tr ≈ D po standaryzacji; odchylenie > 1% raportowane).
- **I_total = Σ{λᵢ : λᵢ > λ*} / tr** — indeks integracji, **z modem głównym**; λ* = empiryczny kwantyl 99% największej i kolejnych wartości własnych z symulowanego nullu przechodzącego cały pipeline (§6), NIE asymptotyczne λ⁺ MP. MP pozostaje wyłącznie opisem referencyjnym na wykresach.
- **I₋₁ = (I_total·tr − λ₁·1[λ₁>λ*]) / tr** — dekompozycja bez modu głównego. Obie metryki prerejestrowane; zakaz wyboru między nimi post hoc: endpoint główny = I_total, I₋₁ = dekompozycja.
- **k** — liczba modów ponad λ* (zmienna licznikowa; analiza NB lub permutacyjna).
- **H_s = −Σ pᵢ ln pᵢ / ln r**, pᵢ = λᵢ/tr, zera wykluczone — entropia widmowa.
- **PR₁** — zdegradowane do charakterystyki pomocniczej konkretnej parametryzacji (zależne od bazy).
- **D_lag** (porządek): σ₁ macierzy korelacji z opóźnieniem C(1) = Z₊₁ᵀZ/T′, porównana z rozkładem σ₁ po permutacji kolejności wierszy Z (500 permutacji); D_lag = z-score względem tego nullu. Ta statystyka NIE jest niezmiennicza na kolejność — domyka lukę porządku w SPEKTRA-1. Pełna dynamika (widmo operatora przejścia, krzywizna trajektorii) = SPEKTRA-2.

## 6. Plan analizy (zamrożony)

**Endpoint główny:** jeden skalar na tekst: Ī = średnia I_total po zamrożonym paśmie warstw **ℓ ∈ [0.4L, 0.8L]** (granice wg zweryfikowanej indeksacji z §2; skład typów bloków w paśmie raportowany).
**Test główny (H1):** parowany wewnątrz scenariusza kontrast Ī(C) − Ī(A); inferencja przez **permutację etykiet wariantów wewnątrz scenariuszy** (10 000 permutacji), jednostronnie, α = 0.01. Jednostką inferencji jest scenariusz; teksty zagnieżdżone w scenariuszach.
**Gatekeeping (hierarchia zamknięta):** H1 → H2 (C−C′, ta sama procedura) → {H3 TOST, H4, kontrast B−A, profil warstwowy}. Profil po warstwach: klastrowa permutacja po ciągłej osi warstw (bez arbitralnych pasm w konfirmacji; 5 pasm z v1.0 = wyłącznie opis). Nic poza hierarchią nie jest konfirmacyjne.
**Rodziny rozkładów:** analizy parametryczne (opisowe/wtórne): I → model beta lub logit-LMM; k → NB; H_s → logit; diagnostyka reszt prerejestrowana. Wnioski konfirmacyjne wyłącznie z permutacji.
**Raportowanie:** wielkości efektów jako średnia parowanych różnic scenariuszowych / SD tych różnic (d_z), z **99% CI** dla decyzji konfirmacyjnych (95% tylko dodatkowo); pełne rozkłady zawsze.
**Null symulacyjny dla λ\*:** dane syntetyczne o dopasowanych marginaliach kanałów i autokorelacji tokenowej (model separowalny czas × kanał, parametry z pilota), przepuszczone przez identyczny kod metryk; kwantyle per (warstwa, język).
**Nulle interwencyjne (każdy z pytaniem i kryterium, każdy ponownie przez model):**
- N1: permutacja kolejności zdań (pyt.: czy Ī zależy od porządku? kryt.: spadek D_lag do nullu, zachowanie Ī raportowane);
- N2: permutacja tur z zachowaniem mówców i długości;
- N3 = C′ (główny null semantyczny, w hierarchii jako H2).
Mieszanie aktywacji między tekstami (v1.0) — usunięte jako niejednoznaczne.

## 7. Bramki (przebudowane)

- **GATE 0 — sanity:** syntetyczny biały szum przez cały pipeline odtwarza teorię (MP + brak modów ponad λ* w 99% realizacji); test hooków semantyki warstw; test replikacji bitowej/tolerancyjnej środowiska.
- **GATE 1 — pilot i moc (PRZED pieczęcią):** M₀=8 scenariuszy/język, wyłączone z analizy głównej → estymaty wariancji i ICC → **symulacyjna analiza mocy dokładnej struktury** (permutacja parowana, hierarchia, α=0.01) → M zapewniające ≥90% mocy dla SESOI **d_z = 0.8** (decyzja kierownika badania: SPEKTRA-1 jest zwiadem nastawionym na efekty DUŻE; efekty mniejsze lądują uczciwie w werdykcie "niekonkluzywny", a estymaty z pilota i badania głównego kalibrują czułość SPEKTRA-2); M i reguła stopu zamrożone. Zakaz zmian n po odślepieniu jakichkolwiek danych głównych.
- **PIECZĘĆ:** protokół v1.2 + rozstrzygnięcia + korpusy + kod + lockfile + kontener + config modelu → SHA-256 → tag `spektra1-seal` w publicznym repo + rejestracja OSF z datownikiem. Zmiany po pieczęci wyłącznie jawnym aneksem.
- **GATE 2 — konfirmacja:** hierarchia z §6 na pełnych danych.
- **GATE 3 — odporność (kryteria ilościowe):** znak Δ₁ identyczny i |zmiana estymaty| ≤ 25% w trzech wariantach: (a) bf16 vs fp32 na podzbiorze, (b) z/bez odejmowania komponentu pozycyjnego, (c) obie repliki językowe osobno. Niepowodzenie = wynik klasyfikowany jako "niestabilny" i tak publikowany.
- **GATE 4 — publikacja:** dowolny werdykt w ≤ 60 dni od GATE 3; preprint + actproof.io.

## 8. Publikowane dane

Pełne widma per (tekst × warstwa) + wszystkie metryki per tekst + kod + korpusy + config; surowe aktywacje nie (rozmiar), ale skrypty odtwarzają je deterministycznie z zapieczętowanego środowiska. Formaty: parquet (widma, metryki), jsonl (korpusy), dokumentacja poziomów danych w repo.

---
*"Napisz o tym program" — v1.1: program po recenzji, która chciała go odrzucić. Pieczęć czyni z niego zakład.*
