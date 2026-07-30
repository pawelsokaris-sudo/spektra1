# Środowisko pomiarowe SPEKTRA-1 — raport wykonania

**Zlecenie:** `ops/DEP-zlecenie-02-srodowisko.md` (STATUS: ZATWIERDZONE, zgoda Pawła 2026-07-30)
**Wykonał:** DEP (Claude Code w terminalu)
**Data:** 2026-07-30, 12:40–13:00
**Maszyna:** `maszyna-pomiarowa`
**Wynik:** wszystkie 7 kroków zaliczone. Krytyczne punkty potwierdzone:
`compute capability (12, 0)` ✓ · `bf16: True` ✓ · `hidden_states = 35` (34 warstwy + embedding) ✓ · lockfile w repo ✓

Jedno ustalenie wykracza poza listę kontrolną i wymaga decyzji przed T2 — sekcja
**„Ustalenie poza zleceniem: sterownik przelewa pamięć karty do RAM"** na końcu.

---

## 0. Test taniej wygody — SSH po nazwie hosta

```
$ ssh operator@maszyna-pomiarowa "echo OK"
Warning: Permanently added 'maszyna-pomiarowa' (ED25519) to the list of known hosts.
OK
(kod wyjścia: 0)

$ ssh operator@maszyna-pomiarowa.local "echo OK"
OK
```

**Działa — i to jest dobra wiadomość.** Oba warianty (`maszyna-pomiarowa` i `maszyna-pomiarowa.local`)
logują się poprawnie. Temat wędrującego adresu z DHCP przestaje mieć znaczenie: od teraz
łączymy się po nazwie, rezerwacja DHCP jest niepotrzebna. **Cała reszta tego zlecenia została
wykonana po nazwie hosta, nie po adresie IP** — czyli ta ścieżka jest przetestowana pod
obciążeniem, nie tylko jednym `echo`.

## Pre-flight (przed pierwszą zmianą)

```
C:\Users\operator\spektra1-env => nie istnieje (czysty start)
$ ollama ps
NAME    ID    SIZE    PROCESSOR    CONTEXT    UNTIL      (pusto — żaden model nie jest w VRAM)
$ nvidia-smi --query-gpu=memory.used,memory.total
1626 MiB, 16303 MiB                                      (tylko pulpit Windows)
Wolne miejsce na C:: 1506 GB
```

**Interpretacja:** katalog docelowy nie istniał, więc nie ryzykowaliśmy nadpisania czegokolwiek.
Ollama nie trzymała modelu w pamięci karty — warunek z „Uwagi operacyjnej" zlecenia spełniony
przed startem, bez zatrzymywania Ollamy.

## 1. Środowisko

```
$ python -m venv C:\Users\operator\spektra1-env
(bez wyjścia — sukces)

$ C:\Users\operator\spektra1-env\Scripts\python.exe --version
Python 3.14.4

$ C:\Users\operator\spektra1-env\Scripts\python.exe -m pip install --upgrade pip
Requirement already satisfied: pip in .\spektra1-env\Lib\site-packages (26.0.1)
Downloading pip-26.2-py3-none-any.whl (1.8 MB)
  Uninstalling pip-26.0.1: Successfully uninstalled pip-26.0.1
Successfully installed pip-26.2
```

**Interpretacja:** środowisko powstało na Pythonie 3.14.4 (jedynym na maszynie, zgodnie
z rekonesansem), pip podniesiony 26.0.1 → 26.2 **wewnątrz środowiska** — systemowy pip
nietknięty.

## 2. PyTorch pod Blackwell (sm_120)

```
$ ...\python.exe -m pip install torch==2.9.1+cu128 --index-url https://download.pytorch.org/whl/cu128
Collecting torch==2.9.1+cu128
  Downloading torch-2.9.1%2Bcu128-cp314-cp314-win_amd64.whl.metadata (29 kB)
Downloading torch-2.9.1%2Bcu128-cp314-cp314-win_amd64.whl (2880.8 MB)
Installing collected packages: mpmath, typing-extensions, sympy, setuptools, networkx,
  MarkupSafe, fsspec, filelock, jinja2, torch
Successfully installed MarkupSafe-3.0.3 filelock-3.29.0 fsspec-2026.4.0 jinja2-3.1.6
  mpmath-1.3.0 networkx-3.6.1 setuptools-78.1.0 sympy-1.14.0 torch-2.9.1+cu128
  typing-extensions-4.15.0
(kod wyjścia 0)
```

