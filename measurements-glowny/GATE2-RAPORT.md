# SPEKTRA-1 — GATE 2, analiza konfirmacyjna

α = 0.01, permutacji = 10000, CI = 99%, pasmo warstw: 14–27.

Repliki językowe są **osobnymi prerejestrowanymi badaniami** — bez łączenia w pulę, z osobnym α. Porównanie między nimi jest wyłącznie opisowe.

> **Zakres werdyktów (ANEKS-4, decyzja z 2026-08-01).** Zbiór możliwych werdyktów SPEKTRA-1 to {efekt wykryty, wynik niekonkluzywny}. Werdykt „efekt praktycznie wykluczony” jest przy M = 24 nieosiągalny i został z badania wycofany jawnym aneksem — nie po zobaczeniu wyników.

## Replika EN

| Krok | Kontrast | Status | Średnia różnica | d_z | CI | p | Werdykt |
|---|---|---|---:|---:|---|---:|---|
| H1 | C-CprimG | **konfirmacyjny** | -0.00578 | -2.650 | [-0.00690; -0.00473] (99%) | 1.00000 | niekonkluzywny |
| H2 | CprimG-CprimU | opisowy | +0.00403 | +1.798 | [+0.00293; +0.00519] (99%) | 0.00010 | OPISOWY (poza hierarchia - lancuch zatrzymany wyzej) |
| H3 | C-B | opisowy | -0.00424 | -2.547 | [-0.00509; -0.00340] (99%) | 1.00000 | OPISOWY (poza hierarchia - lancuch zatrzymany wyzej) |
| C-A | C-A | opisowy | -0.05639 | -6.260 | [-0.06097; -0.05171] (99%) | 1.00000 | — |
| B-A | B-A | opisowy | -0.05215 | -5.818 | [-0.05658; -0.04753] (99%) | 1.00000 | — |

**Hierarchia zatrzymała się na H1.** Wszystko poniżej jest opisowe — protokół zabrania traktowania tych liczb jako konfirmacyjnych, niezależnie od tego, jak wyglądają.

> **Zastrzeżenie obowiązkowe do kroku H1.** Przy M = 24 margines równoważności |d_z| < 0.3 jest NIEOSIĄGALNY (najmniejszy osiągalny: 0.35). Nie odróżnilibyśmy braku efektu od zbyt małej czułości badania. NIE wolno raportować tego jako „efektu nie ma” ani „nie wykazano równoważności”. Patrz ANEKS-4.

### H4 — kontrola równoważności (B − A na udziale modu głównego)

Zmierzona różnica: **-0.00418**, d_z = -1.336, CI [-0.00583; -0.00260] (99%).
Równoważności **nie da się orzec** przy tej liczności — margines |d_z| < 0.3 jest nieosiągalny (najmniejszy osiągalny: 0.35). Patrz ANEKS-4. To NIE znaczy, że efekt jest.

### Profil warstwowy (permutacja klastrowa po ciągłej osi warstw)

Masa klastra: 0.000, p = 1.0000, scenariuszy: 24. Status: opisowy.

## Replika PL

| Krok | Kontrast | Status | Średnia różnica | d_z | CI | p | Werdykt |
|---|---|---|---:|---:|---|---:|---|
| H1 | C-CprimG | **konfirmacyjny** | -0.00363 | -1.494 | [-0.00490; -0.00245] (99%) | 1.00000 | niekonkluzywny |
| H2 | CprimG-CprimU | opisowy | +0.00049 | +0.229 | [-0.00062; +0.00163] (99%) | 0.13789 | OPISOWY (poza hierarchia - lancuch zatrzymany wyzej) |
| H3 | C-B | opisowy | -0.00239 | -1.002 | [-0.00370; -0.00122] (99%) | 1.00000 | OPISOWY (poza hierarchia - lancuch zatrzymany wyzej) |
| C-A | C-A | opisowy | -0.04553 | -3.416 | [-0.05247; -0.03900] (99%) | 1.00000 | — |
| B-A | B-A | opisowy | -0.04313 | -2.969 | [-0.05053; -0.03559] (99%) | 1.00000 | — |

**Hierarchia zatrzymała się na H1.** Wszystko poniżej jest opisowe — protokół zabrania traktowania tych liczb jako konfirmacyjnych, niezależnie od tego, jak wyglądają.

> **Zastrzeżenie obowiązkowe do kroku H1.** Przy M = 24 margines równoważności |d_z| < 0.3 jest NIEOSIĄGALNY (najmniejszy osiągalny: 0.35). Nie odróżnilibyśmy braku efektu od zbyt małej czułości badania. NIE wolno raportować tego jako „efektu nie ma” ani „nie wykazano równoważności”. Patrz ANEKS-4.

### H4 — kontrola równoważności (B − A na udziale modu głównego)

Zmierzona różnica: **-0.00711**, d_z = -2.404, CI [-0.00864; -0.00558] (99%).
Równoważności **nie da się orzec** przy tej liczności — margines |d_z| < 0.3 jest nieosiągalny (najmniejszy osiągalny: 0.35). Patrz ANEKS-4. To NIE znaczy, że efekt jest.

### Profil warstwowy (permutacja klastrowa po ciągłej osi warstw)

Masa klastra: 0.000, p = 1.0000, scenariuszy: 24. Status: opisowy.

## Podsumowanie

- **EN:** H1 (C − C′-G) — wynik niekonkluzywny, p = 1.00000, d_z = -2.650.
- **PL:** H1 (C − C′-G) — wynik niekonkluzywny, p = 1.00000, d_z = -1.494.

Zgodność między replikami jest wymogiem odporności (GATE 3c): znak efektu musi być ten sam, a estymaty nie mogą się różnić o więcej niż 25%. Rozbieżność nie unieważnia wyniku — klasyfikuje go jako niestabilny i tak zostaje opublikowany.
