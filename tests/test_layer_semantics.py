"""Testy weryfikacji semantyki warstw (bez GPU)."""


# --- przelacznik --model (zlecenie DEP-09) ---------------------------------

def test_raport_modelu_z_configu_pisze_pod_domyslna_nazwa():
    from pipeline.layer_semantics import OUT_JSON, OUT_MD, output_paths
    a, b = output_paths("google/gemma-3-4b-it", "google/gemma-3-4b-it")
    assert (a, b) == (OUT_MD, OUT_JSON)


def test_inny_model_NIE_nadpisuje_raportu_modelu_glownego():
    """Raport modelu glownego jest czescia pakietu pieczeci. Uruchomienie
    sprawdzenia na drugim modelu nie moze go skasowac."""
    from pipeline.layer_semantics import OUT_JSON, OUT_MD, output_paths
    a, b = output_paths("CYFRAGOVPL/PLLuM-4B-instruct-2512", "google/gemma-3-4b-it")
    assert a != OUT_MD and b != OUT_JSON
    assert "PLLuM-4B-instruct-2512" in a.name


def test_slug_nie_przepuszcza_ukosnikow_do_nazwy_pliku():
    from pipeline.layer_semantics import model_slug
    s = model_slug("ORG/model:v1.2")
    assert "/" not in s and ":" not in s and "." not in s
