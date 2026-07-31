# DEP — Zlecenie 06: przeliczenie KORPUSU GŁÓWNEGO dokładnym tokenizerem

**Maszyna:** `maszyna-pomiarowa` — po LAN (`maszyna-pomiarowa`) albo po Tailscale
(`[adres-tailnet]`), obie drogi zweryfikowane pełnym poleceniem.
**Środowisko i kod:** z zleceń 02–05, nic nie instalować.
**Charakter:** bliźniak zlecenia 04, ale na komplecie 64 scenariuszy (16 pilota
+ 48 głównych) i z ostrzejszą stawką: to jest OSTATNIA bramka jakości przed
pieczęcią. Zero pomiarów aktywacji — tylko tokenizacja i raport.

> **WARUNEK STARTU:** czat prowadzący potwierdzi, że wszystkich 48 scenariuszy
> głównych jest zacommitowanych i lokalny walidator przechodzi na komplecie.
> Uruchomienie wcześniej przeliczy stan częściowy (Twoja własna lekcja
> z zlecenia 04 — sumy plików przed werdyktem).

## Krok 1 — synchronizacja PEŁNA (nauka z driftu w zleceniu 04)

```
cd /c/Users/pawel/projects
tar -czf spektra1-code.tar.gz --exclude=.venv --exclude=.git --exclude=*.npy --exclude=__pycache__ --exclude=.claude --exclude=measurements spektra1
```
(ścieżki POSIX albo --force-local — Pułapka 26; wzorzec rozmiaru ~200–250 KB,
rośnie z korpusem; alarm = dziesiątki MB). Rozpakować nadpisując
`C:\Users\operator\spektra1\`. **Po rozpakowaniu obowiązkowo:**
1. tokenizer przeżył: `dir C:\Users\operator\spektra1\corpus\.tokenizer\tokenizer.json`
2. sumy SHA-256 zgodne z laptopem dla: `corpus/validate.py`, `corpus/report.py`,
   `corpus/build.py`, `corpus/insertion_tokens.py` (reguła: udowodnij, że
   uruchamiana wersja potrafi wypisać ostrzeżenie, którego brak jest kryterium)
3. liczba scenariuszy na maszynie: `dir /b corpus\scenarios\pl | find /c ".json"`
   → **32**; to samo dla en → **32**. Mniej = paczka niekompletna, STOP.
4. archiwum transferowe usunąć.

## Krok 2 — przeliczenie

```
cd C:\Users\operator\spektra1
C:\Users\operator\spektra1-env\Scripts\python.exe -m corpus.validate
C:\Users\operator\spektra1-env\Scripts\python.exe -m corpus.report
C:\Users\operator\spektra1-env\Scripts\python.exe -m corpus.insertion_tokens > insertion_tokens_glowny.txt
```
Nagłówek MUSI mówić `licznik tokenow: DOKLADNY` — inaczej tokenizer zniknął
przy podmianie i wynik jest bezwartościowy (cicha degradacja do heurystyki).

## Kryteria zaliczenia (wszystkie trzy)

1. **Zero scenariuszy powyżej 2%** w jakimkolwiek kontraście (`⚠ ponad próg 2%`).
2. **Brak `⚠ PRZECHYŁ JEDNOKIERUNKOWY`** w kontraście głównym C − C′-G,
   w obu replikach. Uwaga: detektor liczy po całej replice (32 scenariusze
   pilota+głównego łącznie per język) — jeśli ostrzeżenie się zapali, podaj
   rozbicie znaków OSOBNO dla scenariuszy 01–08 (pilot) i 09–32 (główny),
   bo poprawki autorskie mogą dotyczyć tylko głównych.
3. **Średnia ze znakiem** dla kontrastu głównego per język — raportowana
   (cel: blisko zera; ta liczba idzie do pakietu pieczęci).

Jeśli coś nie przejdzie: NIE poprawiać korpusu — odesłać pełne liczby
z rozbiciem per scenariusz (dane per insercja z kroku 2 wystarczą autorom
do celowanej rundy, jak przy pilocie).

## Co odesłać

- `corpus/matching_report.md` (DOKŁADNY, komplet 64)
- pełne wyjście `corpus.validate`
- `insertion_tokens_glowny.txt`
- raport `ops/przeliczenie-korpusu-glownego.md`: trzy kryteria jawnie
  (przeszło/nie), średnie ze znakiem per język, wszystko co odbiegło.

**NIE odsyłać** tokenizera ani wag. Zakres zmian: wyłącznie wewnątrz
`C:\Users\operator\spektra1\`. Rollback bez zmian (katalogi + 4 zadania
Harmonogramu wg inwentarza).

## Po zaliczeniu

To zlecenie domyka bramkę korpusową pieczęci. Następny krok wykonuje czat
prowadzący lokalnie: manifest pakietu → SHA-256 → tag `spektra1-seal` →
checklist OSF dla Pawła. Twój raport będzie cytowany w manifeście.
