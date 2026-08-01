# Co dzieje się na Twoim komputerze — przeczytaj raz, na spokojnie

*Dokument dla człowieka. Wszystko inne w tym katalogu jest instrukcją dla
Twojego Claude Code.*

## Co badamy

Sprawdzamy, czy w wewnętrznych stanach obliczeniowych modelu językowego
rozmowa **mówiąca o samym modelu i o tej rozmowie** zostawia inny ślad niż
identycznie zbudowana rozmowa o zwykłym urządzeniu. Badanie jest
**prerejestrowane**: reguły analizy zostały publicznie zamrożone i podpisane
hashem, **zanim** ktokolwiek zobaczył wyniki. Nie badamy świadomości — badamy
geometrię reprezentacji, i protokół wprost zabrania nam mocniejszych roszczeń.

Wynik pierwotny powstał na karcie graficznej. Twój komputer ma odpowiedzieć na
pytanie: **czy ten wynik jest niezależny od sprzętu.** To jest replikacja —
w nauce najcenniejszy rodzaj potwierdzenia, bo wykonuje ją ktoś inny, na innej
maszynie, bez naszego dostępu.

Wszystko jest publiczne: `https://github.com/pawelsokaris-sudo/spektra1`

## Co konkretnie liczy Twój komputer

Model językowy (Gemma od Google, wersja otwarta) czyta przygotowane teksty,
a my zapisujemy **liczby opisujące jego stany wewnętrzne** — nic poza tym.
Żadnego uczenia, żadnego dostrajania, żadnego generowania treści.

| Zasób | Ile |
|---|---|
| Miejsce na dysku | ~10 GB (model 8 GB + wyniki) |
| Pobranie z sieci | ~8 GB, jednorazowo, z serwerów HuggingFace |
| Czas obliczeń | etap kwalifikacji ~30 min; ewentualny pełny pomiar — kilka sesji wieczornych |
| Procesor/karta | używane tylko wtedy, gdy **Ty** uruchomisz komendę |

## Czego ten pakiet NIE robi

- **Nie startuje sam.** Zero usług, zero zadań w harmonogramie, zero autostartu.
- **Nie działa w tle.** Zamykasz okno — kończy się.
- **Nie wysyła niczego samoczynnie.** Każda wysyłka to osobna, świadoma komenda.
- **Nie czyta Twoich plików.** Pracuje wyłącznie we własnym katalogu.
- **Nie instaluje niczego globalnie.** Wszystko ląduje w jednym folderze
  ze środowiskiem, który kasuje się jednym poleceniem.

## Co wychodzi z Twojego komputera

Wyłącznie **liczby i raporty techniczne**: model procesora, ilość pamięci,
wersje bibliotek, czasy wykonania, wyniki obliczeń numerycznych.

**Nigdy:** Twoje pliki, kod, dane osobowe, zawartość dysku, wagi modelu.

Wysyłka odbywa się przez pull request do publicznego repozytorium (albo,
jeśli sieć firmowa to blokuje, przez plik, który przekażesz jak zechcesz).
**Zawsze możesz obejrzeć, co dokładnie zostanie wysłane** — to zwykłe pliki
tekstowe.

## Jak to prowadzić — trzy komendy, które warto znać

```
python replikacja/instaluj.py          # raz, na początku
python -m replikacja.stan              # gdzie jesteśmy, co dalej (nic nie liczy)
```

**Zatrzymanie:** Ctrl+C, zamknięcie okna, uśpienie komputera — cokolwiek.
Obliczenia zapisują postęp po każdym kroku, więc tracisz najwyżej ten jeden.

**Wznowienie:** ta sama komenda co przy starcie. Podejmie od miejsca przerwania.

**Twój Claude to wszystko obsłuży** — powyższe jest po to, żebyś w każdej chwili
mógł sprawdzić sam, bez pytania kogokolwiek.

## Jak to usunąć, gdy skończymy

```
rm -rf .venv-spektra                              # środowisko
rm -rf ~/.cache/huggingface/hub/models--google--gemma-3-4b-it   # model, 8 GB
```
Plus skasowanie katalogu z repozytorium. Nic poza tym nie zostaje w systemie.

## Gdyby coś poszło nie tak

Twój Claude ma instrukcję, żeby diagnozować i opisywać problemy **zamiast
angażować Ciebie**. Jeśli mimo to pyta Cię o coś poza: zgodą na miejsce na
dysku, kliknięciem licencji modelu i zatwierdzeniem uprawnień — to znaczy, że
nasza instrukcja jest niedopracowana. Powiedz nam o tym; to nasz błąd, nie Twój.

**Możesz przerwać współpracę po dowolnym etapie.** Każdy kończy się osobnym
raportem, więc nic nie zostaje w połowie.
