# test_parametrize.py
import pytest

@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 5, 4),
    (100, -50, 50)
])
def test_add(a, b, expected):
    assert a + b == expected

# Combine parameters
@pytest.mark.parametrize("word", ["hello", "world"])
@pytest.mark.parametrize("n", [1, 2])
def test_repeat(word, n):
    assert word * n == word * n  # trivial, just shows combos