**Interpretacja:** weszło dokładnie to koło, które rekonesans wskazał jako jedyne możliwe —
`cp314-cp314-win_amd64` w wariancie cu128. Oba ograniczenia (Python 3.14 → torch ≥ 2.9;
Blackwell sm_120 → CUDA ≥ 12.8) są spełnione jednocześnie. Pobranie 2880,8 MB, bez błędów.

## 3. Reszta stosu

```
$ ...\python.exe -m pip install transformers accelerate numpy scipy pyarrow pandas safetensors
Successfully installed accelerate-1.14.0 annotated-doc-0.0.5 anyio-4.14.2 certifi-2026.7.22
  click-8.4.2 colorama-0.4.6 h11-0.16.0 hf-xet-1.5.2 httpcore-1.0.9 httpx-0.28.1
  huggingface-hub-1.25.1 idna-3.18 markdown-it-py-4.2.0 mdurl-0.1.2 numpy-2.5.1
  packaging-26.2 pandas-3.0.5 psutil-7.2.2 pyarrow-25.0.0 pygments-2.20.0
  python-dateutil-2.9.0.post0 pyyaml-6.0.3 regex-2026.7.19 rich-15.0.0 safetensors-0.8.0
  scipy-1.18.0 shellingham-1.5.4 six-1.17.0 tokenizers-0.22.2 tqdm-4.70.0
  transformers-5.14.1 typer-0.27.0 tzdata-2026.3
(kod wyjścia 0)
```

