# SPEKTRA-1 — Zapis rozstrzygnięć recenzji, runda 2 (do pakietu pieczęci)

**Recenzent:** GPT (rola: wrogi recenzent metodologiczny), 30.07.2026.
**Przedmiot recenzji:** skonstruowany korpus pilota (16 scenariuszy, 8 PL + 8 EN) oraz
hierarchia hipotez protokołu v1.2. Brief konsultacyjny: `SPEKTRA-1-konsultacja-GPT-korpus.md`.
**Werdykt recenzji:** WARIANT — cztery zmiany wymagane łącznie przed pieczęcią.
**Rozstrzygający:** Paweł (decyzja: przyjąć cały pakiet) + Claude (weryfikacja i implementacja).
**Konwencja:** Multi-Model Pre-Review Protocol v2.2 (ActProof).

> **Kluczowa okoliczność, istotna dla oceny uczciwości procesu:** wszystkie zmiany
> zapadły **przed pieczęcią** i **przed odczytaniem jakichkolwiek aktywacji modelu**.
> Podstawą były wyłącznie właściwości materiału tekstowego. Środowisko pomiarowe
> w chwili rozstrzygnięcia nie było jeszcze postawione, więc żadna wartość endpointu
> nie istniała nawet potencjalnie.

---

## Kwestia 1 — wariant mechaniczny bez zdań pytających (replika EN)

| | |
|---|---|
| **Zarzut** | W replice EN wariant A ma średnio 0,00 zdań pytających wobec 5,50 w B/C oraz 1,7× więcej przecinków. Jest to niemal doskonały klasyfikator warunku eksperymentalnego, a nie różnica stylistyczna. Protokół §3 wymaga dopasowania rozkładu zdań pytających. |
| **Status** | **PRZYJĘTY** |
| **Weryfikacja własna** | Potwierdzone w wygenerowanym raporcie dopasowania. Replika PL: 3,25 zdania pytającego w **każdym** wariancie (dopasowanie idealne). Replika EN: A = 0,00, B/C = 5,50. Obydwa niezależne zespoły autorskie EN popełniły ten sam błąd, obydwa PL — nie. Dopasowanie jest zatem osiągalne, ale nie wynika samo z instrukcji autorskiej. |
| **Rozstrzygnięcie** | Wariant A w replice EN przepisany: pytania **zadaniowe zamknięte** (jednoznaczna odpowiedź, brak negocjowania celu, brak refleksji nad metodą, brak otwartych alternatyw, brak odniesień do rozmówcy) w liczbie zbliżonej do wariantów dialogowych; redukcja gęstości wyliczeń i przecinków. Samo dopisanie znaków zapytania do istniejącego tekstu uznane za niewystarczające. Wymóg wpisany do §3 protokołu i do specyfikacji autorskiej. |
| **Odrzucona linia obrony** | Teza, że asymetria PL/EN jest „naturalnym testem wrażliwości". Repliki miały mierzyć ten sam konstrukt; obecnie mierzyłyby operacyjnie różne kontrasty. Nazwanie naruszenia dopasowania testem wrażliwości post hoc jest niedopuszczalne. |

## Kwestia 2 — asymetria osadzenia referencyjnego w C′

| | |
|---|---|
| **Zarzut** | Zdanie samozwrotne ma desygnat dostępny (trwająca rozmowa), a zdanie zewnętrzne odnosi się do obiektu niewprowadzonego do dialogu. Kontrast C−C′ miesza więc samozwrotność z samą dostępnością referenta. |
| **Status** | **PRZYJĘTY** |
| **Weryfikacja własna** | Skan wszystkich 16 scenariuszy: desygnaty insercji zewnętrznych występują w bazie niemal wyłącznie jako słowa funkcyjne. Realnie osadzonych referentów garść (`scaffold`, `oprawę`, `szafy`, `flotę`). W przeważającej większości układ zewnętrzny pojawiał się znikąd. |
| **Rozstrzygnięcie** | Wariant C′ rozdzielony na **C′-G** (external grounded — referent wprowadzony wcześniej w tym samym dialogu) i **C′-U** (external ungrounded — obecna postać). Kontrast główny = C − C′-G; kontrast diagnostyczny = C′-G − C′-U; kontrast C − C′-U zdegradowany do opisowego. Dopasowanie C′-G obejmuje: odległość od ostatniego wspomnienia referenta, liczbę wcześniejszych wspomnień, rolę składniową, znaczenie dla rozwiązywanego problemu, ciągłość tematyczną. |
| **Granica utrzymana świadomie** | Samozwrotność i dostępność desygnatu **nie są w pełni ortogonalizowalne** — odniesienie do trwającej rozmowy z definicji korzysta z obiektu obecnego w sytuacji komunikacyjnej. Konsekwencja wpisana do §0: najmocniejsze dopuszczalne roszczenie to *sygnatura kontekstowo osadzonego odniesienia samozwrotnego względem kontekstowo osadzonego odniesienia zewnętrznego*, nigdy „czysta sygnatura samozwrotności". |

