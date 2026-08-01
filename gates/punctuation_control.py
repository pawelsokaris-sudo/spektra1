"""Kontrola interpunkcyjna (wymog zamrozony w ANEKS-2).

Pytanie: czy wariant A da sie odroznic od wariantow dialogowych na SAMEJ
interpunkcji? Jesli tak, roznica widmowa moglaby byc artefaktem stylu zapisu,
a nie tresci - to jest dokladnie ten confound, ktory wykryto na pilocie EN
(wariant A mial zero zdan pytajacych) i usunieto w rundzie 2.

Kryterium (ANEKS-2): dokladnosc ma byc ~przypadkowa. Uzywamy dokladnosci
zbalansowanej, bo klas jest 1 (A) do 4 (dialogowe) - surowa dokladnosc 80%
oznaczalaby tu klasyfikator, ktory zawsze mowi "dialogowy".

Istotnosc: permutacja etykiet WEWNATRZ scenariusza, zgodnie z ta sama zasada
co testy glowne (jednostka = scenariusz). Chcemy p DUZE - to jest kontrola,
w ktorej sukcesem jest brak sygnalu.

UWAGA: bez dokladnego tokenizera Gemmy raport jest oznaczony jako WSTEPNY
(inna dlugosc uciecia niz w tekstach, ktore realnie przeszly przez model).
"""

import argparse
import json
from pathlib import Path

import numpy as np

from corpus.build import build_scenario
from corpus.tokens import TokenCounter

PUNCT = "?!,.:;-—()\"'"
DIALOGIC = ("B", "C", "CprimG", "CprimU")

# Rozszerzenie dodane 2026-08-01, PRZED transferem danych glownych i przed
# odczytaniem endpointu. Powod: kontrola z ANEKS-2 pyta wylacznie o A wobec
# dialogowych, a wariant A NIE WYSTEPUJE w zadnej hipotezie konfirmacyjnej.
# Gdyby kontrola wypadla zle, samo w sobie nie mowiloby to nic o tescie
# glownym - a gdyby wypadla dobrze, dawaloby falszywe poczucie bezpieczenstwa.
# Pytanie o realna wartosc brzmi: czy interpunkcja rozroznia warianty WEWNATRZ
# rodziny dialogowej, bo tam rozgrywaja sie H1, H2 i H3.
CONFIRMATORY_PAIRS = (("C", "CprimG"), ("C", "B"), ("CprimG", "CprimU"))


def text_of(variant_turns):
    return " ".join(" ".join(t["sentences"]) for t in variant_turns)


def features(text):
    """Wylacznie interpunkcja, znormalizowana na 100 znakow (+ udzial zdan pytajacych)."""
    n = max(len(text), 1)
    f = [100.0 * text.count(c) / n for c in PUNCT]
    ends = [s for s in text.replace("!", ".").replace("?", ".").split(".") if s.strip()]
    q = text.count("?") / max(len(ends), 1)
    return np.array(f + [q], dtype=np.float64)


def fit_logistic(X, y, l2=1.0, iters=400, lr=0.5):
    """Regresja logistyczna na numpy - lockfile nie zawiera scikit-learn."""
    X = np.hstack([X, np.ones((X.shape[0], 1))])
    w = np.zeros(X.shape[1])
    for _ in range(iters):
        p = 1.0 / (1.0 + np.exp(-X @ w))
        g = X.T @ (p - y) / X.shape[0] + l2 * np.r_[w[:-1], 0.0] / X.shape[0]
        w -= lr * g
    return w


def predict(w, X):
    X = np.hstack([X, np.ones((X.shape[0], 1))])
    return (1.0 / (1.0 + np.exp(-X @ w))) >= 0.5


def balanced_accuracy(y, yhat):
    out = []
    for cls in (0, 1):
        m = y == cls
        if m.any():
            out.append(float((yhat[m] == cls).mean()))
    return float(np.mean(out))


def leave_one_scenario_out(X, y, groups):
    yhat = np.zeros_like(y, dtype=bool)
    for g in np.unique(groups):
        te = groups == g
        w = fit_logistic(X[~te], y[~te])
        yhat[te] = predict(w, X[te])
    return balanced_accuracy(y, yhat), yhat


def build_matrix(scenario_dir, token_counter, budget=1024, pair=None):
    """pair=None: A wobec dialogowych (ANEKS-2). pair=(va, vb): jeden kontrast."""
    X, y, groups, exact = [], [], [], token_counter.exact
    for path in sorted(Path(scenario_dir).glob("*.json")):
        sc = json.loads(path.read_text(encoding="utf-8"))
        built = build_scenario(sc, token_counter, budget=budget)["variants"]
        wanted = pair if pair else tuple(built)
        for name in wanted:
            X.append(features(text_of(built[name])))
            y.append((0 if name == pair[0] else 1) if pair
                     else (0 if name == "A" else 1))
            groups.append(sc["scenario_id"])
    return np.array(X), np.array(y), np.array(groups), exact


