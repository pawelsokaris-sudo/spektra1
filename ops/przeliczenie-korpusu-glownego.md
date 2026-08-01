# Przeliczenie korpusu głównego — POWTÓRKA po rundzie wyrównawczej

**Zlecenie:** SPEKTRA-1/06bis (procedura wg `ops/DEP-zlecenie-06-przeliczenie-korpusu-glownego.md`)
**Wykonał:** DEP (Claude Code w terminalu)
**Data:** 2026-07-31
**Maszyna:** `maszyna-pomiarowa` przez Tailscale
**Runda wyrównawcza:** commit `9a68279`
**Poprzedni przebieg (przed rundą):** w historii gita, commit `d88f5b6`.

## Trzy kryteria — WSZYSTKIE PRZESZŁY

| Kryterium | Werdykt |
|---|---|
| 1. Zero scenariuszy powyżej 2% | **PRZESZŁO** — zero wystąpień `⚠ ponad próg 2%`; walidator kod 0, „WSZYSTKIE SCENARIUSZE OK" |
| 2. Brak `⚠ PRZECHYŁ JEDNOKIERUNKOWY` | **PRZESZŁO** — **zero ostrzeżeń w całym raporcie**, we wszystkich trzech kontrastach i obu replikach |
| 3. Średnia ze znakiem, kontrast główny | **EN: −0,01%** · **PL: −0,20%** |

Licznik: **DOKŁADNY**, 64 scenariusze (32 EN + 32 PL).

**To nie jest zgaszenie detektora — to realna naprawa.** Angielska średnia w kontraście głównym
spadła z **−0,43% na −0,01%**, czyli praktycznie do zera, i to przy mieszanych znakach
(13 dodatnich, 15 ujemnych, 4 zera). Ostrzegałem w poprzednim raporcie, że kryterium 2 dałoby się
spełnić pozornie, odwracając jeden scenariusz z 32 i zostawiając średnią bez zmian. Tak się
**nie** stało.

## Wszystkie kontrasty, oba języki

| Kontrast | EN: znaki / średnia | PL: znaki / średnia |
|---|---|---|
| **C − C′-G** (główny) | 13 / 15 / 4 zera · **−0,01%** | 10 / 17 / 5 zer · **−0,20%** |
| **C′-G − C′-U** (diagnostyczny) | 6 / 19 / 7 zer · **−0,15%** | 10 / 20 / 2 zera · **−0,23%** |
| **C − B** (wtórny) | 11 / 13 / 8 zer · **−0,04%** | 5 / 20 / 7 zer · **−0,12%** |

Zgodnie z prośbą raportuję też średnie kontrastu wtórnego C − B, choć kryterium 2 formalnie
go nie obejmuje: **EN −0,04%, PL −0,12%**. W poprzednim przebiegu ten kontrast był przechylony
w komplecie w obu językach (EN 1/30, PL 5/25) — teraz znaki są mieszane w obu i średnie zeszły
blisko zera. To był cel postawiony w zleceniu i został osiągnięty.

**Porównanie przed/po dla wszystkich sześciu pozycji:**

| Kontrast / język | przed rundą | po rundzie |
|---|---|---|
| C − C′-G, EN | −0,43% ⚠ przechył | **−0,01%** czysto |
| C − C′-G, PL | −0,26% czysto | **−0,20%** czysto |
| C′-G − C′-U, EN | +0,03% czysto | −0,15% czysto |
| C′-G − C′-U, PL | −0,20% czysto | −0,23% czysto |
| C − B, EN | −0,39% ⚠ przechył | **−0,04%** czysto |
| C − B, PL | −0,48% ⚠ przechył | **−0,12%** czysto |

Trzy ostrzeżenia zgasły, a żadna pozycja się nie pogorszyła w sposób, który miałby znaczenie —
największa zmiana „w złą stronę" to diagnostyczny EN z +0,03% na −0,15%, czyli nadal blisko zera
i z mieszanymi znakami. **Najsłabszą pozostałą liczbą jest diagnostyczny PL: −0,23%.**

## Procedura i kontrole

```
warunek startu:  repo czyste, 64 scenariusze zacommitowane, walidator lokalny kod 0,
                 testy 114 zielonych
paczka:          374 556 B, 174 pliki; wykluczenia czyste (.git/ __pycache__ .venv .claude
                 measurements/ tokenizer.json .parquet .npz) — pusto
scenariusze:     w paczce pl 32 / en 32, na maszynie pl 32 / en 32
tokenizer:       JEST przed podmianą, tokenizer.json po podmianie
archiwum:        ROZPAKOWANO-I-USUNIETO
sumy kontrolne:  40/40 zgodnych (pipeline, corpus, nulls, power, tests + config.yaml)
```

Cztery pliki wymagane wprost przez zlecenie — sumy na maszynie zgodne z laptopem:
`build.py 1e31b86cca4af9ce` · `insertion_tokens.py 7b54b6a7a0cb4fb2` ·
`report.py 77befc445deb6e21` · `validate.py b20f55f1b67cbf04`.

---

## ⚠️ Ustalenie, które NIE dotyczy korpusu, ale dotyczy pieczęci

