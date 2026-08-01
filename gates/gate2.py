"""GATE 2 - analiza konfirmacyjna wg zamrozonej hierarchii (protokol par. 6).

To jest jedyne miejsce, w ktorym wolno policzyc kontrasty konfirmacyjne.
Kod powstal PRZED istnieniem progow lambda* dla korpusu glownego, czyli przed
mozliwoscia zobaczenia jakiejkolwiek liczby endpointu glownego - to jest sens
prerejestracji, a nie formalnosc.

HIERARCHIA ZAMKNIETA (par. 6, po usunieciu H5 w rundzie 3):

    H1 (C - C'-G)  ->  H2 (C'-G - C'-U)  ->  H3 (C - B)
                                              ->  {H4 TOST (B-A na lambda1/tr),
                                                   kontrast C-A, kontrast B-A,
                                                   profil warstwowy}

Pierwsze niezaliczenie ZATRZYMUJE lancuch: nic ponizej nie jest konfirmacyjne.
Kroki po zatrzymaniu liczone sa mimo to, ale oznaczone jako OPISOWE - ukrycie
ich byloby selektywnym raportowaniem, a awansowanie ich na konfirmacyjne
zlamaniem hierarchii.

REPLIKI JEZYKOWE (par. 3): PL i EN to OSOBNE prerejestrowane repliki - osobna
hierarchia, osobne alfa, meta-porownanie wylacznie opisowe. Zadnego laczenia
w pule: to nie jest jeden test o wiekszym n.

Uruchomienie:
    python -m gates.gate2 --measurements measurements-glowny
"""

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from power.permutation import paired_permutation_test
from power.tost import paired_tost_equivalence

ALPHA = 0.01
N_PERM = 10000
CI_LEVEL = 0.99
MAIN_VARIANTS = ("A", "B", "C", "CprimG", "CprimU")

# Kolejnosc ma znaczenie prawne wobec protokolu - nie sortowac, nie przestawiac.
HIERARCHY = [
    ("H1", "C", "CprimG", "GLOWNA - sygnatura samozwrotnosci wzgl. odniesienia osadzonego"),
    ("H2", "CprimG", "CprimU", "diagnostyczna - wklad samego osadzenia referencyjnego"),
    ("H3", "C", "B", "wtorna - insercja meta wzgl. insercji neutralnej"),
]
# Rodzina po zaliczeniu H3 (kolejnosc wewnatrz rodziny bez znaczenia).
FAMILY = [
    ("C-A", "C", "A", "kontrast opisowy szerokich klas dyskursu"),
    ("B-A", "B", "A", "kontrast kontrolny insercji neutralnej"),
]


def load_band(measurements_dir):
    """Zbior warstw pasma z pomiaru (in_band ustawione przez runner wg config)."""
    m = pd.read_parquet(Path(measurements_dir) / "metrics.parquet")
    band = sorted(m.loc[m.in_band, "hidden_state_index"].unique().tolist())
    if not band:
        raise ValueError("pomiar nie zawiera ani jednej warstwy w pasmie")
    return band, m


def load_lambda_star(measurements_dir):
    """lambda* per (scenariusz, jezyk, warstwa) - T' rozni sie miedzy tekstami."""
    p = Path(measurements_dir) / "t5_lambda_star.parquet"
    if not p.exists():
        raise FileNotFoundError(
            f"brak {p} - T5 (null symulacyjny) dla tego korpusu nie jest policzony. "
            "GATE 2 nie moze ruszyc: I_total bez lambda* jest tozsamosciowo zerem."
        )
    t = pd.read_parquet(p)
    return {(r.scenario_id, r.language, int(r.hidden_state_index)): float(r.lambda_star)
            for r in t.itertuples()}


def check_coverage(spectra, lam, band):
    """Kazdy tekst x warstwa pasma musi miec swoj prog. Braki = STOP."""
    need = spectra[spectra.hidden_state_index.isin(band)]
    missing = [(r.scenario_id, r.language, int(r.hidden_state_index))
               for r in need.itertuples()
               if (r.scenario_id, r.language, int(r.hidden_state_index)) not in lam]
    return sorted(set(missing))


