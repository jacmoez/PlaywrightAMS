from conftest import db_engine
def test_insert(db_engine):
    assert db_engine["connected"] is True