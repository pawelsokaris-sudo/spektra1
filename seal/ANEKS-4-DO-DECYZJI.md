# ANEKS 4 (PROJEKT — czeka na decyzję kierownika badania)

**Data znaleziska:** 2026-08-01
**Stan zaślepienia w chwili znaleziska:** żadna liczba konfirmacyjna nie została
odczytana. Progi λ\* dla korpusu głównego jeszcze nie istnieją, więc endpoint
główny jest w tej chwili policzalny tylko jako tożsamościowe zero. Szuflada
zamknięta.

## Znalezisko

Test równoważności zamrożony w [ANEKS-2](ANEKS-2.md) — margines |d_z| < 0.3,
α = 0.05 na stronę, permutacja parowana, per replika językowa — **jest przy
M = 24 nieosiągalny**. Nie „ma małą moc": nie przechodzi **nawet dla różnicy
dokładnie zerowej**.

Sprawdzone dwiema drogami, zgodnymi co do wyniku:

*Analitycznie.* Odrzucenie strony wymaga (margines − |d_z|) · √n ≥ t₀.₀₅,ₙ₋₁.
Przy n = 24 daje to (0.3 − |d_z|) ≥ 1.714/√24 = **0.350**. Lewa strona nie
przekracza 0.3 dla żadnych danych.

*Permutacyjnie* (kod, który realnie policzy GATE 2, na różnicy o d_z = 0):

| n par | p_TOST przy efekcie zerowym | równoważność |
|---:|---:|---|
| 13 | 0.154 | NIE |
| **24** | **0.078** | **NIE** |
| 32 | 0.050 | tak (granicznie) |
| 48 | 0.023 | tak |
| 64 | 0.010 | tak |

Najmniejszy margines osiągalny przy n = 24: **≈ 0.4** (0.3 → p = 0.079;
0.4 → p = 0.032).

## Co to psuje

1. **Werdykt „efekt praktycznie wykluczony" nie istnieje** w przestrzeni
   możliwych wyników SPEKTRA-1. §0 protokołu go przewiduje — bezpodstawnie.
   Każde nieistotne H1 da „niekonkluzywny", niezależnie od danych.
2. **H4 staje się niepotwierdzalna.** Protokół mówi wprost: *„Brak istotności
   NIE potwierdza H4 — potwierdza ją wyłącznie zaliczony TOST"*. Kontrola
   „insercja neutralna nie rusza modu głównego" nie może więc wypaść pozytywnie.

Powód źródłowy jest ten sam co przy bramce GATE 0 w lipcu: **kryterium zostało
zamrożone bez sprawdzenia, czy uruchamiana konstrukcja potrafi je w ogóle
spełnić.** Ta sama lekcja, trzeci raz w tym badaniu.

## Opcje (do rozstrzygnięcia przez kierownika badania)

**(A) Przyjąć nieosiągalność, nie ruszać marginesu.** Zbiór werdyktów
SPEKTRA-1 zawęża się do {potwierdzony, niekonkluzywny}; raport podaje jawnie,
że przy M = 24 równoważności nie dało się wykazać, i notuje minimalny osiągalny
margines (≈0.4) jako informację kalibracyjną dla SPEKTRA-2.
*Za:* zero ruchu przy zamrożonym parametrze po zebraniu danych — najmocniejsza
pozycja obronna. *Przeciw:* H4 zostaje bez możliwości potwierdzenia, a §0
obiecuje werdykt, którego nie dostarczy.

**(B) Poszerzyć margines do |d_z| < 0.5.** Bezpiecznie osiągalny przy n = 24
(0.4 jest na granicy), wciąż daleko poniżej SESOI d_z = 0.8.
*Za:* odzyskuje oba utracone werdykty; decyzja zapada przed odślepieniem.
*Przeciw:* zmiana zamrożonego parametru po zebraniu danych wygląda jak
dobieranie progu — nawet gdy nim nie jest, recenzent ma prawo tak to czytać.

**(C) Podnieść α_TOST do 0.10 na stronę.** Formalnie ratuje margines 0.3
(0.078 < 0.10), ale wyłącznie dla efektów praktycznie zerowych — moc pozostaje
znikoma. *Ocena: pozorne rozwiązanie, odradzam.*

## Rekomendacja

**(A).** Prerejestracja jest warta tyle, ile kosztuje jej dotrzymanie w chwili,
gdy zaczyna uwierać. Uczciwe „przy M = 24 nie moglibyśmy wykluczyć efektu"
jest wynikiem informacyjnym — kalibruje SPEKTRA-2 (n ≥ 64 dla wygodnego
marginesu 0.3) i nic nie udaje. Opcja (B) kupuje dwa werdykty za jedyny
kapitał, jaki to badanie realnie ma.

Zastrzeżenie własne: (B) **nie jest** nieuczciwa — decyzja zapada przed
odczytaniem czegokolwiek i byłaby jawnie zapisana. Uważam ją za gorszą, nie
za niedopuszczalną. Wybór należy do kierownika badania.

## Stan wdrożenia

Niezależnie od decyzji, kod GATE 2 raportuje `min_attainable_margin_dz` przy
każdym teście równoważności — żeby nieosiągalny margines nigdy więcej nie
przeszedł niezauważony. Znalezisko jest zabezpieczone testem regresyjnym
`tests/test_gate2.py::test_margines_0_3_jest_NIEOSIAGALNY_przy_M24`.

**Decyzja kierownika badania:** _(do uzupełnienia)_
**Data decyzji:** _(do uzupełnienia)_
