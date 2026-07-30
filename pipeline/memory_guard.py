"""Bramka pamieci karty (protokol par. 2).

POWOD ISTNIENIA. Sterownik NVIDIA na Windows ma wlaczony "system memory fallback":
gdy zabraknie pamieci karty, cicho dokłada pamiec systemowa zamiast zglosic blad.
Zweryfikowane wprost na maszynie pomiarowej 2026-07-30 - alokacja 20 GB na karcie
o 15.92 GB PRZESZLA. Skutek dla protokolu jest powazniejszy niz spowolnienie:
znika sygnal ostrzegawczy. Bieg, ktory przekroczyl pamiec karty, nie pada, tylko
po cichu zwalnia - wiec "program sie nie wywalil" przestaje byc dowodem, ze pomiar
odbyl sie w zapieczetowanych warunkach.

Stad twarda bramka po stronie naszego kodu. Nie ruszamy ustawien sterownika na
cudzej maszynie; sprawdzamy szczyt zuzycia sami i przerywamy.

Progi (zamrozone w config.yaml):
  - pomiar glowny bf16: 14 GB. Zmierzony szczyt przy budzecie 1024 tokenow to
    8.83 GB, wiec zapas jest duzy, a prog lapie kazde realne przekroczenie.
  - kontrola fp32: 24 GB. Ta kontrola SWIADOMIE przelewa do RAM (patrz nizej).
"""

BYTES_PER_GB = 2 ** 30


class MemoryGuardError(RuntimeError):
    """Szczyt zuzycia pamieci przekroczyl zamrozony prog."""


def check_peak_memory(peak_bytes, limit_gb, context, fp32_control_limit_gb=None):
    """Sprawdza szczyt zuzycia pamieci karty po biegu; podnosi blad przy przekroczeniu.

    peak_bytes: wynik torch.cuda.max_memory_allocated()
    limit_gb: prog dla pomiaru glownego
    context: etykieta biegu (wchodzi do komunikatu i do logu)
    fp32_control_limit_gb: osobny, wyzszy prog dla kontroli fp32
    """
    effective = limit_gb
    if context == "fp32_control" and fp32_control_limit_gb is not None:
        effective = fp32_control_limit_gb
    peak_gb = peak_bytes / BYTES_PER_GB
    if peak_gb > effective:
        raise MemoryGuardError(
            f"[{context}] szczyt pamieci {peak_gb:.2f} GB przekroczyl prog "
            f"{effective:.2f} GB. UWAGA: brak bledu CUDA NIE oznacza, ze bieg sie "
            f"zmiescil - sterownik przelewa nadmiar do RAM po cichu, wiec pomiar "
            f"mogl przebiec w warunkach innych niz zapieczetowane. Przerwano celowo."
        )
    return peak_gb
