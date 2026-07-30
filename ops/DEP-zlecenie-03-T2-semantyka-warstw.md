# DEP — Zlecenie 03: T2 (semantyka warstw) + dokładny tokenizer dla raportu T3

**Maszyna:** `maszyna-pomiarowa` — łączyć się **po nazwie hosta**, nie po IP (zweryfikowane w zleceniu 02).
**Środowisko:** `C:\Users\operator\spektra1-env\` (postawione w zleceniu 02, nie ruszać).
**Cel:** domknąć T2 (protokół §2) i uczynić raport dopasowania korpusu ostatecznym zamiast wstępnego.

> **Rozszerzenie zakresu zmian wobec zlecenia 02 — do świadomej wiadomości Pawła.**
> To zlecenie kopiuje na maszynę operatora maszyny **kod tego repo** (~2 MB tekstu, bez wag i bez
> środowiska) do nowego katalogu `C:\Users\operator\spektra1\`. Poza tym katalogiem nic się
> nie zmienia. Zgoda z 30.07 dotyczyła instalacji środowiska; kopiowanie własnego kodu
> jest jej naturalnym przedłużeniem (bez kodu środowisko nie ma czego uruchomić), ale
> odnotowuję to jawnie, zamiast uznać za oczywiste. Rollback bez zmian: skasowanie
> `spektra1-env` **i** `spektra1`.

## Krok 1 — pakiet z kodem na maszynę

Spakować z laptopa Pawła (uwaga: `--exclude` **przed** nazwą katalogu, inaczej wykluczenia
są ignorowane):

```
cd C:\Users\pawel\projects
tar -czf spektra1-code.tar.gz --exclude=.venv --exclude=.git --exclude=*.npy --exclude=__pycache__ spektra1
```

Sprawdzić rozmiar przed wysłaniem. **Wzorzec zmierzony 2026-07-30: 132 KB.** Jeśli wyjdzie
dziesiątki MB, wykluczenia nie zadziałały (klasyczna pułapka: `--exclude` po nazwie katalogu)
— naprawić, a nie wysyłać.

Przenieść na maszynę i rozpakować do `C:\Users\operator\` tak, aby powstało
`C:\Users\operator\spektra1\` z podkatalogami `pipeline/`, `corpus/`, `docs/`, `config.yaml`.

## Krok 2 — T2: weryfikacja semantyki warstw

```
cd C:\Users\operator\spektra1
C:\Users\operator\spektra1-env\Scripts\python.exe -m pipeline.layer_semantics
```

Skrypt zapisze `docs/layer_semantics.md` i `docs/layer_semantics.json`. Odpowiada na cztery
pytania, których protokół zabrania zgadywać:

1. Który element `hidden_states` jest embeddingiem, a które wyjściami bloków — sprawdzane
   **hookami** na modułach dekodera, nie założeniem.
2. Czy `hidden_states[-1]` jest brane przed końcową normalizacją.
3. Mapa uwagi lokalna/globalna per blok + skład pasma [0.4L, 0.8L].
4. Czy szablon czatu składany przez nasz generator korpusu zgadza się co do znaku
   z `tokenizer.apply_chat_template`. **To jest kontrola krytyczna** — rozbieżność oznacza,
   że mierzylibyśmy inny tekst niż zapisany w scenariuszach.

**Kod wyjścia 0** = indeksacja potwierdzona. **Kod 1** = wymaga decyzji, nie obchodzić.

### Krok 2a — tylko jeśli mapa typów bloków wyjdzie „nieznany"

Skrypt celowo nie zgaduje typu uwagi. Jeśli w raporcie wszystkie bloki mają `nieznany`,
zrzucić surowe pola konfiguracji, żebyśmy mogli wyprowadzić mapę:

```python
import json, transformers
from transformers import AutoConfig
c = AutoConfig.from_pretrained("google/gemma-3-4b-it",
                               revision="093f9f388b31de276ce2de164bdc2081324b9767")
