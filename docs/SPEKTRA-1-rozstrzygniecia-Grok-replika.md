# Rozstrzygnięcia po recenzji zewnętrznej: replika modelowa (2026-08-02)

## Przyjęte bez zastrzeżeń
Zawężenie roszczenia do testu odwrócenia asymetrii (nie „rozdzielenie trzech
wyjaśnień"). Surowa Δ₁ jako endpoint przecięcia; d_z wyłącznie wewnątrz modelu;
SD(Δ) raportowane per model. Zakaz porównywania bezwzględnych I_total między
modelami. Obowiązkowa bramka kompetencji EN przed pomiarem. Osobne wyprowadzenie
pasma warstw hookami. Pieczęć + rejestracja PRZED pierwszym forwardem.
Replika NIE usuwa confoundu abstrakcyjne–konkretne.

## ODRZUCONE: rekomendacja „base zamiast Instruct"
Błąd faktograficzny recenzenta. SPEKTRA-1 działała na `google/gemma-3-4b-it`
(wersja instrukcyjna), a korpus jest renderowany **szablonem rozmowy Gemmy**,
którego suma kontrolna jest w zapieczętowanym configu. Teksty to dialogi z
rolami i turami; wersja bazowa nie ma szablonu rozmowy. Użycie base zerwałoby
porównywalność z badaniem, które replikujemy. **Decyzja: Instruct.**

## DOPISANE (nie zauważone ani przez recenzenta, ani przez nas wcześniej)
**Szablon rozmowy jest częścią bodźca i różni się między modelami.** To trzecie
źródło nierównoważności obok architektury i tokenizera: ten sam korpus
wyrenderowany dwoma szablonami to dwie różne sekwencje, zanim zacznie się
tokenizacja. Do sekcji ograniczeń, wprost.

## DO WERYFIKACJI (nie przyjmować na słowo)
Recenzent podał: Bielik 4.5B = 60 warstw, D=2048, adaptacja Qwen2.5, tokenizer
APT4; PLLuM ma wariant 4B od maja 2026. **Nic z tego nie zostało potwierdzone.**
Projektowanie pasma i budżetu pamięci na niezweryfikowanym opisie architektury
byłoby tym samym błędem, przed którym recenzent ostrzega. Odczytać z kart modeli.

## MOC PRZECIĘCIA — policzona na empirycznych wariancjach ze SPEKTRY-1
Asymetria na Gemmie: **+0,00215** (Δ_PL − Δ_EN). SD per scenariusz: EN 0,00218,
PL 0,00243, n=24 na język. Symulacja 3000 powtórzeń, α=0,01 jednostronnie,
korelacja między modelami w obrębie scenariusza ρ=0,3 (nieznana, założona).

| Zachowanie Bielika | Interakcja | M=24 | M=32 | M=48 |
|---|---:|---:|---:|---:|
| pełne odwrócenie | −0,00431 | 1,00 | 1,00 | 1,00 |
| odwrócenie połowiczne | −0,00323 | 0,95 | 0,99 | 1,00 |
| zrównanie (brak asymetrii) | −0,00215 | **0,64** | 0,78 | 0,94 |
| osłabienie o połowę | −0,00108 | 0,15 | 0,22 | 0,33 |
| osłabienie o ćwierć | −0,00054 | 0,05 | 0,06 | 0,09 |

Minimalny wykrywalny efekt przy mocy 0,90 i M=24: **0,00291** = 1,35× asymetria
z Gemmy.

**Wniosek dla prerejestracji:** badanie jest wykonalne **wyłącznie dla hipotezy
odwrócenia**. Zrównanie (0,64) i osłabienie (0,15) muszą być z góry
zadeklarowane jako wyniki, których ta próba prawdopodobnie nie rozstrzygnie.
Bez tego zamrozilibyśmy hipotezę niewykrywalną — Aneks 4 w drugą stronę.

**Tania dźwignia:** 8 scenariuszy pilotowych na język istnieje i jest
zwalidowanych; były wyłączone ze SPEKTRY-1 z założenia, nie z powodu wady.
W nowym, osobno prerejestrowanym badaniu wolno ich użyć po jawnej deklaracji.
Daje M=32 i podnosi wykrywalność zrównania z 0,64 do 0,78 bez pisania
ani jednego scenariusza.

## Czeka na decyzję kierownika badania
1. Czy robimy replikę modelową (koszt: ~doba maszyny + dzień przygotowania).
2. Czy M=32 z użyciem pilotów, czy M=24 bez nich.
3. Czy hipoteza główna = odwrócenie kierunkowe, czy zestaw werdyktów.

---

# ZMIANA WYBORU MODELU (2026-08-02, po weryfikacji źródeł)

Recenzent wspomniał mimochodem, że PLLuM 4B może być oparty o Gemmę, i sam
oznaczył to jako niezweryfikowane. **Sprawdziliśmy. Jest prawdą.**

Karta modelu `CYFRAGOVPL/PLLuM-4B-instruct-2512` podaje wprost:
**„Based On: gemma-3-4b-pt"** — czyli ta sama podstawa co `gemma-3-4b-it`
użyta w SPEKTRZE-1, dotrenowana na polskim (z domieszką angielskiego).
Licencja Apache 2.0. Trzy warianty: base, instruct, chat.

## Dlaczego to jest lepszy model niż Bielik

| | PLLuM-4B-instruct | Bielik-4.5B-Instruct |
|---|---|---|
| Architektura | **identyczna z Gemmą** | Qwen2.5 przez Depth Up-Scaling |
| Liczba warstw / wymiar | **te same co w SPEKTRZE-1** | 60 / 2048 — inne |
| Tokenizer | **prawdopodobnie ten sam** (do sprawdzenia) | APT4, inny |
| Szablon rozmowy | pochodna Gemmy (do sprawdzenia) | własny |
| Pasmo warstw | **przenosi się** — weryfikacja zamiast wyprowadzania | do wyprowadzenia od zera |
| Wyrównanie korpusu ±0,2% | **przenosi się**, jeśli tokenizer ten sam | do przeliczenia, ryzyko rundy poprawek |

**Trzy warstwy nierównoważności, które recenzent słusznie nazwał — szablon,
tokenizer, architektura — przy PLLuM-ie w dużej mierze znikają.** Zostaje
dokładnie ta jedna zmienna, którą chcemy izolować: **dotrenowanie na polskim.**

To unieważnia jego własny zarzut z punktu 1 (splątanie architektura × język)
w stopniu, w jakim żaden inny dostępny model tego nie robi.

## Uczciwy kontrargument: siła manipulacji

Ta sama podstawa to zaleta dla czystości i **ryzyko dla siły efektu**. Bielik
jest modelem zbudowanym wokół polskiego; PLLuM-4B to Gemma **dotrenowana**.
Jeśli dotrenowanie było lekkie, manipulacja może być za słaba, żeby cokolwiek
odwrócić — i dostaniemy brak efektu z powodu, który nie ma nic wspólnego
z hipotezą.

**Do sprawdzenia przed pieczęcią:** ile tokenów polskiego wchłonął PLLuM-4B
i jak bardzo wagi odbiegły od `gemma-3-4b-pt`. Bez tej liczby nie wiadomo,
czy badanie w ogóle manipuluje tym, co ma manipulować.

## Rekomendacja

**PLLuM-4B-instruct jako model podstawowy** — czysty kontrast, przenoszalny
korpus i pasmo, drastycznie tańsze przygotowanie. **Bielik-4.5B-Instruct jako
opcjonalny drugi model**: mocna manipulacja przy splątanej architekturze.
Razem obejmują pytanie z dwóch stron — czysto ale słabo, oraz mocno ale brudno.
Jeśli budżet pozwala tylko na jeden: PLLuM.

## Nadal wymaga sprawdzenia (nie przyjmować z karty modelu)
1. Czy tokenizer jest **identyczny** z Gemmą (suma pliku), czy rozszerzony.
2. Czy szablon rozmowy PLLuM-instruct różni się od szablonu Gemmy.
3. Indeksacja warstw hookami — weryfikacja, nie założenie.
4. Liczba tokenów dotrenowania (siła manipulacji).
5. Szczyt pamięci na karcie 16 GB z tą samą bramką co w SPEKTRZE-1.

---

# ETAP 0 — WYNIKI WERYFIKACJI (2026-08-02) + KOREKTA WŁASNEJ OBIETNICY

Sprawdzone z publicznych plików `CYFRAGOVPL/PLLuM-4B-instruct-2512` wobec
naszych **zapieczętowanych** sum z `config.yaml`.

| Element | PLLuM | SPEKTRA-1 (Gemma) | Wynik |
|---|---|---|---|
| klasa architektury | `Gemma3ForConditionalGeneration` | ta sama | **identyczna** |
| liczba bloków | 34 | 34 | **identyczna** |
| hidden_size | 2560 | 2560 | **identyczna** |
| `tokenizer.json` sha256 | `86ff7e6e…` | `4667f208…` | **różni się** |
| `tokenizer_config.json` | `cfbb540f…` | `bfe25c27…` | **różni się** |
| szablon rozmowy sha256 | `b3f59621…` (1046 zn.) | `7de1c58e…` | **różni się** |
| vocab_size | 262147 | (niezapisane w naszym configu) | do porównania |
| tokeny dotrenowania | **karta nie podaje** | — | ryzyko otwarte |

## Korekta

W poprzedniej sekcji napisałem, że przy PLLuM-ie „trzy warstwy
nierównoważności w dużej mierze znikają". **To było za optymistyczne i tego
nie potwierdzam.** Znika **jedna** — architektura, i to całkowicie. Tokenizer
i szablon rozmowy **zostają** jako realne różnice bodźca.

Co nadal zyskujemy wobec Bielika: pasmo warstw, indeksacja i budżet pamięci
przenoszą się, bo architektura jest tożsama. Weryfikacja hookami staje się
sprawdzeniem znanej odpowiedzi, nie wyprowadzaniem od zera. To jest realna
oszczędność, ale mniejsza, niż zapowiadałem.

## Otwarte i rozstrzygające

1. **Czy tokenizer PLLuM tokenizuje NASZ korpus tak samo jak Gemma.** Różnica
   sumy pliku nie przesądza: 262147 może być słownikiem Gemmy plus kilka
   tokenów specjalnych, których w korpusie nie ma. Jeśli liczby tokenów wyjdą
   identyczne, wyrównanie ±0,2% przenosi się mimo innej sumy. Nie da się tego
   sprawdzić z laptopa (brak tokenizera Gemmy lokalnie) — zlecone DEP.
2. **Liczba tokenów dotrenowania.** Karta modelu jej nie podaje. Bez niej nie
   wiadomo, czy manipulacja jest wystarczająco silna, żeby cokolwiek odwrócić.
   Szukać w raporcie technicznym / u konsorcjum.
3. **Perplexity jako bramka manipulacji jest warunkowa** wobec punktu 1: przy
   różnej tokenizacji strata na token nie jest porównywalna między modelami
   i trzeba przejść na miarę na znak albo na słowo.
