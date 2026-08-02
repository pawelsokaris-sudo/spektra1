# T2 — semantyka warstw ukrytych (protokół §2)

**Model:** `CYFRAGOVPL/PLLuM-4B-instruct-2512` | rewizja: `domyślna` | bloków dekodera: **34** | elementów `hidden_states`: **35**

## Indeksacja (wchodzi do pieczęci)

- `hidden_states[0]` to **embedding** (różnica wobec wyjścia bloku 0: 12864.4121)
- `hidden_states[ℓ+1]` odpowiada wyjściu bloku ℓ: **NIEZGODNOŚĆ — patrz tabela** (tolerancja 0.01)
- Kształt: `(1, 1057, 2560)`, dtype: `torch.bfloat16`
- Embedding **wyłączony** z pasm pomiarowych zgodnie z §2.

## Final norm

hidden_states[-1] ROZNI SIE od wyjscia bloku - prawdopodobnie po final norm; wymaga decyzji przed pomiarem (max |Δ| = 151552.000000).

## Szablon czatu

ROZBIEZNOSC - korpus musi uzywac renderu tokenizera, inaczej mierzymy inny tekst niz zapisany. Poprawic PRZED pomiarem.

## Typy bloków i skład pasma [0.4L, 0.8L]

Pasmo obejmuje indeksy **13–26** (14 bloków). Skład: globalna: 2, lokalna: 12.

| Blok | Attention |
|---|---|
| 0 | lokalna |
| 1 | lokalna |
| 2 | lokalna |
| 3 | lokalna |
| 4 | lokalna |
| 5 | globalna |
| 6 | lokalna |
| 7 | lokalna |
| 8 | lokalna |
| 9 | lokalna |
| 10 | lokalna |
| 11 | globalna |
| 12 | lokalna |
| 13 | lokalna ← w paśmie |
| 14 | lokalna ← w paśmie |
| 15 | lokalna ← w paśmie |
| 16 | lokalna ← w paśmie |
| 17 | globalna ← w paśmie |
| 18 | lokalna ← w paśmie |
| 19 | lokalna ← w paśmie |
| 20 | lokalna ← w paśmie |
| 21 | lokalna ← w paśmie |
| 22 | lokalna ← w paśmie |
| 23 | globalna ← w paśmie |
| 24 | lokalna ← w paśmie |
| 25 | lokalna ← w paśmie |
| 26 | lokalna ← w paśmie |
| 27 | lokalna |
| 28 | lokalna |
| 29 | globalna |
| 30 | lokalna |
| 31 | lokalna |
| 32 | lokalna |
| 33 | lokalna |

Typ bloku wchodzi jako kowariancja do analiz wtórnych (rozstrzygnięcie #20, runda 1).

## Bloki niezgodne

| Blok | max |Δ| |
|---|---|
| 33 | 151552.000000 |