def test_query(db_engine):
    # Same engine object as in test_file_1
    assert db_engine["url"] == "postgresql://test"