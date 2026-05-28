import pytest
from playwright.sync_api import sync_playwright, Page
import time 
# --- FIXTURE (Shared across all tests in this file) ---

@pytest.fixture(scope="module")
def shared_page():
    """Opens one browser session for the entire test file."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        context = browser.new_context(viewport={"width": 412, "height": 915})
        page = context.new_page()
        
        yield page
        
        context.close()
        browser.close()


# --- INDIVIDUAL TEST CASES ---

def test_01_open_browser(shared_page: Page):
    shared_page.goto('https://www.saucedemo.com/')
    shared_page.set_viewport_size({"width": 1920, "height": 1080}) 
    assert "Swag Labs" in shared_page.title()

def test_02_login(shared_page: Page):
    shared_page.locator('#user-name').fill('standard_user')
    shared_page.locator('#login-button').click()
    shared_page.locator('.error-button').click()

    password_field = shared_page.locator('#password')
    password_field.fill('123')
    password_field.press('Enter')
    shared_page.locator('.error-button').click()
    password_field.clear()
    
    password_field.fill('secret_sauce')
    password_field.press('Enter')
    
    # Simple assertion to ensure we logged in successfully
    assert shared_page.locator('.title').text_content() == "Products"
    print("Login Success")
    time.sleep(3)

def test_03_add_to_cart(shared_page: Page):
    shared_page.locator('#add-to-cart-sauce-labs-backpack').click()
    shared_page.locator('#add-to-cart-sauce-labs-fleece-jacket').click()
    shared_page.locator("[id='add-to-cart-test.allthethings()-t-shirt-(red)']").click()
    shared_page.locator('#remove-sauce-labs-fleece-jacket').click()
    time.sleep(3)
    print("Add To Cart Success")

def test_04_view_cart(shared_page: Page):
    shared_page.locator('.shopping_cart_link').click() 
    shared_page.locator('#item_3_title_link').click()
    
    title = shared_page.locator('.inventory_details_name.large_size').text_content()
    assert "Red" in title
    
    shared_page.locator('.shopping_cart_link').click()
    time.sleep(3)

def test_05_check_out(shared_page: Page):
    shared_page.locator('#checkout').click()
    shared_page.locator('#first-name').fill("QA")
    shared_page.locator('#last-name').fill("Testing") 
    shared_page.locator('#postal-code').fill("123")
    time.sleep(3)

def test_06_verify_totals(shared_page: Page):
    shared_page.locator('#continue').click()
    assert shared_page.locator('.summary_total_label').is_visible()
    time.sleep(3)

def test_07_finish_and_logout(shared_page: Page):
    shared_page.locator('#finish').click()
    assert "Thank you for your order!" in shared_page.locator('h2').text_content()
    
    shared_page.locator('#back-to-products').click()
    shared_page.locator('#react-burger-menu-btn').click()
    shared_page.locator("text=Logout").click()
    time.sleep(3)


"""
Intall python
python3 --version

mkdir playwright-python-project
cd playwright-python-project

Window
python -m venv venv
venv\Scripts\activate

python3 -m venv venv
source venv/bin/activate

pip install playwright pytest pytest-playwright

All browser
playwright install
playwright install chromium
playwright install firefox
playwright install webkit

python -m playwright install chromium
python -m playwright install firefox

tests/test_example.py
pytest --headed
pytest --browser chromium
pytest --browser firefox
pytest --browser webkit

playwright: command not found
python -m playwright install
playwright install

==========================================
mkdir playwright-python-project && cd playwright-python-project

python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install playwright pytest pytest-playwright

playwright install

pytest --headed  
pytest --headed --browser chromium 
===========================================



"""