def per_text_endpoints(spectra, lam, band):
    """Ī = srednia I_total po pasmie + lambda1/tr (dla H4), jeden wiersz na tekst."""
    rows = []
    inb = spectra[spectra.hidden_state_index.isin(band)]
    for (sid, lang, variant, nul), g in inb.groupby(
            ["scenario_id", "language", "variant", "null"], dropna=False):
        iot, lam1 = [], []
        for r in g.itertuples():
            e = np.asarray(r.eigenvalues, dtype=np.float64)
            ls = lam[(r.scenario_id, r.language, int(r.hidden_state_index))]
            tr = e.sum()
            iot.append(float(e[e > ls].sum() / tr))
            lam1.append(float(e.max() / tr))
        rows.append({"scenario_id": sid, "language": lang, "variant": variant,
                     "null": nul, "iota": float(np.mean(iot)),
                     "lambda1_share": float(np.mean(lam1)),
                     "n_layers": len(iot)})
    return pd.DataFrame(rows)


def paired_diffs(df, lang, var_a, var_b, column="iota"):
    """Roznice parowane wewnatrz scenariusza; jednostka inferencji = scenariusz."""
    d = df[(df.language == lang) & (df["null"].isna())]
    piv = d.pivot_table(index="scenario_id", columns="variant", values=column)
    for v in (var_a, var_b):
        if v not in piv.columns:
            raise ValueError(f"brak wariantu {v} w replice {lang}")
    pair = piv[[var_a, var_b]].dropna()
    return pair[var_a].to_numpy() - pair[var_b].to_numpy(), pair.index.tolist()


def layer_profile_cluster(spectra, lam, band, lang, var_a, var_b,
                          n_permutations=N_PERM, rng=None):
    """Profil warstwowy: permutacja klastrowa po CIAGLEJ osi warstw (par. 6).

    Bez arbitralnych pasm w konfirmacji. Znakowanie jest wspolne dla wszystkich
    warstw danego scenariusza - inaczej zniszczyloby korelacje miedzy warstwami,
    czyli dokladnie te strukture, ktora klastrowanie ma wykorzystac.
    """
    if rng is None:
        rng = np.random.default_rng()
    inb = spectra[spectra.hidden_state_index.isin(band) & (spectra.language == lang)
                  & (spectra["null"].isna())]
    per = {}
    for r in inb.itertuples():
        e = np.asarray(r.eigenvalues, dtype=np.float64)
        ls = lam[(r.scenario_id, r.language, int(r.hidden_state_index))]
        per[(r.scenario_id, r.variant, int(r.hidden_state_index))] = \
            float(e[e > ls].sum() / e.sum())

    scen = sorted({k[0] for k in per})
    scen = [s for s in scen
            if all((s, v, l) in per for v in (var_a, var_b) for l in band)]
    if not scen:
        return None
    D = np.array([[per[(s, var_a, l)] - per[(s, var_b, l)] for l in band] for s in scen])

    def cluster_mass(mat):
        m, sd = mat.mean(axis=0), mat.std(axis=0, ddof=1)
        t = np.divide(m, sd, out=np.zeros_like(m), where=sd > 0) * np.sqrt(mat.shape[0])
        thr = 1.0  # prog formowania klastra na skali t; masa = suma t w klastrze
        best, run = 0.0, 0.0
        for v in t:
            run = run + v if v > thr else 0.0
            best = max(best, run)
        return best, t

    obs, t_obs = cluster_mass(D)
    null = np.empty(n_permutations)
    for i in range(n_permutations):
        s = rng.choice([-1.0, 1.0], size=(D.shape[0], 1))
        null[i], _ = cluster_mass(s * D)
    p = float((np.sum(null >= obs) + 1) / (n_permutations + 1))
    return {"cluster_mass": float(obs), "p_value": p, "n_scenarios": len(scen),
            "layers": list(map(int, band)), "t_per_layer": [float(x) for x in t_obs]}


