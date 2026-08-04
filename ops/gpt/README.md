# Katalog roboczy GPT

**Ten katalog należy do agenta GPT. Wszystko, co GPT tworzy, ląduje tutaj.**

Powód: nad repozytorium pracują równolegle dwa agenty. Bez rozdzielenia
katalogów jeden nadpisuje pracę drugiego — zdarzyło się to już w tej sesji
między podagentami, w katalogu roboczym, gdzie stawka była znacznie niższa.

## Zasady dla GPT

**Wolno pisać wyłącznie tutaj:** `ops/gpt/`

**NIE WOLNO dotykać:**

| katalog | dlaczego |
|---|---|
| `corpus/` | bodziec badania; każda zmiana wymaga walidatora i przeliczenia równania tokenów |
| `gates/` | kod i dane bramek, w tym oceny paneli |
| `docs/` | ustalenia projektowe; zmiana bez uzgodnienia rozjeżdża stan |
| `seal/` | pieczęć SPEKTRY-1 i aneksy — materiał zapieczętowany |
| `measurements-glowny/` | dane pomiarowe |

**Nie commitować.** Zostaw zmiany w drzewie roboczym — druga strona przegląda
diff przed włączeniem czegokolwiek do repo.

**Nie zmieniać gałęzi, nie robić push, nie tworzyć tagów.**

## Dlaczego propozycje trafiają tu, a nie od razu do korpusu

Zadanie 2 (frazy referenta obliczeniowego) ma sześć twardych warunków, z czego
trzy da się sprawdzić **wyłącznie maszynowo**: równanie długości ±10% znaków,
równanie tokenów ±2% i reguła określnika. Propozycja przechodzi przez walidator
zanim dotknie `corpus/`.

Trzy razy w tym projekcie kryterium wyglądające na spełnione okazywało się
niespełnione dopiero po przeliczeniu.

## Oczekiwane wytwory

```
ops/gpt/pilot-pl.html          zadanie 1 — prototyp polski
ops/gpt/pilot-en.html          zadanie 1 — prototyp angielski
ops/gpt/referenty-obliczeniowe.md   zadanie 2 — 24 propozycje + lista niewykonalnych
ops/gpt/RAPORT.md              co zrobione, co się nie udało, zastrzeżenia
```

Instrukcja zadań: `ops/GPT-PAKIET.md`
Materiał: `ops/GPT-zadanie-1-material.md`, `ops/GPT-zadanie-2-material.md`
