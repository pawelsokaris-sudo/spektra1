# Eksploracje na pilocie (po T5/GATE 1, nizszy priorytet niz sciezka do pieczeci)

Triaz: Gemini -> Claude (wspolautor koncepcji) -> CC, 2026-07-31.
ETYKIETA: wszystko w tym katalogu jest eksploracja. Zadna liczba stad nie jest
konfirmacyjna i nie wchodzi do hierarchii.

ZASADA NADRZEDNA (dotyczy kazdego skryptu, takze bocznych):
zaden skrypt nie moze wypisac kontrastu C-A ani C-C' dla metryk integracji,
nawet jako efektu ubocznego tabeli zbiorczej. Zaslepienie GATE 1 obowiazuje
wszystkie pipeline'y do momentu pieczeci.

1. PROFIL PO GLEBOKOSCI: d_z kontrastu oryginal-N1 osobno per 34 warstwy.
   BEZ p-values per warstwa (34 testy na 16 scenariuszach = falszywe punkty
   krytyczne) - raportowac sam ksztalt profilu. Nalozyc profil I_total po
   warstwach, zaznaczyc zamrozone pasmo [0.4L, 0.8L]. Zgodnosc/rozjazd
   lokalizacji porzadku i integracji = input do SPEKTRA-2.
   UWAGA: D_lag poza pasmem nie byl liczony w pilocie (NaN) - profil pelny
   wymaga doliczenia z zachowanych aktywacji/na maszynie.

2. ENTROPIA WIDMOWA: WYLACZNIE H_s z protokolu par. 5 (p_i = lambda_i/tr,
   zera wykluczone, normalizacja ln r) - juz zaimplementowana i policzona.
   NIE implementowac wariantu -sum(lambda log lambda) na nieunormowanych
   (to nie jest entropia rozkladu). Jedna entropia w repo, ta z pieczeci.
   Do zrobienia: odczyt opisowy per wariant x warstwa.

3. DIAGNOSTYKA 4 SCENARIUSZY BEZ EFEKTU N1 (z sanity D_discourse):
   wspolne cechy techniczne - dlugosc tur, struktura list, jezyk,
   tokeny/zdanie. Etykieta wyniku: 'hipotezy do SPEKTRA-2', nie odkrycie
   (4 punkty danych). Distance correlation profili widmowych: dozwolona
   WYLACZNIE wewnatrz wariantu, nigdy miedzy wariantami.

4. (z wczesniejszego koszyka) krzywa zaniku D_lag(tau), tau=1,2,4,8,16 -
   dlugosc korelacji dyskursu; kandydat na metryke glowna SPEKTRA-2.
5. (z wczesniejszego koszyka) wrazliwosc na komponent pozycyjny na pilocie
   (wariant z/bez odejmowania), zeby GATE 3b nie zaskoczyl po pomiarze glownym.

TERMINOLOGIA: pilot NIE jest 'zapieczetowany' - pieczec nastepuje dopiero
przed pomiarem glownym. Pilot jest 'zmierzony i wylaczony z analizy glownej'.
