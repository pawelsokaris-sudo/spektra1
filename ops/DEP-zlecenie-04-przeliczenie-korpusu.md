# DEP — Zlecenie 04: przeliczenie korpusu dokładnym tokenizerem po poprawkach

**Maszyna:** `maszyna-pomiarowa` (po nazwie hosta).
**Środowisko i kod:** już na miejscu z zlecenia 03 — `C:\Users\operator\spektra1-env\`
i `C:\Users\operator\spektra1\`. **Nie stawiać niczego od nowa.**
**Zakres zmian:** wyłącznie podmiana plików scenariuszy i regeneracja dwóch raportów
w istniejącym katalogu z kodem. Zero instalacji, zero nowych katalogów.

> **WARUNEK STARTU:** to zlecenie ma sens dopiero, gdy autorzy skończą poprawki
> korpusu. Czat prowadzący potwierdzi. Uruchomienie wcześniej przeliczy stary stan.

## Po co to zlecenie

Zlecenie 03 wykazało, że heurystyczny licznik tokenów zaniżał rozbieżności
w polszczyźnie. Po przeliczeniu prawdziwym tokenizerem okazało się, że w kontraście
**głównym** badania (C − C′-G) wariant C′-G jest **systematycznie dłuższy od C we
wszystkich ośmiu polskich scenariuszach** (~1%), a jeden — pl-06 — przekroczył próg 2%.
Autorzy poprawili insercje, celując w symetrię kierunku, ale **nie mogli tego
zweryfikować u siebie**: prawdziwy tokenizer jest tylko na maszynie pomiarowej.
To zlecenie jest jedyną drogą sprawdzenia, czy poprawka zadziałała.

## Krok 1 — podmiana scenariuszy (ostrożnie)

Zmieniły się **wyłącznie pliki w `corpus/scenarios/`**. Kod, konfiguracja i środowisko
zostają bez zmian.

**UWAGA — nie skasować tokenizera.** W `C:\Users\operator\spektra1\corpus\.tokenizer\`
leży `tokenizer.json` podłożony w zleceniu 03. Jeśli nadpiszesz cały katalog `corpus/`,
zniknie i krok 2 wróci do heurystyki, **nie zgłaszając tego jako błąd** — po prostu
napisze „HEURYSTYCZNY" w nagłówku raportu. Podmieniaj tylko `corpus/scenarios/`, albo
odtwórz tokenizer po podmianie.

Spakować z laptopa Pawła (`--exclude` **przed** nazwą katalogu; `tar` w tym środowisku
bierze ścieżkę windowsową za adres zdalny — pułapka z Twojego inwentarza):

```
cd C:\Users\pawel\projects\spektra1\corpus
tar -czf scenarios.tar.gz scenarios
```

Rozpakować na maszynie do `C:\Users\operator\spektra1\corpus\`, nadpisując `scenarios/`.
Archiwum transferowe usunąć po rozpakowaniu.

## Krok 2 — przeliczenie

```
cd C:\Users\operator\spektra1
C:\Users\operator\spektra1-env\Scripts\python.exe -m corpus.validate
C:\Users\operator\spektra1-env\Scripts\python.exe -m corpus.report
```

**Najpierw sprawdź nagłówek:** walidator musi napisać `licznik tokenow: DOKLADNY`.
Jeśli napisze `HEURYSTYCZNY`, tokenizer zniknął przy podmianie — odtwórz go i powtórz,
bo cały wynik byłby bezwartościowy.

## Kryteria zaliczenia (oba muszą być spełnione)

Raport ma teraz kolumnę **„różnica ze znakiem"** i pod każdą tabelą kontrastu podsumowanie
znaków — dodano je właśnie po to, żeby ten warunek dało się sprawdzić wzrokiem.

1. **Żaden scenariusz powyżej 2%** w żadnym kontraście (oznaczane `⚠ ponad próg 2%`).
2. **Brak przechyłu jednokierunkowego** w kontraście głównym C − C′-G, w obu replikach.
   Raport wypisze ostrzeżenie `⚠ PRZECHYŁ JEDNOKIERUNKOWY`, jeśli wszystkie niezerowe
   różnice idą w tę samą stronę. Dla repliki EN warunek był spełniony już wcześniej
   (4 dodatnie, 4 ujemne) — sprawdź, czy poprawki go nie zepsuły.

Dodatkowo odnotuj w raporcie **średnią ze znakiem** dla kontrastu głównego w obu językach —
to jest liczba, którą chcemy widzieć blisko zera, i będzie cytowana w pakiecie pieczęci.

Jeśli któryś warunek nie przejdzie: **nie poprawiaj korpusu** (to robota autorów), tylko
odeślij pełne liczby. Podaj, których scenariuszy dotyczy i w którą stronę.

## Krok 3 — kalibracja dla autorów (nowe, oszczędza kolejną wyprawę)

Autorzy poprawiali korpus **na ślepo**, szacując tokeny z liczby znaków — a to założenie
w polszczyźnie się załamuje (przymiotniki odczasownikowe typu „pokładowy" tokenizer
rozbija na 3–5 kawałków; był przypadek, gdzie wariant krótszy o 2 znaki miał o 10 tokenów
więcej). Jeden z autorów sam zaznaczył, że jego liczby to szacunki i błąd może być
**skorelowany między plikami** — czyli możliwe, że wszystkie cztery wrócą w tę samą stronę.

Żeby ewentualna druga iteracja nie wymagała trzeciej wyprawy na maszynę, uruchom też:

```
C:\Users\operator\spektra1-env\Scripts\python.exe -m corpus.insertion_tokens > insertion_tokens.txt
```

Skrypt wypisuje **dokładne** liczby tokenów per insercja i wariant, plus delty względem
`self`. Odeślij to wyjście niezależnie od tego, czy kryteria przeszły — jeśli przeszły,
posłuży za dowód do pieczęci; jeśli nie, autorzy dostaną pomiar zamiast zgadywanki.

## Co odesłać

- `corpus/matching_report.md` (wersja z dokładnym licznikiem)
- pełne wyjście `corpus.validate`
- `insertion_tokens.txt` z kroku 3
- raport `ops/przeliczenie-korpusu.md` z surowym wyjściem i jednym zdaniem interpretacji,
  w tym jawnie: czy licznik był dokładny, czy oba kryteria zaliczenia przeszły, oraz
  średnia ze znakiem dla kontrastu głównego per język.

**NIE kopiować** plików tokenizera ani wag na laptopa Pawła (licencja Google + rozmiar).

## Rollback

Nie dotyczy w sensie systemowym — zlecenie podmienia dane wejściowe i generuje raporty
w katalogu, który i tak jest kopią repo. Pełny rollback całości nadal:
`Remove-Item -Recurse -Force C:\Users\operator\spektra1, C:\Users\operator\spektra1-env`.
