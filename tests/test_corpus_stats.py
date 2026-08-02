import pytest

from corpus.stats import (
    count_questions,
    count_words,
    punctuation_profile,
    render_gemma_chat,
    turn_word_lengths,
    variant_structure_check,
)


def test_count_words_simple():
    assert count_words("Ala ma kota, a kot ma Alę.") == 7


def test_count_questions_counts_question_sentences():
    text = "To jest zdanie. Czy to pytanie? Tak. A to drugie pytanie?"
    assert count_questions(text) == 2


def test_punctuation_profile_counts_marks():
    prof = punctuation_profile("Raz, dwa; trzy. Cztery? Pięć! Sześć: siedem,")
    assert prof[","] == 2
    assert prof["."] == 1
    assert prof["?"] == 1
    assert prof["!"] == 1
    assert prof[";"] == 1
    assert prof[":"] == 1


def test_turn_word_lengths_per_turn():
    turns = [
        {"role": "user", "text": "Jedno dwa trzy."},
        {"role": "assistant", "text": "Cztery pięć."},
    ]
    assert turn_word_lengths(turns) == [3, 2]


def test_render_gemma_chat_format():
    turns = [
        {"role": "user", "text": "Cześć."},
        {"role": "assistant", "text": "Witaj."},
    ]
    rendered = render_gemma_chat(turns)
    assert rendered.startswith("<bos><start_of_turn>user\n")
    assert "<start_of_turn>model\nWitaj.<end_of_turn>\n" in rendered
    assert rendered.count("<start_of_turn>") == 2
    assert rendered.count("<end_of_turn>") == 2


def test_variant_structure_check_accepts_matched_variants():
    a = [{"role": "user", "text": "x"}, {"role": "assistant", "text": "y"}]
    b = [{"role": "user", "text": "q q"}, {"role": "assistant", "text": "w"}]
    problems = variant_structure_check({"A": a, "B": b})
    assert problems == []


def test_variant_structure_check_flags_role_mismatch():
    a = [{"role": "user", "text": "x"}, {"role": "assistant", "text": "y"}]
    b = [{"role": "assistant", "text": "q"}, {"role": "user", "text": "w"}]
    problems = variant_structure_check({"A": a, "B": b})
    assert any("rol" in p.lower() for p in problems)


def test_variant_structure_check_flags_turn_count_mismatch():
    a = [{"role": "user", "text": "x"}]
    b = [{"role": "user", "text": "q"}, {"role": "assistant", "text": "w"}]
    problems = variant_structure_check({"A": a, "B": b})
    assert any("tur" in p.lower() for p in problems)


# --- render szablonem wlasnym modelu (SPEKTRA-2, ustalenie DEP zlecenie 09) ---

class _FakeTok:
    """Atrapa tokenizera: zapisuje, co dostala, i sklada wlasny format."""
    def __init__(self):
        self.widziane = None

    def apply_chat_template(self, msgs, tokenize=False, add_generation_prompt=False):
        self.widziane = {"msgs": msgs, "tokenize": tokenize,
                         "add_generation_prompt": add_generation_prompt}
        return "".join(f"[INST]{m['role']}:{m['content']}[/INST]" for m in msgs)


def test_render_chat_uzywa_szablonu_modelu_a_nie_naszego():
    from corpus.stats import render_chat
    tok = _FakeTok()
    out = render_chat(tok, [{"role": "user", "text": "Pierwsze."},
                            {"role": "assistant", "text": "Drugie."}])
    assert "[INST]" in out and "<start_of_turn>" not in out


def test_render_chat_mapuje_role_model_na_assistant():
    """apply_chat_template nie zna roli 'model' - to nazwa wewnetrzna Gemmy."""
    from corpus.stats import render_chat
    tok = _FakeTok()
    render_chat(tok, [{"role": "model", "text": "X"}])
    assert tok.widziane["msgs"][0]["role"] == "assistant"


def test_render_chat_przyjmuje_oba_formaty_tur():
    from corpus.stats import render_chat
    a, b = _FakeTok(), _FakeTok()
    render_chat(a, [{"role": "user", "text": "Jedno. Dwa."}])
    render_chat(b, [{"role": "user", "sentences": ["Jedno.", "Dwa."]}])
    assert a.widziane["msgs"] == b.widziane["msgs"]


def test_render_chat_nie_dokleja_zachety_do_generowania():
    """add_generation_prompt=True dopisalby naglowek tury modelu na koncu -
    czyli tekst, ktorego w korpusie nie ma."""
    from corpus.stats import render_chat
    tok = _FakeTok()
    render_chat(tok, [{"role": "user", "text": "X"}])
    assert tok.widziane["add_generation_prompt"] is False
    assert tok.widziane["tokenize"] is False
