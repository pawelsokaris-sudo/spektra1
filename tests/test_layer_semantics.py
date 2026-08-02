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


def test_write_report_ZAPISUJE_TAM_GDZIE_KAZANO(tmp_path):
    """REGRESJA. Poprzednia wersja liczyla sciezke z sufiksem, wypisywala ja
    w logu, a zapisywala do globalnego OUT_MD - czyli NADPISYWALA raport
    modelu glownego z pakietu pieczeci i przy tym KLAMALA w meldunku.

    Poprzedni test sprawdzal wylacznie funkcje liczaca nazwe, wiec bledu nie
    zlapal. Ten sprawdza sam zapis."""
    from pipeline.layer_semantics import OUT_MD, write_report
    przed = OUT_MD.read_text(encoding="utf-8") if OUT_MD.exists() else None
    cel = tmp_path / "layer_semantics-INNY.md"
    r = {"model": "ORG/inny", "revision": None, "n_blocks": 34,
         "hidden_states": {"n_hidden_states": 35, "n_blocks": 34,
                           "hidden_state_0_is_embedding": True,
                           "embedding_vs_block0_diff": 1.0, "blocks": [],
                           "all_blocks_match": True, "last_hidden_shape": (1, 10, 2560),
                           "dtype": "torch.bfloat16"},
         "final_norm": {"hidden_states_last_equals_block_output": True,
                        "max_abs_diff": 0.0, "interpretacja": "test"},
         "chat_template": {"uwaga": "test"},
         "attention_types": [{"index": i, "attention": "lokalna"} for i in range(34)],
         "band": {"band_indices": [13, 27], "n_blocks_in_band": 14,
                  "counts": {"lokalna": 12, "globalna": 2}}}
    write_report(r, cel)
    assert cel.exists(), "raport nie powstal pod przekazana sciezka"
    po = OUT_MD.read_text(encoding="utf-8") if OUT_MD.exists() else None
    assert po == przed, "raport modelu glownego zostal NADPISANY - dokladnie ten blad"


# --- znaczenie kontroli szablonu po przejsciu na render uniwersalny ---------

class _TokGemma:
    def apply_chat_template(self, msgs, tokenize=False, add_generation_prompt=False):
        from corpus.stats import render_gemma_chat
        return render_gemma_chat([{"role": m["role"], "text": m["content"]} for m in msgs])


class _TokMistral:
    def apply_chat_template(self, msgs, tokenize=False, add_generation_prompt=False):
        return "".join(f"[INST]{m['content']}[/INST]" for m in msgs)


def test_niezgodnosc_szablonu_MODELU_GLOWNEGO_jest_blokujaca():
    """Dla modelu z configu zgodnosc gwarantuje, ze SPEKTRA-1 sie nie zmienia."""
    from pipeline.layer_semantics import check_chat_template
    r = check_chat_template(_TokMistral(), is_config_model=True)
    assert r["match"] is False and r["blokujace"] is True


def test_niezgodnosc_szablonu_DRUGIEGO_MODELU_nie_jest_blokujaca():
    """PLLuM ma szablon Mistralowy - to oczekiwane, nie usterka."""
    from pipeline.layer_semantics import check_chat_template
    r = check_chat_template(_TokMistral(), is_config_model=False)
    assert r["match"] is False and r["blokujace"] is False
    assert "OCZEKIWANE" in r["uwaga"]


def test_zgodnosc_dla_modelu_glownego_potwierdza_odtwarzalnosc_spektry_1():
    from pipeline.layer_semantics import check_chat_template
    r = check_chat_template(_TokGemma(), is_config_model=True)
    assert r["match"] is True and r["blokujace"] is False
