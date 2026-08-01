# SPEKTRA-1 — kwalifikacja sprzętu. Instrukcja DLA AGENTA (Claude Code)

**Czytasz to, bo masz przeprowadzić kwalifikację maszyny pod replikację
prerejestrowanego badania naukowego.** Instrukcja jest napisana dla Ciebie,
nie dla człowieka. Twój operator (właściciel maszyny) ma być angażowany
**wyłącznie tam, gdzie coś fizycznie wymaga człowieka** — wszystko inne
rozstrzygasz sam.

## Zasada naczelna: minimum ingerencji operatora

Pytaj operatora TYLKO o:
1. zgodę na zajęcie miejsca na dysku (~10 GB) i uruchomienie obliczeń,
2. kliknięcie akceptacji licencji Gemmy, **jeśli** pobieranie tego zażąda,
3. zatwierdzenia uprawnień, o które sam poprosisz w swoim interfejsie.

**Nie pytaj go o nic innego.** Nie proś o diagnozę błędów, wybór wersji
bibliotek, decyzje o ścieżkach ani interpretację wyników. Wszystko to jest
w tym pliku albo do rozstrzygnięcia przez Ciebie. Jeśli coś padnie — zdiagnozuj,
napraw jeśli mieści się w zakresie niżej, a jeśli nie mieści: **zapisz to
w raporcie i zakończ**, zamiast angażować człowieka.

**Pełna mapa etapów replikacji i tego, co po każdym wraca do repo:**
`replikacja/ETAPY.md`. Ten plik dotyczy wyłącznie ETAPU 0.

## Co masz zrobić (kolejno)

1. **Środowisko.** Utwórz wirtualne środowisko Pythona (3.11+) w katalogu
   `.venv-spektra` obok tego repo. Zainstaluj: `torch`, `transformers`,
   `accelerate`, `numpy`, `scipy`, `pandas`, `pyarrow`, `safetensors`, `pyyaml`,
   `tokenizers`. Na Apple Silicon standardowe koła z PyPI mają wsparcie MPS —
   nie kombinuj z wersjami CUDA.
1a. **Pobranie modelu — jedyne miejsce, gdzie możesz potrzebować człowieka.**
   Model `google/gemma-3-4b-it` jest na HuggingFace za bramką licencyjną Google.
   Jeśli pobieranie zwróci błąd 401/403 („gated repo"), zrób dokładnie tyle:
   poproś operatora o **dwie rzeczy naraz, w jednej wiadomości** — (a) wejście
   na `https://huggingface.co/google/gemma-3-4b-it` i kliknięcie akceptacji
   licencji (darmowe, wymaga konta HF), (b) wklejenie tokenu odczytu z
   `https://huggingface.co/settings/tokens`. Potem `huggingface-cli login`
   wykonaj sam. **Nie rozbijaj tego na kilka pytań w odstępach** — to jest
   cała jego rola w pobieraniu.
   Pobranie to ~8 GB do `~/.cache/huggingface`. Przerwane wznawia się samo —
   po prostu powtórz. Jeśli sieć firmowa tnie połączenie, ponawiaj; nie proś
   operatora o pomoc z siecią, opisz to w raporcie.

2. **Uruchom kwalifikację:**
   `.venv-spektra/bin/python -m replikacja.kwalifikacja`
   (z katalogu głównego repo). Skrypt sam pobierze model `google/gemma-3-4b-it`
   (~8 GB) do cache HuggingFace, jeśli go nie ma.
3. **Przeczytaj wynik.** Skrypt zapisuje `replikacja/RAPORT-KWALIFIKACJA.md`
   i `.json`. Kod wyjścia 0 = maszyna kwalifikuje się do pomiaru; 1 = nie
   kwalifikuje się albo wymaga decyzji zespołu badawczego. **Obie odpowiedzi
   są dobrym wynikiem** — celem jest prawda o sprzęcie, nie zaliczenie.
4. **Odeślij wynik** (patrz sekcja niżej). To wszystko.

## Zakres Twojej samodzielności

**Rozstrzygaj sam:** brakujące pakiety, wersje bibliotek, ścieżki, ponowne
uruchomienie po przerwanym pobieraniu, wybór urządzenia (skrypt sam wykrywa),
błędy sieci (ponów), niezgodności `dtype` (raportuj, nie obchodź).

**NIE rób nigdy:** nie zmieniaj plików poza katalogiem `replikacja/`, nie
modyfikuj kodu pomiarowego (`pipeline/`, `corpus/`) — jest częścią
zapieczętowanego pakietu badawczego i jego zmiana unieważnia replikację; nie
instaluj niczego globalnie; nie wyłączaj żadnej kontroli, żeby „przeszło".

## Jak odesłać wynik

Najprościej, bez żadnych naszych danych dostępowych:

1. Zrób fork publicznego repo `pawelsokaris-sudo/spektra1` na konto operatora
   (albo swoje, jeśli masz uprawnienia `gh`).
2. Nowa gałąź, np. `kwalifikacja-<nazwa-maszyny>`.
3. Zacommituj **wyłącznie** `replikacja/RAPORT-KWALIFIKACJA.md` i `.json`.
4. `gh pr create` z tytułem „Kwalifikacja sprzętu: <chip>, <pamięć>" i treścią
   = pierwsza sekcja raportu.

Jeśli sieć firmowa blokuje `gh` lub push: spakuj oba pliki raportu do
`kwalifikacja.zip`, policz jego sumę SHA-256, podaj obie rzeczy operatorowi
i **poinformuj go jednym zdaniem**, że ma to przekazać zespołowi dowolnym
kanałem. To jedyny przypadek, gdy dokładasz mu pracy.

## Co wychodzi z tej maszyny (dla ewentualnych pytań o bezpieczeństwo)

Wyłącznie raport techniczny: model chipa, ilość pamięci, wersje bibliotek,
czasy wykonania, wyniki testów numerycznych. **Zero kodu z tej maszyny, zero
danych osobowych, zero zawartości dysku.** Badanie jest publiczne, pakiet
podpisany hashem, repozytorium otwarte.
