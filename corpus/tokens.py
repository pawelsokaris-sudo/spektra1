"""Licznik tokenow: dokladny (tokenizer Gemmy) albo heurystyczny (WSTEPNY).

Sciezka dokladna: pliki tokenizera google/gemma-3-4b-it w corpus/.tokenizer/
(gitignorowane - licencja Google nie pozwala ich publikowac w repo pieczeci;
dociagniecie: ops/DEP-zlecenie-02-tokenizer.md). Wymaga pakietu `tokenizers`.

Sciezka heurystyczna: estymata znaki/token per jezyk. Kazdy raport liczony
heurystycznie MUSI byc oznaczony jako WSTEPNY - ostateczny raport dopasowania
T3 wymaga dokladnego tokenizera.
"""

from pathlib import Path

# Zgrubne stosunki znaki/token dla slownika Gemmy (262k, dobra obsluga PL).
# Kalibracja nastapi automatycznie, gdy pojawi sie dokladny tokenizer.
_CHARS_PER_TOKEN = {"pl": 3.2, "en": 4.0}

DEFAULT_TOKENIZER_DIR = Path(__file__).resolve().parent / ".tokenizer"


class TokenCounter:
    """count() zwraca liczbe tokenow tekstu; exact=False oznacza heurystyke."""

    def __init__(self, tokenizer=None):
        self._tokenizer = tokenizer
        self.exact = tokenizer is not None

    @classmethod
    def load(cls, tokenizer_dir=None):
        d = Path(tokenizer_dir) if tokenizer_dir else DEFAULT_TOKENIZER_DIR
        tok_file = d / "tokenizer.json"
        if tok_file.is_file():
            from tokenizers import Tokenizer  # import lokalny: pakiet opcjonalny
            return cls(Tokenizer.from_file(str(tok_file)))
        return cls(None)

    def count(self, text, language="pl"):
        if self.exact:
            return len(self._tokenizer.encode(text).ids)
        ratio = _CHARS_PER_TOKEN.get(language, 3.6)
        return max(1, round(len(text) / ratio))