def feature_diagnostics(X, y):
    """Ktory znak rozroznia klasy - bez tego 'kontrola nie przeszla' nic nie mowi."""
    names = list(PUNCT) + ["udzial_pytan"]
    out = []
    for i, nm in enumerate(names):
        sd = X[:, i].std(ddof=1)
        a, b = X[y == 0, i].mean(), X[y == 1, i].mean()
        out.append({"znak": nm, "klasa_0": float(a), "klasa_1": float(b),
                    "d": float((a - b) / sd) if sd > 0 else 0.0})
    return sorted(out, key=lambda r: -abs(r["d"]))[:5]


def permutation_p(X, y, groups, observed, n_perm=1000, rng=None):
    """Etykiety mieszane WEWNATRZ scenariusza - struktura par zachowana."""
    if rng is None:
        rng = np.random.default_rng(20260801)
    hits = 0
    for _ in range(n_perm):
        yp = y.copy()
        for g in np.unique(groups):
            m = groups == g
            yp[m] = rng.permutation(y[m])
        acc, _ = leave_one_scenario_out(X, yp, groups)
        hits += acc >= observed
    return float((hits + 1) / (n_perm + 1))


def main():
    ap = argparse.ArgumentParser(description="Kontrola interpunkcyjna (ANEKS-2)")
    ap.add_argument("--corpus", default="corpus/scenarios")
    ap.add_argument("--permutations", type=int, default=200)
    ap.add_argument("--out", default="gates/punctuation_control.json")
    args = ap.parse_args()

    tc = TokenCounter.load()
    results = {"exact_tokenizer": tc.exact, "kryterium": "dokladnosc ~przypadkowa (0.5)",
               "aneks2_A_vs_dialogowe": [], "kontrasty_konfirmacyjne": []}

    for lang_dir in sorted(Path(args.corpus).iterdir()):
        if not lang_dir.is_dir():
            continue
        lang = lang_dir.name

        X, y, groups, _ = build_matrix(lang_dir, tc)
        acc, _ = leave_one_scenario_out(X, y, groups)
        p = permutation_p(X, y, groups, acc, n_perm=args.permutations)
        results["aneks2_A_vs_dialogowe"].append({
            "language": lang, "n_scenarios": int(len(np.unique(groups))),
            "n_texts": int(len(y)), "balanced_accuracy": acc, "p_value": p,
            "przeszla": bool(p > 0.05), "czym_sie_roznia": feature_diagnostics(X, y),
            "zakres": "wariant A nie wystepuje w zadnej hipotezie konfirmacyjnej; "
                      "dotyczy kontrastu opisowego C-A oraz kontroli H4",
        })

        for va, vb in CONFIRMATORY_PAIRS:
            Xp, yp, gp, _ = build_matrix(lang_dir, tc, pair=(va, vb))
            a, _ = leave_one_scenario_out(Xp, yp, gp)
            pp = permutation_p(Xp, yp, gp, a, n_perm=args.permutations)
            results["kontrasty_konfirmacyjne"].append({
                "language": lang, "kontrast": f"{va}-{vb}",
                "balanced_accuracy": a, "p_value": pp, "przeszla": bool(pp > 0.05)})

    Path(args.out).write_text(json.dumps(results, indent=2, ensure_ascii=False),
                              encoding="utf-8")
    tag = "" if tc.exact else "  [WSTEPNY - brak dokladnego tokenizera]"
    print(f"[punctuation] kryterium: dokladnosc zbalansowana ~0.5{tag}")
    print("[punctuation] --- ANEKS-2: A vs dialogowe ---")
    for r in results["aneks2_A_vs_dialogowe"]:
        print(f"[punctuation] {r['language']}: acc={r['balanced_accuracy']:.3f} "
              f"p={r['p_value']:.3f} -> {'OK' if r['przeszla'] else 'NIE PRZESZLA'}")
    print("[punctuation] --- kontrasty konfirmacyjne (H1, H3, H2) ---")
    for r in results["kontrasty_konfirmacyjne"]:
        print(f"[punctuation] {r['language']} {r['kontrast']:15s} "
              f"acc={r['balanced_accuracy']:.3f} p={r['p_value']:.3f} "
              f"-> {'OK' if r['przeszla'] else 'NIE PRZESZLA'}")


if __name__ == "__main__":
    main()