**Interpretacja:** wszystkie siedem żądanych pakietów miało gotowe koła dla Pythona 3.14 —
to nie było oczywiste (`pyarrow` i `scipy` często zostają w tyle za nową wersją Pythona,
i to był realny kandydat na „krok padł"). Nic nie trzeba było kompilować ze źródeł.
Zwracam uwagę na jedno: **`transformers` to wersja 5.14.1**, czyli linia 5.x. Argument
`dtype=` użyty w kroku 6 jest w niej poprawny (w 4.x nazywał się `torch_dtype`) — skrypty
pomiarowe muszą trzymać się tej konwencji, bo lockfile ją zamraża.

## 4. Lockfile (wchodzi do pieczęci)

Zamiast tworzyć plik na maszynie operatora maszyny (co wyszłoby **poza** zakres zmian ze zlecenia —
`pip freeze > requirements-lock.txt` zapisałby go w `C:\Users\operator\`, a nie w środowisku),
zrzuciłem wyjście przez SSH wprost do repo.

**Plik:** `requirements-lock.txt` w katalogu głównym repo, 43 linie.
**SHA-256 lockfile'a:** `e4c1f95420770a1ff731ea7611c7f17961d582ec04c2be54cb1787ec1552c624`

```
accelerate==1.14.0
annotated-doc==0.0.5
anyio==4.14.2
certifi==2026.7.22
click==8.4.2
colorama==0.4.6
filelock==3.29.0
fsspec==2026.4.0
h11==0.16.0
hf-xet==1.5.2
httpcore==1.0.9
httpx==0.28.1
huggingface_hub==1.25.1
idna==3.18
Jinja2==3.1.6
markdown-it-py==4.2.0
MarkupSafe==3.0.3
mdurl==0.1.2
mpmath==1.3.0
networkx==3.6.1
numpy==2.5.1
packaging==26.2
pandas==3.0.5
psutil==7.2.2
pyarrow==25.0.0
Pygments==2.20.0
python-dateutil==2.9.0.post0
PyYAML==6.0.3
regex==2026.7.19
rich==15.0.0
safetensors==0.8.0
scipy==1.18.0
setuptools==78.1.0
shellingham==1.5.4
six==1.17.0
sympy==1.14.0
tokenizers==0.22.2
torch==2.9.1+cu128
tqdm==4.70.0
transformers==5.14.1
typer==0.27.0
typing_extensions==4.15.0
tzdata==2026.3
```

**Interpretacja:** 43 pakiety, wszystkie przypięte do dokładnej wersji. Jedna uwaga do pieczęci:
`pip freeze` nie zapisuje **skąd** pochodzi `torch==2.9.1+cu128` — sam sufiks `+cu128` to jedyny
ślad indeksu `download.pytorch.org/whl/cu128`. Odtworzenie środowiska z tego pliku wymaga podania
tego indeksu ręcznie, więc powinien być zapisany w pakiecie pieczęci obok lockfile'a (albo
lockfile powinien dostać nagłówek `--index-url`). To jest do decyzji czatu prowadzącego.

## 5. Weryfikacja sprzętu i precyzji

```
torch 2.9.1+cu128 cuda 12.8
dostepna: True | NVIDIA GeForce RTX 5080
compute capability: (12, 0)
bf16: True
VRAM total GB: 15.92
```

**Interpretacja:** wszystkie cztery krytyczne punkty ze zlecenia potwierdzone. `compute
capability (12, 0)` jest dokładnie oczekiwaną wartością — torch widzi kartę jako Blackwell
i ma dla niej skompilowane jądra (gdyby koło było zbudowane pod starsze CUDA, dostalibyśmy
ostrzeżenie „no kernel image is available"; nie dostaliśmy). `bf16: True` domyka wymóg
protokołu §2 co do dtype forwardu.

## 6. Test wczytania modelu i ukrytych stanów (sedno T2)

```
Loading weights: 100%|##########| 883/883 [00:02<00:00, 396.68it/s]
klasa modelu: Gemma3ForConditionalGeneration
liczba elementow hidden_states: 35
ksztalt pojedynczego: (1, 10, 2560)
dtype: torch.bfloat16
VRAM zajete GB: 8.03
rewizja/commit: 093f9f388b31de276ce2de164bdc2081324b9767
```

**Interpretacja — cztery rzeczy się tu domykają:**

1. **35 elementów `hidden_states`** przy 34 blokach modelu. Zgadza się z oczekiwaniem L+1
   ze zlecenia i niezależnie z `config.json` w cache (`text_config.num_hidden_layers: 34`).
   Pierwszy element to embedding, kolejne 34 to wyjścia bloków.
2. **Wymiar 2560** to `text_config.hidden_size` — czyli dostajemy stany wieży **tekstowej**,
   nie wizyjnej (wieża SigLIP ma 1152 i 27 warstw). Dokładnie to, czego wymaga pomiar.
3. **`dtype: torch.bfloat16`** — forward faktycznie idzie w bf16, nie w cichym upcastie.
4. **Rewizja `093f9f38…`** zgadza się z nazwą katalogu snapshotu i z zawartością `refs/main`
   w cache. Model wczytał się z lokalnego cache, bez pobierania czegokolwiek z sieci.

Dwie uwagi. Po pierwsze, **`AutoModelForCausalLM` zadziałało**, ale zwróciło klasę
`Gemma3ForConditionalGeneration` (wariant multimodalny) — to poprawne zachowanie, bo `gemma-3-4b-it`
jest modelem obraz+tekst i klasa opakowuje w sobie wieżę tekstową. Dopisałem do skryptu jedną
linię `print(type(model).__name__)`, żeby to było w raporcie jawne — to jedyne odstępstwo od
kodu ze zlecenia i nie zmienia niczego w pomiarze. Po drugie, snapshot w cache **nie zawiera**
`preprocessor_config.json`, więc ścieżka obrazowa tego modelu nie jest na tej maszynie używalna.
Dla nas bez znaczenia (mierzymy tekst), ale warto to wiedzieć, gdyby manifest pieczęci miał
twierdzić, że snapshot jest kompletny — nie jest, jest kompletny **dla trybu tekstowego**.

## 7. Sumy kontrolne wag (do pieczęci)

**Snapshot:** `C:\Users\operator\.cache\huggingface\hub\models--google--gemma-3-4b-it\snapshots\093f9f388b31de276ce2de164bdc2081324b9767`
**Liczba snapshotów w cache:** 1 (brak niejednoznaczności — `refs/main` = `093f9f38…`)

```
added_tokens.json                     35 B  sha256=50b2f405ba56a26d4913fd772089992252d7f942123cc0a034d96424221ba946
config.json                          855 B  sha256=9059f680f4dbd1957f35cb44b9fdd6948f4792db7a7a35ee353ea42e68adf7ff
generation_config.json               215 B  sha256=fd9324becc53c4be610db39e13a613006f09fd6ef71a95fb6320dc33157490a3
model-00001-of-00002.safetensors 4961251752 B  sha256=eb5fd5e97ddd07b56778733e9653c07312529cb00980a318fc3e1c4e3b5a8f1f
model-00002-of-00002.safetensors 3639026128 B  sha256=fdde0e5aa5ced0fa203b3d50f4ab78168b7e3a3e08c6349f5cc9326666e1bb13
model.safetensors.index.json       90558 B  sha256=77f4b67de084c31c7bcd373b039908108eee6c6181607e6d53da730e5f0bc659
special_tokens_map.json              662 B  sha256=2f7b0adf4fb469770bb1490e3e35df87b1dc578246c5e7e6fc76ecf33213a397
tokenizer.json                  33384568 B  sha256=4667f2089529e8e7657cfb6d1c19910ae71ff5f28aa7ab2ff2763330affad795
tokenizer_config.json            1156999 B  sha256=bfe25c2735e395407beb78456ea9a6984a1f00d8c16fa04a8b75f2a614cf53e1
```

**Niezależne potwierdzenie sum:** HuggingFace nazywa pliki blobów ich własnym SHA-256. Nazwy
blobów w cache to `eb5fd5e97ddd07b5…` i `fdde0e5aa5ced0fa…` — czyli sumy, które policzyłem od
zera, zgadzają się z tym, co HuggingFace zapisał w momencie pobrania (2026-07-03). To jest
dowód, że wagi nie uległy uszkodzeniu ani podmianie przez te cztery tygodnie.

**Chat template.** Snapshot **nie zawiera** osobnego pliku `chat_template.jinja` — szablon
siedzi wewnątrz `tokenizer_config.json` jako pole `chat_template` (1532 znaki). Suma z samego
tekstu szablonu (UTF-8, bez opakowania JSON):

```
chat_template sha256 = 7de1c58e208eda46e9c7f86397df37ec49883aeece39fb961e0a6b24088dd3c4
```

### Gotowe wartości do `config.yaml` (pola TBD-RECON)

**Nie wpisałem ich sam** — `config.yaml` jest plikiem pieczętowanym, a wybór wariantu modelu
(4B vs większy) nie został formalnie domknięty w zleceniu 01. Poniżej blok gotowy do wklejenia,
jeśli czat prowadzący potwierdzi wariant 4B:

```yaml
model:
  hf_name: google/gemma-3-4b-it
  hf_revision: 093f9f388b31de276ce2de164bdc2081324b9767
  weights_sha256:
    model-00001-of-00002.safetensors: eb5fd5e97ddd07b56778733e9653c07312529cb00980a318fc3e1c4e3b5a8f1f
    model-00002-of-00002.safetensors: fdde0e5aa5ced0fa203b3d50f4ab78168b7e3a3e08c6349f5cc9326666e1bb13
    model.safetensors.index.json: 77f4b67de084c31c7bcd373b039908108eee6c6181607e6d53da730e5f0bc659
  tokenizer_files_sha256:
    tokenizer.json: 4667f2089529e8e7657cfb6d1c19910ae71ff5f28aa7ab2ff2763330affad795
    tokenizer_config.json: bfe25c2735e395407beb78456ea9a6984a1f00d8c16fa04a8b75f2a614cf53e1
    special_tokens_map.json: 2f7b0adf4fb469770bb1490e3e35df87b1dc578246c5e7e6fc76ecf33213a397
    added_tokens.json: 50b2f405ba56a26d4913fd772089992252d7f942123cc0a034d96424221ba946
  chat_template_sha256: 7de1c58e208eda46e9c7f86397df37ec49883aeece39fb961e0a6b24088dd3c4
```

Uwaga do pola `chat_template_sha256`: skoro szablon nie jest osobnym plikiem, trzeba zapisać
w protokole **czym dokładnie** jest ta suma (u mnie: SHA-256 samego tekstu szablonu w UTF-8,
wyciągniętego z pola `chat_template`). Bez tej definicji suma jest nieodtwarzalna.

---

## Ustalenie poza zleceniem: sterownik przelewa pamięć karty do RAM

To najważniejsza rzecz, jaką znalazłem, i nie było jej na liście kontrolnej. Po zaliczeniu
kroków 1–7 zmierzyłem dodatkowo realne zużycie pamięci przy **docelowym** budżecie 1024
tokenów (zlecenie wymagało tylko krótkiego tekstu) oraz sprawdziłem, czy zmieści się kontrola
fp32 z protokołu (§2, `fp32_control_fraction: 0.10`).

```
=== bf16, 1024 tokenów ===
liczba elementow hidden_states: 35
ksztalt ostatniego: (1, 1024, 2560) torch.bfloat16
same hidden_states zajmuja GB: 0.171
szczyt allocated GB: 8.83
szczyt reserved GB: 8.94
calkowity VRAM GB: 15.92

=== fp32, tylko 256 tokenów ===
fp32 na GPU: ZMIESCILO SIE, szczyt allocated GB: 16.43
fp32 dtype stanow: torch.float32
```

Szczyt **16,43 GB na karcie, która ma 15,92 GB**. To nie może się zmieścić fizycznie, więc
sprawdziłem hipotezę wprost — próbą alokacji świadomie większej niż pamięć karty:

```
calkowity VRAM GB: 15.92
alokacja 20 GB na GPU: PRZESZLA -> sterownik przelewa nadmiar do RAM (fallback wlaczony)
   allocated GB: 20.0
```

**Co to znaczy.** Sterownik NVIDIA na Windows ma włączony mechanizm „system memory fallback":
kiedy zabraknie pamięci karty, cicho dokłada pamięć systemową zamiast zgłosić błąd. Skutki są dwa,
i drugi jest poważniejszy niż pierwszy:

1. **Kontrola fp32 nie mieści się w karcie.** Model w fp32 to ~16 GB samych wag — nie ma
   szans przy 15,92 GB. Przeszła tylko dlatego, że przelała się do RAM, i była przez to
   wielokrotnie wolniejsza. Do rozważenia przez czat prowadzący: kontrolę fp32 policzyć
   **na CPU** (61 GB RAM, wolno ale poprawnie) albo świadomie zaakceptować przelewanie.
   Numerycznie fp32 na GPU z przelewaniem daje ten sam wynik — traci się tylko czas.
2. **Znika sygnał ostrzegawczy.** Bieg, który przekroczy pamięć karty, **nie zgłosi błędu** —
   po cichu zwolni. Dla protokołu, który pieczętuje warunki pomiaru, to znaczy, że „zmieściło
   się" przestaje być weryfikowalne przez sam fakt, że program nie padł. Zalecam twardą bramkę
   w kodzie pomiarowym: po każdym biegu sprawdzić `torch.cuda.max_memory_allocated()` względem
   progu (np. 14 GB) i przerwać, jeśli przekroczony. To zmiana wyłącznie w naszym repo, nie
   wymaga niczyjej zgody ani ruszania sterownika. Alternatywa — wyłączenie fallbacku w panelu
   NVIDIA — jest zmianą w systemie maszyny operatora maszyny i **wymagałaby nowej zgody**, więc jej nie
   ruszałem.

**Dobra wiadomość przy okazji:** właściwy pomiar w bf16 przy pełnym budżecie 1024 tokenów ma
szczyt 8,83 GB przy 15,92 GB dostępnych, a same ukryte stany to zaledwie 0,17 GB. Zapas jest
duży, docelowy pomiar nie zbliża się do progu przelewania.

---

## Kontrola zakresu zmian

Zlecenie zamknęło zakres trzema punktami. Weryfikacja po wykonaniu:

```
--- rozmiar srodowiska ---
C:\Users\operator\spektra1-env => 4,83 GB (36086 plikow)
--- cache HF: rozmiar i integralnosc blobow ---
cache HF razem => 8,97 GB          (identycznie jak przed zleceniem)
   blob eb5fd5e97ddd07b5... 4961251752 B
   blob fdde0e5aa5ced0fa... 3639026128 B
ref main = 093f9f388b31de276ce2de164bdc2081324b9767
--- zmienione w katalogu domowym w ostatnich 3h ---
   spektra1-env  (30.07.2026 12:50:28)
--- VRAM po testach ---
409 MiB
--- ollama ---
qwen2.5:14b / gemma4:latest / gemma3:12b   (3 modele, bez zmian)
```

**Interpretacja:** w katalogu domowym zmienił się **wyłącznie** `spektra1-env`. Cache
HuggingFace ma identyczny rozmiar i identyczne blobów co przed zleceniem — wagi nie zostały
ponownie pobrane ani ruszone. Ollama nietknięta (trzy modele jak były), VRAM wrócił do 409 MiB.
Nie zmieniano systemu, rejestru, PATH ani sterowników.

**Środowisko waży 4,83 GB, nie ~3 GB jak szacowało zlecenie** — różnica to bibliotekii CUDA
wewnątrz koła torcha. Przy 1,5 TB wolnego bez znaczenia, ale zapisuję, bo szacunek był
w treści zgody.

### Jedna rzecz, którą zrobiłem poza zakresem i cofnąłem

W pre-flighcie źle zacytowałem przekierowanie w komendzie `ollama ps`, przez co powstał
śmieciowy plik `C:\Users\operator\%` (53 B, sam nagłówek tabeli Ollamy, godzina 12:43).
To była zmiana **poza** zamkniętym zakresem. Wykryłem ją w kontroli końcowej, sprawdziłem
zawartość (potwierdzone: mój artefakt, nie plik operatora maszyny) i usunąłem:

```
usuniety: C:\Users\operator\%
--- kontrola koncowa: co w katalogu domowym zmienione w ostatnich 3h ---
   spektra1-env  (30.07.2026 12:50:28)
```

Zgłaszam to jawnie, bo zlecenie zamykało zakres zmian listą, a ja tę listę na chwilę
przekroczyłem — nawet jeśli skutek był zerowy i odwracalny.

## Rollback

Nadal ważny i wystarczający: `Remove-Item -Recurse -Force C:\Users\operator\spektra1-env`.
Poza tym katalogiem nic na maszynie nie zostało zmienione (plik `%` już usunięty), cache
HuggingFace jest nienaruszony, Ollama nietknięta.

## Co jest gotowe, a co czeka na decyzję

**Gotowe (T1 domknięte po stronie maszyny):** środowisko działa, karta rozpoznana jako
Blackwell z bf16, model wczytuje się z lokalnego cache i zwraca 35 warstw ukrytych stanów
w bf16, lockfile w repo, sumy kontrolne wag policzone i niezależnie potwierdzone.

**Czeka na czat prowadzący / Pawła:**
1. Potwierdzenie wariantu modelu (4B) → wtedy wklejenie bloku do `config.yaml`.
2. Definicja, czym jest `chat_template_sha256` (szablon nie jest osobnym plikiem).
3. Zapisanie w pakiecie pieczęci indeksu `download.pytorch.org/whl/cu128` — sam lockfile
   nie wystarczy do odtworzenia środowiska.
4. Decyzja o kontroli fp32: CPU czy świadome przelewanie do RAM.
5. Zgoda (lub nie) na bramkę pamięci w kodzie pomiarowym — moim zdaniem potrzebna, bo bez
   niej przekroczenie pamięci karty nie da żadnego sygnału.
