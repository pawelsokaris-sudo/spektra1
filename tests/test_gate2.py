"""Testy GATE 2 na danych SYNTETYCZNYCH o znanej odpowiedzi.

Swiadomie zero testow na realnym kontrascie glownym: sprawdzanie kodu
konfirmacyjnego na danych badania byloby zagladaniem do zamknietej szuflady
tylnymi drzwiami. Kazdy przypadek ma odpowiedz znana z konstrukcji.
"""

import numpy as np
import pandas as pd
import pytest

from gates.gate2 import (check_coverage, layer_profile_cluster, paired_diffs,
                         per_text_endpoints, run_replica)
from power.tost import paired_tost_equivalence

BAND = [14, 15, 16]


def make_spectra(effect=0.0, n_scen=16, lang="pl", seed=7, layer_effect=None,
                 effects=None):
    """Widma syntetyczne: wariant C dostaje 'effect' dodatkowych modow ponad prog.

    Kazde widmo to 40 wartosci wlasnych; kilka duzych (ponad przyszle lambda*=5)
    i ogon szumu. Efekt realizowany przez podniesienie modow C, wiec I_total
    rosnie w sposob kontrolowany.
    """
    rng = np.random.default_rng(seed)
    rows = []
    for i in range(n_scen):
        sid = f"{lang}-{i + 1:02d}-syn"
        base = np.sort(rng.uniform(0.5, 3.0, size=40))[::-1]
        for variant in ("A", "B", "C", "CprimG", "CprimU"):
            for li, hsi in enumerate(BAND):
                e = base.copy()
                if effects is not None:
                    bump = float(effects.get(variant, 0.0))
                else:
                    bump = effect if variant == "C" else 0.0
                if layer_effect is not None and variant == "C":
                    bump = layer_effect[li]
                # Szum per (scenariusz, wariant, warstwa). Bez niego warianty
                # bez efektu bylyby identyczne co do bitu, SD roznic = 0,
                # a testy sprawdzalyby przypadek, ktory w danych nie wystepuje.
                bump = bump + rng.normal(0.0, 0.35)
                e[:3] = np.array([12.0, 9.0, 7.0]) + bump
                rows.append({"scenario_id": sid, "language": lang, "variant": variant,
                             "null": None, "hidden_state_index": hsi,
                             "eigenvalues": e})
    return pd.DataFrame(rows)


def make_lambda(spectra, value=5.0):
    return {(r.scenario_id, r.language, int(r.hidden_state_index)): value
            for r in spectra.itertuples()}


def test_iota_liczona_z_progu_a_nie_ze_wszystkich_modow():
    """Ī musi sumowac WYLACZNIE mody ponad lambda* - inaczej zawsze wyjdzie 1.0."""
    s = make_spectra(n_scen=1)
    lam = make_lambda(s, value=5.0)
    df = per_text_endpoints(s, lam, BAND)
    assert (df.iota < 1.0).all(), "I_total = 1.0 oznacza prog ponizej calego widma"
    assert (df.iota > 0.0).all()
    # przy progu ponad najwiekszym modem endpoint musi byc tozsamosciowo zerem
    df0 = per_text_endpoints(s, make_lambda(s, value=1e6), BAND)
    assert (df0.iota == 0.0).all()


def test_brak_efektu_nie_daje_istotnosci():
    s = make_spectra(effect=0.0)
    lam = make_lambda(s)
    df = per_text_endpoints(s, lam, BAND)
    res = run_replica(df, s, lam, BAND, "pl")
    h1 = res["steps"][0]
    assert h1["p_value"] > 0.01
    assert res["stopped_at"] == "H1"


def test_silny_efekt_przechodzi_h1_ale_lancuch_stoi_na_h2_bez_efektu_osadzenia():
    """H1 dodatnie samo w sobie NIE otwiera calego lancucha - H2 jest osobna bramka."""
    s = make_spectra(effect=3.0)
    lam = make_lambda(s)
    df = per_text_endpoints(s, lam, BAND)
    res = run_replica(df, s, lam, BAND, "pl")
    h1 = res["steps"][0]
    assert h1["p_value"] < 0.01, h1
    assert h1["verdict"] == "efekt potwierdzony"
    assert res["stopped_at"] == "H2"


