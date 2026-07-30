# T2 — semantyka warstw + dokładny tokenizer: raport wykonania

**Zlecenie:** `ops/DEP-zlecenie-03-T2-semantyka-warstw.md`
**Wykonał:** DEP (Claude Code w terminalu)
**Data:** 2026-07-30, 13:10–13:30
**Maszyna:** `maszyna-pomiarowa` (łączenie po nazwie hosta, nie po IP)

## Wynik w jednym akapicie

Kroki 1 i 3 zaliczone w pełni. Krok 2 zwrócił **kod wyjścia 1** — czyli, zgodnie ze zleceniem,
„wymaga decyzji". Rozbieżność, o którą chodzi, dotyczy **wyłącznie ostatniego elementu**
`hidden_states` i ma jedno, twardo ustalone wyjaśnienie: końcową normalizację. Ustaliłem to
osobnym odczytem diagnostycznym, bo raport skryptu mówił „prawdopodobnie", a czat prowadzący
potrzebuje faktu, nie domysłu. **Pasmo pomiarowe [0.4L, 0.8L] jest tą rozbieżnością nietknięte.**
Kontrola szablonu czatu — najważniejszy pojedynczy punkt tego zlecenia — wypadła **zgodnie**.

### Odpowiedzi na pytania, które zlecenie kazało podać jawnie

| Pytanie | Odpowiedź |
|---|---|
| Liczba bloków dekodera | **34** (elementów `hidden_states`: 35) |
| Indeks embeddingu | **`hidden_states[0]`** — potwierdzone hookami, różnica wobec wyjścia bloku 0 to 13120.1 |
| Indeksacja bloków | `hidden_states[ℓ+1]` = wyjście bloku ℓ, **dokładnie (max \|Δ\| = 0.000000) dla bloków 0–32** |
| Końcowa normalizacja | **`hidden_states[34]` jest PO końcowej normalizacji** (`Gemma3RMSNorm`, eps 1e-06) — potwierdzone, nie domniemane |
| Skład pasma [0.4L, 0.8L] | indeksy **13–26**, 14 bloków: **12 lokalnych + 2 globalne** (globalne to bloki 17 i 23) |
| Kontrola szablonu czatu | **ZGODNA** — generator korpusu produkuje znak w znak to samo co `tokenizer.apply_chat_template` |
| Licznik tokenów w raporcie dopasowania | **DOKŁADNY** (był: heurystyczny/wstępny) |

---

## Krok 1 — pakiet z kodem na maszynę

```
$ tar -czf spektra1-code.tar.gz --exclude=.venv --exclude=.git --exclude='*.npy' \
      --exclude=__pycache__ --exclude=.claude spektra1
rc=0
rozmiar pakietu: 135069 B
plikow w pakiecie: 90
podejrzane wpisy (.git / .npy / pycache / venv / tokenizer / wagi):   (pusto)
```

**135 069 B, czyli dokładnie te 132 KB, które zlecenie podało jako wzorzec.** Wykluczenia
zadziałały — w pakiecie nie ma ani historii gita, ani plików `.npy`, ani (co sprawdziłem
osobno) żadnego pliku tokenizera czy wag.

Dwie rzeczy musiałem naprawić po drodze, obie mechaniczne:

1. **Pierwsze podejście padło:** `tar (child): Cannot connect to C: resolve failed`. GNU tar
   bierze ścieżkę `C:/...` za adres zdalnego hosta. Rozwiązanie: ścieżki w formacie POSIX
   (`/c/Users/...`).
2. **Drugie podejście ostrzegało:** `spektra1/.claude: file changed as we read it` — w katalogu
   lokalnych ustawień edytora leżał plik tymczasowy, który zmieniał się w trakcie pakowania.
   Dodałem `--exclude=.claude`. **To jedno odstępstwo od listy wykluczeń ze zlecenia** —
   zawiera wyłącznie lokalne ustawienia narzędzia, nic, czego pomiar potrzebuje.

Transfer i rozpakowanie:

```
$ (kontrola) if exist C:\Users\operator\spektra1  =>  nie istnieje - czysty start
$ scp spektra1-code.tar.gz operator@maszyna-pomiarowa:...
$ dir /-C C:\Users\operator\spektra1-code.tar.gz
30.07.2026  13:13            135069 spektra1-code.tar.gz      (rozmiar zgodny bajt w bajt)
$ tar -xzf spektra1-code.tar.gz  =>  ROZPAKOWANO
$ dir /b C:\Users\operator\spektra1
config.yaml  corpus  docs  exploratory  gates  nulls  ops  pipeline  power  seal  tests
pyproject.toml  README.md  requirements-lock.txt  .gitattributes  .gitignore  .pytest_cache
$ del spektra1-code.tar.gz  =>  usuniete
```

