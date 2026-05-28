# test_class.py
class TestMathOperations:
    def test_add(self):
        assert 2 + 3 == 5

    def test_multiply(self):
        assert 3 * 4 == 12

class TestStringOperations:
    def test_lower(self):
        assert "PYTHON".lower() == "python"