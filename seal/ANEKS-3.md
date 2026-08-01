# ANEKS 3 — usunięcie danych osobowych z historii publicznej

**Data:** 2026-08-01
**Charakter:** zmiana **po** pieczęci, jawna, nienaukowa.
**Powód:** ochrona danych osobowych osób trzecich w publicznym repozytorium.

## Rzecz najważniejsza na wstępie

**Suma kontrolna zapisana w tagu `spektra1-seal` przestała się zgadzać
z zawartością repozytorium.** Ten aneks istnieje po to, żeby nikt nie musiał
tego odkrywać samodzielnie i zastanawiać się, co zostało po cichu zmienione.

| | SHA-256 archiwum (`git archive spektra1-seal --format=tar`) |
|---|---|
| stan zapieczętowany 2026-07-31 | `7ca4870a4e60c23f823a7a8fe0dddcf70e7741d534205eb31e2a3455caa763ce` |
| stan po anonimizacji 2026-08-01 | `93c55ea9f66f0b72c8a7b44bc1087dbe6437a23bc8f0f61e3b21fed4511797ae` |

Pierwsza suma nadal daje się odtworzyć z kopii historii sprzed anonimizacji
(patrz „Weryfikowalność" niżej) — i została odtworzona przed napisaniem tego
aneksu, co potwierdza, że plomba do tej chwili była nienaruszona.

## Co dokładnie się zmieniło

Anonimizacja dotknęła **trzech plików**, wszystkich administracyjnych:

| Plik | Zmiana |
|---|---|
| `ops/DEP-zlecenie-06-przeliczenie-korpusu-glownego.md` | nazwa konta w ścieżkach → `operator`; nazwa hosta w sieci lokalnej → `maszyna-pomiarowa`; adres w sieci prywatnej → `[adres-tailnet]` |
| `ops/przeliczenie-korpusu-glownego.md` | jw. |
| `seal/CHECKLIST-OSF.md` | adres e-mail kierownika badania → `[konto kierownika badania]` |

Zmieniono także **metadane autorskie commitów** (imię, nazwisko i adres e-mail
osoby trzeciej, która wykonała jednorazową kwalifikację sprzętu i nie jest
współautorką badania) — na `operator maszyny`.

## Czego NIE zmieniono

Zweryfikowane porównaniem sum SHA-256 plik po pliku względem kopii sprzed
anonimizacji — **identyczne bajt w bajt**:

- `docs/SPEKTRA-1-protokol-FINAL.md` oraz rozstrzygnięcia rund 1–3
- `config.yaml` (z sumami wag modelu) i `requirements-lock.txt`
- **wszystkie 64 scenariusze korpusu** × 5 wariantów (zero różnic)
- **cały kod pomiarowy**: `pipeline/`, `power/`, `nulls/`, `gates/`, `corpus/`
- **wszystkie dane pomiarowe** pilota (`measurements/*.parquet`)

Żadna hipoteza, żaden próg, żadne kryterium bramki, żadna liczba wchodząca do
analizy nie została ruszona. Zmiana jest kosmetyczna wobec treści badania
i została wykonana **przed** poznaniem wyniku pomiaru głównego.

## Weryfikowalność

Anonimizacja historii git jest z natury nieodwracalna publicznie — stare
obiekty przestają istnieć w repozytorium zdalnym (o to właśnie chodziło).
Aby zmiana pozostała sprawdzalna, zachowano **prywatną kopię historii sprzed
anonimizacji** (pakiet `git bundle`, poza repozytorium publicznym, u kierownika
badania). Kopia pozwala każdemu recenzentowi, któremu zostanie udostępniona:

1. odtworzyć sumę `7ca4870a…` i potwierdzić, że plomba z 2026-07-31 była prawdziwa,
2. wykonać `diff` całych drzew i potwierdzić, że powyższa lista zmian jest kompletna.

Kopia zawiera dane osobowe, więc **nie jest publikowana**; udostępniana na
żądanie recenzenta lub redakcji, za zgodą osoby, której dane dotyczą.

## Dlaczego nie „poprawiono cicho"

Bo wtedy pieczęć nie byłaby nic warta. Sens prerejestracji polega na tym, że
suma kontrolna albo się zgadza, albo istnieje jawny zapis mówiący dlaczego nie.
Milcząca zmiana zawartości przy zachowanej starej sumie byłaby gorsza niż brak
pieczęci — sugerowałaby gwarancję, której nie ma.

## Wniosek proceduralny do przyszłych badań

Audyt danych osobowych należy do **listy kontrolnej pieczęci**, a nie do
czynności po niej. Wpisano to do `seal/CHECKLIST-PIECZEC.md` jako pozycję
wykonywaną przed nadaniem tagu. Koszt przeoczenia: rozspójniona plomba
i konieczność tego aneksu.