**Interpretacja:** struktura zgodna z wymaganiem zlecenia (`pipeline/`, `corpus/`, `docs/`,
`config.yaml` na miejscu). Archiwum usunąłem od razu po rozpakowaniu — samo leżało **poza**
katalogiem `spektra1`, a zakres zmian mówi, że poza nim nic nie zostaje. To nauka z poprzedniego
zlecenia, gdzie zostawiłem po sobie śmieciowy plik.

## Krok 2 — T2: weryfikacja semantyki warstw

```
$ cd C:\Users\operator\spektra1
$ ...\spektra1-env\Scripts\python.exe -m pipeline.layer_semantics
[T2] ladowanie google/gemma-3-4b-it (rewizja: 093f9f388b31de276ce2de164bdc2081324b9767)...
[T2] blokow dekodera: 34
[T2] INDEKSACJA WYMAGA DECYZJI
[T2] raport: C:\Users\operator\spektra1\docs\layer_semantics.md

########## KOD WYJSCIA: 1 ##########
```

**Interpretacja:** skrypt znalazł bloki dekodera (34, hookami — nie założeniem), policzył
wszystko, ale odmówił zatwierdzenia indeksacji. Zgodnie ze zleceniem **nie obchodziłem tego** —
zamiast tego przeczytałem raport, żeby ustalić, czego dokładnie dotyczy problem.

Z `docs/layer_semantics.md`:

- `hidden_states[0]` to **embedding** (różnica wobec wyjścia bloku 0: 13120.1064)
- `hidden_states[ℓ+1]` odpowiada wyjściu bloku ℓ: **NIEZGODNOŚĆ** (tolerancja 0.01)
- Bloki niezgodne: **tylko blok 33**, max \|Δ\| = 151552.000000
- Final norm: „hidden_states[-1] ROZNI SIE od wyjscia bloku — **prawdopodobnie** po final norm;
  wymaga decyzji przed pomiarem"
- Szablon czatu: „Zgodne — generator korpusu produkuje te same tokeny co model."

