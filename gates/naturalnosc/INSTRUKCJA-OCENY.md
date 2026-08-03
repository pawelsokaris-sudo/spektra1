# Instrukcja oceny — bramka naturalności

Oceniasz **pojedyncze zdanie** wstawione w rozmowę. Dostajesz kontekst
(kilka wcześniejszych zdań) i to jedno zdanie. Kontekstu **nie oceniasz** —
on jest tłem.

Nie wiesz, które zdania są nienaruszone, a które celowo popsute. Część
zestawu jest jedna, część druga. **Nie zgaduj klasy** — oceniaj to, co widzisz.

## Dwie skale, obie 1–7

### 1. Naturalność

Czy to zdanie mógł napisać człowiek piszący swobodnie o tej sprawie?

| | |
|---|---|
| **7** | całkowicie naturalne, nie zwraca uwagi |
| **5** | lekko sztywne, ale bez zgrzytu |
| **3** | wyraźnie niezręczne, czytelnik się potyka |
| **1** | zdanie, którego człowiek by nie napisał |

### 2. Jasność odniesienia

Czy wiadomo, **o czym** to zdanie mówi — do jakiej rzeczy albo sprawy się
odnosi?

| | |
|---|---|
| **7** | odniesienie jednoznaczne, wiadomo dokładnie o co chodzi |
| **5** | odniesienie zrozumiałe, choć trzeba się chwilę zastanowić |
| **3** | odniesienie mgliste albo dwuznaczne |
| **1** | nie wiadomo, o czym mowa |

## Na co zwracać uwagę

- **Czy referent w ogóle istnieje w rozmowie?** Zdanie może odwoływać się
  do czegoś, o czym nigdy nie było mowy.
- **Czy referent pasuje rodzajem?** Odniesienie do dnia tygodnia tam, gdzie
  mowa o rzeczy fizycznej, jest niedopasowaniem.
- **Czy zdanie nie mówi przypadkiem o samej rozmowie**, gdy z kontekstu
  wynika, że miało mówić o świecie zewnętrznym.
- **Czy fraza brzmi jak polszczyzna / angielszczyzna**, którą ktoś naprawdę
  napisał.

## Czego NIE oceniasz

- treści merytorycznej — nie sprawdzasz, czy rzemieślnik ma rację;
- długości zdania;
- tego, czy temat jest ciekawy.

## Format odpowiedzi

Zapisujesz **plik JSON** o strukturze:

```json
{
  "oceniajacy": "<numer>",
  "oceny": [
    {"id": "K000", "naturalnosc": 6, "jasnosc_odniesienia": 5},
    {"id": "K001", "naturalnosc": 3, "jasnosc_odniesienia": 2}
  ]
}
```

Wszystkie 96 elementów, oceny całkowite od 1 do 7. Żadnych komentarzy
w pliku — komentarze idą do raportu, nie do danych.
