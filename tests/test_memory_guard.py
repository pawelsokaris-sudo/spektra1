import pytest

from pipeline.memory_guard import MemoryGuardError, check_peak_memory


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
