import pytest

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)


def test_divide_by_zero_message():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)

def test_divide_by_zero_capture():
    with pytest.raises(ValueError) as exc_info:
        divide(10, 0)
    assert str(exc_info.value) == "Cannot divide by zero"
    assert exc_info.type is ValueError


@pytest.mark.parametrize("a,b", [
    (10, 0),
    (99, 0),
    (-5, 0),
    (0, 0)
])
def test_divide_by_zero_multiple_inputs(a, b):
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(a, b)


def test_divide_normal():
    # Should NOT raise – we assert it runs without exception
    result = divide(10, 2)
    assert result == 5


def assert_division_fails(a, b):
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(a, b)

def test_division_failure():
    assert_division_fails(100, 0)


def divide_str(a: str, b: int):
    return int(a) / b

def test_invalid_input_type():
    with pytest.raises(TypeError):
        divide_str("10", "0")  # b should be int, not str

def test_all_divisions_fail():
    inputs = [(5,0), (8,0), (0,0)]
    for a, b in inputs:
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(a, b)

def divide(a,b):
    return a/b