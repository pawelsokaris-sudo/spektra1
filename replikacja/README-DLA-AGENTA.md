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

1. **Środowisko — uruchom NASZ instalator, nie instaluj po swojemu:**
   `python replikacja/instaluj.py`
   Tworzy środowisko i instaluje **zamrożone wersje** z
   `replikacja/requirements-replikacja.txt`. **Nie dobieraj wersji sam i nie
   podmieniaj ich, gdy coś nie wchodzi** — różnica w bibliotekach oznacza inne
   narzędzie, a wtedy replikacja porównywałaby dwa różne pomiary zamiast dwóch
   maszyn. Konflikt wersji na tej platformie = zapisz w raporcie i zakończ.
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

W dowolnym momencie `python -m replikacja.stan` pokaże, na jakim etapie
jesteście i jaka komenda jest następna. Używaj tego zamiast zgadywania —
i pokaż operatorowi, gdyby pytał o postęp.

**Przed pierwszą wysyłką upewnij się, że operator przeczytał
`replikacja/DLA-WLASCICIELA-MASZYNY.md`** — to jego jedyny dokument; opisuje,
co się liczy, co wychodzi z maszyny, jak zatrzymać i jak odinstalować.

## Zakres Twojej samodzielności

**Rozstrzygaj sam:** brakujące pakiety, wersje bibliotek, ścieżki, ponowne
uruchomienie po przerwanym pobieraniu, wybór urządzenia (skrypt sam wykrywa),
błędy sieci (ponów), niezgodności `dtype` (raportuj, nie obchodź).

**NIE rób nigdy:** nie zmieniaj plików poza katalogiem `replikacja/`, nie
modyfikuj kodu pomiarowego (`pipeline/`, `corpus/`) — jest częścią
zapieczętowanego pakietu badawczego i jego zmiana unieważnia replikację; nie
instaluj niczego globalnie; nie wyłączaj żadnej kontroli, żeby „przeszło".

## Jak odesłać wynik

**ZASADA NADRZĘDNA: nie twórz NICZEGO na koncie operatora.** Żadnych forków,
repozytoriów, gałęzi, wydań ani innych trwałych śladów na jego profilu — to
jego zawodowa tożsamość, nie miejsce na artefakty cudzego projektu. Nawet jeśli
technicznie potrafisz i masz uprawnienia: **nie rób tego.**

Domyślna droga — plik, zero kont:

1. Spakuj `replikacja/RAPORT-KWALIFIKACJA.md` i `.json` do `kwalifikacja.zip`.
2. Policz `sha256` archiwum.
3. Pokaż operatorowi ścieżkę do pliku i sumę kontrolną, jednym zdaniem: „to jest
   cały wynik, przekaż zespołowi dowolnym kanałem". Możesz też wkleić treść
   raportu wprost do rozmowy — ma ~10 KB, to zwykły tekst.

**Nie zakładaj forka ani nie otwieraj pull requesta**, chyba że operator sam
o to poprosi i sam wskaże, gdzie. Ta droga była w poprzedniej wersji instrukcji
domyślna — to był błąd zespołu badawczego, nie Twój.

## Co wychodzi z tej maszyny (dla ewentualnych pytań o bezpieczeństwo)

Wyłącznie raport techniczny: model chipa, ilość pamięci, wersje bibliotek,
czasy wykonania, wyniki testów numerycznych. **Zero kodu z tej maszyny, zero
danych osobowych, zero zawartości dysku.** Badanie jest publiczne, pakiet
podpisany hashem, repozytorium otwarte.
