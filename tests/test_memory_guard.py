import pytest

from pipeline.memory_guard import (
    MemoryGuardError,
    check_foreign_vram,
    check_peak_memory,
)

GB = 2 ** 30


def test_foreign_vram_passes_when_card_is_ours():
    # tylko pulpit (1.6 GB obcych) + nasz proces
    check_foreign_vram(total_bytes=int(15.92 * GB), free_bytes=int(5.5 * GB),
                       ours_bytes=int(8.8 * GB), max_foreign_gb=3.0)


def test_foreign_vram_raises_when_someone_else_uses_the_card():
    # sytuacja z 2026-07-30: [gra] trzyma ~6.9 GB, nasz proces jeszcze zero
    with pytest.raises(MemoryGuardError, match="obcy"):
        check_foreign_vram(total_bytes=int(15.92 * GB), free_bytes=int(8.7 * GB),
                           ours_bytes=0, max_foreign_gb=3.0)


def test_foreign_vram_message_explains_why_own_process_guard_is_blind():
    with pytest.raises(MemoryGuardError) as exc:
        check_foreign_vram(total_bytes=int(15.92 * GB), free_bytes=int(8.7 * GB),
                           ours_bytes=0, max_foreign_gb=3.0)
    assert "wlasnego procesu" in str(exc.value)


def test_passes_below_threshold():
    # bf16 przy 1024 tokenach: zmierzone 8.83 GB na maszynie pomiarowej
    check_peak_memory(peak_bytes=int(8.83 * 2**30), limit_gb=14.0, context="bf16")


def test_raises_above_threshold():
    with pytest.raises(MemoryGuardError, match="przekroczyl"):
        check_peak_memory(peak_bytes=int(15.5 * 2**30), limit_gb=14.0, context="bf16")


def test_error_names_the_spill_mechanism_not_just_the_number():
    """Komunikat ma tlumaczyc DLACZEGO brak bledu CUDA nie oznacza sukcesu."""
    with pytest.raises(MemoryGuardError) as exc:
        check_peak_memory(peak_bytes=int(20 * 2**30), limit_gb=14.0, context="bf16")
    msg = str(exc.value)
    assert "RAM" in msg
    assert "15.5" in msg or "20.0" in msg
    assert "bf16" in msg


def test_fp32_control_uses_its_own_higher_limit():
    """Kontrola fp32 swiadomie przelewa do RAM - inny prog, jawnie nazwany."""
    check_peak_memory(peak_bytes=int(16.43 * 2**30), limit_gb=14.0,
                      context="fp32_control", fp32_control_limit_gb=24.0)


def test_fp32_control_still_bounded():
    with pytest.raises(MemoryGuardError):
        check_peak_memory(peak_bytes=int(30 * 2**30), limit_gb=14.0,
                          context="fp32_control", fp32_control_limit_gb=24.0)
