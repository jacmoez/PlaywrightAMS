import pytest

@pytest.mark.fast
def test_addition():
    assert 1 + 1 == 2

@pytest.mark.slow
def test_database_query():
    # Simulate slow DB operation
    import time
    time.sleep(2)
    assert True

@pytest.mark.fast
def test_string_upper():
    assert "hello".upper() == "HELLO"

@pytest.mark.slow
class TestSlowOperations:
    def test_file_processing(self):
        # heavy file I/O
        pass

    def test_api_call(self):
        # network request
        pass

@pytest.mark.fast
class TestFastMath:
    def test_add(self):
        assert 2 + 2 == 4

    def test_multiply(self):
        assert 3 * 3 == 9

@pytest.mark.fast
def test_parse_json():
    import json
    data = json.loads('{"key": "value"}')
    assert data["key"] == "value"


@pytest.mark.fast
def test_in_memory_sort():
    assert sorted([3,1,2]) == [1,2,3]

@pytest.mark.slow
def test_database_sort():
    # sort rows from real DB
    pass

def test_no():
    print('Hello')
'''
# Run only fast tests
pytest -m fast

# Run only slow tests
pytest -m slow

# Skip slow tests (run everything else)
pytest -m "not slow"

# Run both fast and slow (i.e., all tests)
pytest -m "fast or slow"



@pytest.mark.slow – Tests that take a long time (e.g., database calls, network requests, heavy computations). You typically skip them during quick feedback loops.

@pytest.mark.fast – Tests that run quickly (e.g., unit tests, simple logic checks). You run these often, like before every commit.
'''