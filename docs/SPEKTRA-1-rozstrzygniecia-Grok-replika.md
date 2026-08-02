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