Bramka korpusowa jest domknięta. Ale przy okazji tej rundy powstała **nowa** rozbieżność
i chcę ją postawić przed złożeniem pieczęci, a nie po.

**Runda wyrównawcza `9a68279` zmieniła wszystkie 16 scenariuszy pilota.** Zmieniła pola
`self`, `neutral`, `external_grounded` i `external_ungrounded` — czyli **wszystkie warianty
z insercjami**. Nietknięte zostały tylko tury bazowe, więc wariant A jest identyczny.

Konsekwencja arytmetyczna:

```
wariant A (bez insercji, nietknięty):        16 tekstów
warianty B, C, C′-G, C′-U (tekst zmieniony): 64 teksty
nulle N1/N2 pochodne od nich:               128 tekstów
------------------------------------------------------
NIEAKTUALNE: 192 z 208 tekstów pilota (92%)
```

W 26 z 80 tekstów głównych zmieniła się nawet **liczba tokenów** (reszta zmieniła słowa przy tej
samej długości). Liczba tur nie zmieniła się w żadnym scenariuszu, więc struktura okien jest
stabilna — ale teksty nie są te same.

**Czego to dotyczy.** Wszystkie artefakty pomiarowe pilota są kluczowane po tych 16 scenariuszach:

| Plik | Wiersze | Co zawiera |
|---|---|---|
| `measurements/metrics.parquet` | 7 072 | metryki pilota, 208 tekstów × 34 warstwy |
| `measurements/spectra.parquet` | 7 072 | widma |
| `measurements/dlag_sentence.parquet` | 2 912 | D_lag zdaniowy |
| `measurements/discourse.parquet` | 2 912 | metryka dyskursu |
| `measurements/t5_lambda_star.parquet` | 224 | **progi λ\* per (scenariusz, warstwa)** |

Wszystkie policzone na tekstach, których w zapieczętowanym korpusie **już nie ma**.

**Dlaczego to ma znaczenie mimo że pilot jest wyłączony z analizy głównej.** Zgoda co do tego,
że pilot nie wchodzi do wyniku — służy estymacji wariancji, ICC i parametrów nullu. Problem jest
inny i dotyczy **odtwarzalności**: ktoś, kto weźmie zapieczętowany korpus i uruchomi tego samego
runnera, **nie odtworzy** `metrics.parquet`. Dla pakietu, którego sensem jest weryfikowalność,
to jest realna dziura — i to taka, którą recenzent znajdzie w pięć minut, porównując sumy
kontrolne scenariuszy z datą pomiaru.

Osobno: `t5_lambda_star.parquet` to progi wyestymowane z tych właśnie tekstów. Liczba tur się
nie zmieniła, więc `T'` prawdopodobnie zostało, ale sama estymacja nullu pochodzi z innych danych
niż te w korpusie.

**Trzy drogi, decyzja nie moja:**

1. **Przeliczyć pilota na poprawionym korpusie.** Koszt czasowy jest znany z pomiarów:
   pomiar główny pilota 2 h 45 min + D_lag zdaniowy ~1 h 20 min + dyskurs ~5 min + T5 ~4 h 20 min,
   czyli **około 8,5 godziny** maszyny. Karta jest wolna, wszystkie cztery zadania w Harmonogramie
   gotowe. To jedyna droga dająca pełną odtwarzalność.
2. **Zapieczętować z jawną adnotacją**, że artefakty pilota odpowiadają rewizji korpusu `d88f5b6`
   (sprzed rundy), a nie rewizji pieczętowanej. Uczciwe, tanie, ale osłabia obietnicę
   „ten sam runner odtworzy wynik".
3. **Uznać pilota za dane kalibracyjne historyczne** i udokumentować, że jego rolą było wyłącznie
   ustawienie parametrów, nie wejście do wyniku.

Nie rekomenduję żadnej z nich jako operator — to jest rozstrzygnięcie protokolarne. Zwracam
tylko uwagę, że opcja 1 kosztuje jedną noc maszyny, a opcje 2 i 3 kosztują zdanie w manifeście,
którego recenzent nie przeoczy.

## Co odesłane do repo

| Plik | Rozmiar |
|---|---|
| `corpus/matching_report.md` | 14 313 B (nadpisany, komplet 64, DOKŁADNY) |
| `ops/insertion_tokens_glowny.txt` | 47 839 B (dane per insercja) |
| `ops/validate-glowny.txt` | 5 336 B (pełne wyjście `corpus.validate`) |

Żaden plik tokenizera ani wag nie trafił na laptopa. Zakres zmian na maszynie: wyłącznie
wewnątrz `C:\Users\operator\spektra1`, archiwum transferowe usunięte.

## Podsumowanie

**Bramka korpusowa: domknięta.** Trzy kryteria przeszły, cel postawiony w zleceniu — średnie
przy zerze w obu językach i mieszane znaki we wszystkich kontrastach — osiągnięty realnie,
nie formalnie.

**Do rozstrzygnięcia przed pieczęcią:** status artefaktów pilota, które opisują teksty
nieobecne w pieczętowanym korpusie (192 z 208).
