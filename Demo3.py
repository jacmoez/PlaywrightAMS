import pytest
from playwright.sync_api import sync_playwright, Page

# --- FIXTURES ---

@pytest.fixture(scope="function")
def page_session():
    """Sets up the browser, context with specific initial viewport, and tears down after."""
    with sync_playwright() as p:
        # Launch browser maximized
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        
        # 1. Set initial specific window size (412x915) via viewport
        context = browser.new_context(viewport={"width": 412, "height": 915})
        page = context.new_page()
        
        yield page
        
        # Teardown
        context.close()
        browser.close()


# --- HELPER FUNCTIONS ---

def open_browser(page: Page):
    page.goto('https://www.saucedemo.com/')
    # 2. Change 'context' to 'page' to simulate maximizing the window
    page.set_viewport_size({"width": 1920, "height": 1080}) 
    print('Open Browser Success!')


def login(page: Page):
    # Enter partial details to trigger the first error
    page.locator('#user-name').fill('standard_user')
    page.locator('#login-button').click()

    err = page.locator('h3').text_content()
    print(err)
    
    page.locator('.error-button').click()

    password_field = page.locator('#password')
    password_field.fill('123')
    password_field.press('Enter')
    
    err = page.locator('h3').text_content()
    print(err)
    
    page.locator('.error-button').click()
    password_field.clear()
    
    password_field.fill('secret_sauce')
    password_field.press('Enter')
    print('Login Success')


def add_to_cart(page: Page):
    page.locator('#add-to-cart-sauce-labs-backpack').click()
    page.locator('#add-to-cart-sauce-labs-fleece-jacket').click()
    
    # Playwright comfortably handles escape characters in IDs natively
    page.locator("[id='add-to-cart-test.allthethings()-t-shirt-(red)']").click()

    # Remove item
    page.locator('#remove-sauce-labs-fleece-jacket').click()
    print("Add To Cart Success")


def view_cart(page: Page):
    # 1. Click to go to the cart page
    page.locator('.shopping_cart_link').click() 

    # 2. Click the red T-shirt link using its stable ID
    page.locator('#item_3_title_link').click()

    # 3. Grab the title and price on the details page
    title = page.locator('.inventory_details_name.large_size').text_content()
    price = page.locator('.inventory_details_price').text_content()

    print(title)
    print(price)

    # 4. Return to the cart page so the checkout button is visible
    page.locator('.shopping_cart_link').click()
    print("View Cart Success")


def check_out(page: Page):
    page.locator('#checkout').click()

    # Fill out the form
    page.locator('#first-name').fill("QA")
    page.locator('#last-name').fill("Testing") 
    page.locator('#postal-code').fill("123")
    print("Check Out Success")


def check_check_out(page: Page):
    page.locator('#continue').click()

    item_total = page.locator('.summary_subtotal_label').text_content()
    tax = page.locator('.summary_tax_label').text_content()
    total = page.locator('.summary_total_label').text_content()

    print(item_total)
    print(tax)
    print(total)
    print("Check Check Out Success")


def finish(page: Page):
    page.locator('#finish').click()

    complete = page.locator('h2').text_content()
    print(complete)

    page.locator('#back-to-products').click()
    print("Finish Success!")


def logout(page: Page):
    page.locator('#react-burger-menu-btn').click()
    page.locator("text=Logout").click()
    print('Logout Success')


# --- TEST CASE ---

def test_saucedemo_end_to_end(page_session):
    """The main test execution block running sequentially."""
    open_browser(page_session)
    login(page_session)
    add_to_cart(page_session)
    view_cart(page_session)
    check_out(page_session)
    check_check_out(page_session)
    finish(page_session)
    logout(page_session)