# Panel oceniający — co wychodzi po drugiej recenzji

**Data:** 2026-08-03
**Podstawa:** krytyka adwersaryjna do `docs/BRIEF-GPT-panel-actproof.md`
**Status:** budowa **wstrzymana** do wykonania pilota czasowego

---

## 1. Błąd, który przewracał cały rachunek

W briefie podałem **12 sekund na parę, 5 minut na osobę, 10–12 osób na język**.

Wyceniłem czas **decyzji** i zapomniałem o czasie **czytania kontekstu**.
Kontekstem jest cały dialog do miejsca wstawki — mediana **243 słowa**.

Przeliczone na realnych danych korpusu:

| tempo czytania | s / para | 24 pary |
|---|---:|---:|
| 250 sł./min (pobieżnie) | 74 | 29 min |
| **200 sł./min (ze zrozumieniem)** | **90** | **36 min** |
| 160 sł./min (uważnie) | 110 | 44 min |

**Pomyłka sześcio- do ośmiokrotna.** Recenzent policzył to samo niezależnie
i wyszedł na 20–35 minut.

To nie jest korekta kosmetyczna. Zmienia zgodę uczestnika, ryzyko porzucenia
zadania, jakość odpowiedzi i przede wszystkim **liczbę potrzebnych ludzi**.

---

## 2. Dwie dźwignie, którymi da się to odzyskać

| wariant | s/para | par w 10 min | osób/język | osób razem |
|---|---:|---:|---:|---:|
| **A.** 1 para na scenariusz, pełny kontekst | 90 | 7 | 45 | **90** |
| **B.** 5 par na scenariusz, pełny kontekst | 32 | 19 | 16 | **32** |
| **C.** 1 para na scenariusz, skrócony (90 sł.) | 44 | 14 | 22 | **44** |
| **D.** 5 par na scenariusz, skrócony | 22 | 27 | 12 | **24** |

**Dźwignia 1 — amortyzacja kontekstu.** Uczestnik czyta rozmowę **raz**
i ocenia pary z kilku różnych pozycji wstawki tego samego scenariusza.
Koszt na parę spada 2,8×.

**Dźwignia 2 — skrócenie kontekstu.** Zamiast całego dialogu — okno kilku
zdań obejmujące wprowadzenie referenta.

**Obie mają cenę i żadnej nie wolno przyjąć bez pomiaru:**

- amortyzacja **łamie ślepotę**: widząc pięć wstawek w jednej rozmowie
  uczestnik może odkryć, że zmienia się jedna fraza — a to jest dokładnie
  mechanizm, przed którym ostrzegał recenzent;
- skrócenie kontekstu **zmienia oceny** — zmierzyliśmy to własnym panelem
  na wszystkich trzech skalach.

## 3. Rzecz, którą przy okazji sobie wyjaśniłem

Zakładałem, że oceniający musi widzieć to samo, co mierzony model. **To nie
jest prawda.** Model widzi cały dialog, bo tak wygląda pomiar. Panel oceniający
to **osobny przyrząd**, który ocenia, czy tekst jest dobrze napisany.

Wymóg jest inny i słabszy: **człowiek i model-oceniający muszą widzieć to
samo.** Długość kontekstu wolno więc skrócić — pod warunkiem, że zostanie
zamrożona, zadeklarowana i sprawdzona pod kątem stabilności uporządkowania.

To otwiera wariant C i D, które inaczej byłyby zakazane.

---

## 4. Zarzuty przyjęte bez zastrzeżeń

**To nie jest BIBD.** Dla 60 par i 5 ocen parametr współwystępowania wynosi
λ = 5·(k−1)/59, a 59 jest liczbą pierwszą — dla bloku niepełnego nie wyjdzie
liczba całkowita. Nazwa zmieniona na **„ograniczony, w przybliżeniu
zbalansowany plan przydziału"**, z jawną listą siedmiu ograniczeń zamiast
odwołania do nieistniejącej konstrukcji. Doszło ograniczenie, którego nie
miałem: **wyrównywać łączną liczbę znaków w blokach**, nie tylko liczbę par.

**„Panel" to zła nazwa.** Trwały panel uczestników wymaga identyfikatora,
czyli wyklucza pełną anonimowość. Rozdzielone: **narzędzie** może być trwałe,
**uczestnicy** rekrutowani od nowa do każdego badania. Nazwa robocza:
*anonimowy system przydziału zadań i zbierania ocen*.

