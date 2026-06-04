import os
import time
import pytest
from playwright.sync_api import Page, Browser

# We override the built-in browser_context_args fixture 
# to ensure the window starts maximized
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "no_viewport": True
    }



def test_basic_flows(page: Page):
    # --- A/B Testing ---
    page.goto('https://the-internet.herokuapp.com/')
    page.click('text="A/B Testing"')
    time.sleep(3)

    print(page.locator('h3').text_content())
    print(page.locator('p').first.text_content())

    page.go_back()
    time.sleep(3)

    # --- Add/Remove Elements ---
    page.click('text="Add/Remove Elements"')
    time.sleep(2)
    page.click('button[onclick="addElement()"]')
    time.sleep(2)
    page.locator('.added-manually').first.click()
    time.sleep(2)
    page.go_back()
    time.sleep(2)

    # --- Broken Images ---
    page.click('text="Broken Images"')
    time.sleep(2)
    page.go_back()
    time.sleep(2)

    # --- Challenging DOM ---
    page.click('text="Challenging DOM"')
    time.sleep(2)
    page.locator('.button').nth(0).click()
    time.sleep(3) 
    page.locator('.button.alert').click()
    time.sleep(3)
    page.locator('.button.success').click()
    page.go_back()

    # --- Checkboxes ---
    page.click('text="Checkboxes"')
    time.sleep(3)
    page.locator('#checkboxes input').nth(0).click()
    time.sleep(3)
    page.locator('#checkboxes input').nth(1).click()
    page.go_back()

    # --- Context Menu (Right Click & Alert) ---
    page.click('text="Context Menu"')
    time.sleep(3)
    print(page.locator('h3').text_content())
    
    # Accept the JavaScript dialog when it appears
    page.once("dialog", lambda dialog: dialog.accept())
    page.locator('#hot-spot').click(button="right")
    time.sleep(3)
    page.go_back()

    # --- Disappearing Elements ---
    page.click('text="Disappearing Elements"')
    time.sleep(2)
    page.click('text="Home"')
    time.sleep(3)
    page.click('text="Disappearing Elements"')
    time.sleep(2)

    for link_text in ["About", "Contact Us", "Portfolio"]:
        if page.locator(f'text="{link_text}"').is_visible():
            page.click(f'text="{link_text}"')
            time.sleep(2)
            print(page.locator('h1').text_content())
            page.go_back()
    time.sleep(3)
    page.go_back()
    time.sleep(2)

    # --- Drag and Drop ---
    page.click('text="Drag and Drop"')
    time.sleep(2)
    page.drag_and_drop('#column-b', '#column-a')
    time.sleep(3)
    page.go_back()

    # --- Dropdown ---
    page.click('text="Dropdown"')
    time.sleep(2)
    page.select_option('#dropdown', index=2) 
    time.sleep(2)


def test_entry_ad(page: Page):
    page.goto('https://the-internet.herokuapp.com/')
    page.click('text="Entry Ad"')
    time.sleep(2)
    page.click('.modal-footer p')
    time.sleep(2)
    print('Test : Entry Ad')


def test_exit_intent(page: Page):
    page.goto('https://the-internet.herokuapp.com/')
    page.click('text="Exit Intent"')
    
    # 1. Start the mouse near the center of the page
    page.mouse.move(x=400, y=400)
    time.sleep(1)
    
    # 2. Fast-move the mouse past the top boundary (y=0) to trigger the exit intent
    page.mouse.move(x=400, y=-10)
    
    # 3. Explicitly wait for the modal to become visible before clicking
    close_button = page.locator('.modal-footer p')
    close_button.wait_for(state="visible", timeout=5000)
    
    # 4. Click it!
    close_button.click()
    print("Test : Exit Intent Success")
    time.sleep(2)

def test_file_download(page: Page):
    page.goto('https://the-internet.herokuapp.com/')
    page.click('text="File Download"')
    time.sleep(2)
    
    # 1. Look for all download links inside the content area
    file_links = page.locator('#content a')
    
    if file_links.count() > 0:
        # 2. Target the first available file link dynamically
        first_file = file_links.nth(0)
        print(f"Downloading file: {first_file.text_content()}")
        
        # 3. Handle the download safely
        with page.expect_download() as download_info:
            first_file.click()
        download = download_info.value
        print(f"Downloaded file safely to: {download.path()}")
    else:
        print("No files available to download.")
        
    time.sleep(2)


def test_file_upload(page: Page):
    page.goto('https://the-internet.herokuapp.com/')
    page.click('text="File Upload"')
    
    test_file = os.path.join(os.getcwd(), 'test_upload.txt')
    with open(test_file, 'w') as f:
        f.write('this is test file content')

    page.set_input_files('#file-upload', test_file)
    time.sleep(2)
    page.click('#file-submit')
    time.sleep(2)
    
    os.remove(test_file)
    print("Test : file upload")


def test_basic_auth(browser: Browser):
    # Basic auth is isolated because it needs specific HTTP credentials applied at context creation
    context = browser.new_context(
        http_credentials={"username": "admin", "password": "admin"},
        no_viewport=True
    )
    auth_page = context.new_page()
    auth_page.goto('https://the-internet.herokuapp.com/basic_auth')
    time.sleep(2)
    
    text = auth_page.locator('#content div p').text_content()
    print(text)
    time.sleep(2)
    context.close()
    print('Test : Basic Auth')