t = getattr(c, "text_config", c)
for k in ("sliding_window", "sliding_window_pattern", "layer_types",
          "num_hidden_layers", "rope_local_base_freq", "rope_theta"):
    print(k, "=", getattr(t, k, "BRAK"))
print("transformers", transformers.__version__)
```

To jest odczyt, nic nie zmienia.

## Krok 3 — dokładny tokenizer dla raportu dopasowania (domknięcie T3)

Raport dopasowania korpusu jest dziś liczony **heurystycznie** (szacunek znaki/token),
więc nosi etykietę „WSTĘPNY". Na maszynie operatora maszyny jest prawdziwy tokenizer Gemmy, więc
możemy policzyć go dokładnie **bez przenoszenia plików tokenizera** (33 MB, licencja Google —
nie mogą trafić do publicznego repo pieczęci).

Podłączyć tokenizer ze snapshotu do naszego licznika:

```
mkdir C:\Users\operator\spektra1\corpus\.tokenizer
copy "C:\Users\operator\.cache\huggingface\hub\models--google--gemma-3-4b-it\snapshots\093f9f388b31de276ce2de164bdc2081324b9767\tokenizer.json" C:\Users\operator\spektra1\corpus\.tokenizer\
```

(`corpus/.tokenizer/` jest w `.gitignore` właśnie po to.) Następnie:

```
cd C:\Users\operator\spektra1
C:\Users\operator\spektra1-env\Scripts\python.exe -m corpus.validate
C:\Users\operator\spektra1-env\Scripts\python.exe -m corpus.report
```

Walidator powinien teraz napisać `licznik tokenow: DOKLADNY`, a raport przestać być wstępny.

**Uwaga: walidator może teraz zgłosić problemy, których nie było przy heurystyce** — bo
prawdziwe długości tokenowe różnią się od szacunku, zwłaszcza w polszczyźnie. To jest
oczekiwane i pożądane: po to ten krok robimy. **Nie poprawiać korpusu** — to robota
autorów. Wystarczy przekazać pełną listę problemów.

## Co odesłać

Skopiować z maszyny z powrotem do repo na laptopie Pawła:
- `docs/layer_semantics.md` i `docs/layer_semantics.json`
- `corpus/matching_report.md` (wersja z dokładnym licznikiem)
- pełne wyjście `corpus.validate`

Plus raport `ops/T2-semantyka-warstw.md` z surowym wyjściem każdego kroku i jednym zdaniem
interpretacji, w tym jawnie: liczba bloków, indeks embeddingu, werdykt o końcowej
normalizacji, skład pasma, wynik kontroli szablonu czatu.

**NIE kopiować** plików tokenizera ani wag na laptopa Pawła — mają zostać na maszynie
pomiarowej (licencja + rozmiar).

## Weryfikacja

Zlecenie zaliczone, gdy: `layer_semantics.md` istnieje i podaje indeksację, kontrola
szablonu czatu ma jednoznaczny werdykt, a `matching_report.md` mówi „DOKŁADNY".

Jeśli którykolwiek krok padnie — **STOP i raport**. Nie instalować niczego spoza środowiska
ze zlecenia 02, nie zmieniać ustawień sterownika, nie ruszać Ollamy ani cache HuggingFace.

## Rollback

`Remove-Item -Recurse -Force C:\Users\operator\spektra1` (kod) i, jeśli trzeba cofnąć całość,
także `C:\Users\operator\spektra1-env`. Cache HuggingFace i Ollama pozostają nietknięte.

## Kontekst techniczny (żeby nie tracić czasu na zaskoczenia)

- `transformers` to linia **5.x** — argument nazywa się `dtype=`, nie `torch_dtype=`.
- `AutoModelForCausalLM` zwraca `Gemma3ForConditionalGeneration` (model obraz+tekst).
  Skrypt szuka bloków dekodera w kilku miejscach zagnieżdżenia; jeśli nie znajdzie,
  podniesie czytelny błąd zamiast zgadywać.
- Model wczytuje się z lokalnego cache, nic nie jest pobierane z sieci.
- Bramka pamięci (`pipeline/memory_guard.py`) nie dotyczy T2 — to krótka sonda.