**Zgoda była nieprecyzyjna.** Zdanie „nie ma odpowiedzi poprawnych i błędnych"
jest prawdziwe dla naturalności, ale **fałszywe dla klasyfikacji referenta** —
tam istnieje referent zamierzony. Nowe brzmienie: *„Nie sprawdzamy Twojej
wiedzy ani umiejętności."*

**Dane demograficzne.** Zostaje **wyłącznie język ojczysty** — jest wymagany
przez plan badania. Wiek i wykształcenie **wypadają**, bo nie ma
prerejestrowanej analizy, która by ich używała, a przy 12 osobach ich
połączenie z czasem i tokenem wskazuje konkretną osobę.

**Dokładny znacznik czasu wypada z eksportu.** Zostaje czas trwania pozycji
i kolejność. Rekruter mógłby pamiętać, że ktoś wypełniał formularz o 19:42.

**Tokeny.** Hash tokenu, `response_id` osobno, **zero powiązania token↔odpowiedź**,
tabela tokenów usuwana po zamknięciu badania. Bez tego dane są pseudonimowe,
nie anonimowe.

**IP.** Dopóki serwer loguje pełne adresy, słowo „anonimowe" jest nie do
obrony. Do rozstrzygnięcia przy wdrożeniu — to zadanie dla DEP, nie dla treści
formularza.

**Kontrole uwagi.** Dwie, **spoza korpusu analitycznego**, z regułą zapisaną
z góry: obie oblane → wykluczenie; jedna oblana → zostaje w analizie głównej
plus osobna analiza wrażliwości. Bez automatycznego progu czasowego, dopóki
pilot nie pokaże, ile trwa rzeczywiste czytanie.

**Rekrutacja celowana bije publiczny link.** Jednorazowe tokeny, dwóch–trzech
niezależnych rekruterów, badacz nie przechowuje powiązania token–osoba.
Publiczna próba ewentualnie później, jako **osobna analiza odporności**,
nigdy zmieszana z zaplanowaną walidacją.

---

## 5. Bramka przeciw zajęciu zastępczemu

Recenzent nazwał wprost ryzyko, które sam zgłosiłem: **narzędzie nie
rekrutuje.** Warunki przed napisaniem pierwszej linijki kodu:

1. sześć osób, które przeszły **pilot czasowy** na statycznym prototypie
   (3 PL + 3 EN, nie wchodzą potem do walidacji właściwej);
2. lista **co najmniej 10 potencjalnych uczestników na język**;
3. gotowy schemat przydziału;
4. **dowód, że zwykły formularz nie obsługuje konkretnego wymogu**;
5. limit implementacji: **dwa dni**.

> **Jeżeli nie da się znaleźć sześciu osób na statyczny prototyp, własna
> platforma tego nie naprawi.**

## 6. Zakres, gdyby doszło do budowy

**Budować:** generowanie i weryfikację tokenów, wybór bloku, przekazanie
`block_id` do gotowego formularza, oznaczanie tokenu jako wykorzystanego,
wersjonowanie badania, eksport i audyt przydziału.

**Nie budować:** kont uczestników, panelu administracyjnego, systemu zaproszeń,
profili demograficznych, historii międzybadaniowej, analityki, własnego
kreatora formularzy.

Czyli: **cienki alokator + gotowy formularz + własny eksport**, nie system
ankietowy od zera.

---

## 7. Co robimy teraz

**Pilot czasowy jest jedyną rzeczą, która ma sens jako następny krok.**
Dziesięć realnych par, statyczny prototyp, trzy osoby na język. Mierzymy czas
całkowity, czas na parę, powroty do kontekstu, zmęczenie — i **czy uczestnik
potrafi nazwać manipulację** (to rozstrzyga o dopuszczalności amortyzacji).

Dopiero wynik pilota wybiera wariant z tabeli w §2 i mówi, ilu ludzi naprawdę
potrzeba.

**Kryterium NIE-budowania:** jeśli nie uda się zrekrutować pilota, jeśli sesja
przekracza akceptowalny czas, jeśli ograniczenia obsłuży arkusz z gotowym
formularzem, albo jeśli jedynym uzasadnieniem jest przydatność
w nieokreślonych przyszłych badaniach.
