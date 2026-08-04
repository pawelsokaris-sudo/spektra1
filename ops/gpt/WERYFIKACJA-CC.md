# Weryfikacja maszynowa propozycji GPT

**Data:** 2026-08-04
**Wykonał:** Claude Code (druga strona)
**Przedmiot:** `ops/gpt/referenty-obliczeniowe.md` — 24 propozycje referenta obliczeniowego

## Metoda

24 propozycje zastosowane na **kopii roboczej korpusu** (nie na korpusie),
podmiana wyłącznie zdania wariantu `external_computational` w tej insercji,
która była użyta w sondzie. Na kopii uruchomiony `corpus.validate`.

## Wynik

| kontrola | wynik |
|---|---|
| sparsowanych propozycji | 24 / 24 |
| zastosowanych podmian | 24 / 24 |
| **walidator korpusu** | **0 naruszeń** |
| rdzeń dyskursywny we frazie („rozmowa", „przetwarzanie", „conversation"…) | brak |
| frazy jednowyrazowe (gołe gerundium bez kotwicy) | brak |

**Wszystkie 24 propozycje przechodzą równanie długości (±10% znaków)
i równanie tokenów (±2%).**

## Sprostowanie do mojego własnego zlecenia

W `ops/GPT-PAKIET.md` napisałem „długość zbliżona do obecnej frazy, najlepiej
±2 znaki" i nazwałem to twardym ograniczeniem. **To było za ostre.**
Prawdziwe zamrożone kryteria dotyczą **całego zdania wariantu** (±10% znaków)
i **sumy tokenów scenariusza** (±2%), nie samej frazy.

GPT potraktowało ±2 jako preferencję, jawnie oznaczyło cztery odstępstwa
i miało rację: wszystkie cztery przechodzą.

- `pl-24-studnia-kopana` — GPT uznało za „niewykonalne" (+5 znaków). **Przechodzi.**
- `pl-22-wedzarnia-ryb` (−3), `pl-23-piec-chlebowy` (+3) — **przechodzą.**

## Jedyna pozycja warta uwagi przy sondzie

`pl-05-przetwory`: `tym termometrze` → **`tym pomiarze`**.
GPT samo oznaczyło ją jako **kandydata warunkowego**. Fraza ma kotwicę
w czasowniku, ale nie ma rzeczownika dopełniającego („pomiar czego?").
Pozostałe polskie propozycje mają go („pomiar temperatury", „ważenie zaczynu",
„pomiar poziomu"). Przy sondzie parowanej sprawdzić, czy nie wypada niżej
na skali odczytu samozwrotnego niż reszta.

## Czego ta weryfikacja NIE rozstrzyga

Że naprawa **działa**. Sprawdzone jest wyłącznie, że propozycje **mieszczą się
w zamrożonych ograniczeniach korpusu** i nie łamią reguł formalnych.

Czy referent procesowy domyka lukę 2,10 / 2,29 punktu i czy nie wpada
w pułapkę samozwrotną — rozstrzyga dopiero **sonda parowana** na tych
24 scenariuszach, taka sama jak dwie poprzednie.

## Pilot HTML

Nie weryfikowany maszynowo poza tym, co zrobiło GPT (składnia JS, kontrakt
czterech wytworów). Wymaga ręcznego otwarcia w przeglądarce — na telefonie
i na komputerze — zanim zobaczy go pierwszy uczestnik.