def run_replica(df, spectra, lam, band, lang, seed=20260801):
    """Pelna hierarchia dla jednej repliki jezykowej."""
    rng = np.random.default_rng(seed)
    out = {"language": lang, "steps": [], "stopped_at": None}
    gate_open = True

    for name, va, vb, desc in HIERARCHY:
        diffs, scen = paired_diffs(df, lang, va, vb)
        res = paired_permutation_test(diffs, n_permutations=N_PERM,
                                      ci_level=CI_LEVEL, rng=rng)
        passed = res["p_value"] < ALPHA
        step = {"step": name, "contrast": f"{va}-{vb}", "opis": desc,
                "confirmatory": gate_open, "passed": bool(passed),
                "alpha": ALPHA, "n_scenarios": len(scen), **res}
        if gate_open and not passed:
            # Werdykt "praktycznie wykluczony" wymaga zaliczonego TOST (ANEKS-2).
            step["tost"] = paired_tost_equivalence(diffs, rng=rng)
            step["verdict"] = ("efekt praktycznie wykluczony"
                               if step["tost"]["equivalent"] else "niekonkluzywny")
            out["stopped_at"] = name
            gate_open = False
        elif gate_open:
            step["verdict"] = "efekt potwierdzony"
        else:
            step["verdict"] = "OPISOWY (poza hierarchia - lancuch zatrzymany wyzej)"
        out["steps"].append(step)

    for name, va, vb, desc in FAMILY:
        diffs, scen = paired_diffs(df, lang, va, vb)
        res = paired_permutation_test(diffs, n_permutations=N_PERM,
                                      ci_level=CI_LEVEL, rng=rng)
        out["steps"].append({"step": name, "contrast": f"{va}-{vb}", "opis": desc,
                             "confirmatory": gate_open, "n_scenarios": len(scen),
                             "passed": bool(res["p_value"] < ALPHA), **res})

    # H4: rownowaznosc B-A na udziale modu glownego lambda1/tr.
    d4, _ = paired_diffs(df, lang, "B", "A", column="lambda1_share")
    out["H4"] = {"contrast": "B-A (lambda1/tr)", "confirmatory": gate_open,
                 **paired_tost_equivalence(d4, rng=rng)}

    out["profil_warstwowy"] = layer_profile_cluster(
        spectra, lam, band, lang, "C", "CprimG", rng=rng)
    out["profil_warstwowy_confirmatory"] = gate_open
    return out


def main():
    ap = argparse.ArgumentParser(description="GATE 2 - analiza konfirmacyjna")
    ap.add_argument("--measurements", default="measurements-glowny")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    mdir = Path(args.measurements)
    band, _ = load_band(mdir)
    lam = load_lambda_star(mdir)
    spectra = pd.read_parquet(mdir / "spectra.parquet")

    missing = check_coverage(spectra, lam, band)
    if missing:
        raise SystemExit(
            f"STOP: brak lambda* dla {len(missing)} par (tekst, warstwa), np. "
            f"{missing[:3]}. Uruchomienie na czesciowych progach dalo by endpoint "
            "policzony rozna miara dla roznych scenariuszy."
        )

    df = per_text_endpoints(spectra, lam, band)
    results = {"alpha": ALPHA, "n_permutations": N_PERM, "ci_level": CI_LEVEL,
               "band_hidden_state_index": band, "replicas": []}
    for lang in sorted(df.language.unique()):
        results["replicas"].append(run_replica(df, spectra, lam, band, lang))

    out = Path(args.out or (mdir / "gate2_results.json"))
    out.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[gate2] zapisane: {out}")
    for r in results["replicas"]:
        h1 = r["steps"][0]
        print(f"[gate2] {r['language']}: H1 p={h1['p_value']:.5f} "
              f"d_z={h1['d_z']:.3f} -> {h1['verdict']}")


if __name__ == "__main__":
    main()
