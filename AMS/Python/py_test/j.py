import pytest
@pytest.fixture(scope="function")
def temp_file():
    # Setup
    filename = "test_temp.txt"
    with open(filename, "w") as f:
        f.write("initial data")
    
    yield filename  # Provide fixture value to test
    
    # Teardown – runs after each test
    import os
    if os.path.exists(filename):
        os.remove(filename)

def test_write_to_file(temp_file):
    with open(temp_file, "a") as f:
        f.write("\nmore data")
    with open(temp_file) as f:
        content = f.read()
    assert "initial data\nmore data" in content

#=============================

@pytest.fixture(scope="function")
def fresh_list():
    return []

def test_add_one(fresh_list):
    fresh_list.append(1)
    assert fresh_list == [1]

def test_add_two(fresh_list):
    fresh_list.append(2)
    assert fresh_list == [2]  # Not [1,2] because it's a new list

#=======================================
@pytest.fixture(scope="function")
def base_value():
    return 10

@pytest.fixture(scope="function")
def computed_value(base_value):
    return base_value * 2

def test_computed(computed_value):
    assert computed_value == 20


@pytest.fixture(scope="function")
def base_value1():
    return 10

@pytest.fixture(scope="function")
def computed_value1(base_value):
    return base_value * 2

def test_computed1(computed_value):
    assert computed_value == 20

#=================================
@pytest.fixture(scope="function")
def user_dict():
    """Each test gets a brand new dict."""
    return {"name": "default", "age": 0}

def test_update_user(user_dict):
    user_dict["name"] = "Alice"
    assert user_dict["name"] == "Alice"

def test_user_reset(user_dict):
    # Starts fresh – no leftover "Alice"
    assert user_dict["name"] == "default"
#======================================
@pytest.fixture(scope="function")
def database_connection():
    # In real code, this would create a transaction
    print("\n[SETUP] New connection for test")
    conn = {"cursor": None, "data": []}
    yield conn
    print("[TEARDOWN] Closing connection\n")

def test_insert(database_connection):
    database_connection["data"].append(1)
    assert len(database_connection["data"]) == 1

def test_empty(database_connection):
    # Fresh connection – no leftover data from previous test
    assert len(database_connection["data"]) == 0