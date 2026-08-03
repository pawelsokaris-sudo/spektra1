# Brief dla konsultacji zewnętrznej — anonimowy panel oceniający na actproof.io

**Do:** modelu zewnętrznego (GPT), proszonego o krytykę adwersaryjną
**Od:** zespołu SPEKTRA-2
**Data:** 2026-08-03
**Prośba:** oceń, czy ten pomysł **ratuje walidację, czy tworzy pozór
walidacji**. Interesuje nas zarzut, nie potwierdzenie.

**Kontekst poprzedni:** ten sam recenzent ocenił wcześniej projekt modułu
walidacji ludzkiej (`docs/SPEKTRA-2-walidacja-ludzka.md`) i wskazał sześć wad,
które przyjęliśmy w całości — m.in. że model musi wykonywać identyczne zadanie
co ludzie, że potrzeba 10–12 oceniających na język zamiast 5, i że przedziały
ufności trzeba liczyć bootstrapem klastrowym po scenariuszach.

---

## 1. Bariera, którą próbujemy usunąć

Moduł walidacji ludzkiej jest zaprojektowany i zaakceptowany. Blokuje go
**jedna rzecz: brak ludzi.** Potrzeba 10–12 native speakerów na język (polski
i angielski), po około 5 minut każdy, 5 ocen na parę, rozdzielonych między
możliwie wielu oceniających.

Projekt prowadzi jedna osoba, bez budżetu badawczego i bez zaplecza
instytucjonalnego. Płatna platforma badawcza to 200–250 euro i nie jest
dostępna.

## 2. Propozycja

**Zbudować na actproof.io stałą sekcję do anonimowej oceny**, wielokrotnego
użytku — nie jednorazowy formularz dla SPEKTRY-2, tylko moduł, który obsłuży
kolejne badania.

### Wymagania funkcjonalne

- **zero danych osobowych**: bez konta, bez e-maila, bez nazwiska;
- deklarowany **język ojczysty** (konieczny dla planu badania) i opcjonalnie
  zgrubny przedział wieku oraz wykształcenia;
- **przydział zbalansowanym niepełnym planem blokowym**: każdy oceniający
  dostaje podzbiór (~24 z 60 par), każda para zbiera 5 ocen od różnych osób;
- losowana kolejność pozycji i kolejność opcji A/B;
- **jedna osoba nie widzi dwóch wersji tego samego scenariusza**;
- dwa typy zadania: porównawcze (naturalność) i klasyfikacyjne (odniesienie);
- eksport surowych odpowiedzi ze znacznikiem czasu;
- **wersjonowana definicja badania**, żeby prerejestracja mogła wskazać
  dokładnie to, co pokazano.

### Co uczestnik widzi przed rozpoczęciem

Kto prowadzi, po co, ile to trwa, że jest anonimowe, co się dzieje
z odpowiedziami, że można przerwać w każdej chwili.

**Czego uczestnik NIE widzi: hipotezy ani tego, które warianty są
porównywane i dlaczego.**

## 3. Napięcie, które sami widzimy — i prosimy o rozstrzygnięcie

Zleceniodawca sformułował wymóg: *„człowiek musi wiedzieć, o co chodzi
w badaniu i czy to jest anonimowe"*.

Poprzednia recenzja postawiła warunek: *„zero informacji o hipotezie"*.

Nasze rozstrzygnięcie robocze: **uczestnik poznaje CEL i SPOSÓB POSTĘPOWANIA
Z DANYMI, ale nie POSTAWIONĄ HIPOTEZĘ.** Przykład zgody, którą rozważamy:

> Badamy, jak ludzie oceniają naturalność zdań w rozmowie. Pokażemy Ci
> fragmenty rozmów o pracach rzemieślniczych i poprosimy o krótkie sądy.
> Nie ma odpowiedzi poprawnych i błędnych — interesuje nas Twoje wrażenie
> językowe. Zajmie to około 5 minut. Nie zbieramy żadnych danych, które
> pozwalałyby Cię zidentyfikować. Możesz przerwać w każdej chwili.

**Pytanie: czy to wystarcza jako świadoma zgoda, a jednocześnie nie skaża
pomiaru?** Gdzie dokładnie przebiega granica?

## 4. Ryzyka, które sami widzimy