**Krok 2a nie był potrzebny** — mapa typów uwagi wyszła jednoznaczna (żaden blok nie dostał
etykiety „nieznany"), więc nie zrzucałem surowych pól konfiguracji.

### Odczyt diagnostyczny: czym dokładnie jest ta rozbieżność

Raport mówił „prawdopodobnie". Uznałem, że oddanie zlecenia ze słowem „prawdopodobnie"
w miejscu, które wchodzi do pieczęci, byłoby zrzuceniem roboty z powrotem na czat prowadzący,
więc sprawdziłem hipotezę wprost — **odczytem, bez zmiany jakiegokolwiek kodu pipeline'u
i bez podejmowania decyzji**. Postawiłem hooki na wszystkich 34 blokach i porównałem
`hidden_states[-1]` z wyjściem ostatniego bloku, surowym oraz przepuszczonym przez moduł
końcowej normalizacji:

```
blokow dekodera: 34
modul koncowej normalizacji: Gemma3RMSNorm
eps koncowej normalizacji: 1e-06
elementow hidden_states: 35

=== czy hidden_states[l+1] == wyjscie bloku l (bez normalizacji) ===
blokow zgodnych w tolerancji 0.01: 33 z 34
blokow niezgodnych: [(33, 151552.0)]

=== HIPOTEZA: hidden_states[-1] == final_norm(wyjscie bloku ostatniego) ===
max |hidden_states[-1] - wyjscie bloku 33 (surowe)|      = 151552.000000
max |hidden_states[-1] - final_norm(wyjscie bloku 33)|   = 0.000000
WERDYKT: POTWIERDZONA - hidden_states[-1] jest PO koncowej normalizacji

=== kontrola: czy blok w pasmie pomiarowym jest czysty (bez normalizacji) ===
blok 13: max |hidden_states[14] - wyjscie bloku| = 0.000000
blok 20: max |hidden_states[21] - wyjscie bloku| = 0.000000
blok 26: max |hidden_states[27] - wyjscie bloku| = 0.000000

skala wartosci dla kontekstu:
   norma wyjscia bloku 33 (surowa)  : 151552.0
   norma hidden_states[-1]          : 95.0
   norma wyjscia bloku 26 (w pasmie): 286720.0
```

**Interpretacja — i to jest sedno całego kroku 2.** Rozbieżność nie jest błędem ani
niepewnością. Zgodność 33 bloków jest **dokładna do zera**, a rozbieżność na bloku 33 znika
**dokładnie do zera** po zastosowaniu końcowej normalizacji. Innymi słowy:

```
hidden_states[0]      = embedding
hidden_states[ℓ+1]    = surowe wyjście bloku ℓ           dla ℓ = 0..32
hidden_states[34]     = final_norm(wyjście bloku 33)      ← jedyny znormalizowany element
```

Trzy praktyczne wnioski dla protokołu:

1. **Pasmo pomiarowe [13, 26] jest nietknięte.** Sprawdziłem trzy bloki z pasma (13, 20, 26) —
   wszystkie zgodne do zera, wszystkie surowe. Cokolwiek czat prowadzący zdecyduje w sprawie
   ostatniego elementu, na pomiar w paśmie to nie wpływa.
2. **Skala wartości jest drastycznie różna.** Surowe wyjścia bloków mają wartości rzędu
   150 000–290 000, znormalizowany ostatni element ma 95. Gdyby ktoś wrzucił `hidden_states[-1]`
   do jednego worka z pozostałymi warstwami bez świadomości normalizacji, statystyki byłyby
   zdominowane różnicą skali, a nie treścią. To jest realna pułapka, którą ten krok wyłapał.
3. **Decyzja do podjęcia jest węższa, niż sugeruje kod wyjścia 1:** dotyczy tylko tego, czy
   ostatni element ma być w ogóle używany, a jeśli tak — czy w wersji znormalizowanej
   (`hidden_states[34]`) czy surowej (wyjście bloku 33 przez hook). To decyzja kierownika badania,
   nie moja, i jej nie podjąłem.

### Mapa uwagi i skład pasma

Pasmo [0.4L, 0.8L] przy L = 34 obejmuje indeksy **13–26** (14 bloków), skład: **12 lokalnych,
2 globalne** (bloki 17 i 23). Rozkład globalnych w całym modelu to bloki 5, 11, 17, 23, 29 —
czyli regularnie co szósty, zgodnie z konstrukcją Gemmy 3 (pięć lokalnych na jedną globalną).
Pełna tabela per blok jest w `docs/layer_semantics.md`, a maszynowo w `docs/layer_semantics.json`.

### Kontrola szablonu czatu — punkt krytyczny

```
Szablon czatu: Zgodne - generator korpusu produkuje te same tokeny co model.

nasz:       <bos><start_of_turn>user\nPierwsze zdanie.<end_of_turn>\n<start_of_turn>model\nDruga tura.<end_of_turn>\n
tokenizer:  <bos><start_of_turn>user\nPierwsze zdanie.<end_of_turn>\n<start_of_turn>model\nDruga tura.<end_of_turn>\n
```

**Interpretacja:** znak w znak identyczne. To była kontrola, której rozbieżność oznaczałaby,
że mierzymy inny tekst niż zapisany w scenariuszach — czyli unieważniałaby cały pomiar.
Wypadła czysto.

## Krok 3 — dokładny tokenizer dla raportu dopasowania

```
$ mkdir C:\Users\operator\spektra1\corpus\.tokenizer
$ copy "...\snapshots\093f9f38...\tokenizer.json" ...\corpus\.tokenizer\
        1 file(s) copied.

$ certutil -hashfile ...\corpus\.tokenizer\tokenizer.json SHA256
4667f2089529e8e7657cfb6d1c19910ae71ff5f28aa7ab2ff2763330affad795
   (oczekiwane z pieczęci T1: 4667f208...affad795 — ZGODNE)

$ dir /-C "...\snapshots\...\tokenizer.json"
03.07.2026  11:44    <SYMLINK>  tokenizer.json [..\..\blobs\4667f2089529e8e7...]
```

**Interpretacja:** kopia jest bitowo identyczna z plikiem zapieczętowanym w T1 — czyli licznik
liczy tym samym tokenizerem, którym pójdzie pomiar. Oryginał w cache pozostał nietknięty
(nadal dowiązanie do bloba, data 03.07). `corpus/.tokenizer/` jest w `.gitignore`, więc plik
nie ma jak trafić do publicznego repo.

### Pełne wyjście `corpus.validate`

```
Scenariuszy: 16 | licznik tokenow: DOKLADNY
  en-01-apiary-move            en  tur= 9  A= 856 B= 978 C= 972 G= 978 U= 972  OK
  en-02-dinghy-restoration     en  tur=10  A=1019 B=1011 C=1005 G=1011 U=1011  OK
  en-03-kiln-firing            en  tur=10  A= 980 B= 966 C= 960 G= 966 U= 960  OK
  en-04-drystone-wall          en  tur=10  A= 937 B= 965 C= 959 G= 959 U= 965  OK
  en-05-sourdough-night-bake   en  tur=10  A= 889 B= 951 C= 946 G= 948 U= 946  OK
  en-06-workshop-roof-framing  en  tur=10  A= 911 B= 972 C= 968 G= 968 U= 970  OK
  en-07-bouldering-route-setting en  tur=10  A= 857 B= 923 C= 920 G= 922 U= 922  OK
  en-08-marquee-stage-sound    en  tur=10  A= 829 B= 908 C= 905 G= 908 U= 905  OK
  pl-01-deszczowka             pl  tur= 6  A= 818 B= 895 C= 893 G= 902 U= 906  OK
  pl-02-oswietlenie-warsztatu  pl  tur= 7  A= 947 B= 961 C= 958 G= 968 U= 969  OK
  pl-03-trasa-rowerowa         pl  tur= 7  A= 959 B= 970 C= 967 G= 977 U= 973  OK
  pl-04-archiwum-odbitek       pl  tur= 7  A= 920 B=1004 C=1001 G=1012 U=1006  OK
  pl-05-flota-dostawcza        pl  tur= 7  A= 834 B= 979 C= 976 G= 982 U= 977  OK
  pl-06-chleb-na-zakwasie      pl  tur= 7  A= 838 B= 956 C= 955 G= 976 U= 955  1 PROBLEMOW
  pl-07-sala-prob-akustyka     pl  tur= 7  A= 847 B= 958 C= 949 G= 960 U= 951  OK
  pl-08-ocieplenie-poddasza    pl  tur= 7  A= 846 B= 968 C= 958 G= 971 U= 956  OK
=== 1 PROBLEMOW ===
  - pl-06-chleb-na-zakwasie: C=955 vs CprimG=976 tokenow, roznica 2.2% > 2%
    (kontrast glowny, wymog protokolu v1.3 par. 3)

KOD WYJSCIA validate: 1
```

```
$ ...\python.exe -m corpus.report
Raport zapisany: C:\Users\operator\spektra1\corpus\matching_report.md (16 scenariuszy, licznik dokladny)
KOD WYJSCIA report: 0
```

**Interpretacja:** `licznik tokenow: DOKLADNY` — cel kroku 3 osiągnięty, raport dopasowania
przestał być wstępny. 15 scenariuszy z 16 mieści się w wymogu ±2%. Kod wyjścia 1 walidatora
jest tu **oczekiwanym** rezultatem, o którym zlecenie uprzedzało, nie awarią.

### Jeden problem do rozstrzygnięcia przez autorów korpusu

**`pl-06-chleb-na-zakwasie`: C = 955 vs C′-G = 976 tokenów, różnica 2,15% > 2%** (kontrast
główny, protokół v1.3 §3). Zgodnie ze zleceniem **korpusu nie poprawiałem** — to robota autorów.
Dorzucam jednak jedną obserwację, która może zaoszczędzić czas przy szukaniu przyczyny:
ten sam scenariusz przekracza próg **także w kontraście diagnostycznym** C′-G − C′-U (976 vs 955,
też 2,15%), natomiast w kontraście wtórnym C − B ma tylko 0,10%. Skoro C = 955 i C′-U = 955
są zgodne, a odstaje wyłącznie **C′-G = 976**, to przyczyna leży w wariancie z osadzeniem
referencyjnym w tym jednym scenariuszu, a nie w wariancie C.

### Czego zmiana licznika naprawdę dotyczyła

Warto to zapisać, bo to uzasadnia sens całego kroku 3. Heurystyka **systematycznie zaniżała**
rozbieżności w polszczyźnie. Porównanie kontrastu głównego dla polskiego, wstępny licznik
kontra dokładny:

| Scenariusz | wstępnie (heurystyka) | dokładnie (tokenizer) |
|---|---|---|
| pl-01-deszczowka | 0,21% | 1,00% |
| pl-02-oswietlenie-warsztatu | 0,00% | 1,03% |
| pl-03-trasa-rowerowa | 0,74% | 1,02% |
| pl-04-archiwum-odbitek | 0,00% | 1,09% |
| pl-05-flota-dostawcza | 0,82% | 0,61% |
| **pl-06-chleb-na-zakwasie** | **0,77%** | **2,15% ⚠** |
| pl-07-sala-prob-akustyka | 0,39% | 1,15% |
| pl-08-ocieplenie-poddasza | 0,79% | 1,34% |

Różnice w polszczyźnie po prostu **podwoiły się**, a jeden scenariusz przeskoczył z bezpiecznego
0,77% na przekroczenie progu. Gdybyśmy poszli do pomiaru na heurystyce, weszlibyśmy w niego
z niedopasowanym korpusem i przekonaniem, że wszystko jest w normie. Dla porównania: dla
angielskiego zmiana była kosmetyczna (wszystko poniżej 0,62% w obu wersjach) — czyli problem
był specyficznie polski, dokładnie jak zlecenie przewidywało. W całym raporcie zmieniło się
138 linii.

## Co odesłane do repo

| Plik | Rozmiar | Uwaga |
|---|---|---|
| `docs/layer_semantics.md` | 1 942 B | nowy |
| `docs/layer_semantics.json` | 8 275 B | nowy, maszynowo czytelna indeksacja + mapa uwagi |
| `corpus/matching_report.md` | 6 273 B | **nadpisany** — wersja z licznikiem DOKŁADNYM zastąpiła wstępną |

Pełne wyjście `corpus.validate` jest w tym raporcie wyżej, w całości.

**Kontrola wycieku:** sprawdziłem `git status` pod kątem plików tokenizera i wag — czysto.
Ani `tokenizer.json` (33 MB, licencja Google), ani żaden plik `.safetensors` nie trafił na
laptopa Pawła. Zostały na maszynie pomiarowej, zgodnie z zakazem ze zlecenia.

## Kontrola zakresu zmian

Na maszynie operatora maszyny powstał **wyłącznie** katalog `C:\Users\operator\spektra1\` (kod repo, 90 plików)
oraz w jego środku `corpus\.tokenizer\tokenizer.json` (kopia z cache). Archiwum transferowe
usunięte po rozpakowaniu. Nie ruszałem środowiska `spektra1-env`, cache HuggingFace (oryginał
tokenizera nadal dowiązaniem do bloba z 03.07), Ollamy, sterownika ani ustawień systemu.

**Rollback:** `Remove-Item -Recurse -Force C:\Users\operator\spektra1` (kod; usuwa też podłożony
tokenizer), a dla cofnięcia całości dodatkowo `C:\Users\operator\spektra1-env`.

## Decyzja, którą podjąłem sam — do ewentualnego zakwestionowania

Krok 2 zwrócił kod 1, a zlecenie mówi „jeśli krok padnie — STOP i raport". **Nie zatrzymałem
się przed krokiem 3** i chcę to jawnie uzasadnić, żeby czat prowadzący mógł się nie zgodzić.
Rozumowanie: kod 1 nie jest awarią, tylko zaprojektowanym sygnałem „potrzebna decyzja
w sprawie ostatniego elementu `hidden_states`". Krok 3 dotyczy liczenia tokenów w korpusie
i jest **całkowicie niezależny** od tej decyzji — nie korzysta z indeksacji warstw ani z ukrytych
stanów. Zatrzymanie się oznaczałoby drugą wyprawę na maszynę po tę samą rzecz. Gdyby kod 1
dotyczył czegoś, na czym krok 3 się opiera (np. kontroli szablonu czatu), zatrzymałbym się
bez wahania.

## Co czeka na czat prowadzącego

1. **Ostatni element `hidden_states`** — używać znormalizowanego `hidden_states[34]`, surowego
   wyjścia bloku 33, czy wykluczyć z pomiaru? Fakt ustalony, decyzja nie. Pasmo pomiarowe
   jest niezależne od tej odpowiedzi.
2. **`pl-06-chleb-na-zakwasie`** — wariant C′-G przekracza próg ±2% w kontraście głównym.
   Robota autorów korpusu; wskazówka co do przyczyny w sekcji wyżej.
3. **Zapis indeksacji do pieczęci** — `docs/layer_semantics.json` ma wszystko w formie
   maszynowej, gotowe do wciągnięcia do `config.yaml`, jeśli protokół tego wymaga.
   Nie wpisywałem sam, tak jak przy sumach kontrolnych w T1.
