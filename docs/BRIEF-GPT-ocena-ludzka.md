# Brief dla konsultacji zewnętrznej — walidacja ludzka bramki naturalności

**Do:** modelu zewnętrznego (GPT), proszonego o krytykę adwersaryjną
**Od:** zespołu SPEKTRA-2
**Data:** 2026-08-05
**Prośba:** oceń, czy proponowane rozwiązanie ratuje walidację, czy tylko
ukrywa jej brak. **Interesuje nas zarzut, nie potwierdzenie.**

---

## 1. Czym jest badanie

SPEKTRA-2 to prerejestrowane badanie na modelach językowych (Gemma-3-4B jako
ramię główne, PLLuM-4B jako replikacyjne). Mierzymy geometryczną własność
stanów ukrytych — udział modów widma korelacji aktywacji powyżej progu
wyznaczonego z symulowanego rozkładu zerowego, uśredniony po zamrożonym paśmie
warstw. Jeden skalar na tekst.

Bodźcem jest **korpus rozmów rzemieślniczych** (96 scenariuszy: 48 polskich,
48 angielskich, repliki nigdy nie łączone). W każdym scenariuszu jest 5 miejsc
wstawki, a każda wstawka istnieje w **sześciu wariantach**, które dzielą
identyczną ramę zdaniową i różnią się **wyłącznie frazą referenta**:

| wariant | referent | przykład |
|---|---|---|
| B | neutralny, obecny w rozmowie | „to koło wodne" |
| C | samozwrotny | „ta nasza rozmowa" |
| C′-G | zewnętrzny, osadzony w rozmowie | „ten drugi piec" |
| C′-comp | obliczeniowy, obecny w scenie | „ten miernik ciągu" |
| C′-M | zwyczajny, spoza rozmowy | „tamto coroczne mycie okien" |
| C′-U | nieosadzony, techniczny | „tamten falownik" |

Hipoteza główna porównuje C z C′-comp.

## 2. Po co bramka naturalności

Jeśli któryś wariant jest **gorzej napisany** od pozostałych, zmierzona różnica
geometryczna może pochodzić z jakości języka, a nie z badanej własności
odniesienia. Bramka ma to wykluczyć przed zapieczętowaniem korpusu.

Bramka ocenia każdy wariant na trzech skalach 1–7:
1. **naturalność** — czy człowiek mógł tak napisać;
2. **jasność odniesienia** — czy wiadomo, o czym mowa;
3. **odczyt samozwrotny** — czy zdanie da się odczytać jako mówiące
   o trwającej rozmowie (skala faktograficzna, nie oceniająca).

## 3. Problem, z którym przychodzimy

Panel oceniający to **dziewięć wywołań tego samego modelu**. Zmierzona zgodność
jest bardzo wysoka (korelacja par 0,84–0,98), ale dowodzi **podobieństwa,
nie trafności**. Projekt przewiduje więc **ocenę ludzką na próbce 20%** jako
sprawdzenie, czy panel modelowy w ogóle zgadza się z człowiekiem.

Ta pozycja **nie ma wykonawcy od początku projektu.**

Rachunek w wersji pierwotnej (ocena bezwzględna na skali 1–7):

- 58 elementów na język (× 2 języki),
- 7 ocen na element → 406 ocen na język,
- 3 sądy na ocenę,
- sesja 30–45 minut → **około 28 osób**, native speakerzy obu języków,
- koszt platformy badawczej: **200–250 euro**.

Projekt jest prowadzony przez jedną osobę bez budżetu badawczego i bez
zaplecza instytucjonalnego. To jest realna bariera, nie wymówka.

## 4. Co już wiemy o zachowaniu panelu — dwa twarde ustalenia

Podajemy je, bo są istotne dla oceny propozycji.

**(a) Efekt kontrastu.** Zmieniliśmy frazę w JEDNYM wariancie (C).
Bezwzględne oceny **wszystkich pozostałych** wariantów przesunęły się,
i to systematycznie — tym mocniej, im mniej osadzony referent
(B −0,19, C′-comp −0,29, C′-M −0,44, C′-U −0,74). Wniosek: **bezwzględne
wartości panelu nie są porównywalne między zestawami bodźców.**

**(b) Długość kontekstu jest zmienną eksperymentalną.** Pokazanie
oceniającym całego dialogu zamiast czterech ostatnich zdań zmieniło oceny
na wszystkich trzech skalach, w różnych kierunkach dla różnych wariantów.

Oba ustalenia podważają sens **ocen bezwzględnych** jako miary — i to jest
punkt wyjścia dla naszej propozycji.

## 5. Propozycja do skrytykowania

