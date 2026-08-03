# Bramka naturalności — kalibracja na rzeczywistych ocenach

**Data:** 2026-08-03
**Materiał:** zestaw ofiarny SPEKTRY-1, wersja 2 (odbudowana)
**Panel:** 9 oceniających, 95 elementów, 2 skale, ocena ślepa
**Kod:** `gates/naturalnosc/zbuduj_kalibracje.py`, `gates/naturalnosc/prog.py`

---

## 1. Dlaczego trzeba było zaczynać od nowa

Pierwszy zestaw kalibracyjny **nie mierzył tego, co miał mierzyć.** Cztery
wady, każda z osobna wystarczająca do unieważnienia:

| # | Wada | Skutek |
|---|---|---|
| 1 | Frazy uszkadzające PL pisane **bez diakrytyków**, otoczenie z diakrytykami | oceniający wykrywał uszkodzenie po **zapisie**, nie po badanej właściwości |
| 2 | Uszkodzone warianty gubiły **przecinek** przed „gdzie" | drugi trop ortograficzny |
| 3 | Uszkodzenia EN to **urwane zdania** („Whatever sits the thing that was there") | mierzono obcięcie, nie odniesienie |
| 4 | **Wszystkie** uszkodzenia wstrzyknięte do wariantu `self` | klasa „samozwrotny" była **pozorna** — w wariancie samozwrotnym odniesienie do rozmowy jest poprawne |

Wada 4 jest najpoważniejsza, bo nie dotyczy zapisu tylko konstrukcji:
**dwanaście elementów udawało uszkodzone, nie będąc uszkodzonymi.**

### Jak zbudowano wersję 2

Każde uszkodzenie powstaje z **bliźniaka nienaruszonego** (ten sam scenariusz,
wariant i kontekst) przez podmianę **wyłącznie frazy referenta**, w ramie
odczytanej mechanicznie. Kontrola przy budowie odrzuca zestaw, jeśli
uszkodzone różni się od bliźniaka czymkolwiek poza frazą — sprawdzana jest
gęstość diakrytyków, liczba przecinków ramy i długość ramy.

Klasa uszkodzenia trafia do wariantu, w którym **jest błędem**:
samozwrotny → do wariantu zewnętrznego osadzonego, nieosadzony → do
neutralnego, i tak dalej.

---

## 2. Próg — reguła zamrożona przed obejrzeniem ocen

> **próg = kwantyl 10% rozkładu średnich elementów NIENARUSZONYCH**

Wykrywalność uszkodzeń jest wtedy **wynikiem pomiaru, nie przedmiotem wyboru.**
Gdyby próg dobierać tak, żeby wyszła ładna wykrywalność, kalibracja byłaby
autoportretem.

Próg liczony **osobno dla każdego języka** — repliki są osobnymi badaniami.

## 3. Wynik

| Język | Skala | Nienaruszone | Uszkodzone | **PRÓG** | Fałsz. odrzucenie | **Wykrywalność** |
|---|---|---:|---:|---:|---:|---:|
| PL | naturalność | 4,92 | 2,19 | **3,22** | 8% | **100%** |
| EN | naturalność | 5,46 | 1,90 | **3,78** | 8% | **100%** |
| PL | jasność odniesienia | 4,12 | 1,69 | **2,00** | 4% | 75% |
| EN | jasność odniesienia | 4,44 | 1,46 | **2,11** | 8% | 83% |

**Skala naturalności działa.** Rozdzielenie +2,7 (PL) i +3,6 (EN) punktu,
wykrywalność stuprocentowa we wszystkich czterech klasach uszkodzeń.

**Skala jasności odniesienia ma ślepą plamę** i jest ona strukturalna:

| Klasa uszkodzenia | Wykrywalność (jasność) PL | EN |
|---|---:|---:|
| niedopasowany | 6/6 | 6/6 |
| nieosadzony | 6/6 | 6/6 |
| niezgrabny | 6/6 | 5/5 |
| **samozwrotny** | **0/6** | **2/6** |

Powód podali sami oceniający, niezależnie od siebie: przy odniesieniu do
rozmowy **referent istnieje i jest jasny** — wadą jest to, że nie o nim miała
być mowa. Skala jasności z definicji tego nie złapie.

> **Wniosek: pułapki samozwrotnej pilnuje skala naturalności, nie jasności.**
> Jasność zostaje jako kontrola osadzenia, ale nie może być jedynym
> detektorem tej pułapki.

---

## 4. Trzy zamrożone kryteria, które realny materiał obala

To jest ważniejsze niż sam próg.

| Kryterium z projektu §6 | Co pokazuje materiał | Werdykt |
|---|---|---|
| naturalność **każdego wariantu ≥ 5,0** | nienaruszony materiał PL ma średnią **4,92**, wariant `self` **3,17** | **nieosiągalne** |
| jasność referenta **każdego wariantu ≥ 5,0** | nienaruszony wariant nieosadzony ma **2,09** w obu językach | **nieosiągalne z definicji** |
| **rozstęp** średnich naturalności między wariantami **≤ 1,0** | rozstęp nienaruszonego materiału: **3,27** (PL), **2,52** (EN) | **nieosiągalne** |

Mechanizm jest wspólny i ten sam co przy marginesie równoważności
(ANEKS-4 do SPEKTRY-1): **kryterium zamrożono, nie sprawdzając, czy jest
osiągalne.**

Tutaj przyczyna jest szczególnie wyraźna. Warianty **różnią się z założenia
na dokładnie tych wymiarach, które bramka mierzy**:

- wariant **nieosadzony** ma nierozstrzygalny referent — to jego definicja,
  więc niska jasność jest cechą, nie wadą;
- wariant **samozwrotny** czyta się mniej naturalnie niż zewnętrzny — po
  polsku szczególnie („to przetwarzanie", „to nasze zastanawianie" to ciężkie
  nominalizacje).

Bramka żądająca, by wszystkie warianty wypadły jednakowo wysoko, żąda
zniesienia różnicy, którą badanie ma zmierzyć.

---

## 5. Czego ten wynik NIE rozstrzyga

**Progi policzono na materiale SPEKTRY-1, a stosować je mamy do SPEKTRY-2 —
a te korpusy różnią się konstrukcją dokładnie tam, gdzie to istotne.**

W SPEKTRZE-1 warianty nie musiały dzielić ramy. W SPEKTRZE-2 **muszą**:
sześć wariantów tego samego wstawienia różni się wyłącznie frazą referenta
(spec §2). Rozstęp między wariantami może więc być w SPEKTRZE-2 wielokrotnie
mniejszy niż zmierzone 3,27.

**Dlatego progów z tej kalibracji nie wolno zamrozić jako progów badania.**
Ta kalibracja dowodzi czego innego, i to jest jej właściwy wynik:

1. **przyrząd działa** — panel odróżnia materiał uszkodzony od nienaruszonego
   z wykrywalnością 100% na skali naturalności;
2. **skala jasności ma znaną ślepą plamę** na pułapce samozwrotnej;
3. **trzy zamrożone kryteria są nieosiągalne** i wymagają przeprojektowania
   przed rejestracją.

Próg do badania trzeba policzyć na **próbce korpusu SPEKTRY-2**, ocenionej
tym samym panelem i tą samą regułą kwantylową. To jest następny krok.

---

## 6. Ograniczenie panelu — do zadeklarowania w rejestracji

| Miara | Wartość | Założenie w projekcie |
|---|---:|---:|
| średnia korelacja par oceniających (naturalność) | **0,93** | — |
| średnie SD ocen elementu (naturalność) | **0,51** | 1,0 |
| średnie SD ocen elementu (jasność) | **0,34** | 1,0 |

Dziewięciu oceniających to **dziewięć wywołań tego samego modelu**. Ich zgoda
jest dowodem **podobieństwa, nie trafności**. Zmierzone SD jest o połowę
mniejsze od założonego w rachunku mocy, więc:

- przedziały ufności progu są **za wąskie**;
- „9 ocen" nie niesie niezależności, którą projekt zakładał;
- **ocena ludzka na próbce 20% pozostaje niezbędna** — bez niej nie wiadomo,
  czy panel mierzy naturalność, czy własne preferencje stylistyczne.

---

## 7. Element wykluczony z rachunku

**K055** — odbudowa zestawu wstawiła frazę pojedynczą pod czasownik w liczbie
mnogiej: „that whole other thing there **arrive** in". Element psuje się na
dwa sposoby naraz, więc nie mierzy samego odniesienia. Zgłosiło go
niezależnie **siedmiu z dziewięciu** oceniających.

Wykluczenie jest jawne i zapisane w kodzie (`prog.py`, stała `WYKLUCZONE`)
razem z powodem — element usunięty po cichu byłby dopasowaniem wyniku.

---

## 8. Co zrobić dalej

1. **Przeprojektować kryteria §6** tak, żeby porównywały wariant z oczekiwaniem
   dla **jego rodzaju**, a nie wszystkie z jedną stałą.
2. **Ocenić próbkę korpusu SPEKTRY-2** tym samym panelem i policzyć progi na
   materiale o właściwej konstrukcji.
3. **Zorganizować ocenę ludzką** na 20% — bez wykonawcy ta pozycja wisi
   od początku projektu.
4. Dopiero potem **rejestracja OSF** i pieczęć.
