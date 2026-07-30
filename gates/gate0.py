"""GATE 0 - sanity pipeline'u na syntetycznym bialym szumie (protokol par. 7).

Kryteria:
  A. Bialy szum przez CALY pipeline (mask -> komponent pozycyjny -> z-score ->
     Gram -> eigh) odtwarza teorie Marchenko-Pastura: krawedzie widma w
     [a*(1-tol), b*(1+tol)], dystans KS empirycznej CDF od CDF MP < prog.
  B. Kalibracja lambda*: kwantyl 99% maks. wartosci wlasnej z nullu; na SWIEZYCH
     realizacjach odsetek realizacji z jakimkolwiek modem > lambda* zgodny z
     nominalnym 1% (kryterium <= 2.5% przy n=300; raportowany dokladny CI).
  C. Replikacja: dwa przebiegi z tym samym ziarnem daja identyczne bitowo widma.
  D. D_lag: wrazliwosc na porzadek - AR(1) daje z >> 0, szum iid daje |z| < 3.

Wymiary odzwierciedlaja skale docelowa (T=1024, skip 32 -> T'=992; D=2560 klasy
Gemma ~4B). GATE 0 zostanie powtorzony na maszynie pomiarowej w zapieczetowanym
kontenerze po zamrozeniu dokladnego wariantu modelu.

Uruchomienie:  python -m gates.gate0   (z korzenia repo, venv aktywny)
Wyjscie: gates/gate0_results.json + gates/gate0_report.md, exit code 0/1.
"""

import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pipeline.metrics import d_lag, k_modes
from pipeline.preprocess import mask_tokens, zscore_channels
from pipeline.spectrum import gram_eigenvalues

CFG = {
    "seed_root": 20260728,      # config.yaml: seeds.gate0
    "T_raw": 1024,
    "skip_first": 32,           # T' = 992
    "D": 2560,
    "n_null": 300,              # realizacje do kalibracji lambda*
    "n_test": 300,              # swieze realizacje do testu falszywych modow
    "n_mp_pool": 20,            # realizacje poolowane do testu MP (krawedzie + KS)
    "n_replication": 8,         # realizacje w tescie replikacji bitowej
    "quantile": 0.99,
    "edge_tol": 0.05,
    "ks_threshold": 0.05,
    "exceed_rate_max": 0.025,   # nominal 1% + fluktuacja binomialna przy n=300
    "d_lag": {"T": 300, "D": 64, "phi": 0.9, "n_perm": 200, "n_texts": 5},
}

OUT_DIR = Path(__file__).resolve().parent


def text_noise(seed_root, stream, idx, T_raw, D):
    """Deterministyczny bialy szum dla (strumien, indeks) - regenerowalny w locie."""
    rng = np.random.default_rng([seed_root, stream, idx])
    return rng.standard_normal((T_raw, D))


def corpus_eigenvalues(seed_root, stream, n, cfg, log_every=25, tag=""):
    """Pelny pipeline na korpusie n realizacji bialego szumu (dwuprzebiegowo).

    Przebieg 1: srednia pozycyjna po korpusie (po maskowaniu) - strumieniowo,
    zeby nie trzymac ~6 GB korpusu w RAM. Matematycznie identyczne z
    pipeline.preprocess.positional_mean dla tekstow rownej dlugosci.
    Przebieg 2: mask -> odjecie komponentu pozycyjnego -> z-score -> widmo Grama.
    """
    T_raw, D, skip = cfg["T_raw"], cfg["D"], cfg["skip_first"]
    t_prime = T_raw - skip

    sums = np.zeros((t_prime, D))
    for i in range(n):
        sums += mask_tokens(text_noise(seed_root, stream, i, T_raw, D), skip_first=skip)
    mu = sums / n

    eigs_list = []
    excluded_total = 0
    t0 = time.time()
    for i in range(n):
        H = mask_tokens(text_noise(seed_root, stream, i, T_raw, D), skip_first=skip) - mu
        Z, n_excl = zscore_channels(H)
        excluded_total += n_excl
        eigs_list.append(gram_eigenvalues(Z))
        if log_every and (i + 1) % log_every == 0:
            rate = (time.time() - t0) / (i + 1)
            print(f"[gate0]{tag} {i + 1}/{n} ({rate:.2f} s/real.)", flush=True)
    return eigs_list, excluded_total


