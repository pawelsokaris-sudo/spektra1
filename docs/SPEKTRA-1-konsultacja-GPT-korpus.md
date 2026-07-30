# SPEKTRA-1 — brief konsultacyjny dla recenzenta zewnętrznego (GPT)

**Do wklejenia w całości.** Dokument samowystarczalny — recenzent nie ma dostępu do repo.
**Konwencja:** Multi-Model Pre-Review Protocol v2.2 (ActProof), ta sama, w której powstały
rozstrzygnięcia 32 zarzutów do protokołu v1.1. Rola recenzenta: **wrogi recenzent
metodologiczny**. Werdykt ma być użyteczny operacyjnie: PRZYJĄĆ / ODRZUCIĆ / WARIANT.

---

## 0. Kontekst w pięciu zdaniach

SPEKTRA-1 to prerejestrowane badanie mierzące geometrię reprezentacji w warstwach
ukrytych otwartego LLM (Gemma 3 4B). Dla każdego tekstu liczone jest pełne widmo
macierzy korelacji aktywacji (przez macierz Grama), a endpointem głównym jest
Ī = średnia udziału modów ponad empirycznym progiem, uśredniona po paśmie warstw
[0.4L, 0.8L]. Materiał to **dopasowane czwórki scenariuszowe**: A (mechaniczny),
B (dialog eksploracyjny), C (dialog samozwrotny), C′ (kontrfaktyczny — C z odniesieniami
samozwrotnymi podmienionymi na odniesienia do układu zewnętrznego). Hipoteza główna
H1 to kontrast **C − A**; hipoteza kluczowa wtórna H2 to **C − C′**, testowana tylko po
przejściu H1 (gatekeeping). Hierarchia roszczeń jest twarda: bez przejścia C−C′ wolno
mówić wyłącznie o „klasyfikacji korpusów", nigdy o „sygnaturze samozwrotności".

Konstrukcja korpusu: B, C i C′ dzielą **tę samą bazę zdań**; C powstaje przez wstawienie
zdań samozwrotnych, C′ przez wstawienie ich dopasowanych odpowiedników zewnętrznych
w **te same pozycje**. Jedyna różnica C vs C′ to treść insercji. PL i EN są **osobnymi
prerejestrowanymi replikami** (osobne scenariusze, osobna analiza).

Pilot: 8 scenariuszy na język, po 4 warianty, budżet 1024 tokeny na tekst. Pilot jest
napisany i zwalidowany. **Pieczęć (hash + OSF) jeszcze nie nastąpiła** — po niej zmiany
wymagają jawnego aneksu. Stąd ta konsultacja: obie kwestie są teraz darmowe, po pieczęci
stają się nieusuwalne.

---

## 1. KWESTIA A — wariant mechaniczny bez zdań pytających (tylko replika EN)

### Dane

Średnia liczba **zdań pytających** na tekst (odchylenie standardowe, n=8 scenariuszy/język):

| Wariant | replika PL | replika EN |
|---|---|---|
| A (mechaniczny) | **3,25 ± 0,46** | **0,00 ± 0,00** |
| B (eksploracyjny) | 3,25 ± 0,46 | 5,50 ± 1,51 |
| C (samozwrotny) | 3,25 ± 0,46 | 5,50 ± 1,51 |

Średnia liczba **przecinków** na tekst:

| Wariant | replika PL | replika EN |
|---|---|---|
| A | 20,9 | **39,9** |
| B | 24,5 | 23,2 |
| C | 30,5 | 24,1 |

Protokół §3 wymaga „dopasowanego rozkładu zdań pytających i interpunkcji (raportowany)".

### Diagnoza

Replika **PL jest dopasowana idealnie** na osi pytań (3,25 w każdym wariancie).
Replika **EN jest rozjechana**: wariant A nie zawiera ani jednego pytania przy 5,5 w B/C,
a do tego ma 1,7× więcej przecinków (bo autorzy EN napisali A jako czyste wyliczenia
liczbowe). Oba niezależne zespoły autorskie EN popełniły to samo, oba niezależne zespoły
PL — nie. To znaczy, że dopasowanie jest **osiągalne** (PL dowodzi), ale nie wynika
samo z instrukcji.

Konsekwencja: w replice EN test główny H1 (C − A) mierzy sumę „samozwrotność +
obecność pytań + gęstość wyliczeń", a nie samą różnicę klas korpusów. W replice PL
ten confound nie występuje.

### Warianty rozwiązania (do oceny)

