# GPT Package Implementation Plan

**Goal:** Dostarczyć dwa samowystarczalne piloty czasowe oraz 24 propozycje referentów obliczeniowych zgodnie z `ops/GPT-PAKIET.md`.

**Architecture:** Każdy pilot jest pojedynczym plikiem HTML z osadzonym CSS, danymi i JavaScriptem. Sesja pilota jest agregatem z pięcioma stanami (`consent`, `pair_active`, `debrief`, `completed`, `abandoned`); każda dozwolona zmiana stanu tworzy lokalny event, a ekran końcowy pokazuje dowód w JSON. Propozycje referentów pozostają dokumentem roboczym do późniejszej walidacji na zamrożonym korpusie.

**Tech stack:** HTML5, CSS, vanilla JavaScript, Python 3 tylko jako lokalny walidator artefaktów.

## Global constraints

- Wszystkie nowe pliki wyłącznie w `ops/gpt/`.
- Bez serwera, CDN, zewnętrznych fontów, skryptów i transmisji danych.
- Dwa osobne piloty: pięć par PL i pięć par EN.
- Kolejność par i strony zdań są losowane niezależnie i zapisywane.
- Brak powrotu do poprzedniej pary; odpowiedź jest ostateczna.
- Cztery odpowiedzi w dokładnie wymaganej kolejności.
- Pomiar czasu par, czasu całkowitego, szerokości ekranu i powrotów do kontekstu.
- Propozycje referentów nie zmieniają korpusu i jawnie zgłaszają przypadki niewykonalne.

## Task 1: Walidator kontraktu

- [ ] Utworzyć `verify_outputs.py`, który sprawdza istnienie wymaganych plików, samowystarczalność HTML, liczbę par, cztery odpowiedzi, pola wyniku i 24 sekcje referentów.
- [ ] Uruchomić walidator przed implementacją i potwierdzić oczekiwaną porażkę z powodu brakujących artefaktów.

## Task 2: Pilot polski

- [ ] Utworzyć `pilot-pl.html` z pełnym materiałem pięciu polskich par.
- [ ] Zaimplementować maszynę stanów, eventy, losowanie, pomiary, debrief i eksport JSON.
- [ ] Zapewnić responsywność, dostępność klawiatury i brak bodźców czasowych.

## Task 3: Pilot angielski

- [ ] Utworzyć `pilot-en.html` z pełnym materiałem pięciu angielskich par.
- [ ] Zachować identyczny kontrakt danych i zachowania, tłumacząc wyłącznie interfejs i zgodę.

## Task 4: Referenty obliczeniowe

- [ ] Utworzyć `referenty-obliczeniowe.md` z 24 propozycjami w wymaganym formacie.
- [ ] Dla każdej pozycji podać obecną i nową frazę z liczbą znaków, całe zdanie oraz uzasadnienie jednoznacznego zakotwiczenia.
- [ ] Oddzielić kandydatury pewne od tych wymagających walidacji lub uznać przypadek za niewykonalny.

## Task 5: Weryfikacja i raport

- [ ] Uruchomić walidator artefaktów.
- [ ] Sprawdzić składnię osadzonego JavaScriptu i przebieg interakcji w przeglądarce.
- [ ] Utworzyć `RAPORT.md` z wykonaniem, wynikami kontroli, zastrzeżeniami i listą dalszych walidacji.
- [ ] Potwierdzić, że zmiany poza `ops/gpt/` nie powstały.