**Zamienić zadanie ludzkie z oceny bezwzględnej na porównanie parami.**

Człowiek dostaje kontekst i **dwa zdania** różniące się wyłącznie frazą
referenta, i odpowiada na jedno pytanie: *które brzmi naturalniej?*
(z opcją „nie widzę różnicy").

| | ocena bezwzględna | porównanie parami |
|---|---|---|
| sądów na element | 3 skale × 7 ocen | 1 wybór × 5 ocen |
| czas na sąd | 45–90 s | ~12 s |
| sesja | 30–45 min | **~11 min** |
| osób na język | 14 | **5** |
| osób łącznie | 28 | **10** |
| koszt | 200–250 € | **0** (rekrutacja nieformalna) |

Statystyka zgodności zmienia się z korelacji średnich na **udział par,
w których uporządkowanie panelu modelowego zgadza się z większością ludzką**.
Przy 58 parach na język przedział ufności dla zgodności 80% wynosi 0,70–0,90.

Uzasadnienie merytoryczne, nie tylko kosztowe:

- porównanie parami **nie wymaga kalibracji skali**, więc jest odporne na
  efekt kontrastu z punktu 4(a);
- materiał jest do tego wprost stworzony: warianty **już są parami** różniącymi
  się jedną frazą przy identycznej ramie;
- porównanie parami jest standardowo rzetelniejsze od ocen bezwzględnych przy
  małej liczbie sędziów.

## 6. Pytania, na które prosimy o odpowiedź

1. **Czy zamiana zadania nie zmienia konstruktu?** Panel modelowy ocenia
   bezwzględnie, ludzie porównawczo. Czy zgodność między nimi da się w ogóle
   sensownie policzyć — i jaką statystyką? Rozważaliśmy: uporządkowanie par
   z ocen modelowych i porównanie z wyborem ludzkim. Czy to wystarcza, czy
   trzeba, żeby model też wykonał zadanie parami?

2. **Które pary pokazywać?** Wszystkich par jest 15 na wstawkę (6 wariantów
   po 2). Nie pokażemy wszystkich. Nasza intuicja: pokazywać wyłącznie pary
   wchodzące do hipotez (C vs C′-comp, C′-comp vs C′-U, C′-U vs C′-M) oraz
   kotwicę (B vs każdy). Czy to nie tworzy selekcji, która zawyża zgodność?

3. **Pięć osób na język — czy to nie za mało**, żeby cokolwiek twierdzić?
   Rozstrzygamy większością z pięciu na parę. Jaki jest realny koszt tego,
   że sędziowie nie są losową próbą populacji, tylko znajomymi autora?

4. **Czy porównanie parami wystarczy dla WSZYSTKICH TRZECH skal?**
   Naturalność — tak, to sąd porównawczy z natury. Ale „jasność odniesienia"
   i „odczyt samozwrotny" są bliższe **anotacji faktu** niż ocenie. Czy dla
   nich lepszy nie byłby inny format (np. pytanie zamknięte: „do czego odnosi
   się to zdanie?" z listą kandydatów)?

5. **Czy istnieje tańsza droga, której nie widzimy?** Rozważaliśmy:
   - panel z **kilku różnych rodzin modeli** zamiast jednej (rozwiązuje
     zależność od jednego modelu, ale nadal nie jest walidacją ludzką);
   - kalibrację wobec **istniejących zbiorów z ocenami ludzkimi**
     (akceptowalność językowa) — ale nasz konstrukt jest inny niż
     akceptowalność gramatyczna;
   - **rezygnację z walidacji ludzkiej** i jawne zadeklarowanie tego jako
     ograniczenia.

   Który z tych wariantów jest najmniej zły, jeśli porównanie parami
   też okaże się niewystarczające?

6. **Pytanie najważniejsze: czy bez walidacji ludzkiej badanie nadal ma
   sens?** Bramka naturalności jest kontrolą konstrukcyjną korpusu, a nie
   pomiarem głównym. Czy jej niepełna walidacja unieważnia wynik główny,
   czy jest ograniczeniem do zadeklarowania obok innych?

---

## 7. Czego NIE potrzebujemy

Nie potrzebujemy zapewnienia, że rozwiązanie jest dobre. Projekt ma za sobą
serię przypadków, w których zamrożone kryterium okazywało się **nieosiągalne**
dopiero po zmierzeniu — margines równoważności, próg naturalności 5,0, rozstęp
między wariantami ≤ 1,0. Za każdym razem ratował nas pomiar, nie rozumowanie.

Szukamy więc zarzutu, który da się sprawdzić pomiarem, zanim zaprosimy
pierwszą osobę.
