# test_fixture_yield.py
import pytest

@pytest.fixture
def temp_file():
    print("\nSetup: create temporary file")
    with open("temp.txt", "w") as f:
        f.write("test data")
    yield "temp.txt"                  # provide resource to test
    print("\nTeardown: delete temporary file")
    import os
    os.remove("temp.txt")

def test_file_content(temp_file):
    with open(temp_file) as f:
        content = f.read()
    assert content == "test data"