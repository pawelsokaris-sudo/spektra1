# ANEKS 1 do pieczęci spektra1-seal (2026-07-31, tego samego dnia co pieczęć)

## Ustalenie (zgłosił DEP po pieczęci, w raporcie 06bis)
Runda wyrównawcza korpusu (commit 9a68279) zmieniła teksty insercji we
WSZYSTKICH 16 scenariuszach pilota. Artefakty pomiarowe pilota w pakiecie
(metrics/spectra/discourse/dlag_sentence/t5_lambda_star) powstały więc na
WCZEŚNIEJSZEJ rewizji korpusu niż ta zaplombowana — uruchomienie runnera na
zaplombowanych plikach nie odtworzy ich bajt w bajt.

## Rozstrzygnięcie: przypięcie rewizji (bez ponownego pomiaru)
Artefakty pilota odpowiadają scenariuszom z rewizji **d88f5b6**
(= 9a68279~1, dostępna w historii TEGO SAMEGO zaplombowanego repo).
Odtworzenie: `git checkout d88f5b6 -- corpus/scenarios` + runner.
Pełna odtwarzalność zachowana — wymaga jednej komendy więcej.

## Dlaczego bez ponownego pomiaru
Wszystkie zamrożone decyzje oparte na pilocie (SD na ślepo do GATE 1, M=24,
walidacja D_discourse, phi do T5) zapadły na danych z rewizji d88f5b6 i takimi
pozostają. Pomiar główny NICZEGO z artefaktów pilota nie dziedziczy: okna,
komponent pozycyjny i progi lambda* dla scenariuszy głównych liczone są od
zera na korpusie zaplombowanym. Ponowny pomiar pilota (~8,5 h maszyny) nie
zmieniłby żadnej zamrożonej decyzji — byłby nowymi danymi, których nic nie
używa; dopuszczalny w przyszłości wyłącznie jako eksploracja z etykietą.

## Status pilota (doprecyzowanie)
Pilot = historyczne dane kalibracyjne, przypięte do rewizji d88f5b6, wyłączone
z analizy głównej (jak w protokole od zawsze). Wariant A pilota jest
identyczny w obu rewizjach; różnią się wyłącznie teksty insercji wariantów
B/C/C'-G/C'-U (192 z 208 tekstów).

## Zapis procesu
Wykryte przez DEP po pieczęci; zgłoszone zanim jakiekolwiek dane pomiaru
głównego zostały odczytane. Aneks jawny, zgodnie z regułą pieczęci.
