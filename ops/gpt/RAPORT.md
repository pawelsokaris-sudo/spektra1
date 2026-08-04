# Raport wykonania pakietu GPT

**Data:** 2026-08-04  
**Zakres zapisu:** wyłącznie `ops/gpt/`  
**Commit / push / zmiana gałęzi:** nie wykonywano

## Wynik

Powstały oba wymagane wytwory:

1. `pilot-pl.html` — samowystarczalny polski pilot z pięcioma parami.
2. `pilot-en.html` — samowystarczalny angielski pilot z pięcioma parami.
3. `referenty-obliczeniowe.md` — 24 propozycje referentów wraz z pełnymi zdaniami, długościami i uzasadnieniami.

Dołączono `verify_outputs.py`, lokalny walidator kontraktu, oraz `PLAN.md`.

## Pilot: kontrakt i zachowanie

Agregat: `TimingPilotSession`.

Stany:

- `consent` — stan początkowy;
- `pair_active` — pięć kolejnych, losowanych par;
- `debrief` — pytanie o zauważoną regułę i zmęczenie 1–5;
- `completed` — stan finalny z JSON-em i dowodem operacji;
- `abandoned` — stan finalny emitowany przy zamknięciu rozpoczętej sesji.

Każde przejście tworzy event zgodny z minimalnym Event Envelope: identyfikatory eventu, agregatu i korelacji, poprzedni i nowy stan, typ aktora oraz timestamp. JSON zawiera:

- czasy każdej pary i czas całkowity;
- liczbę powrotów do kontekstu;
- kolejność wyświetlenia;
- przypisanie zdań źródłowych do stron A/B;
- szerokość ekranu;
- odpowiedzi i debrief;
- pełną historię eventów.

Wskaźnik powrotu do kontekstu jest operacyjnie zdefiniowany jako ponowne pojawienie się co najmniej 25% bloku kontekstu po tym, gdy uczestnik zobaczył co najmniej 35% bloku odpowiedzi. To mierzy rzeczywisty powrót przez przewinięcie, nie ruchy kółka lub dotyku bez zmiany widoku.

Losowanie używa `crypto.getRandomValues` i odrzucania wartości spoza wielokrotności zakresu, dzięki czemu nie wprowadza biasu modulo. Kolejność zdań A/B jest losowana osobno dla każdej pary.

## Rozstrzygnięcie sprzeczności w briefie

Tekst zgody podany w pakiecie mówi o 10 pytaniach, ale wymaganie techniczne nakazuje dwa oddzielne pliki po 5 par i zakazuje mieszania języków. W każdym pliku zgoda mówi zatem prawdziwie o **5 pytaniach**. Pozostała treść zgody zachowuje sens i wszystkie zakazy ujawniania hipotezy.

## Referenty obliczeniowe

Dokument zawiera 12 propozycji angielskich i 12 polskich. Preferowane ±2 znaki na poziomie samej frazy spełnia 20 kandydatów. Jawnie oznaczono:

- `pl-24-studnia-kopana` — niewykonalne w ±2 znakach; naturalne `ten pomiar poziomu` ma +5 znaków;
- `pl-05-przetwory` — kandydat warunkowy `tym pomiarze` ma −3 znaki i wymaga sprawdzenia jednoznaczności;
- `pl-22-wedzarnia-ryb` oraz `pl-23-piec-chlebowy` — naturalne kandydatury mają odpowiednio −3 i +3 znaki, więc wymagają szczególnej kontroli pełnego równania.

Nie zmieniono korpusu. Tokenów i pełnego równania sześciu wariantów nie można uczciwie zatwierdzić na podstawie samych materiałów pakietu; to pozostaje zadaniem istniejącego walidatora korpusu.

## Weryfikacja

Wykonano:

- kontrolę kontraktu obu HTML-i: po 5 par, cztery odpowiedzi w wymaganej kolejności, wszystkie wymagane pola JSON, lokalne losowanie i kopiowanie;
- kontrolę 24 unikalnych sekcji referentów oraz kompletności czterech pól w każdej;
- maszynowe przeliczenie deklarowanych długości fraz znak po znaku;
- kompilację składni osadzonego JavaScriptu obu plików przez Node.js — oba bez błędu składni.

Pełnego klikanego testu w przeglądarce aplikacji nie wykonano: polityka bezpieczeństwa tej przeglądarki blokuje nawigację do lokalnych adresów `file://`. Blokady nie obchodzono serwerem. Przed użyciem z uczestnikiem należy ręcznie otworzyć oba pliki dwuklikiem i przejść jedną pełną sesję na telefonie oraz komputerze.

## Zastrzeżenia przed włączeniem do badania

1. Uruchomić istniejący walidator korpusu na 24 propozycjach: ±10% znaków całego wariantu, ±2% tokenów i reguła określnika.
2. Przeprowadzić ręczny smoke test obu HTML-i w co najmniej dwóch przeglądarkach, w tym mobilnej.
3. Potwierdzić decyzję metodologiczną, czy licznik powrotów oparty o widoczność bloków jest wystarczający. Jest uczciwy i prosty, ale nie odróżnia powrotu w celu ponownego czytania od przypadkowego przewinięcia.
4. Nie scalać automatycznie kandydatów warunkowych i przekraczających ±2 znaki.