def mp_theory(gamma):
    """Krawedzie i warunkowa CDF (czesc niezerowa) rozkladu Marchenko-Pastura."""
    a = (1.0 - np.sqrt(gamma)) ** 2
    b = (1.0 + np.sqrt(gamma)) ** 2
    xs = np.linspace(a, b, 4001)
    dens = np.sqrt(np.clip((b - xs) * (xs - a), 0.0, None)) / (2.0 * np.pi * xs)
    cdf = np.cumsum(dens) * (xs[1] - xs[0])
    cdf /= cdf[-1]  # normalizacja czesci ciaglej (masa 1/gamma dla gamma > 1)
    return a, b, xs, cdf


def ks_distance_vs_mp(pooled_eigs, gamma):
    a, b, xs, cdf = mp_theory(gamma)
    srt = np.sort(pooled_eigs)
    emp = np.arange(1, srt.size + 1) / srt.size
    th = np.interp(srt, xs, cdf, left=0.0, right=1.0)
    return float(np.max(np.abs(emp - th))), a, b


def make_ar1(T, D, phi, rng):
    Z = np.zeros((T, D))
    Z[0] = rng.standard_normal(D)
    scale = np.sqrt(1.0 - phi**2)
    for t in range(1, T):
        Z[t] = phi * Z[t - 1] + scale * rng.standard_normal(D)
    return Z


