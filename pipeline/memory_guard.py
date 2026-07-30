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


def check_foreign_vram(total_bytes, free_bytes, ours_bytes, max_foreign_gb=3.0):
    """Bramka na OBCE zuzycie karty (torch.cuda.mem_get_info + memory_allocated).

    Dziura wykryta przez DEP 2026-07-30 (drugie podejscie do pilota): bramka
    check_peak_memory mierzy alokacje WLASNEGO procesu, wiec przepusci bieg,
    ktory fizycznie sie nie miesci, bo obcy proces (wtedy: [gra], 6.9 GB)
    zajal karte - sterownik po cichu przeleje nadmiar do RAM i wielogodzinny
    bieg zamieni sie w wielodniowy, raportujac przy tym 'zmiescilem sie'.

    obce = total - free - nasze. Prog domyslny 3 GB: pulpit Windows to ~1.6 GB,
    wiec 3 GB toleruje przegladarke, ale nie gre. Sprawdzane przed biegiem
    i przed kazdym tekstem - gdy operator maszyny wlaczy gre W TRAKCIE, bieg zatrzyma
    sie czysto na checkpointcie zamiast pelznac dniami.
    """
    foreign = (total_bytes - free_bytes - ours_bytes) / BYTES_PER_GB
    if foreign > max_foreign_gb:
        raise MemoryGuardError(
            f"obcy proces trzyma {foreign:.2f} GB pamieci karty (prog "
            f"{max_foreign_gb:.1f} GB) - maszyna jest w uzyciu. Bramka szczytu "
            f"wlasnego procesu tego nie widzi, a sterownik przelalby nadmiar do "
            f"RAM po cichu. Bieg zatrzymany na checkpointcie; wznowic ta sama "
            f"komenda, gdy karta bedzie wolna."
        )
    return foreign


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
