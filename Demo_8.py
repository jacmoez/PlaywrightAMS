import os
import time
import pytest
from playwright.sync_api import Page, BrowserContext

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "no_viewport": True,
        # Mock geolocation permission and coordinates so the GPS test doesn't hang!
        "permissions": ["geolocation"],
        "geolocation": {"latitude": 37.7749, "longitude": -122.4194} 
    }

def test_menu(page: Page):
    page.goto('https://the-internet.herokuapp.com/')
    page.click('text="Floating Menu"')
    time.sleep(2)
    
    # Clicking floating elements
    page.click('text="Home"')
    time.sleep(2)
    page.click('text="News"')
    time.sleep(2)
    page.click('text="Contact"')
    time.sleep(2)
    page.click('text="About"')
    time.sleep(2)
    
    # Clicking the specific paragraph paragraph or link via flexible text/relative selector
    page.locator('p').nth(8).click()
    time.sleep(2)


def test_forgot_password(page: Page):
    try:
        page.goto('https://the-internet.herokuapp.com/forgot_password')
        time.sleep(2)

        # In Playwright, you can combine multiple CSS selectors with a comma. 
        # It will automatically find the first one that matches! No loop required.
        email_selector = '#email, input[name="email"], input[type="text"], input[type="email"]'
        email_field = page.locator(email_selector).first
        
        if email_field.is_visible():
            email_field.fill('ei@qa.com')
            time.sleep(1)
            print("Forgot Password form filled")
        else:
            print('Email field not found')
            
    except Exception as err:
        print(f'Forgot Password test caught an error: {err}')

    page.click('#form_submit')
    result = page.locator('h1').text_content()
    print(result)


def test_login(page: Page):
    page.goto('https://the-internet.herokuapp.com/login')
    time.sleep(2)

    # Attempting login with incorrect credentials
    page.fill('#username', 'QA Testing')
    time.sleep(2)
    page.fill('#password', '123456')
    time.sleep(2)
    page.click('.radius')
    time.sleep(3)

    # Get error message text
    error_text = page.locator('.flash.error').text_content()
    print(error_text)

    # Re-attempting login with correct credentials
    page.fill('#username', 'tomsmith')
    time.sleep(2)
    page.fill('#password', 'SuperSecretPassword!')
    time.sleep(2)
    page.click('.radius')
    time.sleep(2)

    # Validate secure area header
    print(page.locator('h4').text_content())
    
    # Logout
    page.click('.button.secondary.radius')


def test_hover(page: Page):
    page.goto('https://the-internet.herokuapp.com/hovers')
    time.sleep(2)
    
    # Instead of ActionChains, Playwright just uses .hover() directly on the element locator
    page.locator('.figure img').nth(0).hover()
    time.sleep(2)
    
    page.locator('.figcaption a').nth(0).click()
    time.sleep(2)


def test_gps(page: Page):
    page.goto('https://the-internet.herokuapp.com/geolocation')
    time.sleep(2)

    # Triggers the geolocation API
    page.click('button[onclick="getLocation()"]')
    
    # Because we mocked permissions and coordinates in the fixture setup, 
    # it loads instantly! No more time.sleep(25) required.
    page.click('#map-link')
    time.sleep(2)