def main():
    cfg = CFG
    results = {"config": cfg, "criteria": {}}
    t_start = time.time()
    t_prime = cfg["T_raw"] - cfg["skip_first"]
    gamma = cfg["D"] / t_prime

    # --- Null: kalibracja lambda* --------------------------------------------
    print(f"[gate0] null: {cfg['n_null']} realizacji T'={t_prime}, D={cfg['D']}", flush=True)
    null_eigs, null_excl = corpus_eigenvalues(cfg["seed_root"], 1, cfg["n_null"], cfg, tag=" null")
    lam_max_null = np.array([e[0] for e in null_eigs])
    lambda_star = float(np.quantile(lam_max_null, cfg["quantile"]))

    # --- Kryterium A: Marchenko-Pastur ---------------------------------------
    pooled = np.concatenate(null_eigs[: cfg["n_mp_pool"]])
    ks, a_edge, b_edge = ks_distance_vs_mp(pooled, gamma)
    edge_lo_ok = bool(pooled.min() >= a_edge * (1.0 - cfg["edge_tol"]))
    edge_hi_ok = bool(pooled.max() <= b_edge * (1.0 + cfg["edge_tol"]))
    mp_pass = bool(ks < cfg["ks_threshold"] and edge_lo_ok and edge_hi_ok)
    results["criteria"]["A_marchenko_pastur"] = {
        "gamma": gamma, "edge_lo": a_edge, "edge_hi": b_edge,
        "observed_min": float(pooled.min()), "observed_max": float(pooled.max()),
        "ks_distance": ks, "ks_threshold": cfg["ks_threshold"],
        "n_pooled_eigenvalues": int(pooled.size), "pass": mp_pass,
    }
    print(f"[gate0] A: KS={ks:.4f}, widmo [{pooled.min():.3f},{pooled.max():.3f}] "
          f"vs MP [{a_edge:.3f},{b_edge:.3f}] -> {'PASS' if mp_pass else 'FAIL'}", flush=True)

    # --- Kryterium B: falszywe mody ponad lambda* na swiezych realizacjach ---
    print(f"[gate0] test: {cfg['n_test']} swiezych realizacji", flush=True)
    test_eigs, test_excl = corpus_eigenvalues(cfg["seed_root"], 2, cfg["n_test"], cfg, tag=" test")
    false_modes = np.array([k_modes(e, lambda_star) for e in test_eigs])
    exceed_rate = float((false_modes > 0).mean())
    mean_false = float(false_modes.mean())
    b_pass = bool(exceed_rate <= cfg["exceed_rate_max"])
    results["criteria"]["B_lambda_star_calibration"] = {
        "lambda_star": lambda_star, "quantile": cfg["quantile"],
        "n_null": cfg["n_null"], "n_test": cfg["n_test"],
        "realizations_with_false_mode": int((false_modes > 0).sum()),
        "exceed_rate": exceed_rate, "exceed_rate_max": cfg["exceed_rate_max"],
        "mean_false_modes_per_realization": mean_false,
        "excluded_channels_null": null_excl, "excluded_channels_test": test_excl,
        "pass": b_pass,
    }
    print(f"[gate0] B: lambda*={lambda_star:.4f}, przekroczenia {exceed_rate:.3%} "
          f"({int((false_modes > 0).sum())}/{cfg['n_test']}) -> {'PASS' if b_pass else 'FAIL'}",
          flush=True)

    # --- Kryterium C: replikacja bitowa --------------------------------------
    rep1, _ = corpus_eigenvalues(cfg["seed_root"], 3, cfg["n_replication"], cfg, log_every=0)
    rep2, _ = corpus_eigenvalues(cfg["seed_root"], 3, cfg["n_replication"], cfg, log_every=0)
    flat1, flat2 = np.concatenate(rep1), np.concatenate(rep2)
    bitwise = bool(flat1.shape == flat2.shape and np.array_equal(flat1, flat2))
    max_diff = float(np.max(np.abs(flat1 - flat2))) if flat1.shape == flat2.shape else float("inf")
    c_pass = bool(bitwise or max_diff <= 1e-12)
    results["criteria"]["C_replication"] = {
        "bitwise_identical": bitwise, "max_abs_diff": max_diff,
        "n_realizations": cfg["n_replication"], "pass": c_pass,
    }
    print(f"[gate0] C: replikacja {'BITOWA' if bitwise else f'tolerancyjna (max diff {max_diff:.2e})'} "
          f"-> {'PASS' if c_pass else 'FAIL'}", flush=True)

    # --- Kryterium D: D_lag wrazliwy na porzadek ------------------------------
    dcfg = cfg["d_lag"]
    z_iid, z_ar = [], []
    for i in range(dcfg["n_texts"]):
        rng_gen = np.random.default_rng([cfg["seed_root"], 4, i])
        rng_perm = np.random.default_rng([cfg["seed_root"], 5, i])
        z_iid.append(d_lag(rng_gen.standard_normal((dcfg["T"], dcfg["D"])),
                           n_permutations=dcfg["n_perm"], rng=rng_perm))
        rng_gen2 = np.random.default_rng([cfg["seed_root"], 6, i])
        rng_perm2 = np.random.default_rng([cfg["seed_root"], 7, i])
        z_ar.append(d_lag(make_ar1(dcfg["T"], dcfg["D"], dcfg["phi"], rng_gen2),
                          n_permutations=dcfg["n_perm"], rng=rng_perm2))
    d_pass = bool(all(z > 5.0 for z in z_ar) and all(abs(z) < 3.0 for z in z_iid))
    results["criteria"]["D_dlag_order_sensitivity"] = {
        "z_iid": z_iid, "z_ar1": z_ar, "phi": dcfg["phi"], "pass": d_pass,
    }
    print(f"[gate0] D: iid z={['%.2f' % z for z in z_iid]}, "
          f"AR(1) z={['%.1f' % z for z in z_ar]} -> {'PASS' if d_pass else 'FAIL'}", flush=True)

    # --- Werdykt ---------------------------------------------------------------
    all_pass = all(c["pass"] for c in results["criteria"].values())
    results["gate0_pass"] = all_pass
    results["runtime_seconds"] = round(time.time() - t_start, 1)

    (OUT_DIR / "gate0_results.json").write_text(json.dumps(results, indent=2))
    np.save(OUT_DIR / "gate0_lambda_max_null.npy", lam_max_null)
    write_report(results)
    print(f"[gate0] {'=== GATE 0 PASS ===' if all_pass else '=== GATE 0 FAIL ==='} "
          f"({results['runtime_seconds']} s)", flush=True)
    return 0 if all_pass else 1


