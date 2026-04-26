import pytest

from solution import two_sum


def test_finds_basic_pair():
    assert two_sum([2, 7, 11, 15], 9) == (0, 1)


def test_handles_duplicate_values():
    assert two_sum([3, 3, 4], 6) == (0, 1)


def test_returns_increasing_indices():
    assert two_sum([5, 1, 4], 9) == (0, 2)


def test_raises_when_missing():
    with pytest.raises(ValueError):
        two_sum([1, 2, 3], 100)

