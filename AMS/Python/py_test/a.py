# test_basic.py
def test_addition():
    assert 1 + 1 == 2

def test_string_upper():
    assert "hello".upper() == "HELLO"

def test_list_contains():
    assert 3 in [1, 2, 3]