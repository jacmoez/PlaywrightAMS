import pytest
from playwright.sync_api import sync_playwright
import time
# ==========================================
# FIXTURE: Handles Setup and Teardown Once
# ==========================================
@pytest.fixture(scope="class")
def demo_bot():
    """Initializes Playwright and yields the bot instance to all tests."""
    with sync_playwright() as playwright:
        bot = SauceDemoTestRunner(playwright)
        yield bot
        bot.close_browser()


# ==========================================
# TEST CLASS: Each method is a standalone test
# ==========================================
class TestSauceDemoSuite:

    def test_01_open_browser(self, demo_bot):
        demo_bot.open_browser()

    def test_02_login(self, demo_bot):
        demo_bot.login()

    def test_03_add_to_cart(self, demo_bot):
        demo_bot.add_to_cart()

    def test_04_view_cart(self, demo_bot):
        demo_bot.view_cart()

    def test_05_check_out(self, demo_bot):
        demo_bot.check_out()

    def test_06_verify_checkout_totals(self, demo_bot):
        demo_bot.check_check_out()

    def test_07_finish_order(self, demo_bot):
        demo_bot.finish()

    def test_08_logout(self, demo_bot):
        demo_bot.logout()


# ==========================================
# CORE ENGINE: Your unmodified browser logic
# ==========================================
class SauceDemoTestRunner:

    def __init__(self, playwright_instance):
        self.browser = playwright_instance.chromium.launch(
            headless=False, 
            args=["--start-maximized"]
        )
        # self.context = self.browser.new_context(viewport={"width": 412, "height": 915})
        self.page = self.context.new_page()
        
    def open_browser(self):
        self.page.goto('https://www.saucedemo.com/')
        self.page.set_viewport_size({"width": 1920, "height": 1080}) 
        print('\nOpen Browser Success!')
        time.sleep(2)
        

    def login(self):
        self.page.locator('#user-name').fill('standard_user')
        self.page.locator('#login-button').click()
        
        err = self.page.locator('h3').text_content()
        print(f"\nCaptured Error 1: {err}")
        self.page.locator('.error-button').click()

        password_field = self.page.locator('#password')
        password_field.fill('123')
        password_field.press('Enter')
        
        err = self.page.locator('h3').text_content()
        print(f"Captured Error 2: {err}")
        self.page.locator('.error-button').click()
        password_field.clear()
        
        password_field.fill('secret_sauce')
        password_field.press('Enter')
        print('Login Success')
        time.sleep(2)

    def add_to_cart(self):
        self.page.locator('#add-to-cart-sauce-labs-backpack').click()
        self.page.locator('#add-to-cart-sauce-labs-fleece-jacket').click()
        self.page.locator("[id='add-to-cart-test.allthethings()-t-shirt-(red)']").click()
        self.page.locator('#remove-sauce-labs-fleece-jacket').click()
        print("Add To Cart Success")
        time.sleep(2)

    def view_cart(self):
        self.page.locator('.shopping_cart_link').click() 
        self.page.locator('#item_3_title_link').click()

        title = self.page.locator('.inventory_details_name.large_size').text_content()
        price = self.page.locator('.inventory_details_price').text_content()
        print(f"Item: {title} | Price: {price}")

        self.page.locator('.shopping_cart_link').click()
        print("View Cart Success")
        time.sleep(2)
    def check_out(self):
        self.page.locator('#checkout').click()
        self.page.locator('#first-name').fill("QA")
        self.page.locator('#last-name').fill("Testing") 
        self.page.locator('#postal-code').fill("123")
        print("Check Out Success")
        time.sleep(2)

    def check_check_out(self):
        self.page.locator('#continue').click()
        item_total = self.page.locator('.summary_subtotal_label').text_content()
        tax = self.page.locator('.summary_tax_label').text_content()
        total = self.page.locator('.summary_total_label').text_content()
        print(f"{item_total} | {tax} | {total}")
        print("Check Check Out Success")
        time.sleep(2)

    def finish(self):
        self.page.locator('#finish').click()
        complete = self.page.locator('h2').text_content()
        print(f"Confirmation status: {complete}")
        self.page.locator('#back-to-products').click()
        print("Finish Success!")
        time.sleep(2)

    def logout(self):
        self.page.locator('#react-burger-menu-btn').click()
        self.page.locator("text=Logout").click()
        print('Logout Success')
        time.sleep(2)
        
    def close_browser(self):
        self.context.close()
        self.browser.close()