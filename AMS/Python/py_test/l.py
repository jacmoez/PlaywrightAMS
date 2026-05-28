import pytest

#conftest.py
@pytest.fixture(scope="session")
def db_engine():
    print("\n[Setup] Creating database engine (once for all tests)")
    engine = {"url": "postgresql://test", "connected": True}
    return engine

# In test_file_1.py
def test_insert(db_engine):
    assert db_engine["connected"] is True

# In test_file_2.py (different test file)
def test_query(db_engine):
    # Same engine object as in test_file_1
    assert db_engine["url"] == "postgresql://test"

#=================================
# conftest.py
import pytest

@pytest.fixture(scope="session")
def session_counter():
    return {"count": 0}

# test_a.py
def test_a(session_counter):
    session_counter["count"] += 1
    assert session_counter["count"] == 1

# test_b.py
def test_b(session_counter):
    session_counter["count"] += 1
    assert session_counter["count"] == 2   # Continues from test_a!

#=============================================
@pytest.fixture(scope="session")
def reference_data():
    print("\n[Session] Generating huge reference data once")
    data = [i * i for i in range(100_000)]  # expensive computation
    return data

def test_checksum(reference_data):
    assert sum(reference_data) == expected

def test_slice(reference_data):
    assert reference_data[9999] == 9999**2
#======================================
# conftest.py
import pytest

@pytest.fixture(scope="session")
def global_state():
    print("\n[Session] Initializing global resources")
    resources = {"cache": {}}
    return resources

# test_module1.py
def test_one(global_state):
    global_state["cache"]["key1"] = "value1"

# test_module2.py
def test_two(global_state):
    # Can see what test_one left – beware of coupling
    assert "key1" in global_state["cache"]    