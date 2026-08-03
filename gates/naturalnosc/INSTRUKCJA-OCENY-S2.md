# Instrukcja oceny — próbka korpusu SPEKTRY-2

Oceniasz **pojedyncze zdanie** wstawione w rozmowę. Dostajesz kontekst
(kilka wcześniejszych zdań) i to jedno zdanie. Kontekstu **nie oceniasz** —
on jest tłem.

Materiał jest z założenia bardzo powtarzalny: te same ramy zdaniowe wracają
z podmienioną frazą odsyłającą. **Tak ma być** — badanie izoluje właśnie tę
frazę. Oceniaj każde wystąpienie osobno, wobec **jego własnego** kontekstu.

## Trzy skale, wszystkie 1–7

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
| **7** | odniesienie jednoznaczne |
| **5** | zrozumiałe, choć trzeba się chwilę zastanowić |
| **3** | mgliste albo dwuznaczne |
| **1** | nie wiadomo, o czym mowa |

### 3. Odczyt samozwrotny — **nowa skala**

Czy to zdanie da się odczytać jako odniesienie **do trwającej rozmowy** albo
**do czynności właśnie wykonywanej** — a nie do rzeczy w świecie?

| | |
|---|---|
| **7** | mówi wprost o tej rozmowie / o tym, co teraz robimy |
| **5** | da się tak odczytać przy niewielkim wysiłku |
| **3** | raczej nie, choć odczyt jest do obronienia |
| **1** | wcale — odniesienie jest jednoznacznie do świata zewnętrznego |

**To NIE jest skala oceny.** Nie oznaczaj wysokiej wartości jako wady.
Część materiału ma odnosić się do rozmowy z założenia. Twoim zadaniem jest
**stwierdzić fakt**, nie ocenić go.

Ta skala istnieje, bo skala jasności odniesienia tego nie wykrywa: gdy zdanie
mówi o rozmowie, referent **istnieje i jest jasny** — więc jasność wychodzi
wysoka, choć zdanie może być zupełnie nie o tym, o czym miało być.

## Czego NIE oceniasz

- treści merytorycznej — nie sprawdzasz, czy rzemieślnik ma rację;
- długości zdania;
- tego, czy temat jest ciekawy;
- **tego, czy zdanie „pasuje" do kontekstu tematycznie** — od tego jest
  skala jasności odniesienia, nie naturalności. Naturalność dotyczy tego,
  czy fraza brzmi jak żywy język.

## Format odpowiedzi

```json
{
  "oceniajacy": "<numer>",
  "oceny": [
    {"id": "S000", "naturalnosc": 6, "jasnosc_odniesienia": 5, "samozwrotnosc": 1}
  ]
}
```

Wszystkie 144 elementy, oceny całkowite 1–7. Żadnych komentarzy w pliku.