**(a) Narzędzie nie rozwiązuje rekrutacji.** Nawet z gotowym panelem ktoś
musi poprosić dwadzieścia osób. Istnieje realne ryzyko, że budowa narzędzia
stanie się **zajęciem zastępczym** wobec problemu, którym jest brak ludzi.

**(b) Samoselekcja.** Kto kliknie link, nie jest próbą losową. Wcześniejsza
recenzja zaakceptowała próbę dogodnościową pod warunkiem jawnej deklaracji —
ale publiczny link to inny rodzaj dogodności niż dziesięcioro proszonych
znajomych. **Który jest gorszy?**

**(c) Powtórny udział.** Przy pełnej anonimowości ta sama osoba może wypełnić
formularz wielokrotnie. Rozważamy jednorazowe tokeny w linku, niepowiązane
z tożsamością. Czy to wystarczy, czy psuje anonimowość?

**(d) Urządzenie.** Kontekstem jest **cały dialog do miejsca wstawki**
(mediana ~1300 znaków), bo dokładnie to widzi mierzony model. Na telefonie to
dużo czytania. Czy długość kontekstu nie zostanie skorelowana z urządzeniem,
a przez to z uwagą uczestnika? Ustaliliśmy wcześniej pomiarem, że **długość
kontekstu zmienia oceny na wszystkich trzech skalach** — więc to nie jest
drobiazg.

**(e) Panel wielokrotnego użytku.** Jeśli te same osoby będą oceniać kolejne
badania, nauczą się formatu i zaczną zgadywać strukturę wariantów. Czy panel
stały nie wprowadza skażenia międzybadaniowego?

**(f) Kontrole uwagi.** Wiemy, że są potrzebne, i że reguła wykluczenia musi
być **zapisana przed zebraniem danych**. Nie wiemy, jakie i ile.

## 5. Alternatywa, której nie odrzuciliśmy

Istnieją gotowe darmowe narzędzia (samodzielnie hostowany LimeSurvey,
Formbricks, formularze Google). Budowa własnego modułu jest uzasadniona tylko
wtedy, gdy:

- **przydział blokowy** (każdy ocenia podzbiór, każda pozycja zbiera 5 ocen
  od różnych osób) jest poza zasięgiem zwykłego formularza — a naszym zdaniem
  jest;
- wielokrotny użytek w kolejnych badaniach jest realny, a nie deklarowany.

**Czy ten argument wystarcza, czy powinniśmy użyć gotowego narzędzia
i skupić się na rekrutacji?**

---

## 6. Pytania

1. Gdzie przebiega granica między świadomą zgodą a skażeniem pomiaru?
   Czy zaproponowany tekst zgody (§3) jest po właściwej stronie?
2. Publiczny anonimowy link czy dziesięcioro proszonych znajomych — która
   próba dogodnościowa jest mniej zła dla tego konkretnego celu, i jak to
   uzasadnić w publikacji?
3. Jak zapobiec powtórnemu udziałowi bez naruszenia anonimowości?
4. Jakie kontrole uwagi i jaka reguła wykluczenia — zapisane z góry?
5. Czy panel wielokrotnego użytku wprowadza skażenie międzybadaniowe,
   i czy da się je ograniczyć bez identyfikowania uczestników?
6. Czy budowa własnego modułu jest uzasadniona, czy to zajęcie zastępcze
   wobec rekrutacji?
7. **Jakie minimum dokumentacji** musi mieć taki panel, żeby dało się go
   przywołać w prerejestracji jako źródło danych?
8. Czy zbieranie języka ojczystego, przedziału wieku i wykształcenia nadal
   pozwala nazywać badanie anonimowym — i czy adres IP w logach serwera tego
   nie przekreśla?

## 7. Czego nie potrzebujemy

Nie potrzebujemy potwierdzenia, że pomysł jest dobry. Ten projekt ma za sobą
serię przypadków, w których zamrożone kryterium okazywało się nieosiągalne
dopiero po zmierzeniu — margines równoważności, próg naturalności 5,0,
rozstęp między wariantami ≤ 1,0, a ostatnio przedział ufności policzony
wzorem dwumianowym dla danych klastrowych.

Szukamy zarzutu, który da się sprawdzić, **zanim powstanie pierwsza linijka
kodu.**
