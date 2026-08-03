"""Ustawienie progu bramki naturalnosci z RZECZYWISTYCH ocen.

DLACZEGO NIE Z SYMULACJI. Prog 5,0/7 pochodzil z rachunku przy zalozeniu
SD ocen = 1,0 i prawdziwej sredniej 6,0. Zalozenia nie sprawdzono na
materiale. Skutek: realny material SPEKTRY-1, nienaruszony, dostawal 4,85 -
czyli SPEKTRA-1 nie przeszlaby wlasnej bramki. Prog musi wynikac z rozkladu
ocen materialu nienaruszonego, nie z zalozonej stalej.

REGULA WYBORU PROGU - ZAMROZONA PRZED OBEJRZENIEM OCEN:

    prog = kwantyl rozkladu srednich elementow NIENARUSZONYCH,
           dobrany tak, by falszywe odrzucenie dobrego materialu
           nie przekraczalo BUDZET_BLEDU (10%).

Wykrywalnosc uszkodzen jest wtedy WYNIKIEM POMIARU, nie przedmiotem wyboru.
To rozroznienie jest cale sedno: gdybysmy dobierali prog tak, zeby wyszla
ladna wykrywalnosc, kalibracja bylaby autoportretem, nie pomiarem.

Prog liczony OSOBNO DLA KAZDEGO JEZYKA - repliki jezykowe sa osobnymi
badaniami i nigdy nie sa laczone.

Uruchomienie:
    python -m gates.naturalnosc.prog
"""

import json
import statistics as st
import sys
from itertools import combinations
from pathlib import Path

KATALOG = Path(__file__).resolve().parent
BUDZET_BLEDU = 0.10        # dopuszczalne falszywe odrzucenie dobrego materialu

# Elementy wykluczone z rachunku wraz z powodem. Wykluczenie jest jawne
# i policzalne - element usuniety po cichu bylby dopasowaniem wyniku.
WYKLUCZONE = {
    "K055": ("blad zgody liczby wniesiony przez odbudowe zestawu: podmiana "
             "frazy pojedynczej pod czasownik mnogi dala 'that whole other "
             "thing there arrive in'. Element psuje sie na DWA sposoby naraz, "
             "wiec nie mierzy samego odniesienia. Zglosilo go niezaleznie "
             "siedmiu z dziewieciu oceniajacych."),
}
POWTORZEN_BOOTSTRAP = 5000
ZIARNO = 20260803


