# GATE 0 — raport sanity pipeline'u (protokół §7)

**Werdykt: PASS** | czas: 275.4 s | konfiguracja: T'=992, D=2560, ziarno 20260728

| Kryterium | Wynik | Status |
|---|---|---|
| A. Marchenko–Pastur | KS=0.0014 (próg 0.05); widmo [0.363, 6.836] w krawędziach [0.368, 6.794]±5%; 19820 wartości własnych | PASS |
| B. Kalibracja λ* | λ*=6.8400 (kwantyl 0.99, n_null=1000); fałszywe mody w 21/1000 świeżych realizacji (2.10%); rozkład predykcyjny: E[X]=11.0, próg q0.995=26 (rachunek rangowy uwzględniający niepewność λ*); śr. fałszywych modów/realizację: 0.0210 | PASS |
| C. Replikacja | bitowa (identyczne co do bitu), 8 realizacji × 2 przebiegi | PASS |
| D. D_lag (porządek) | iid: z = 0.07, 1.47, 0.22, 0.34, -1.45 (|z|<3); AR(1) φ=0.9: z = 32.7, 52.8, 44.4, 40.5, 45.0 (z>5) | PASS |

Wykluczone kanały niskiej wariancji: null 0, test 0 (oczekiwane 0 dla szumu gaussowskiego).

Uwagi: (1) średnia pozycyjna liczona strumieniowo — matematycznie identyczna z `pipeline.preprocess.positional_mean` dla tekstów równej długości; (2) GATE 0 zostanie powtórzony na maszynie pomiarowej w zapieczętowanym kontenerze po zamrożeniu wariantu modelu (wymiar D i indeksacja warstw wg raportu T2); (3) λ* konfirmacyjne powstanie w T5 z nullu symulacyjnego czas × kanał per (warstwa, język) — tutaj kalibrowana jest wyłącznie maszyneria kwantylowa.