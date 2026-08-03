# Która fraza jest wariantem samozwrotnym — rozstrzygnięcie

**Data:** 2026-08-04
**Materiał:** 24 scenariusze × 2 wersje frazy = 48 elementów
**Panel:** 9 oceniających, 3 skale, parowanie w obrębie scenariusza
**Test:** dokładna permutacja parowana (2¹² = 4096), osobno per język
**Kod:** `gates/naturalnosc/sonda_self.py`, `gates/naturalnosc/sonda_wynik.py`

---

## 1. Skąd wzięło się pytanie

Specyfikacja autorska dopuszczała dla wariantu `self` **dwa referenty naraz**:
„bieżącą wymianę" **albo** „układ, który ją prowadzi". Próbka korpusu pokazała,
że korpus faktycznie używa obu — 22 scenariusze „to przetwarzanie", 2 „ten tok
pytań" — i że wypadają skrajnie różnie.

Wybór między nimi **jest definicją hipotezy głównej**, nie kwestią redakcyjną.
Przy n = 2 na wersję nie dało się go podjąć. Ta sonda daje n = 12 na język,
parowane w obrębie scenariusza.

---

## 2. Wynik

| Skala | | „to przetwarzanie" | „ten tok pytań" | różnica | p |
|---|---|---:|---:|---:|---:|
| naturalność | PL | 3,08 | 5,43 | **+2,34** | 0,0005 |
| | EN | 3,27 | 5,62 | **+2,35** | 0,0005 |
| jasność odniesienia | PL | 2,39 | 5,91 | **+3,52** | 0,0005 |
| | EN | 2,56 | 6,56 | **+3,99** | 0,0005 |
| **odczyt samozwrotny** | PL | **3,94** | **6,78** | **+2,84** | 0,0005 |
| | EN | **3,90** | **7,00** | **+3,10** | 0,0005 |

p = 0,0005 to **minimum osiągalne** przy 12 parach (2/4096) — wszystkie
dwanaście par w obu językach idzie w tę samą stronę, bez wyjątku.

---

## 3. Rozstrzygające nie jest to, co się wydawało

Szedłem po naturalność. Decydujące okazało się co innego.

**„To przetwarzanie" nie jest niezawodnie czytane jako samoodniesienie:
3,94 (PL) i 3,90 (EN) — poniżej środka skali.**

Wariant, który ma być samozwrotny, w połowie przypadków samozwrotny nie jest.
Dziewięciu oceniających opisało niezależnie ten sam mechanizm: w rzemiosłach,
które **same są przetwórstwem** (kiszenie, wędzenie, miodosytnictwo, czerpanie
papieru, wypał, przemiał), czytelnik podstawia pod tę frazę **proces w świecie**.
W rzemiosłach mechanicznych (rower, kosiarka, dach, studnia, mur) żadnego
kandydata nie ma, więc odczyt samozwrotny wraca — ale jako domysł, nie jako
znaczenie.

To jest poważniejsze niż niska naturalność. **Manipulacja nie działa
jednorodnie w korpusie**, a jej działanie zależy od tematu rzemiosła — czyli
od zmiennej, której nie kontrolujemy.

## 4. Efekt zakotwiczenia — i co z niego wynika

Ta sama fraza dostała **5,57** na odczycie samozwrotnym w próbce korpusu
i **3,92** tutaj. Różnica bierze się z tego, że w sondzie obie wersje leżą
obok siebie: przy „this conversation" na 7,0 „this processing" przestaje
wyglądać na samoodniesienie.

**Wniosek: samozwrotność „przetwarzania" nie jest własnością frazy, tylko
własnością zestawienia, w jakim się ją ogląda.** Referent, który zmienia
kategorię zależnie od sąsiedztwa, nie nadaje się na warunek eksperymentalny.

---

## 5. Kryterium formalne — dopasowanie obecności

Specyfikacja §1 wymaga, by para `self` ↔ `external_computational` miała **oba
referenty obecne i bliskie**; to był cały powód dodania szóstego wariantu.

| Język | jasność C′-comp (cel) | „przetwarzanie" | niedopasowanie | „tok pytań" | niedopasowanie |
|---|---:|---:|---:|---:|---:|
| PL | 4,23 | 2,39 | 1,84 | 5,91 | **1,68** |
| EN | 5,01 | 2,56 | 2,45 | 6,56 | **1,55** |

Obie repliki wskazują tę samą wersję. Po polsku przewaga jest **niewielka**
(0,16 pkt) — tam decyduje odczyt samozwrotny, nie obecność.

**Uczciwie: „tok pytań" też nie jest dopasowany.** Niedopasowanie spada
z 1,84–2,45 do 1,55–1,68, ale zmienia znak — z referenta zbyt mglistego robi
się referent zbyt oczywisty. Para główna nadal nie jest wyrównana i to zostaje
jako znane ograniczenie.

---

## 6. Decyzja

**Wariantem samozwrotnym jest „ta rozmowa" / „ten tok pytań" /
„this conversation". „To przetwarzanie" wypada z korpusu.**

Zapisane w `corpus/AUTHORING-SPEC-SPEKTRA-2.md`, sekcja `self`.

### Co trzeba zrobić

1. **Przepisać wariant `self`** w 96 scenariuszach (5 wstawek każdy).
2. **Przeliczyć równanie tokenów ±2%** — polska fraza jest o słowo dłuższa;
   angielska ma tę samą długość.
3. **Zachować starą frazę jako wariant opisowy**, żeby ciągłość ze SPEKTRĄ-1
   (ramię replikacyjne C − C′-G) dała się policzyć osobno. Bez tego zmiana
   zrywa porównywalność z zapieczętowanym badaniem.
4. Powtórzyć bramkę naturalności na poprawionym korpusie.

### Dlaczego to jest dozwolone przed rejestracją

Zmiana bodźca po zobaczeniu **ocen naturalności**, a nie po zobaczeniu
endpointu. Żaden przebieg modelu jeszcze nie padł, I_total nie istnieje.
Bramka naturalności jest dokładnie tym miejscem, w którym bodziec ma być
poprawiany — to jej funkcja. **Po rejestracji ta sama zmiana byłaby
niedopuszczalna.**

---

## 7. Ograniczenia

**Ślepota warunku nie została zachowana w pełni.** Przy 48 pozycjach ułożonych
w pary ten sam kontekst wraca dwa razy z podmienioną frazą; jeden z oceniających
zgłosił wprost, że konstrukcja jest czytelna. Kierunek wyniku jest tak duży
(+2,3 do +4,0 punktu), że nie da się go tym wyjaśnić, ale wielkość efektu może
być zawyżona.

**Panel jednorodny** — dziewięć wywołań tego samego modelu. To samo ograniczenie
co w poprzednich dwóch rundach.

**Szum ram.** Sześć scenariuszy ma pleonazm „kolejność kolejnych / kolejno
wykonywanych kroków". Oceniający obniżali za to naturalność **w obu ramionach
pary**, więc porównania nie obciąża — ale zaniża sufit i powinno zostać
poprawione osobno.
