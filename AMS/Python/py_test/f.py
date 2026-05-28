# test_exception.py
import pytest

def divide(a, b):
    if b == 0:
        raise ValueError("Division by zero!")
    return a / b

def test_divide_by_zero():
    with pytest.raises(ValueError, match="Division by zero!"):
        divide(10, 0)

def test_exception_details():
    with pytest.raises(ZeroDivisionError) as exc_info:
        1 / 0
    assert "division by zero" in str(exc_info.value)