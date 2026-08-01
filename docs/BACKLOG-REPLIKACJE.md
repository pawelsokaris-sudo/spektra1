# Backlog replikacji (po GATE 4 — zero implementacji wcześniej)

## SPEKTRA-1c: skala — Gemma 3 27B na maszynie Apple (128 GB)
**Zielone światło 2026-08-01:** zgoda właściciela maszyny TAK, zasoby (dysk/sieć) TAK.

- **Model:** google/gemma-3-27b-it, bf16, bez kwantyzacji (~54 GB wag, margines >2x).
  Ten sam ród co 1a => izoluje SKALĘ jako jedyną zmienną.
- **Korpus:** BEZ ZMIAN — rodzina Gemma 3 dzieli tokenizer między rozmiarami,
  więc parowanie wtrąceń (3 rundy pracy) zachowuje waznosc. WERYFIKACJA TWARDA:
  porownac SHA-256 tokenizer.json 27B z zapieczetowanym 4B; przy roznicy —
  pelna rewalidacja korpusu przed pomiarem.
- **Model pracy: KOPERTA (zero zdalnego dostepu).** Maszyna pod nadzorem
  korporacyjnym. Repo + jednorazowa konfiguracja + jedna komenda wieczorami;
  aplikacja po kazdym etapie pakuje i wysyla wyniki (glownie: wydanie w repo
  publicznym; zapas: paczka z suma kontrolna do przekazania recznie).
- **Wymogi narzedzia (bo nie mozna debugowac na zywo):** pierwszy wieczor =
  egzamin sprzetu (GATE 0 + replikacja bitowa na Apple) z prawem ODMOWY pomiaru;
  raport po kazdym etapie; komunikaty dla czlowieka; wznowienie ta sama komenda.
- **Rytm:** start wieczorem, stop kiedykolwiek (checkpoint per tekst), kilka sesji.
- **Otwarte przed startem:** determinizm backendu Apple (Metal) — jesli nie
  przechodzi, pomiar na CPU (128 GB pozwala, wolniej ale poprawnie).
- **Formalnie:** OSOBNA prerejestracja i pieczec. Nie post-hoc.

## SPEKTRA-1b: rodzina — model ~3B innej rodziny na RTX 5080
Punkt Groka. Qwen2.5-3B / Llama-3.2-3B / Phi-3.5-mini. Odpowiada na pytanie
"wlasnosc Gemmy czy modeli w ogole". UWAGA KOSZTOWA: inny tokenizer =>
korpus wymaga rewalidacji i prawdopodobnie rundy dostrajania wtracen.
Osobna prerejestracja.

## Kolejnosc
GATE 4 (publikacja 1a) -> narzedzie-koperta (raz, sluzy wszystkim replikacjom)
-> 1c (skala, Apple) -> 1b (rodzina, RTX). Docelowo: pakiet uruchamialny
przez dowolna osoba na swiecie jedna komenda.
