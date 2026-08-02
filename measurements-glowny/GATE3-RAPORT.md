# SPEKTRA-1 — GATE 3, odporność wyniku

Tolerancja precyzji: 0.005 na tekst. Maksymalna zmiana estymaty: 25%. Progi zamrożone w protokole §2 i §7, wpisane w kod przed biegami.

> **Ograniczenie zamierzone.** Progi λ\* z biegu glownego (progi NIE przeliczane - DEP-08). Kryterium **znaku** jest przez to mocne, kryterium **wielkości** przybliżone. Przeliczenie progów dla biegów kontrolnych kosztowałoby kolejny dzień maszyny i nie zmieniłoby odpowiedzi na pytanie, po co ta bramka istnieje: czy efekt jest realny.

## Kryterium (a) — precyzja: bf16 wobec fp32

| Replika | Scenariuszy | Δ₁ główny | Δ₁ kontrolny | Zmiana | Znak zgodny | Wynik |
|---|---:|---:|---:|---:|---|---|
| EN | 12 | -0.00561 | -0.00544 | 3.1% | tak | spełnione |
| PL | 12 | -0.00315 | -0.00326 | 3.5% | tak | spełnione |

**Tolerancja na pojedynczy tekst** (kontrola surowsza niż kryterium kontrastowe — sprawdza sam pomiar, nie różnicę między wariantami):

- tekstów porównanych: 48
- największa różnica: 0.000660 (próg 0.005)
- średnia różnica: 0.000212
- przekroczeń: **0**

## Kryterium (b) — z odejmowaniem komponentu pozycyjnego i bez

| Replika | Scenariuszy | Δ₁ główny | Δ₁ kontrolny | Zmiana | Znak zgodny | Wynik |
|---|---:|---:|---:|---:|---|---|
| EN | 24 | -0.00578 | -0.00532 | 7.9% | tak | spełnione |
| PL | 24 | -0.00363 | -0.00331 | 8.8% | tak | spełnione |

## Kryterium (c) — obie repliki językowe osobno

| Replika | Δ₁ |
|---|---:|
| EN | -0.00578 |
| PL | -0.00363 |

Znak zgodny: **tak**. Różnica wielkości: **37.2%** (próg 25%). Wynik: **niespełnione**.

## Werdykt

**NIESTABILNY**

Protokół §7 przewiduje ten wynik wprost: niepowodzenie bramki odporności **nie unieważnia** pomiaru, tylko klasyfikuje go jako niestabilny — i tak zostaje opublikowany. Który dokładnie warunek zawiódł, widać w tabelach wyżej; to jest informacja o granicach wyniku, nie o jego nieważności.
