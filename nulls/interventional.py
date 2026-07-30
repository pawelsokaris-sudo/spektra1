"""Nulle interwencyjne N1 i N2 (protokol par. 6).

Kazdy null przechodzi PONOWNIE przez model - to nie jest przestawianie liczb
w policzonych juz aktywacjach, tylko nowy tekst i nowy forward. Kazdy ma osobne
pytanie i osobne kryterium (rozstrzygniecie #5 z pierwszej rundy recenzji).

N1 - permutacja kolejnosci ZDAN.
  Pytanie: czy Ī zalezy od porzadku?
  Kryterium: D_lag spada do nullu; zachowanie Ī raportowane.
  Zdania mieszaja sie miedzy turami, zachowane sa: sekwencja rol i dlugosc
  kazdej tury w zdaniach. Wybor swiadomy: permutacja WYLACZNIE wewnatrz tur
  zostawilaby nienaruszony porzadek dalekiego zasiegu, czyli test bylby slabszy
  niz nazwa sugeruje. Skutkiem ubocznym jest to, ze zdanie napisane dla jednej
  roli moze trafic do tury drugiej - dla nullu porzadku to nie wada, ale nalezy
  to raportowac, bo zmienia takze spojnosc dialogu, nie tylko kolejnosc.

N2 - permutacja TUR z zachowaniem mowcow i dlugosci.
  Pytanie: czy Ī zalezy od ukladu tur, a nie od kolejnosci zdan w nich?
  Tury zamieniaja sie miejscami tylko w obrebie tej samej roli, wiec sekwencja
  mowcow zostaje nietknieta. Kolejnosc zdan WEWNATRZ tury zostaje - inaczej N2
  mieszaloby sie z N1 i zaden z nich nie mierzylby czegos rozlacznego.
"""

import numpy as np


def _derangement_indices(n, rng, max_tries=200):
    """Permutacja bez punktow stalych - zeby 'permutacja' faktycznie cos zmieniala."""
    if n < 2:
        raise ValueError(
            f"permutacja niemozliwa: {n} element(ow) - potrzebne co najmniej 2"
        )
    for _ in range(max_tries):
        idx = rng.permutation(n)
        if not np.any(idx == np.arange(n)):
            return idx
    # deterministyczny fallback: przesuniecie cykliczne (zawsze bez pkt stalych)
    return np.roll(np.arange(n), 1)


def permute_sentences(turns, rng=None):
    """N1: przetasowanie zdan w calym tekscie, z zachowaniem rol i dlugosci tur."""
    if rng is None:
        rng = np.random.default_rng()
    flat = [s for t in turns for s in t["sentences"]]
    order = _derangement_indices(len(flat), rng)
    shuffled = [flat[i] for i in order]
    out, pos = [], 0
    for t in turns:
        n = len(t["sentences"])
        out.append({"role": t["role"], "sentences": shuffled[pos:pos + n]})
        pos += n
    return out


def permute_turns(turns, rng=None):
    """N2: przetasowanie tur w obrebie tej samej roli; zdania w turze nietkniete."""
    if rng is None:
        rng = np.random.default_rng()
    by_role = {}
    for i, t in enumerate(turns):
        by_role.setdefault(t["role"], []).append(i)

    out = [None] * len(turns)
    for role, positions in by_role.items():
        if len(positions) < 2:
            raise ValueError(
                f"permutacja tur niemozliwa dla roli '{role}': tylko "
                f"{len(positions)} tura w tekscie"
            )
        order = _derangement_indices(len(positions), rng)
        for slot, src in zip(positions, [positions[i] for i in order]):
            out[slot] = {"role": role, "sentences": list(turns[src]["sentences"])}
    return out
