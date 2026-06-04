import os
import time
import pytest
from playwright.sync_api import Page, BrowserContext

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "no_viewport": True,
        "permissions": ["geolocation"],
        "geolocation": {"latitude": 37.7749, "longitude": -122.4194} 
    }

def test_infinite_scroll(page: Page):
    page.goto("https://the-internet.herokuapp.com/infinite_scroll")
    time.tuple = 2
    
    initial_count = page.locator('.jscroll-added').count()
    
    for _ in range(5):
        # Playwright lets you scroll to the bottom of the page directly via the keyboard API
        page.keyboard.press("End")
        time.sleep(1.5) # Allow a tiny buffer for content to load dynamically
        
    final_count = page.locator('.jscroll-added').count()
    print(f'Initial paragraphs: {initial_count}')
    print(f'Final Count: {final_count}')
    assert final_count > initial_count


def test_inputs(page: Page):
    page.goto('https://the-internet.herokuapp.com/inputs')
    time.sleep(2)

    input_field = page.locator('input')
    
    # 1. Numbers work perfectly with .fill()
    input_field.fill("123")
    print(f'After Numbers: {input_field.input_value()}')
    time.sleep(1)
    input_field.clear()

    # 2. Letters: Simulate typing keys sequentially.
    # The browser will block them, meaning the input value will stay empty ("").
    input_field.focus()
    page.keyboard.type("abc") 
    print(f'After letters (should be empty): "{input_field.input_value()}"')
    assert input_field.input_value() == ""
    time.sleep(1)
    input_field.clear()

    # 3. Special Characters
    page.keyboard.type("!@")
    print(f'After special chars (should be empty): "{input_field.input_value()}"')
    assert input_field.input_value() == ""
    time.sleep(1)
    input_field.clear()

    # 4. Mixed Input (Only the digits '123' should register)
    page.keyboard.type("123abc")
    print(f'After mixed input (should only show numbers): {input_field.input_value()}')
    assert input_field.input_value() == "123"
    time.sleep(2)


def test_jquery_ui(page: Page):
    page.goto('https://the-internet.herokuapp.com/jqueryui/menu')
    time.sleep(2)
    
    # Hover over the cascade menu items
    page.locator('text="Enabled"').hover()
    time.sleep(1)
    page.locator('text="Downloads"').hover()
    time.sleep(1)
    
    # Trigger download inside the sub-hover menus
    with page.expect_download() as download_info:
        page.click('text="PDF"')
    download = download_info.value
    print(f"Downloaded JQuery Menu PDF to: {download.path()}")


def test_js_alerts(page: Page):
    page.goto('https://the-internet.herokuapp.com/javascript_alerts')
    time.sleep(2)
    
    result_locator = page.locator('#result')

    # 1. Standard Alert (Accept)
    page.once("dialog", lambda dialog: dialog.accept())
    page.click('button:has-text("Click for JS Alert")')
    print('Alert Text:', result_locator.text_content())
    time.sleep(3)
    # 2. Confirm Alert (Accept / OK)
    page.once("dialog", lambda dialog: dialog.accept())
    page.click('button:has-text("Click for JS Confirm")')
    print('Confirm Alert Text (OK):', result_locator.text_content())
    time.sleep(3)
    # 3. Confirm Alert (Dismiss / Cancel)
    page.once("dialog", lambda dialog: dialog.dismiss())
    page.click('button:has-text("Click for JS Confirm")')
    print('Confirm Alert Text (Cancel):', result_locator.text_content())
    time.sleep(3)
    # 4. Prompt Alert (Send text + Accept)
    page.once("dialog", lambda dialog: dialog.accept("Hello Playwright"))
    page.click('button:has-text("Click for JS Prompt")')
    print('Prompt Alert Text (OK):', result_locator.text_content())
    time.sleep(3)
    # 5. Prompt Alert (Send text + Dismiss)
    page.once("dialog", lambda dialog: dialog.dismiss())
    page.click('button:has-text("Click for JS Prompt")')
    print('Prompt Alert Text (Cancel):', result_locator.text_content())


def test_js_error(page: Page):
    # Setup an array to dynamically collect raw browser errors
    errors = []
    page.on("pageerror", lambda exc: errors.append(exc))
    
    page.goto('https://the-internet.herokuapp.com/javascript_error')
    time.sleep(2)
    
    print(f"Captured browser exceptions:")
    for err in errors:
        print(f" - Error: {err}")
    assert len(errors) > 0


def test_key_presses(page: Page):
    page.goto('https://the-internet.herokuapp.com/key_presses')
    time.sleep(1)
    
    # Playwright maps standard keyboard shortcuts to explicit strings
    test_keys = ["Enter", "Escape", "Space", "ArrowUp", "a", "b", "Tab"]
    
    target_input = page.locator('#target')
    result_locator = page.locator('#result')
    
    for key in test_keys:
        target_input.focus()
        page.keyboard.press(key)
        time.sleep(1)
        print(f'Key: {key} => Result: {result_locator.text_content()}')


def test_large_dom(page: Page):
    page.goto('https://the-internet.herokuapp.com/large')
    time.sleep(2)
    
    # Count matching elements instantly using locator queries
    all_elements_count = page.locator('*').count()
    print(f'Total elements in DOM: {all_elements_count}')
    
    # CSS selector matching ids starting with "sibling-"
    siblings_count = page.locator('[id^="sibling-"]').count()
    print(f'Number of siblings: {siblings_count}')

    # CSS selector matching classes starting with "row-"
    rows_count = page.locator('[class^="row-"]').count()
    print(f'Rows: {rows_count}')
