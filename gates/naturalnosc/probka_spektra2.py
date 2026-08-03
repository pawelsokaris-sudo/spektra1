"""Probka kalibracyjna z korpusu SPEKTRY-2.

WARUNEK NIEKOLISTOSCI (projekt par. 6): material kalibracyjny musi byc
ZEWNETRZNY wobec ocenianego. Progi policzone na tej samej puli, ktora sie
przesiewa, wykryja wylacznie scenariusze odstajace - nigdy systematycznie
slabego korpusu, bo slaby korpus sam ustawilby sobie niski prog.

Dlatego scenariusze wylosowane do tej probki ZOSTAJA WYLACZONE Z BADANIA.
Ich miejsce zajma scenariusze dopisane po bramce (projekt przewiduje pule
nadmiarowa). Lista wykluczonych zapisywana jest jawnie razem z ziarnem.

Probka bierze JEDNA insercje na scenariusz i wszystkie szesc jej wariantow -
kryteria K1-K5 porownuja warianty miedzy soba w obrebie scenariusza, wiec
komplet wariantow jest konieczny, a wiecej niz jedna insercja tylko mnozylaby
oceny bez zmiany tego, co da sie policzyc.

Uruchomienie:
    python -m gates.naturalnosc.probka_spektra2
"""

import json
import random
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
KATALOG = Path(__file__).resolve().parent
ZIARNO = 20260803          # zamrozone
SCENARIUSZY_NA_JEZYK = 12
OCENIAJACYCH = 9

KLUCZE = ["neutral", "external_grounded", "external_computational",
          "external_mundane", "external_ungrounded", "self"]
WARIANT = {"neutral": "B", "self": "C", "external_grounded": "CprimG",
           "external_computational": "CprimComp", "external_mundane": "CprimM",
           "external_ungrounded": "CprimU"}


def kontekst(sc, ins, ile=4):
    """Zdania poprzedzajace wstawke - z tej tury i, jesli trzeba, z poprzedniej."""
    tura = sc["turns"][ins["turn"]]
    zdania = tura["base"][:ins["after_sentence"] + 1]
    if len(zdania) < ile and ins["turn"] > 0:
        brak = ile - len(zdania)
        zdania = sc["turns"][ins["turn"] - 1]["base"][-brak:] + zdania
    return " ".join(zdania[-ile:])


def zbuduj():
    rng = random.Random(ZIARNO)
    elementy, wykluczone = [], {}

    for jezyk in ("pl", "en"):
        pliki = sorted((REPO / "corpus" / "scenarios-2" / jezyk).glob("*.json"))
        wybrane = rng.sample(pliki, SCENARIOSZY := SCENARIUSZY_NA_JEZYK)
        wykluczone[jezyk] = sorted(p.stem for p in wybrane)

        for p in sorted(wybrane):
            sc = json.loads(p.read_text(encoding="utf-8"))
            ins = rng.choice(sc["insertions"])
            k = kontekst(sc, ins)
            for klucz in KLUCZE:
                elementy.append({
                    "scenariusz": sc["scenario_id"], "jezyk": jezyk,
                    "wariant": WARIANT[klucz], "klucz_insercji": klucz,
                    "kontekst": k, "zdanie": ins[klucz],
                })

    rng.shuffle(elementy)
    for i, e in enumerate(elementy):
        e["id"] = f"S{i:03d}"
    return elementy, wykluczone


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    elementy, wykluczone = zbuduj()

    (KATALOG / "probka-s2.json").write_text(json.dumps({
        "opis": ("Probka kalibracyjna z korpusu SPEKTRY-2. Scenariusze z tej "
                 "listy SA WYLACZONE Z BADANIA - kalibracja na materiale, ktory "
                 "potem sie przesiewa, bylaby kolista."),
        "ziarno": ZIARNO,
        "wykluczone_z_badania": wykluczone,
        "elementy": elementy,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    slepe = [{k: e[k] for k in ("id", "jezyk", "kontekst", "zdanie")} for e in elementy]
    for n in range(1, OCENIAJACYCH + 1):
        kop = list(slepe)
        random.Random(9000 + n).shuffle(kop)
        (KATALOG / f"do-oceny-s2-{n}.json").write_text(
            json.dumps({"oceniajacy": str(n), "elementy": kop},
                       ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"elementow: {len(elementy)} "
          f"({SCENARIUSZY_NA_JEZYK} scenariuszy x 6 wariantow x 2 jezyki)")
    print(f"plikow do oceny: {OCENIAJACYCH}, rozne kolejnosci")
    print("\nWYLACZONE Z BADANIA (kalibracja):")
    for j, lista in wykluczone.items():
        print(f"  {j}: {', '.join(x.split('-')[0] + '-' + x.split('-')[1] for x in lista)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
