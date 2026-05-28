import pytest

@pytest.mark.skip(reason="Test is pointless: 2+2 never changes")
def test_always_true():
    assert 2 + 2 == 4
    

import pytest
# Simple condition: skip on Friday
import datetime
today_is_friday = datetime.datetime.today().weekday() == 4

@pytest.mark.skipif(today_is_friday, reason="No tests on Friday! Go home early.")
def test_work_hours():
    assert check_system() == "operational"



import pytest
@pytest.mark.xfail(reason="Known bug: reverse of empty string raises error")
def test_reverse_empty_string():
    assert reverse_string("") == ""