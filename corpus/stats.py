"""Statystyki dopasowania korpusow (protokol par. 3).

Raport dopasowania czworek A/B/C/C' wymaga: tokeny/slowo, interpunkcja,
zdania pytajace, dlugosci tur. Struktura wariantow scenariusza musi byc
identyczna: liczba tur i sekwencja rol.
"""

import re


_WORD_RE = re.compile(r"[\w'-]+", re.UNICODE)
_PUNCT_MARKS = ",.?!;:"
# zdanie = fragment zakonczony ., ?, ! (wielokropki traktowane jak kropka)
_SENTENCE_RE = re.compile(r"[^.?!]*[.?!]+", re.DOTALL)


def count_words(text):
    """Liczba slow (sekwencje znakow slownych, z apostrofem i dywizem)."""
    return len(_WORD_RE.findall(text))


def count_questions(text):
    """Liczba zdan pytajacych (zakonczonych '?')."""
    return sum(1 for s in _SENTENCE_RE.findall(text) if s.rstrip().endswith("?"))


def punctuation_profile(text):
    """Slownik zliczen znakow interpunkcyjnych , . ? ! ; :"""
    return {mark: text.count(mark) for mark in _PUNCT_MARKS}


def turn_word_lengths(turns):
    """Lista dlugosci tur w slowach."""
    return [count_words(t["text"]) for t in turns]


def render_gemma_chat_with_spans(turns):
    """Jak render_gemma_chat, ale zwraca tez zakresy znakowe zdan.

    Zwraca (text, spans), spans = lista (start, end, sentence_idx) dla kazdego
    zdania globalnie (idx rosnie przez caly tekst). Znaki poza zakresami
    (markery szablonu, spacje sklejajace) nie naleza do zadnego zdania.
    Tury podaja zdania w polu 'sentences' (format runnera).
    """
    parts = ["<bos>"]
    pos = len("<bos>")
    spans = []
    idx = 0
    for t in turns:
        role = "model" if t["role"] == "assistant" else t["role"]
        head = f"<start_of_turn>{role}\n"
        parts.append(head)
        pos += len(head)
        for j, s in enumerate(t["sentences"]):
            if j > 0:
                parts.append(" ")
                pos += 1
            spans.append((pos, pos + len(s), idx))
            parts.append(s)
            pos += len(s)
            idx += 1
        tail = "<end_of_turn>\n"
        parts.append(tail)
        pos += len(tail)
    return "".join(parts), spans


def render_gemma_chat(turns):
    """Deterministyczny render szablonu czatu Gemmy (identyczny dla WSZYSTKICH
    wariantow, takze A - protokol par. 3).

    Format Gemma 3: <bos><start_of_turn>user\\n...<end_of_turn>\\n
    <start_of_turn>model\\n...<end_of_turn>\\n
    Rola 'assistant' mapowana na 'model'. Zgodnosc z tokenizer.apply_chat_template
    zostanie zweryfikowana w T2 na maszynie pomiarowej (odnotowac w raporcie T2).
    """
    parts = ["<bos>"]
    for t in turns:
        role = "model" if t["role"] == "assistant" else t["role"]
        parts.append(f"<start_of_turn>{role}\n{t['text']}<end_of_turn>\n")
    return "".join(parts)


def variant_structure_check(variants):
    """Sprawdza zgodnosc struktury wariantow scenariusza.

    variants: dict nazwa -> lista tur. Zwraca liste problemow (pusta = OK).
    Wymogi: identyczna liczba tur i identyczna sekwencja rol we wszystkich
    wariantach (protokol par. 3: identyczna liczba i dlugosc tur, te same role).
    """
    problems = []
    names = sorted(variants)
    ref_name = names[0]
    ref = variants[ref_name]
    for name in names[1:]:
        turns = variants[name]
        if len(turns) != len(ref):
            problems.append(
                f"{name}: liczba tur {len(turns)} != {len(ref)} ({ref_name})"
            )
            continue
        for i, (a, b) in enumerate(zip(ref, turns)):
            if a["role"] != b["role"]:
                problems.append(
                    f"{name}: rola tury {i} = {b['role']} != {a['role']} ({ref_name})"
                )
    return problems
