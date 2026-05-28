import pytest

@pytest.fixture(scope="session")
def db_engine():
    print("\n[Setup] Creating database engine (once for all tests)")
    engine = {"url": "postgresql://test", "connected": True}
    return engine