def wczytaj():
    zestaw = json.loads((KATALOG / "zestaw-kalibracyjny-v2.json").read_text(encoding="utf-8"))
    meta = {e["id"]: e for e in zestaw["elementy"] if e["id"] not in WYKLUCZONE}

    oceny = {}
    braki = []
    for p in sorted(KATALOG.glob("oceny-v2-*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        kto = d["oceniajacy"]
        for o in d["oceny"]:
            oceny.setdefault(o["id"], {})[kto] = (o["naturalnosc"], o["jasnosc_odniesienia"])

    for eid in meta:
        n = len(oceny.get(eid, {}))
        if n == 0:
            braki.append(f"{eid}: brak jakiejkolwiek oceny")
    return meta, oceny, braki


def srednie(meta, oceny, metryka):
    """metryka: 0 = naturalnosc, 1 = jasnosc odniesienia."""
    out = {}
    for eid, m in meta.items():
        v = [w[metryka] for w in oceny.get(eid, {}).values()]
        if v:
            out[eid] = st.mean(v)
    return out


def kwantyl(dane, q):
    """Kwantyl typu 'nearest rank', bez interpolacji - prog ma byc ocena,
    ktora ktos realnie wystawil, a nie liczba miedzy ocenami.

    Indeks ucinany W DOL, nie zaokraglany. Zaokraglanie do najblizszego
    przepuszczalo prog odrzucajacy 10,4% zdrowego materialu przy budzecie
    10% (n=48) - budzet bledu ma byc sufitem, nie wartoscia orientacyjna.
    """
    d = sorted(dane)
    if not d:
        return float("nan")
    i = max(0, min(len(d) - 1, int(q * (len(d) - 1))))
    return d[i]


def zgodnosc(meta, oceny, metryka):
    """Ile oceniajacy sie miedzy soba roznia - i czy w ogole sie zgadzaja."""
    kto = sorted({k for w in oceny.values() for k in w})
    pary = []
    for a, b in combinations(kto, 2):
        xa, xb = [], []
        for eid in meta:
            w = oceny.get(eid, {})
            if a in w and b in w:
                xa.append(w[a][metryka])
                xb.append(w[b][metryka])
        if len(xa) > 2 and len(set(xa)) > 1 and len(set(xb)) > 1:
            pary.append(st.correlation(xa, xb))
    sd_elementu = [st.stdev([w[metryka] for w in oceny[eid].values()])
                   for eid in meta if len(oceny.get(eid, {})) > 1]
    return (st.mean(pary) if pary else float("nan"),
            st.mean(sd_elementu) if sd_elementu else float("nan"),
            len(kto))


def bootstrap_progu(nienaruszone, rng):
    """Niepewnosc progu przy 24 elementach na jezyk - to malo."""
    n = len(nienaruszone)
    out = []
    for _ in range(POWTORZEN_BOOTSTRAP):
        prob = [nienaruszone[rng.randrange(n)] for _ in range(n)]
        out.append(kwantyl(prob, BUDZET_BLEDU))
    return kwantyl(out, 0.025), kwantyl(out, 0.975)


def analiza(meta, oceny, jezyk, metryka, nazwa, rng):
    ids = [i for i, m in meta.items() if m["jezyk"] == jezyk]
    sr = srednie(meta, oceny, metryka)
    ok = [sr[i] for i in ids if meta[i]["klasa"] == "nienaruszony" and i in sr]
    zle = {i: sr[i] for i in ids if meta[i]["klasa"] != "nienaruszony" and i in sr}

    prog = kwantyl(ok, BUDZET_BLEDU)
    lo, hi = bootstrap_progu(ok, rng)

    odrzucone_ok = sum(1 for v in ok if v < prog) / len(ok)
    wykryte = sum(1 for v in zle.values() if v < prog) / len(zle)

    print(f"\n--- {jezyk.upper()} | {nazwa} ---")
    print(f"  nienaruszone (n={len(ok)}): srednia {st.mean(ok):.2f}, "
          f"mediana {st.median(ok):.2f}, min {min(ok):.2f}, max {max(ok):.2f}")
    print(f"  uszkodzone   (n={len(zle)}): srednia {st.mean(zle.values()):.2f}, "
          f"mediana {st.median(zle.values()):.2f}, "
          f"min {min(zle.values()):.2f}, max {max(zle.values()):.2f}")
    print(f"  rozdzielenie: {st.mean(ok) - st.mean(zle.values()):+.2f} pkt")
    print(f"  PROG = {prog:.2f}   (95% bootstrap: {lo:.2f} - {hi:.2f})")
    print(f"  falszywe odrzucenie dobrego : {odrzucone_ok:.0%}")
    print(f"  WYKRYWALNOSC uszkodzen      : {wykryte:.0%}   <- wynik, nie wybor")

    print("  wykrywalnosc wg klasy uszkodzenia:")
    for klasa in sorted({meta[i]["klasa"] for i in zle}):
        v = [zle[i] for i in zle if meta[i]["klasa"] == klasa]
        print(f"    {klasa.replace('uszkodzony:',''):>14}: "
              f"{sum(1 for x in v if x < prog)}/{len(v)}  (srednia {st.mean(v):.2f})")

    # Kluczowa kontrola: czy ktorys WARIANT nienaruszony wypada systematycznie
    # nizej. Wariant nieosadzony ma nierozstrzygalny referent Z ZALOZENIA, wiec
    # reguła "kazdy wariant >= prog" moglaby go odrzucac za wlasnosc zamierzona.
    print("  material NIENARUSZONY wg wariantu (kontrola reguly 'kazdy wariant'):")
    for w in sorted({meta[i]["wariant"] for i in ids if meta[i]["klasa"] == "nienaruszony"}):
        v = [sr[i] for i in ids
             if meta[i]["klasa"] == "nienaruszony" and meta[i]["wariant"] == w and i in sr]
        ponizej = sum(1 for x in v if x < prog)
        znak = "  <-- WARIANT PONIZEJ PROGU" if ponizej > len(v) / 2 else ""
        print(f"    {w:>20}: srednia {st.mean(v):.2f}, ponizej progu {ponizej}/{len(v)}{znak}")

    return {"jezyk": jezyk, "metryka": nazwa, "prog": round(prog, 2),
            "bootstrap95": [round(lo, 2), round(hi, 2)],
            "falszywe_odrzucenie": round(odrzucone_ok, 3),
            "wykrywalnosc": round(wykryte, 3),
            "srednia_nienaruszonych": round(st.mean(ok), 2),
            "srednia_uszkodzonych": round(st.mean(zle.values()), 2)}


def main():
    import random
    sys.stdout.reconfigure(encoding="utf-8")
    rng = random.Random(ZIARNO)

    meta, oceny, braki = wczytaj()
    if braki:
        print(f"=== BRAKI W OCENACH: {len(braki)} ===")
        for b in braki[:10]:
            print("  -", b)
        return 1

    liczby = sorted({len(w) for w in oceny.values()})
    print(f"elementow: {len(meta)} | ocen na element: {liczby}")

    for metryka, nazwa in ((0, "naturalnosc"), (1, "jasnosc odniesienia")):
        r, sd, n = zgodnosc(meta, oceny, metryka)
        print(f"\nzgodnosc panelu ({nazwa}): {n} oceniajacych, "
              f"srednia korelacja par r={r:.2f}, sredni SD elementu {sd:.2f}")
        if sd < 0.5:
            print("  UWAGA: SD ponizej 0,5 przy zalozonym w projekcie 1,0.")
            print("  Panel jest jednorodny - to sa oceniajacy tego samego modelu,")
            print("  wiec ich zgoda NIE jest dowodem trafnosci, tylko podobienstwa.")

    wynik = []
    for metryka, nazwa in ((0, "naturalnosc"), (1, "jasnosc odniesienia")):
        for jezyk in ("pl", "en"):
            wynik.append(analiza(meta, oceny, jezyk, metryka, nazwa, rng))

    (KATALOG / "prog-wynik.json").write_text(
        json.dumps({"budzet_bledu": BUDZET_BLEDU, "regula":
                    "prog = kwantyl 10% rozkladu srednich elementow nienaruszonych",
                    "wyniki": wynik}, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\nzapisano gates/naturalnosc/prog-wynik.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
