# Raport kwalifikacji sprzętu — SPEKTRA-1

**Werdykt: KWALIFIKUJE SIE**

Maszyna: Apple M5 Max | pamięć: 128.0 GB | urządzenie obliczeniowe: `mps`
System: macOS-26.5.2-arm64-arm-64bit-Mach-O | Python 3.14.6 | torch 2.9.1 | transformers 5.14.1

| Test | Wynik |
|---|---|
| B. GATE 0 (białe widmo vs teoria) | PASS — krawędzie pomiar 0.370–6.498 wobec teorii 0.338–6.662 |
| C. Powtarzalność forwardu | PASS — max różnica 0.00e+00; powtarzalnosc CO DO BITU |
| F. Sumy kontrolne wag i tokenizera | PASS — wszystkie 7 plików zgodnych co do bajtu |
| D. Struktura modelu | PASS — 35 stanów, wymiar 2560, torch.bfloat16 |
| E. Tempo | 0.26 s/tekst → ~0.1 h na pełny pomiar (624 teksty × 2 przebiegi) |

## Co ten werdykt znaczy

- **KWALIFIKUJE SIĘ** — maszyna liczy powtarzalnie i zgodnie z teorią; można na niej wykonać replikację spełniającą rygor pieczęci.
- **WYMAGA DECYZJI ZESPOŁU** — najczęściej brak powtarzalności co do bitu na akceleratorze. To NIE dyskwalifikuje maszyny: pomiar można wykonać na procesorze (wolniej, ale deterministycznie) albo zamrozić łagodniejsze kryterium replikacji. Decyzja należy do zespołu badawczego, nie do operatora.
