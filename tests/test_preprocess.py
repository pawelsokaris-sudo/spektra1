import numpy as np
import pytest

from pipeline.preprocess import (
    mask_tokens,
    positional_mean,
    subtract_positional,
    zscore_channels,
)


def test_mask_drops_first_32_tokens():
    H = np.arange(100, dtype=float).reshape(100, 1)
    out = mask_tokens(H, skip_first=32)
    assert out.shape == (68, 1)
    assert out[0, 0] == 32.0


def test_mask_drops_special_tokens_after_skip():
    H = np.arange(100, dtype=float).reshape(100, 1)
    special = np.zeros(100, dtype=bool)
    special[50] = True   # token specjalny w srodku
    special[10] = True   # w obrebie pierwszych 32 - i tak wyciete
    out = mask_tokens(H, special_mask=special, skip_first=32)
    assert out.shape == (67, 1)
    assert 50.0 not in out[:, 0]
    assert 51.0 in out[:, 0]


def test_positional_mean_and_subtraction_zero_out_shared_component():
    # dwa teksty o identycznym komponencie pozycyjnym -> po odjeciu zostaje roznica od sredniej
    rng = np.random.default_rng(0)
    pos = rng.standard_normal((50, 4))
    t1 = pos + 1.0
    t2 = pos - 1.0
    mu = positional_mean([t1, t2])
    np.testing.assert_allclose(mu, pos, atol=1e-12)
    out = subtract_positional([t1, t2], mu)
    np.testing.assert_allclose(out[0], np.ones((50, 4)), atol=1e-12)
    np.testing.assert_allclose(out[1], -np.ones((50, 4)), atol=1e-12)


def test_positional_mean_handles_ragged_lengths():
    t1 = np.ones((10, 2))
    t2 = 3.0 * np.ones((6, 2))
    mu = positional_mean([t1, t2])
    assert mu.shape == (10, 2)
    np.testing.assert_allclose(mu[:6], 2.0 * np.ones((6, 2)))   # srednia z obu
    np.testing.assert_allclose(mu[6:], 1.0 * np.ones((4, 2)))   # tylko t1 siega tak daleko
    out = subtract_positional([t1, t2], mu)
    assert out[0].shape == (10, 2)
    assert out[1].shape == (6, 2)


def test_zscore_gives_zero_mean_unit_variance():
    rng = np.random.default_rng(1)
    H = rng.standard_normal((200, 8)) * 5.0 + 3.0
    Z, n_excluded = zscore_channels(H)
    assert n_excluded == 0
    np.testing.assert_allclose(Z.mean(axis=0), 0.0, atol=1e-10)
    np.testing.assert_allclose(Z.var(axis=0), 1.0, atol=1e-10)


def test_zscore_excludes_low_variance_channels():
    rng = np.random.default_rng(2)
    H = rng.standard_normal((200, 5))
    H[:, 2] = 7.0  # kanal staly: wariancja 0 < eps
    Z, n_excluded = zscore_channels(H, eps=1e-6)
    assert n_excluded == 1
    assert Z.shape == (200, 4)
