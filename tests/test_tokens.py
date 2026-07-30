from corpus.tokens import TokenCounter


def test_heuristic_counter_marks_itself_preliminary():
    tc = TokenCounter.load(tokenizer_dir="nonexistent-dir")
    assert tc.exact is False


def test_heuristic_scales_with_text_length_and_language():
    tc = TokenCounter.load(tokenizer_dir="nonexistent-dir")
    short = tc.count("Ala ma kota.", language="pl")
    long = tc.count("Ala ma kota. " * 10, language="pl")
    assert 0 < short < long
    # ten sam tekst po polsku ma wyzsza estymate tokenow niz po angielsku
    text = "informacja o systemie kompostowania odpadow organicznych"
    assert tc.count(text, language="pl") >= tc.count(text, language="en")
