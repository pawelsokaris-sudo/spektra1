# DEP — Uzupełnienie do zlecenia 07 (nic nie zmienia w krokach 1–3)

Trzy rzeczy, których w zleceniu 07 zabrakło. **Kroki 1–3 zostają bez zmian** —
jeśli już je wykonałeś, po prostu dopisz to niżej.

## 1. Gdzie mają trafić pliki

Na laptopa kierownika badania, do katalogu **`measurements-glowny\`** wewnątrz
katalogu repozytorium (dokładna ścieżka przekazana przy zleceniu — dokumenty
operacyjne nie zawierają nazw kont, żeby anonimizacja nie psuła instrukcji;
patrz ANEKS-3).

Nazwy plików **bez zmian** (`spectra-en.parquet`, `spectra-pl.parquet`,
`t5_lambda_star.parquet`, `t5_phi.json`). Analiza szuka ich dokładnie tam
i dokładnie pod tymi nazwami; skleja oba pliki widm sama i sprawdza, czy
liczba plików zgadza się z liczbą replik językowych.

Po skopiowaniu podaj sumy SHA-256 — porównam je po stronie laptopa przed
uruchomieniem czegokolwiek. Niezgodność choćby jednej = transfer do powtórki,
nie do naprawiania.

## 2. Czego NIE liczyć na maszynie

**Nie licz metryk z prawdziwym λ\*, nie licz żadnych kontrastów między
wariantami.** To nie jest kwestia zaufania, tylko higieny: endpoint główny ma
zostać nieotwarty do momentu uruchomienia zamrożonej analizy, a każde wcześniejsze
spojrzenie na te liczby psuje zapis „nikt nie widział wyniku przed testem".
Twoje zadanie kończy się na przeliczeniu progów i przesłaniu plików.

Jeśli w trakcie kontroli kompletności coś wypisze wartości metryk — to normalne,
nie musisz nic robić, po prostu nie licz z nich różnic.

## 3. Powtórzenie GATE 0 na maszynie (wymóg zamrożony w ANEKS-2)

Aneks 2 wymaga powtórzenia bramki sanity na maszynie pomiarowej **po pomiarze**.
Sens: sprawdzić, że środowisko numeryczne maszyny odtwarza tę samą matematykę,
na której stoi cały wynik. Do zrobienia **po transferze**, nie przed.

```
..\spektra1-env\Scripts\python.exe -m gates.gate0
```

- **Wyłącznie procesor** — karta wolna, nikt nie musi czekać.
- Czas odniesienia: **816 s** na laptopie kierownika badania. Na maszynie
  pomiarowej powinno być szybciej; jeśli będzie kilkukrotnie wolniej, zgłoś,
  bo to sygnał, że coś zjada procesor w tle.
- Można przerwać i uruchomić ponownie — bramka liczy się od zera, nic nie psuje.

**Do raportu:** werdykt każdego z trzech kryteriów (A: zgodność z rozkładem
Marczenki–Pastura, B: kalibracja λ\*, C: replikacja bitowa), czas wykonania
oraz `gates/gate0_report.md` wygenerowany na maszynie. Odniesienie z laptopa:
werdykt PASS, KS = 0.0014, fałszywe mody 2.10% przy progu rangowym 26/1000.

Jeśli kryterium C wyjdzie „tolerancyjna" zamiast „bitowa" — **to nie jest
awaria**, tylko informacja o różnicy sprzętowej. Podaj maksymalną różnicę
i idziemy dalej.
