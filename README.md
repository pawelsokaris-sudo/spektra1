# SPEKTRA-1 — Widmowe sygnatury struktury korelacyjnej w warstwach ukrytych LLM

Badanie prerejestrowane. Źródło prawdy: [docs/SPEKTRA-1-protokol-FINAL.md](docs/SPEKTRA-1-protokol-FINAL.md) (v1.2-FINAL).

**Role:**
- Paweł (Sokaris / ActProof) — kierownik badania, decyzje, sprzęt, wykonanie
- Claude (chat prowadzący) — protokół, kod, statystyka, zlecenia
- DEP — wykonanie na maszynie pomiarowej (SSH): instalacje, uruchomienia
- Maszyna pomiarowa: komputer z RTX (rekonesans: `ops/`), forward Gemma bf16 przez `transformers`

**Struktura repo (per handoff T1):**

```
docs/         protokół v1.2 + rozstrzygnięcia recenzji + handoff (pakiet pieczęci)
corpus/       generator i korpusy: czwórki A/B/C/C′, PL i EN (T3)
pipeline/     pomiar widma: maskowanie → z-score → Gram → eigh → metryki (T4)
nulls/        null symulacyjny λ* + nulle interwencyjne N1–N2 (T5–T6)
power/        pilot, symulacja mocy, wybór M (GATE 1, T7)
gates/        testy bramek: GATE 0 sanity (MP na białym szumie), replikacja
seal/         pakiet pieczęci: hash, tag, checklist OSF (T8)
exploratory/  WYŁĄCZNIE analizy eksploracyjne z etykietą, nigdy przed konfirmacją
ops/          zlecenia dla DEP i raporty z maszyny pomiarowej
```

**Twarde zakazy (handoff):** zmiany n/M po obejrzeniu danych głównych; podpróbkowanie
kanałów w konfirmacji; analizy konfirmacyjne poza hierarchią H1→H2→{H3,H4,B−A,profil};
język „sygnatura samozwrotności" przed przejściem kontrastu C−C′.

**Status:** T1 w toku (szkielet ✓, lockfile+kontener czekają na rekonesans GPU — wersja
CUDA/torch zależy od karty i sterownika maszyny pomiarowej).
