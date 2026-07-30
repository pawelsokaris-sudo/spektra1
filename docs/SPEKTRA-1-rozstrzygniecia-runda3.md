# SPEKTRA-1 — Zapis rozstrzygnięć recenzji, runda 3: metryka porządku (do pakietu pieczęci)

**Recenzent:** GPT (wrogi recenzent metodologiczny), 30.07.2026 (noc).
**Przedmiot:** metryka porządku po niepowodzeniu prerejestrowanego sanity N1 w pilocie.
**Werdykt recenzji:** WARIANT — W3 zmodyfikowany. **Decyzja:** przyjęty w całości.

## Zapis wymagany przez recenzenta (7 punktów)

1. **Pierwotna definicja:** D_lag = z-score σ₁ tokenowej macierzy C(1)=Z₊₁ᵀZ/T′
   wobec nulla z permutacji pojedynczych tokenów (500 permutacji).
2. **Przewidywanie:** na nullu interwencyjnym N1 (tekst z przetasowanymi zdaniami,
   nowy forward) D_lag miał spaść do nullu.
3. **Wynik:** brak spadku — N1: 43,1 wobec 42,5–42,8 na wariantach dialogowych.
4. **Diagnoza:** sygnał zdominowany zależnością wewnątrzzdaniową; przy T≈1000 i
   J≈40–60 zdań permutacja zdań zmienia tylko (J−1)/(T−1) ≈ 4–6% przejść
   tokenowych. Z tego samego rachunku recenzent odrzucił także W1 (null z bloków
   zdań w tokenowej C(1)) — >94% przejść pozostaje identycznych.
5. **Nowa definicja:** patrz niżej, DEFINICJA ZAMROŻONA.
6. **Data decyzji:** 2026-07-30, noc.
7. **Potwierdzenie:** decyzja i zamrożenie definicji nastąpiły PRZED obejrzeniem
   jakiejkolwiek wartości nowej metryki. Przyjęto najostrzejszą regułę recenzenta:
   **definicja nie będzie zmieniana niezależnie od wyniku jej pierwszego
   przeliczenia**; jeśli sanity nie przejdzie, oś porządku otrzymuje werdykt
   „niekonkluzywny" i tak jest publikowana. Pilot służył do wykrycia wady starej
   metryki, nie do strojenia nowej.

## DEFINICJA ZAMROŻONA: D_discourse (2026-07-30, przed pierwszym przeliczeniem)

- **Reprezentacja zdania:** s_j = średnia po tokenach zdania j z macierzy Z
  (po maskowaniu, wspólnym oknie, odjęciu komponentu pozycyjnego i z-score per
  kanał — preprocessing identyczny z resztą pomiaru). Tokeny szablonu (poza
  zdaniami) wyłączone. Zdania ucięte oknem: wchodzą tokeny, które przetrwały.
- **Statystyka:** σ₁ macierzy C_sent(1) = Σⱼ s_{j+1} s_jᵀ / (J−1).
- **Null wewnętrzny (pomocniczy, nazwany za recenzentem "adjacency null"):**
  permutacja kolejności reprezentacji s_j (500 permutacji, bez punktów stałych);
  zachowuje liczbę i reprezentacje zdań. Jest to null WARUNKOWY na już policzonych
  stanach — NIE odpowiednik N1.
- **Raportowanie (dotyczy też D_local):** surowe σ₁, średnia i SD nulla,
  empiryczny percentyl/p (rozdzielczość 1/501), z-score wyłącznie opisowo.
  Zakaz interpretowania z jak kwantyla rozkładu normalnego.
- **Główny test walidacyjny porządku (zastępuje sanity N1 starej metryki):**
  parowany kontrast surowego σ₁_disc: oryginał − N1 (N1 = nowy forward tekstu
  z przetasowanymi zdaniami; N1 zachowuje liczbę i długości zdań, więc σ₁ jest
  parowalne). Jednostka inferencji = scenariusz; permutacja parowana, α=0.01,
  jednostronnie (oryginał > N1). Wymóg: efekt dodatni łącznie w wariantach
  dialogowych B, C, C′-G, C′-U; wariant A poza wymogiem (brak realnej osi
  dyskursu w tekście zadaniowym). Kilka N1 na tekst = powtórzenia zagnieżdżone
  w scenariuszu (uśredniane), nigdy niezależne teksty.

## Pozostałe rozstrzygnięcia rundy

| Kwestia | Decyzja |
|---|---|
| Dwie metryki w hierarchii | NIE — D_discourse jest prerejestrowanym testem walidacyjnym osi porządku; **D_lag-token przemianowany na D_local i zdegradowany do opisu** (mierzy porządek lokalny/składniowy — nie jest błędny, błędne było przypisanie mu znaczenia dyskursowego). Obu nie wolno wprowadzać jako równorzędnych endpointów (wielokrotność + pokusa wyboru po wyniku). |
| H5 (D_lag C−A) | **Usunięta z konfirmacji, zdegradowana do opisu.** Pilot pokazuje D_local A=58,7 vs dialogowe 42,5 — kontrast mierzy styl wyliczeniowy, nie dynamikę rozmowy. |
| Hipoteza o samozwrotności dynamicznej | Interakcja [σ₁(C)−σ₁(N1_C)] − [σ₁(C′-G)−σ₁(N1_{C′-G})] zapisana jako **prerejestrowana analiza wtórna opisowa** (poza hierarchią konfirmacyjną; oczekiwany efekt mały — bez roszczeń bez osobnej symulacji mocy). |
| Null blokowy na aktywacjach (nocny bieg W1) | Dane zachowane i raportowane jako **pomocniczy adjacency null na poziomie tokenów** — jawnie nazwany, bez statusu interwencyjnego nulla dyskursu. |
| Duże z-score'y (42–59) | Uznane za artefakt wąskiego nulla permutacyjnego, nie za wagę naukową — stąd obowiązek raportowania wartości surowych i empirycznych percentyli. |

**Bilans:** wszystkie punkty werdyktu przyjęte; zabezpieczenie przed „pilotem jako
zbiorem treningowym metryki" = zamrożenie definicji przed pierwszym przeliczeniem
+ reguła niezmienności niezależnie od wyniku.
