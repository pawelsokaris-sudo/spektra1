import numpy as np
import pytest

from pipeline.window import WindowNotDecidedError, common_window, apply_window


def test_common_window_is_the_minimum_across_variants():
    assert common_window({"C": 950, "CprimG": 958, "B": 961}) == 950


def test_apply_window_truncates_all_variants_to_the_same_length():
    acts = {"C": np.zeros((950, 8)), "CprimG": np.zeros((958, 8))}
    out = apply_window(acts, mode="equalize")
    assert {k: v.shape[0] for k, v in out.items()} == {"C": 950, "CprimG": 950}


def test_apply_window_keeps_the_prefix_not_the_suffix():
    acts = {"C": np.arange(10).reshape(10, 1).astype(float),
            "CprimG": np.arange(12).reshape(12, 1).astype(float)}
    out = apply_window(acts, mode="equalize")
    np.testing.assert_array_equal(out["CprimG"][:, 0], np.arange(10))


def test_mode_none_leaves_lengths_untouched():
    acts = {"C": np.zeros((950, 8)), "CprimG": np.zeros((958, 8))}
    out = apply_window(acts, mode="none")
    assert {k: v.shape[0] for k, v in out.items()} == {"C": 950, "CprimG": 958}


def test_undecided_mode_refuses_to_run():
    """Wybor wchodzi do pieczeci - pipeline nie moze go podjac milczaco."""
    acts = {"C": np.zeros((950, 8)), "CprimG": np.zeros((958, 8))}
    with pytest.raises(WindowNotDecidedError, match="TBD-DECISION"):
        apply_window(acts, mode="TBD-DECISION")


def test_reports_how_many_tokens_were_dropped():
    acts = {"C": np.zeros((950, 8)), "CprimG": np.zeros((958, 8))}
    out, dropped = apply_window(acts, mode="equalize", report_dropped=True)
    assert dropped == {"C": 0, "CprimG": 8}