## Kwestia 3 — wariant B bez insercji kontrolnych (znaleziona przez recenzenta)

| | |
|---|---|
| **Zarzut** | B pozostaje samą bazą, podczas gdy C i C′ otrzymują insercje. Każda różnica C−B może więc pochodzić z samego faktu dodania zdań: dodatkowych przejść semantycznych, zmiany lokalnej koherencji, zmiany rozkładu informacji po pozycjach. Dopasowanie końcowej liczby tokenów tego nie naprawia. |
| **Status** | **PRZYJĘTY** — uznane wprost jako błąd konstrukcyjny po stronie autorów kodu (`corpus/build.py`, wariant B budowany jako goła baza). |
| **Weryfikacja własna** | Potwierdzone w kodzie: `"A": base_a, "B": base_b, "C": _apply_insertions(...)`. B faktycznie nie otrzymywał żadnych insercji. |
| **Rozstrzygnięcie** | B otrzymuje **insercje neutralne** w identycznych pozycjach, o tej samej długości i typie składniowym, z referentem osadzonym w kontekście, bez samozwrotności i bez opisywania układu podobnego do modelu. Wpisane do §3 protokołu, wymuszone w kodzie (`INSERTION_KEY`) i sprawdzane przez walidator (niekompletny zestaw insercji = błąd twardy). |

## Kwestia 4 — odwrócona hierarchia hipotez

| | |
|---|---|
| **Zarzut** | Protokół v1.2 ustanawiał bramkę: H2 (C−C′) testowana wyłącznie po przejściu H1 (C−A). Kontrast mniej specyficzny bramkował bardziej specyficzny. Możliwy jest wynik C−C′ > 0 przy C−A ≈ 0 (np. przy odmiennej wariancji A), w którym obecna reguła **zabroniłaby** przetestowania najlepiej kontrolowanego kontrastu. |
| **Status** | **PRZYJĘTY** |
| **Rozstrzygnięcie** | Nowa hierarchia: **H1 = C − C′-G (główna)** → H2 = C′-G − C′-U (diagnostyczna) → H3 = C − B (wtórna) → {H4 TOST B−A, H5 D_lag, kontrast opisowy C−A, profil warstwowy}. Symulacja mocy w GATE 1 celuje w kontrast główny C−C′-G, nie w C−A. C′-U wchodzi jako pojedynczy krok diagnostyczny, nie jako współgłówny endpoint — inaczej płaska korekta wielokrotności obniżyłaby moc testu głównego. |
| **Warunek uczciwości (spełniony)** | Do §0 protokołu wpisane jawne oświadczenie: hierarchia zmieniona przed pieczęcią, po audycie konstrukcji korpusu, przed jakimkolwiek pomiarem aktywacji; nowa hierarchia **nie jest** przedstawiana jako plan istniejący od początku. |

---

## Bilans

Cztery kwestie, cztery przyjęte, zero odrzuconych. Dwie (kwestia 3 i 4) uznane wprost
jako błędy autorów v1.2: pierwsza konstrukcyjna w kodzie, druga projektowa w hierarchii.
Jedna granica utrzymana świadomie (nieusuwalna resztkowa nierozłączność samozwrotności
i indeksykalnej dostępności desygnatu) — z konsekwencją wpisaną w osłabione brzmienie
roszczenia, nie obchodzoną.

**Koszt przyjęcia:** pięć wariantów zamiast czterech (+25% pomiaru), edycja baz
scenariuszy w celu wprowadzenia referentów osadzonych, przepisanie wariantu A w replice
EN, przebudowa §0/§1/§3/§6/§7 protokołu oraz kodu budującego, walidatora i raportu.

**Wniosek:** warunki werdyktu „WARIANT" spełnione w v1.3. Dokument dołączany do pakietu
pieczęci jako dowód drugiej rundy pre-review.
