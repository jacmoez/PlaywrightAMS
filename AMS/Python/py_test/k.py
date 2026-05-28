import pytest

@pytest.fixture(scope="module")
def db_connection():
    print("\n[Setup] Creating database connection (once per module)")
    conn = {"host": "localhost", "connected": True}
    return conn

def test_insert(db_connection):
    assert db_connection["connected"] is True

def test_query(db_connection):
    # Same connection object as in test_insert
    assert db_connection["host"] == "localhost"
#=========================================

@pytest.fixture(scope="module")
def counter():
    return {"value": 0}

def test_increment(counter):
    counter["value"] += 1
    assert counter["value"] == 1

def test_increment_again(counter):
    # Counter retains value from previous test!
    counter["value"] += 1
    assert counter["value"] == 2   # Not 1 – be careful with mutable shared state

#=======================================
@pytest.fixture(scope="module")
def api_client():
    print("\n[Setup] Creating API client")
    return {"token": "abc123", "base_url": "https://api.example.com"}

@pytest.fixture(scope="module")
def authenticated_client(api_client):
    # Reuses the same api_client across the whole module
    api_client["authenticated"] = True
    return api_client

def test_get_user(authenticated_client):
    assert authenticated_client["authenticated"] is True

def test_post_data(authenticated_client):
    # Same client, still authenticated
    assert authenticated_client["token"] == "abc123"
#==================================
from selenium import webdriver

@pytest.fixture(scope="module")
def browser():
    print("\n[Setup] Launching browser once")
    driver = webdriver.Chrome()
    yield driver
    print("[Teardown] Closing browser")
    driver.quit()

def test_homepage(browser):
    browser.get("https://example.com")
    assert "Example" in browser.title

def test_contact(browser):
    # Same browser session – faster, but tests share cookies/session
    browser.get("https://example.com/contact")
    assert "Contact" in browser.title
#=================================
from selenium import webdriver

@pytest.fixture(scope="module")
def browser():
    print("\n[Setup] Launching browser once")
    driver = webdriver.Chrome()
    yield driver
    print("[Teardown] Closing browser")
    driver.quit()

def test_homepage(browser):
    browser.get("https://example.com")
    assert "Example" in browser.title

def test_contact(browser):
    # Same browser session – faster, but tests share cookies/session
    browser.get("https://example.com/contact")
    assert "Contact" in browser.title