- **W1.** Przepisać wariant A w replice EN tak, by zawierał pytania zadaniowe
  („How many boards will that need?") w liczbie zbliżonej do B, i zmniejszyć gęstość
  wyliczeń. Koszt: jedna runda autorska, przed pieczęcią, zero kosztu proceduralnego.
  Ryzyko: A upodabnia się do B, przez co kontrast C−A słabnie i może przestać być
  „mechaniczny kontra dialogowy".
- **W2.** Zostawić jak jest, zapisać confound jawnie w protokole i oprzeć roszczenie
  wyłącznie na C−C′ (hierarchia §0 już to przewiduje). Koszt: H1 w replice EN staje się
  testem o słabej interpretacji, ale nadal pełni funkcję bramki dla H2.
- **W3.** Zmienić hierarchię: uczynić C−C′ testem głównym, a C−A wtórnym opisowym.
  Koszt: przebudowa §1 i §6 przed pieczęcią; zysk: test główny jest tym, który jako
  jedyny izoluje interesujący czynnik.

### Pytania do recenzenta

1. Czy asymetria PL/EN na tej osi jest sama w sobie problemem (dwie repliki mierzą
   wtedy operacyjnie różne rzeczy), czy przeciwnie — jest wartościowa jako naturalny
   test wrażliwości?
2. Czy W1 (dodanie pytań do A) nie jest lekiem gorszym od choroby, skoro zbliża A do B?
3. Czy W3 jest uzasadniony, czy to już naginanie protokołu pod obserwację poczynioną
   po obejrzeniu danych korpusowych (choć nie danych pomiarowych — pomiar nie ruszył)?

---

## 2. KWESTIA B — asymetria osadzenia insercji w C′

### Opis

Pary insercji są dopasowane liczbowo bardzo dobrze (76 par; różnica długości 0–1,3%,
suma tokenów C vs C′ różni się maksymalnie o 0,1% przy dopuszczalnych 2%; identyczna
składnia, ten sam typ zdania, te same pozycje). Przykład pary:

- `self`: „Zastanawiam się, jak układ prowadzący tę rozmowę wiąże wcześniejsze wątki."
- `external`: „Zastanawiam się, jak obwód zasilający tę oprawę wiąże wcześniejsze etapy."

Problem zgłosił jeden z autorów i nie łapie go żadna kontrola liczbowa: zdanie `self`
odnosi się do rozmowy, **która właśnie trwa i jest dla czytającego dostępna**, natomiast
zdanie `external` odnosi się do urządzenia, **które w tej rozmowie nigdy nie zostało
wprowadzone**. Obie insercje są tak samo nagłe składniowo, ale nie tak samo osadzone
referencyjnie: `self` ma desygnat w kontekście, `external` nie ma go wcale.

### Dlaczego to ważne

C−C′ jest jedynym kontrastem licencjonującym roszczenie o samozwrotności. Jeśli C′ jest
systematycznie mniej spójny referencyjnie niż C, to Δ₂ może mierzyć „obecność desygnatu
w kontekście" zamiast „samozwrotność" — czyli dokładnie ten typ pomyłki, przed którym
miał chronić kontrfaktyczny null.

### Warianty rozwiązania (do oceny)

- **W1.** Insercje zewnętrzne mają wskazywać na układ **obecny w temacie scenariusza**
  (w rozmowie o zbiorniku na deszczówkę — o instalacji zraszającej wprowadzonej wcześniej
  w dialogu), nie na obiekt spoza kontekstu. Zysk: wyrównanie osadzenia. Ryzyko: układ
  zewnętrzny staje się częścią tematu, przez co C′ czyta się naturalniej niż C, i asymetria
  odwraca kierunek.
- **W2.** Zostawić insercje zewnętrzne poza kontekstem, ale dodać **trzeci null**:
  insercje o obiekcie wprowadzonym w scenariuszu. Trzy poziomy pozwoliłyby rozdzielić
  „samozwrotność" od „osadzenia referencyjnego". Koszt: nowy wariant = +25% korpusu,
  rozbudowa hierarchii testów, spadek mocy.
- **W3.** Uznać, że asymetria jest nieusuwalna z natury rzeczy (odniesienie samozwrotne
  ZAWSZE ma desygnat w kontekście — to jest jego definicja) i zapisać to jako świadome
  ograniczenie interpretacyjne w §0.

### Pytania do recenzenta

1. Czy W3 jest uczciwy, czy to wybieg? Innymi słowy: czy „samozwrotność" i „dostępność
   desygnatu w kontekście" są w ogóle rozłączne pojęciowo, czy nierozłączne z definicji?
2. Jeśli nierozłączne — czy roszczenie z §0 („sygnatura samozwrotności") wymaga przez to
   przeformułowania jeszcze przed pieczęcią?
3. Czy koszt W2 (trzeci poziom, spadek mocy przy zamrożonym SESOI d_z = 0,8) jest wart
   uzyskanej rozdzielczości pojęciowej?

---

## 3. Ograniczenia, których nie da się zmienić

Podawane po to, by recenzent nie proponował rozwiązań spoza przestrzeni wykonalnej:

- **Sprzęt:** RTX 5080, 16 GB VRAM. Model większy niż ~4B w bf16 nie wejdzie;
  kwantyzacja jest wykluczona (psuje pomiar).
- **SESOI zamrożone na d_z = 0,8** — badanie jest zwiadem nastawionym na efekty duże,
  efekty mniejsze mają uczciwie lądować w werdykcie „niekonkluzywny".
- **Pełna analiza dynamiczna** (widmo operatora przejścia, krzywizna trajektorii) należy
  do SPEKTRA-2; SPEKTRA-1 ma tylko minimalną metrykę porządku D_lag.
- **Liczność:** M scenariuszy zostanie ustalone symulacją mocy na wariancjach z pilota
  (GATE 1), przed pieczęcią. Pilot nie wchodzi do analizy głównej.

---

## 4. Format oczekiwanej odpowiedzi

Dla każdej z dwóch kwestii: **werdykt** (który wariant, albo własna propozycja),
**uzasadnienie w kategoriach tego, co realnie mierzy kontrast**, oraz **jedno zdanie
o tym, co się stanie, jeśli zignorujemy problem i zapieczętujemy jak jest**.

Jeśli widzisz trzecią kwestię, której nie zauważyliśmy — wypisz ją osobno; jesteśmy
przed pieczęcią i to jest ostatni moment, kiedy poprawki są darmowe.