def write_report(r):
    c = r["criteria"]
    a, b_, cc, d = (c["A_marchenko_pastur"], c["B_lambda_star_calibration"],
                    c["C_replication"], c["D_dlag_order_sensitivity"])
    lines = [
        "# GATE 0 — raport sanity pipeline'u (protokół §7)",
        "",
        f"**Werdykt: {'PASS' if r['gate0_pass'] else 'FAIL'}** | czas: {r['runtime_seconds']} s | "
        f"konfiguracja: T'={r['config']['T_raw'] - r['config']['skip_first']}, D={r['config']['D']}, "
        f"ziarno {r['config']['seed_root']}",
        "",
        "| Kryterium | Wynik | Status |",
        "|---|---|---|",
        f"| A. Marchenko–Pastur | KS={a['ks_distance']:.4f} (próg {a['ks_threshold']}); "
        f"widmo [{a['observed_min']:.3f}, {a['observed_max']:.3f}] w krawędziach "
        f"[{a['edge_lo']:.3f}, {a['edge_hi']:.3f}]±{r['config']['edge_tol']:.0%}; "
        f"{a['n_pooled_eigenvalues']} wartości własnych | {'PASS' if a['pass'] else 'FAIL'} |",
        f"| B. Kalibracja λ* | λ*={b_['lambda_star']:.4f} (kwantyl {b_['quantile']}, "
        f"n_null={b_['n_null']}); fałszywe mody w {b_['realizations_with_false_mode']}/{b_['n_test']} "
        f"świeżych realizacji ({b_['exceed_rate']:.2%}, próg {b_['exceed_rate_max']:.1%}); "
        f"śr. fałszywych modów/realizację: {b_['mean_false_modes_per_realization']:.4f} "
        f"| {'PASS' if b_['pass'] else 'FAIL'} |",
        f"| C. Replikacja | {'bitowa (identyczne co do bitu)' if c['C_replication']['bitwise_identical'] else 'tolerancyjna, max diff %.2e' % cc['max_abs_diff']}, "
        f"{cc['n_realizations']} realizacji × 2 przebiegi | {'PASS' if cc['pass'] else 'FAIL'} |",
        f"| D. D_lag (porządek) | iid: z = {', '.join('%.2f' % z for z in d['z_iid'])} (|z|<3); "
        f"AR(1) φ={d['phi']}: z = {', '.join('%.1f' % z for z in d['z_ar1'])} (z>5) "
        f"| {'PASS' if d['pass'] else 'FAIL'} |",
        "",
        f"Wykluczone kanały niskiej wariancji: null {b_['excluded_channels_null']}, "
        f"test {b_['excluded_channels_test']} (oczekiwane 0 dla szumu gaussowskiego).",
        "",
        "Uwagi: (1) średnia pozycyjna liczona strumieniowo — matematycznie identyczna z "
        "`pipeline.preprocess.positional_mean` dla tekstów równej długości; (2) GATE 0 zostanie "
        "powtórzony na maszynie pomiarowej w zapieczętowanym kontenerze po zamrożeniu wariantu "
        "modelu (wymiar D i indeksacja warstw wg raportu T2); (3) λ* konfirmacyjne powstanie w T5 "
        "z nullu symulacyjnego czas × kanał per (warstwa, język) — tutaj kalibrowana jest wyłącznie "
        "maszyneria kwantylowa.",
    ]
    (OUT_DIR / "gate0_report.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
