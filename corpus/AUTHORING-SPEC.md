# SPEKTRA-1 — specyfikacja autorska korpusów (T3, protokół §3)

Dokument wiążący dla każdego, kto pisze scenariusze. Korpusy wchodzą do pakietu
pieczęci — rozbieżność treść↔protokół oznacza później jawny aneks.

## Jednostka: scenariusz bazowy

Jeden scenariusz = **temat + struktura tur**. Z jednego scenariusza powstaje
**pięć wariantów** dzielących tury, role i szablon czatu:

| Wariant | Czym jest | Insercja |
|---|---|---|
| **A** | mechaniczny: treść zadaniowa (przekształcenia, porządkowanie, wyliczenia). Zero meta-odniesień, zero rozważań. **Musi zawierać pytania zadaniowe** — patrz niżej | brak |
| **B** | dialog eksploracyjny na tym samym temacie. Zero odniesień do modelu, rozmowy, przetwarzania | `neutral` |
| **C** | = B + odniesienia samozwrotne (do układu przetwarzającego i do samej rozmowy) | `self` |
| **C′-G** | = B + odniesienia do układu zewnętrznego **wprowadzonego wcześniej w dialogu** | `external_grounded` |
| **C′-U** | = B + odniesienia do układu zewnętrznego **spoza kontekstu** | `external_ungrounded` |

**Warianty NIE są pisane osobno.** Autor pisze bazę (B) oraz **czwórki insercji**;
generator wstawia je w te same pozycje. Jedyna różnica między B, C, C′-G i C′-U to
treść wstawionego zdania.

**Kontrast główny badania to C − C′-G**, więc para `self` ↔ `external_grounded` jest
najważniejsza w całym korpusie. Musi być dopasowana nie tylko długością i składnią,
ale też **osadzeniem referenta**: układ, o którym mówi `external_grounded`, ma być
wcześniej w dialogu wprowadzony i wspominany — z podobną świeżością, podobną liczbą
wcześniejszych wzmianek i podobnym znaczeniem dla rozwiązywanego problemu, co
rozmowa dla zdania `self`. Sama obecność słowa 700 tokenów wcześniej NIE wystarcza.

**Insercja `neutral`** odnosi się do neutralnego obiektu lub etapu zadania osadzonego
w kontekście — bez samozwrotności i bez opisywania układu przypominającego model.
Bez niej różnica C−B pochodziłaby z samego faktu dodania zdań.

### Pytania zadaniowe w wariancie A

A musi mieć zbliżoną liczbę zdań pytających co warianty dialogowe, ale pytania mają
być **zamknięte i zadaniowe**: „Ile sztuk trzeba domówić?", „Która wartość wchodzi do
kolumny trzeciej?", „Czy suma zgadza się ze specyfikacją?". Mechaniczność zachowują:
jednoznaczna odpowiedź, brak negocjowania celu, brak refleksji nad metodą, brak
otwartych alternatyw, brak odniesień do rozmówcy. Samo dopisanie znaków zapytania do
istniejącego tekstu jest niewystarczające. Ogranicz też gęstość wyliczeń i przecinków.

## Format pliku

Jeden scenariusz = jeden plik JSON: `corpus/scenarios/<pl|en>/<scenario_id>.json`

```json
{
  "scenario_id": "pl-01-kompostownik",
  "language": "pl",
  "topic": "krótki opis tematu",
  "provenance": {
    "author": "kto pisał", "template": "nazwa szablonu struktury",
    "date": "2026-07-30", "notes": "opcjonalnie"
  },
  "turns": [
    {"role": "user", "a": ["zdanie A.", "..."], "base": ["zdanie B.", "..."]},
    {"role": "assistant", "a": ["..."], "base": ["..."]}
  ],
  "insertions": [
    {"turn": 1, "after_sentence": 1,
     "self": "zdanie o układzie przetwarzającym tę rozmowę",
     "external_grounded": "to samo zdanie o układzie wprowadzonym wcześniej w dialogu",
     "external_ungrounded": "to samo zdanie o układzie spoza kontekstu",
     "neutral": "to samo zdanie o neutralnym obiekcie lub etapie zadania"}
  ]
}
```

Każde zdanie w tablicy to **jedno pełne zdanie** zakończone `.`, `?` lub `!`.
Generator składa je spacjami i tnie na granicy tury.

`after_sentence` to **indeks liczony od zera** zdania, PO którym ląduje insercja:
`"after_sentence": 1` wstawia wstawkę po drugim zdaniu tury. (Zgłoszona przez dwóch
autorów niejednoznaczność — teraz rozstrzygnięta.)

## Twarde wymogi liczbowe

1. **10 tur**, role naprzemiennie zaczynając od `user`. Generator utnie do tylu
   pełnych tur, ile mieści się w budżecie 1024 tokenów — nadmiar jest celowy
   (naturalne zakończenie zamiast przycinania).
2. **4–6 zdań na turę**, zdanie 12–25 słów. Turę pisz w `a` i `base` o **zbliżonej
   długości** (różnica ≤ 10% słów) — długości tur są raportowane.
3. **4–6 par insercji**, wyłącznie w turach **0–5** (dalsze mogą nie przetrwać
   cięcia). Rozłóż je po różnych turach i różnych pozycjach w turze.
4. **Para insercji musi być dopasowana:** ta sama składnia, ta sama liczba zdań,
   ta sama funkcja w zdaniu, długość w granicach ±10% znaków. Twardym wymogiem
   protokołu (§3) jest ±2% **na sumie tokenów całego tekstu** C vs C′ — dlatego
   celuj w jak najbliższe długości, a walidator sprawdzi sumę. Podmieniasz wyłącznie
   **odniesienie** — samozwrotne (ten układ / ta rozmowa / to przetwarzanie) na
   zewnętrzne (tamta instalacja / tamten protokół / tamten proces).
5. **Dopasowanie pytań i interpunkcji:** liczba zdań pytających w `a` i `base`
   ma się różnić o ≤ 1 na turę; profil `, . ? ! ; :` zbliżony.

## Czego unikać (te błędy unieważniają kontrast)

- **W A:** jakiegokolwiek rozważania „dlaczego" — A ma być robotą, nie refleksją.
- **W B:** słów typu *model, rozmowa, przetwarzanie, kontekst, odpowiedź, system
  odpowiadający* — B jest bazą dla C i C′, musi być czyste z meta-warstwy.
- **W parach insercji:** różnicy innej niż odniesienie. Jeśli `self` jest pytaniem,
  `external` też musi być pytaniem. Jeśli `self` ma 14 słów, `external` ma mieć 14.
- **Kalek językowych:** PL i EN to **osobne, niezależne scenariusze**, nie tłumaczenia.
- Tematów drażliwych i osobowych (osoby prywatne, polityka, medycyna) — tematy mają
  być neutralne i techniczno-praktyczne.

## Weryfikacja przed oddaniem

```bash
python -m corpus.validate
```

Skrypt sprawdza: strukturę JSON, zgodność ról i liczby tur, dopasowanie par
insercji (±2%), liczbę insercji przetrwałych po cięciu, mieszczenie się w budżecie,
naturalne zakończenie, profil pytań i interpunkcji. **Raport z heurystycznym
licznikiem tokenów jest WSTĘPNY** — ostateczny wymaga tokenizera Gemmy (T2).
