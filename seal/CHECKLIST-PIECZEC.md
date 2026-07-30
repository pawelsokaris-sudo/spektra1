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
4. Rollback maszyny obejmuje TAKZE 2 zadania Harmonogramu:
   schtasks /delete /tn SPEKTRA1-pomiar-pilota /f oraz SPEKTRA1-dlag-sentence.
5. Pakiet pieczeci: protokol v1.3 + rozstrzygniecia rundy 1-3 + uwagi zewnetrzne
   + korpus + kod + lockfile (z naglowkiem --extra-index-url) + config + hash
   -> tag spektra1-seal + rejestracja OSF (checklist dla Pawla w T8).
