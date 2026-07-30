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
