# SPEKTRA-1 — konsultacja: metryka porządku D_lag po pilocie (runda 3)

**Do wklejenia w całości; dokument samowystarczalny.** Konwencja: Multi-Model
Pre-Review Protocol v2.2, rola: wrogi recenzent metodologiczny. Poprzednie dwie
rundy (32 zarzuty do v1.0; 4 kwestie korpusowe → v1.3) zostały przyjęte w całości.

## Kontekst w czterech zdaniach

SPEKTRA-1 mierzy widma macierzy korelacji aktywacji warstw Gemmy 3 4B na pięciu
wariantach scenariuszy (A mechaniczny / B + insercja neutralna / C samozwrotny /
C′-G zewnętrzny osadzony / C′-U zewnętrzny nieosadzony); test główny to C − C′-G
na indeksie widmowym Ī. **Metryka porządku D_lag** istnieje, bo pierwsza recenzja
zarzuciła protokołowi, że cała statystyka jest niezmiennicza na permutacje
tokenów, a język teorii dotyczy dynamiki. D_lag = z-score największej wartości
osobliwej macierzy korelacji z opóźnieniem C(1) = Z₊₁ᵀZ/T′ względem rozkładu
z **permutacji pojedynczych wierszy (tokenów)** Z, 500 permutacji. Sanity
prerejestrowane dla nulla interwencyjnego N1 (tekst z przetasowanymi zdaniami,
ponownie przepuszczony przez model): „D_lag spada do nullu".

**Pomiar pilota właśnie się zakończył** (16 scenariuszy × 5 wariantów × 2 języki
+ nulle N1/N2 = 208 tekstów, 34 warstwy). Pieczęci jeszcze nie ma. Endpoint
główny (I_total) nie ma jeszcze progów, więc żadna wartość konfirmacyjna nie
została obejrzana — obejrzano wyłącznie prerejestrowane sanity D_lag/N1.

## Wynik, który wymusza tę konsultację

Średni D_lag w paśmie konfirmacyjnym (bloki 13–26), pilot:

| Tekst | D_lag |
|---|---|
| warianty dialogowe (B, C, C′-G, C′-U) | 42,5–42,8 |
| wariant mechaniczny A | 58,7 |
| **null N1 (przetasowane zdania)** | **43,1 — brak jakiegokolwiek spadku** |

**Sanity N1 nie wyszło.** Diagnoza mechanizmu: null D_lag tasuje pojedyncze
tokeny, więc sygnał zdominowany jest lokalną ciągłością wewnątrz zdania
(składnia), której N1 nie narusza — N1 tasuje całe zdania. Obecny D_lag mierzy
porządek **gramatyczny**, jest ślepy na porządek **dyskursu**, a to ten drugi
miał domykać „lukę porządku" z pierwszej recenzji.

## Opcje (decyzja przed pieczęcią)

- **W1.** Przedefiniować null D_lag: permutacja **bloków zdań** (wiersze Z
  pogrupowane po zdaniach; kolejność wewnątrz zdania nietknięta) zamiast
  permutacji tokenów. Metryka mierzy wtedy dokładnie to, co N1 niszczy.
- **W2.** Zostawić D_lag jako kontrolę porządku lokalnego i usunąć kryterium
  N1 w obecnym brzmieniu. Uczciwe, ale protokół znów zostaje bez narzędzia
  wrażliwego na dynamikę dyskursu.
- **W3.** Dwie prerejestrowane metryki: D_lag-token (null tokenowy, porządek
  lokalny) i D_lag-zdaniowy (null blokowy, porządek dyskursu), każda z własnym
  sanity (token: brak spadku na N1 to własność, nie porażka; zdaniowy: spadek
  do nullu na N1).

**Fakt operacyjny:** tej nocy liczymy D_lag z nullem zdaniowym dla całego pilota
niezależnie od werdyktu (nadzbiór danych obsługuje każdą opcję; maszyna
pomiarowa jest akurat wolna). Decyzja dotyczy tego, co wchodzi do §5 protokołu
jako konfirmacyjne, nie tego, co mierzymy.

## Pytania

1. Który wariant? Jeśli W3 — czy obie metryki mogą wejść do hierarchii, czy
   zdaniowa jako H5, a tokenowa wyłącznie opisowo (nasza preferencja)?
2. Czy null z bloków zdań jest właściwym odpowiednikiem N1? Czy widzisz
   subtelność, przez którą permutacja bloków w Z (na aktywacjach ORYGINALNEGO
   tekstu) nie jest równoważna N1 (nowy forward przetasowanego tekstu)?
   To dwie różne operacje: pierwsza tasuje wiersze policzonych aktywacji,
   druga daje modelowi inny tekst. Sanity porównuje D_lag(tekst N1) z jego
   własnym nullem blokowym — czy to poprawna konstrukcja?
3. Obserwacja opisowa: wariant A ma D_lag-token 58,7 wobec 42,5 w dialogowych.
   H5 (D_lag różnicuje C od A) przejdzie trywialnie z powodu stylu wyliczeniowego
   A, nie dynamiki rozmowy. Czy H5 w obecnym brzmieniu ma jakąkolwiek wartość
   konfirmacyjną, czy zdegradować ją do opisu?
4. Czy zmiana definicji D_lag po obejrzeniu WYŁĄCZNIE prerejestrowanego sanity
   (nie endpointu) jest czystą korektą przedpieczęciową, czy widzisz ryzyko,
   które powinniśmy jawnie opisać?

Format odpowiedzi: werdykt per pytanie + jedno zdanie, co się stanie, jeśli
zignorujemy problem i zapieczętujemy jak jest.
