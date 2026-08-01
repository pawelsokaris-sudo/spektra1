"""Raport GATE 3 po polsku. Napisany przed biegami kontrolnymi, jak reszta.

Zasada raportowania ta sama co w GATE 2: wypisujemy WSZYSTKIE kryteria, takze
te niespelnione, i nazywamy ograniczenia wprost. Niepowodzenie GATE 3 nie
uniewaznia wyniku - klasyfikuje go jako niestabilny (protokol par. 7) i tak
zostaje opublikowany.
"""

import argparse
import json
from pathlib import Path

OPIS = {
    "a_dtype": "Kryterium (a) — precyzja: bf16 wobec fp32",
    "b_pozycyjny": "Kryterium (b) — z odejmowaniem komponentu pozycyjnego i bez",
    "c_repliki": "Kryterium (c) — obie repliki językowe osobno",
}


def tabela_replik(repliki):
    L = ["| Replika | Scenariuszy | Δ₁ główny | Δ₁ kontrolny | Zmiana | Znak zgodny | Wynik |",
         "|---|---:|---:|---:|---:|---|---|"]
    for r in repliki:
        L.append(f"| {r['language'].upper()} | {r['n_scenarios']} | "
                 f"{r['delta1_glowny']:+.5f} | {r['delta1_kontrolny']:+.5f} | "
                 f"{r['zmiana_wzgledna']:.1%} | {'tak' if r['znak_ten_sam'] else 'NIE'} | "
                 f"{'spełnione' if r['spelnione'] else '**niespełnione**'} |")
    return L


def render(res):
    L = ["# SPEKTRA-1 — GATE 3, odporność wyniku", "",
         f"Tolerancja precyzji: {res['tolerancja_dtype']} na tekst. "
         f"Maksymalna zmiana estymaty: {res['max_zmiana_wzgledna']:.0%}. "
         f"Progi zamrożone w protokole §2 i §7, wpisane w kod przed biegami.", "",
         f"> **Ograniczenie zamierzone.** Progi λ\\* {res['lambda_star']}. "
         "Kryterium **znaku** jest przez to mocne, kryterium **wielkości** "
         "przybliżone. Przeliczenie progów dla biegów kontrolnych kosztowałoby "
         "kolejny dzień maszyny i nie zmieniłoby odpowiedzi na pytanie, po co "
         "ta bramka istnieje: czy efekt jest realny.", ""]

    for klucz in ("a_dtype", "b_pozycyjny", "c_repliki"):
        k = res["kryteria"].get(klucz)
        L += [f"## {OPIS[klucz]}", ""]
        if k is None or "brak_danych" in (k or {}):
            L += [f"**Brak danych** — bieg kontrolny nie dotarł "
                  f"(`{k.get('brak_danych') if k else '?'}`).", ""]
            continue

        if klucz == "c_repliki":
            r = k["repliki"]
            L += ["| Replika | Δ₁ |", "|---|---:|"]
            L += [f"| {lang.upper()} | {v:+.5f} |" for lang, v in r.items()]
            L += ["", f"Znak zgodny: **{'tak' if k['znak_ten_sam'] else 'NIE'}**. "
                      f"Różnica wielkości: **{k['zmiana_wzgledna']:.1%}** "
                      f"(próg {res['max_zmiana_wzgledna']:.0%}). "
                      f"Wynik: {'spełnione' if k['spelnione'] else '**niespełnione**'}.", ""]
            continue

        L += tabela_replik(k["repliki"]) + [""]
        tol = k.get("tolerancja_per_tekst")
        if tol:
            L += ["**Tolerancja na pojedynczy tekst** (kontrola surowsza niż "
                  "kryterium kontrastowe — sprawdza sam pomiar, nie różnicę "
                  "między wariantami):", "",
                  f"- tekstów porównanych: {tol['n_tekstow']}",
                  f"- największa różnica: {tol['max_delta']:.6f} "
                  f"(próg {tol['tolerancja']})",
                  f"- średnia różnica: {tol['srednia_delta']:.6f}",
                  f"- przekroczeń: **{tol['n_przekroczen']}**", ""]
            if tol["przekroczenia"]:
                L += ["Teksty przekraczające tolerancję (do dziesięciu):", ""]
                L += [f"- `{'/'.join(p['tekst'])}` — {p['delta']:.6f}"
                      for p in tol["przekroczenia"]]
                L.append("")

    L += ["## Werdykt", "",
          f"**{res['werdykt']}**", ""]
    if res["werdykt"] == "NIESTABILNY":
        L += ["Protokół §7 przewiduje ten wynik wprost: niepowodzenie bramki "
              "odporności **nie unieważnia** pomiaru, tylko klasyfikuje go jako "
              "niestabilny — i tak zostaje opublikowany. Który dokładnie "
              "warunek zawiódł, widać w tabelach wyżej; to jest informacja "
              "o granicach wyniku, nie o jego nieważności.", ""]
    elif res["werdykt"] == "NIEKOMPLETNY":
        L += ["Brakuje co najmniej jednego biegu kontrolnego. Werdykt "
              "odporności nie może zapaść na podstawie części kryteriów.", ""]
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="Raport GATE 3")
    ap.add_argument("--results", default="measurements-glowny/gate3_results.json")
    ap.add_argument("--out", default="measurements-glowny/GATE3-RAPORT.md")
    args = ap.parse_args()
    res = json.loads(Path(args.results).read_text(encoding="utf-8"))
    Path(args.out).write_text(render(res), encoding="utf-8")
    print(f"[gate3] raport: {args.out}")


if __name__ == "__main__":
    main()
