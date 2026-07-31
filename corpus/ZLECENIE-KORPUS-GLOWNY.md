# Zlecenie autorskie: KORPUS GŁÓWNY (M=24/język, zamrożone w GATE 1)

Obowiązuje w całości `corpus/AUTHORING-SPEC.md` (5 wariantów, czwórki insercji,
pytania zadaniowe w A, osadzenie referenta C′-G w bazie). Ten plik dodaje tylko
reguły kampanii głównej:

1. **Numeracja:** pl-09…pl-32 oraz en-09…en-32. Scenariusze pilotowe (01–08)
   są NIETYKALNE — nie edytować, nie kopiować z nich fraz.
2. **Tematy:** każdy autor dostaje w prompcie SWOJĄ listę 4 tematów — trzymać
   się jej (listy są rozłączne między autorami i rozłączne z pilotem).
   Zakaz tematów: komputery, AI, język, modele.
3. **Ślepota:** autor nie zna i nie próbuje poznać żadnych wyników pomiarów
   pilota. Pisze wyłącznie według spec.
4. **Długość insercji:** lekcja z pilota (zapisana w spec §4): frazy odniesienia
   w `external_grounded` budować z KRÓTKICH, CZĘSTYCH rzeczowników (nie
   przymiotników odczasownikowych typu „pokładowy" — tokenizer tnie je na
   3–5 kawałków). Cel: różnice sum tokenów C vs C′-G o mieszanych znakach.
5. **Weryfikacja przed oddaniem:** `python -m corpus.validate` musi być czyste
   dla WSZYSTKICH twoich plików (licznik heurystyczny — wynik wstępny; pomiar
   dokładny nastąpi na maszynie i może wymusić rundę poprawek).
6. Provenance: author wg promptu, date 2026-07-31, template opisujący strukturę.