def test_efekt_we_wszystkich_krokach_przepuszcza_cala_hierarchie():
    s = make_spectra(effects={"C": 3.0, "CprimG": 1.5, "B": 0.6})
    lam = make_lambda(s)
    df = per_text_endpoints(s, lam, BAND)
    res = run_replica(df, s, lam, BAND, "pl")
    assert res["stopped_at"] is None, [(x["step"], x["p_value"]) for x in res["steps"]]
    for step in res["steps"][:3]:
        assert step["confirmatory"] is True and step["passed"] is True
    assert res["H4"]["confirmatory"] is True


def test_hierarchia_zamknieta_degraduje_kroki_po_zatrzymaniu():
    """Po niezaliczeniu H1 kolejne kroki musza byc policzone, ale NIE konfirmacyjne."""
    s = make_spectra(effect=0.0)
    lam = make_lambda(s)
    df = per_text_endpoints(s, lam, BAND)
    res = run_replica(df, s, lam, BAND, "pl")
    assert res["steps"][0]["confirmatory"] is True
    for step in res["steps"][1:]:
        assert step["confirmatory"] is False
        assert "OPISOWY" in step.get("verdict", "") or step["step"] in ("C-A", "B-A")
    assert res["H4"]["confirmatory"] is False


def test_kierunkowosc_efekt_odwrotny_nie_jest_istotny():
    """Hipotezy sa kierunkowe: C ponizej C'-G ma dawac p bliskie 1, nie istotnosc."""
    s = make_spectra(effect=-3.0)
    lam = make_lambda(s)
    df = per_text_endpoints(s, lam, BAND)
    res = run_replica(df, s, lam, BAND, "pl")
    assert res["steps"][0]["p_value"] > 0.5
    assert res["stopped_at"] == "H1"


def test_tost_orzeka_rownowaznosc_tylko_przy_malym_efekcie():
    """Przy marginesie OSIAGALNYM dla tego n (0.5 > 0.4) TOST musi rozrozniac."""
    rng = np.random.default_rng(3)
    maly = rng.normal(0.0, 1.0, size=24)
    maly = (maly - maly.mean()) + 0.05 * maly.std(ddof=1)   # d_z ~ 0.05
    duzy = rng.normal(1.0, 1.0, size=24)
    assert paired_tost_equivalence(maly, margin_dz=0.5,
                                   rng=np.random.default_rng(1))["equivalent"]
    assert not paired_tost_equivalence(duzy, margin_dz=0.5,
                                       rng=np.random.default_rng(1))["equivalent"]


def test_margines_0_3_jest_NIEOSIAGALNY_przy_M24():
    """REGRESJA / znalezisko 2026-08-01 wobec ANEKS-2.

    Margines |d_z| < 0.3 przy alfa 0.05 na strone i n = 24 nie przechodzi NAWET
    dla roznicy dokladnie zerowej. Werdykt "efekt praktycznie wykluczony" nie
    istnieje wiec w przestrzeni wynikow SPEKTRA-1 przy zamrozonym M. Ten test
    pilnuje, zeby fakt nie zniknal po cichu przy przyszlych zmianach kodu.
    """
    zero = np.zeros(24)
    zero[0], zero[1] = 1.0, -1.0            # d_z = 0, SD > 0
    r = paired_tost_equivalence(zero, margin_dz=0.3, rng=np.random.default_rng(4))
    assert r["observed_d_z"] == pytest.approx(0.0, abs=1e-12)
    assert r["equivalent"] is False, "margines 0.3 nagle stal sie osiagalny - sprawdz alfe/n"
    assert r["min_attainable_margin_dz"] > 0.3


