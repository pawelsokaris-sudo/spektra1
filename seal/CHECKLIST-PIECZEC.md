# Checklist przed pieczecia (T8) - miny rozbrojone zawczasu

1. GITIGNORE PRZY PODKATALOGACH WYNIKOW: !measurements/*.parquet NIE przechodzi
   przez ukosnik. Jesli wyniki pomiaru glownego pojda do podkatalogow, dopisac
   !measurements/**/*.parquet. (DEP, 2026-07-30; celowo niedopisane na zapas.)
2. LIMIT GITHUB 100 MB/PLIK - PEWNY przy pomiarze glownym, nie hipotetyczny:
   pilot = 48.4 MB widm / 208 tekstow; M=24/jezyk daje 240 tekstow glownych
   + ~384 nulli = ~624 tekstow => ~145 MB. ROZWIAZANIE: runner zapisuje widma
   per jezyk (2 pliki po ~72 MB) - zmiana jednej linii przed pomiarem glownym;
   alternatywnie LFS/release assets. NIE usuwac wyjatku z gitignore.
   RACHUNEK DEP (do reki przy zamrazaniu M): 0.2327 MB widm/tekst, 13*M
   tekstow/jezyk (5 wariantow + 8 nulli na scenariusz). Podzial per jezyk
   wytrzymuje do M=33 (99.8 MB); M>=34 => LFS/release assets. DECYZJA O M
   I O FORMACIE ZAPISU MUSZA ZAPASC RAZEM w GATE 1, nie jedna po drugiej.
3. Anonimizacja: wykonana 2026-07-30 (filter-repo, bloby+opisy); przy kazdym
   nowym raporcie ops/ pilnowac konwencji (operator maszyny / maszyna-pomiarowa).
   LEKCJA 2026-08-01 (ANEKS-3): audyt danych osobowych NALEZY WYKONAC PRZED
   nadaniem tagu, nie po. Druga anonimizacja ruszyla TRESC 3 plikow ops/seal,
   przez co suma archiwum zapisana w tagu przestala sie zgadzac. Koszt: jawny
   aneks rozspojniajacy plombe. Pozycja obowiazkowa listy: "grep po nazwiskach,
   loginach, adresach e-mail, hostach i adresach IP w calym drzewie ORAZ
   w metadanych autorskich commitow (git log --format='%an %ae' | sort -u)".
   LEKCJA 2 (zgloszona przez DEP tego samego dnia): dokumenty operacyjne NIE
   moga zawierac nazw kont ani hostow w komendach - anonimizacja podmienia
   tresc plikow i psuje wykonywalnosc instrukcji. Konwencja: wejscie do
   katalogu roboczego przez cd + wylacznie sciezki wzgledne, interpreter jako
   ..\spektra1-env\Scripts\python.exe. Wzorzec: ops/DEP-zlecenie-07.
4. Rollback maszyny obejmuje TAKZE 2 zadania Harmonogramu:
   schtasks /delete /tn SPEKTRA1-pomiar-pilota /f oraz SPEKTRA1-dlag-sentence.
5. Pakiet pieczeci: protokol v1.3 + rozstrzygniecia rundy 1-3 + uwagi zewnetrzne
   + korpus + kod + lockfile (z naglowkiem --extra-index-url) + config + hash
   -> tag spektra1-seal + rejestracja OSF (checklist dla Pawla w T8).

6. GATE 1 NA SLEPO (blinded sample size estimation, propozycja wspolautora
   koncepcji 2026-07-31): skrypt mocy liczy SD parowanych roznic kontrastu
   glownego C-C'-G, ale NIE WYPISUJE sredniej ani znaku - kierunek efektu
   glownego na pilocie pozostaje nieobejrzany do pieczeci. Koszyk zakazany
   (kontrasty integracji C-A, C-C' na pilocie) egzekwowany przez kod, nie
   przez dyscypline. Pierwsza liczba po pieczeci = otwarcie tej szuflady.
7. Do eksploracji z etykieta (kandydaci SPEKTRA-2, NIE przed konfirmacja):
   krzywa zaniku D_lag(tau) dla tau=1,2,4,8,16 (dlugosc korelacji dyskursu);
   profil porzadku po glebokosci vs pasmo integracji; wrazliwosc na komponent
   pozycyjny juz na pilocie (zeby GATE 3b nie zaskoczyl).
8. N2 JUZ ZMIERZONE w pilocie (64 teksty, D_local + D_discourse w danych) -
   odczyt opisowy skali porzadku (tury vs zdania) przy raporcie GATE 1.
