"""Testy GATE 3 na danych syntetycznych o znanej odpowiedzi."""

import numpy as np
import pandas as pd

from gates.gate3 import (MAX_REL_CHANGE, compare_run, dtype_tolerance_check,
                         relative_change, replica_agreement)


def make_df(delta, n=12, lang="pl", base=0.40, jitter=0.0, seed=1):
    """Ramka endpointow: C = base + delta, C'-G = base, plus opcjonalny szum."""
    rng = np.random.default_rng(seed)
    rows = []
    for i in range(n):
        sid = f"{lang}-{i + 9:02d}-syn"
        for v, off in (("C", delta), ("CprimG", 0.0)):
            rows.append({"scenario_id": sid, "language": lang, "variant": v,
                         "null": None, "iota": base + off + rng.normal(0, jitter),
                         "lambda1_share": 0.1, "n_layers": 14})
    return pd.DataFrame(rows)


def test_identyczny_bieg_kontrolny_spelnia_kryterium():
    main = make_df(-0.005)
    ctrl = make_df(-0.005)
    r = compare_run(main, ctrl, "test")
    assert r["kryterium_spelnione"] is True
    assert r["repliki"][0]["zmiana_wzgledna"] == 0.0


def test_odwrocony_znak_lamie_kryterium():
    r = compare_run(make_df(-0.005), make_df(+0.005), "test")
    assert r["kryterium_spelnione"] is False
    assert r["repliki"][0]["znak_ten_sam"] is False


def test_zmiana_ponad_25_procent_lamie_kryterium():
    r = compare_run(make_df(-0.004), make_df(-0.006), "test")   # +50%
    assert r["repliki"][0]["zmiana_wzgledna"] > MAX_REL_CHANGE
    assert r["kryterium_spelnione"] is False


def test_zmiana_ponizej_25_procent_przechodzi():
    r = compare_run(make_df(-0.004), make_df(-0.0044), "test")  # +10%
    assert r["repliki"][0]["spelnione"] is True


def test_porownanie_ogranicza_sie_do_scenariuszy_biegu_kontrolnego():
    """Bieg kontrolny obejmuje mniej scenariuszy - porownanie musi liczyc
    bieg glowny NA TYCH SAMYCH, inaczej mierzy dobor probki, nie precyzje."""
    main = make_df(-0.005, n=24)
    ctrl = make_df(-0.005, n=12)
    r = compare_run(main, ctrl, "test")
    assert r["repliki"][0]["n_scenarios"] == 12
    assert r["repliki"][0]["zmiana_wzgledna"] == 0.0


def test_tolerancja_dtype_wykrywa_przekroczenie():
    main = make_df(-0.005, base=0.40)
    zly = make_df(-0.005, base=0.41)      # 0.01 roznicy > 0.005
    r = dtype_tolerance_check(main, zly)
    assert r["spelnione"] is False and r["n_przekroczen"] > 0
    dobry = make_df(-0.005, base=0.4009)  # 0.0009 < 0.005
    assert dtype_tolerance_check(main, dobry)["spelnione"] is True


def test_zgodnosc_replik_liczona_od_wiekszej_co_do_modulu():
    """Wynik nie moze zalezec od tego, ktora replike nazwiemy pierwsza."""
    df = pd.concat([make_df(-0.006, lang="en"), make_df(-0.003, lang="pl")],
                   ignore_index=True)
    r = replica_agreement(df)
    odwrotnie = replica_agreement(pd.concat(
        [make_df(-0.003, lang="pl"), make_df(-0.006, lang="en")], ignore_index=True))
    assert r["zmiana_wzgledna"] == odwrotnie["zmiana_wzgledna"]
    assert r["znak_ten_sam"] is True
    assert r["spelnione"] is False        # 50% > 25%


def test_zgodne_repliki_przechodza():
    df = pd.concat([make_df(-0.0050, lang="en"), make_df(-0.0045, lang="pl")],
                   ignore_index=True)
    assert replica_agreement(df)["spelnione"] is True


def test_zerowa_baza_nie_wywraca_rachunku():
    assert relative_change(0.0, 0.001) == float("inf")
