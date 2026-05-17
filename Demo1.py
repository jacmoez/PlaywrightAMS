import pytest
from playwright.sync_api import sync_playwright

class SauceDemo:

    def __init__(self, playwright_instance):
        # Using Chromium (which powers Edge and Chrome)
        self.browser = playwright_instance.chromium.launch(
            headless=False, 
            args=["--start-maximized"]
        )
        # 1. Set the initial specific window size (412x915) via viewport
        self.context = self.browser.new_context(viewport={"width": 412, "height": 915})
        self.page = self.context.new_page()
        
    def open_browser(self):
        self.page.goto('https://www.saucedemo.com/')
        
        # 2. Change 'context' to 'page' to simulate maximizing the window
        self.page.set_viewport_size({"width": 1920, "height": 1080}) 
        print('Open Browser Success!')

    def login(self):
        # Enter partial details to trigger the first error
        self.page.locator('#user-name').fill('standard_user')
        self.page.locator('#login-button').click()

        err = self.page.locator('h3').text_content()
        print(err)
        
        self.page.locator('.error-button').click()

        password_field = self.page.locator('#password')
        password_field.fill('123')
        password_field.press('Enter')
        
        err = self.page.locator('h3').text_content()
        print(err)
        
        self.page.locator('.error-button').click()
        password_field.clear()
        
        password_field.fill('secret_sauce')
        password_field.press('Enter')
        print('Login Success')

    def add_to_cart(self):
        self.page.locator('#add-to-cart-sauce-labs-backpack').click()
        self.page.locator('#add-to-cart-sauce-labs-fleece-jacket').click()
        
        # Playwright comfortably handles escape characters in IDs natively
        self.page.locator("[id='add-to-cart-test.allthethings()-t-shirt-(red)']").click()

        # Remove item
        self.page.locator('#remove-sauce-labs-fleece-jacket').click()
        print("Add To Cart Success")

    def view_cart(self):
        # 1. Click to go to the cart page
        self.page.locator('.shopping_cart_link').click() 

        # 2. Click the red T-shirt link using its stable ID instead of text matching
        self.page.locator('#item_3_title_link').click()

        # 3. Grab the title and price on the details page
        title = self.page.locator('.inventory_details_name.large_size').text_content()
        price = self.page.locator('.inventory_details_price').text_content()

        print(title)
        print(price)

        # 4. Return to the cart page so the checkout button is visible for the next step
        self.page.locator('.shopping_cart_link').click()
        print("View Cart Success")

    def check_out(self):
        self.page.locator('#checkout').click()

        # Fill out the form
        self.page.locator('#first-name').fill("QA")
        self.page.locator('#last-name').fill("Testing") 
        self.page.locator('#postal-code').fill("123")
        print("Check Out Success")

    def check_check_out(self):
        self.page.locator('#continue').click()

        item_total = self.page.locator('.summary_subtotal_label').text_content()
        tax = self.page.locator('.summary_tax_label').text_content()
        total = self.page.locator('.summary_total_label').text_content()

        print(item_total)
        print(tax)
        print(total)
        print("Check Check Out Success")

    def finish(self):
        self.page.locator('#finish').click()

        complete = self.page.locator('h2').text_content()
        print(complete)

        self.page.locator('#back-to-products').click()
        print("Finish Success!")

    def logout(self):
        self.page.locator('#react-burger-menu-btn').click()
        self.page.locator("text=Logout").click()
        print('Logout Success')
        
    def close_browser(self):
        self.context.close()
        self.browser.close()

    def main(self):
        self.open_browser()
        self.login()
        self.add_to_cart()
        self.view_cart()
        self.check_out()
        self.check_check_out()
        self.finish()
        self.logout()
        self.close_browser()


# FIX: This explicit function wrapper makes Pytest recognize and execute the script
def test_saucedemo_end_to_end():
    with sync_playwright() as playwright:
        bot = SauceDemo(playwright)
        bot.main()