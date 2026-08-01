"""Raport GATE 2 po polsku z wyniku analizy konfirmacyjnej.

Napisany razem z gates/gate2.py, czyli PRZED istnieniem progow korpusu
glownego. Powod jest ten sam co przy samej analizie: forma raportu nie moze
byc dobierana po zobaczeniu wyniku - inaczej wnioski ukladaja sie pod to,
co wyszlo.

Raport ma wypisac wszystko, takze kroki, ktore wypadly poza hierarchie po jej
zatrzymaniu. Selektywne raportowanie jest tu latwiejsze niz gdziekolwiek
indziej, wiec generator nie zostawia na to miejsca.
"""

import argparse
import json
from pathlib import Path

WERDYKT_OPIS = {
    "efekt potwierdzony": "efekt wykryty",
    "niekonkluzywny": "wynik niekonkluzywny",
    "efekt praktycznie wykluczony": "efekt praktycznie wykluczony",
}


def fmt_ci(ci, level):
    if not ci:
        return "—"
    return f"[{ci[0]:+.5f}; {ci[1]:+.5f}] ({level:.0%})"


def step_row(s):
    znacznik = "**konfirmacyjny**" if s.get("confirmatory") else "opisowy"
    return (f"| {s['step']} | {s['contrast']} | {znacznik} | {s['mean']:+.5f} | "
            f"{s['d_z']:+.3f} | {fmt_ci(s.get('ci'), s.get('ci_level', 0.99))} | "
            f"{s['p_value']:.5f} | {s.get('verdict', '—')} |")


def render_replica(r):
    L = [f"## Replika {r['language'].upper()}", ""]
    L += ["| Krok | Kontrast | Status | Średnia różnica | d_z | CI | p | Werdykt |",
          "|---|---|---|---:|---:|---|---:|---|"]
    L += [step_row(s) for s in r["steps"]]
    L.append("")

    stop = r.get("stopped_at")
    if stop:
        L.append(f"**Hierarchia zatrzymała się na {stop}.** Wszystko poniżej jest "
                 "opisowe — protokół zabrania traktowania tych liczb jako "
                 "konfirmacyjnych, niezależnie od tego, jak wyglądają.")
    else:
        L.append("**Cała hierarchia przeszła.** Wszystkie kroki są konfirmacyjne.")
    L.append("")

    for s in r["steps"]:
        if "zastrzezenie_obowiazkowe" in s:
            L += [f"> **Zastrzeżenie obowiązkowe do kroku {s['step']}.** "
                  f"{s['zastrzezenie_obowiazkowe']}", ""]

    h4 = r.get("H4", {})
    if h4:
        L += ["### H4 — kontrola równoważności (B − A na udziale modu głównego)", ""]
        o = h4.get("opis_efektu", {})
        L.append(f"Zmierzona różnica: **{o.get('mean', float('nan')):+.5f}**, "
                 f"d_z = {o.get('d_z', float('nan')):+.3f}, "
                 f"CI {fmt_ci(o.get('ci'), o.get('ci_level', 0.99))}.")
        if h4.get("equivalent") is True:
            L.append("Równoważność **potwierdzona** (TOST zaliczony).")
        elif h4.get("margin_attainable") is False:
            L.append(f"Równoważności **nie da się orzec** przy tej liczności — "
                     f"margines |d_z| < {h4['margin_dz']} jest nieosiągalny "
                     f"(najmniejszy osiągalny: {h4.get('min_attainable_margin_dz'):.2f}). "
                     "Patrz ANEKS-4. To NIE znaczy, że efekt jest.")
        else:
            L.append("Równoważności nie wykazano (TOST niezaliczony).")
        L.append("")

    prof = r.get("profil_warstwowy")
    if prof:
        L += ["### Profil warstwowy (permutacja klastrowa po ciągłej osi warstw)", "",
              f"Masa klastra: {prof['cluster_mass']:.3f}, p = {prof['p_value']:.4f}, "
              f"scenariuszy: {prof['n_scenarios']}. Status: "
              f"{'konfirmacyjny' if r.get('profil_warstwowy_confirmatory') else 'opisowy'}.",
              ""]
    return L


def render(results):
    L = ["# SPEKTRA-1 — GATE 2, analiza konfirmacyjna", "",
         f"α = {results['alpha']}, permutacji = {results['n_permutations']}, "
         f"CI = {results['ci_level']:.0%}, pasmo warstw: "
         f"{min(results['band_hidden_state_index'])}–"
         f"{max(results['band_hidden_state_index'])}.", "",
         "Repliki językowe są **osobnymi prerejestrowanymi badaniami** — bez "
         "łączenia w pulę, z osobnym α. Porównanie między nimi jest wyłącznie "
         "opisowe.", "",
         "> **Zakres werdyktów (ANEKS-4, decyzja z 2026-08-01).** Zbiór możliwych "
         "werdyktów SPEKTRA-1 to {efekt wykryty, wynik niekonkluzywny}. Werdykt "
         "„efekt praktycznie wykluczony” jest przy M = 24 nieosiągalny i został "
         "z badania wycofany jawnym aneksem — nie po zobaczeniu wyników.", ""]
    for r in results["replicas"]:
        L += render_replica(r)

    L += ["## Podsumowanie", ""]
    for r in results["replicas"]:
        h1 = r["steps"][0]
        L.append(f"- **{r['language'].upper()}:** H1 (C − C′-G) — "
                 f"{WERDYKT_OPIS.get(h1.get('verdict'), h1.get('verdict'))}, "
                 f"p = {h1['p_value']:.5f}, d_z = {h1['d_z']:+.3f}.")
    L += ["",
          "Zgodność między replikami jest wymogiem odporności (GATE 3c): znak "
          "efektu musi być ten sam, a estymaty nie mogą się różnić o więcej niż "
          "25%. Rozbieżność nie unieważnia wyniku — klasyfikuje go jako "
          "niestabilny i tak zostaje opublikowany.", ""]
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="Raport GATE 2")
    ap.add_argument("--results", default="measurements-glowny/gate2_results.json")
    ap.add_argument("--out", default="measurements-glowny/GATE2-RAPORT.md")
    args = ap.parse_args()
    results = json.loads(Path(args.results).read_text(encoding="utf-8"))
    Path(args.out).write_text(render(results), encoding="utf-8")
    print(f"[gate2] raport: {args.out}")


if __name__ == "__main__":
    main()