def test_tost_wchodzi_dopiero_gdy_h1_nie_przeszlo():
    s = make_spectra(effect=0.0)
    lam = make_lambda(s)
    df = per_text_endpoints(s, lam, BAND)
    res = run_replica(df, s, lam, BAND, "pl")
    assert "tost" in res["steps"][0]
    assert res["steps"][0]["verdict"] in ("efekt praktycznie wykluczony", "niekonkluzywny")


def test_brak_progu_dla_choc_jednego_tekstu_jest_wykryty():
    s = make_spectra(n_scen=3)
    lam = make_lambda(s)
    lam.pop(next(iter(lam)))
    assert len(check_coverage(s, lam, BAND)) == 1


def test_profil_warstwowy_wykrywa_klaster_a_nie_widzi_szumu():
    lam_v = 5.0
    s_eff = make_spectra(layer_effect=[3.0, 3.0, 3.0])
    r = layer_profile_cluster(s_eff, make_lambda(s_eff, lam_v), BAND, "pl",
                              "C", "CprimG", n_permutations=500,
                              rng=np.random.default_rng(5))
    assert r["p_value"] < 0.05, r

    s_flat = make_spectra(effect=0.0)
    r0 = layer_profile_cluster(s_flat, make_lambda(s_flat, lam_v), BAND, "pl",
                               "C", "CprimG", n_permutations=500,
                               rng=np.random.default_rng(5))
    assert r0["p_value"] > 0.05, r0


def test_jednostka_inferencji_to_scenariusz():
    """Liczba roznic musi rownac sie liczbie scenariuszy, nie liczbie tekstow."""
    s = make_spectra(n_scen=11)
    lam = make_lambda(s)
    df = per_text_endpoints(s, lam, BAND)
    diffs, scen = paired_diffs(df, "pl", "C", "CprimG")
    assert diffs.size == 11 == len(scen)


def test_repliki_jezykowe_sa_rozdzielone():
    """Zadnego laczenia PL i EN w pule - to osobne prerejestrowane repliki."""
    a = make_spectra(n_scen=8, lang="pl", seed=1)
    b = make_spectra(n_scen=8, lang="en", seed=2)
    s = pd.concat([a, b], ignore_index=True)
    lam = make_lambda(s)
    df = per_text_endpoints(s, lam, BAND)
    d_pl, _ = paired_diffs(df, "pl", "C", "CprimG")
    d_en, _ = paired_diffs(df, "en", "C", "CprimG")
    assert d_pl.size == 8 and d_en.size == 8


def test_nulle_nie_wchodza_do_kontrastow_konfirmacyjnych():
    s = make_spectra(n_scen=6)
    extra = s[s.variant == "A"].copy()
    extra["null"] = "N1"
    s2 = pd.concat([s, extra], ignore_index=True)
    lam = make_lambda(s2)
    df = per_text_endpoints(s2, lam, BAND)
    diffs, scen = paired_diffs(df, "pl", "C", "A")
    assert diffs.size == 6, "wiersze nulli przeciekly do kontrastu"


def test_gate2_odmawia_startu_bez_t5(tmp_path):
    from gates.gate2 import load_lambda_star
    with pytest.raises(FileNotFoundError, match="T5"):
        load_lambda_star(tmp_path)


def test_aneks4_wymusza_zastrzezenie_gdy_margines_nieosiagalny():
    """ANEKS-4 opcja A: raport nie moze wyjsc bez zdania o nieosiagalnym marginesie."""
    s = make_spectra(effect=0.0, n_scen=24)
    lam = make_lambda(s)
    df = per_text_endpoints(s, lam, BAND)
    res = run_replica(df, s, lam, BAND, "pl")
    h1 = res["steps"][0]
    assert h1["verdict"] == "niekonkluzywny"
    assert h1["tost"]["margin_attainable"] is False
    assert "NIEOSIAGALNY" in h1["zastrzezenie_obowiazkowe"]
    assert "ANEKS-4" in res["H4"]["zastrzezenie_obowiazkowe"]
    # H4 mimo braku orzeczenia musi podac wielkosc efektu i przedzial
    assert res["H4"]["opis_efektu"]["ci"] is not None
