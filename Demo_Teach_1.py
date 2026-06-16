import time
import pytest
from playwright.sync_api import Page,Browser,expect
import os
@pytest.fixture(scope='session')
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "args":['--start-maximized']
    }


@pytest.fixture(scope='session')
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "no_viewport":True
    }


def test_AB_testing(page:Page):
    page.goto('https://the-internet.herokuapp.com/')
    time.sleep(2)
    page.click('text="A/B Testing"')
    time.sleep(3)
    print(page.locator('h3').text_content())
    print(page.locator('p').text_content())

def test_add_or_remove_element(page:Page):
    page.goto('https://the-internet.herokuapp.com/')
    time.sleep(2)
    page.click('text="Add/Remove Elements"')
    time.sleep(2)
    add_count=10
    for _ in range(add_count):
        page.click('button[onclick="addElement()"]')
        time.sleep(1)
    delete_buttons=page.locator('.added-manually') # buttons
    time.sleep(2)
    print('Count ',delete_buttons.count())
    total_buttons = delete_buttons.count()
    print('Buttons found: ', total_buttons)
    for i in range(total_buttons - 1, -1, -1):
        delete_buttons.nth(i).click()
        page.wait_for_timeout(100) 
        
    print('Buttons left: ', delete_buttons.count())

def test_auth(browser:Browser):
    context=browser.new_context(
        http_credentials={'username':'admin',"password":'admin'},
        no_viewport=True
    )
    auth_page=context.new_page()
    auth_page.goto('https://the-internet.herokuapp.com/basic_auth')
    time.sleep(2)
    print(auth_page.locator('h3').text_content())
    print(auth_page.locator('p').text_content())
    
def test_broken_image(page:Page):
    page.goto('https://the-internet.herokuapp.com/')
    time.sleep(2)
    page.click('text="Broken Images"')
    print(page.locator('h3').text_content())

def test_dom(page:Page):
    page.goto('https://the-internet.herokuapp.com/')
    time.sleep(2)
    page.click('text="Challenging DOM"')
    # ['a']=l[0]
    page.locator('.button').nth(0).click()
    time.sleep(3)
    page.locator('.button.alert').nth(0).click()
    time.sleep(3)
    page.locator('.button.success').nth(0).click()
    time.sleep(3)

def test_dom(page:Page):
    page.goto('https://the-internet.herokuapp.com/')
    time.sleep(2)
    page.click('text="Checkboxes"')
    time.sleep(2)
    page.locator('#checkboxes input').nth(0).click()
    time.sleep(2)
    page.locator('#checkboxes input').nth(1).click()
    time.sleep(3)

def test_content_menu(page:Page):
    page.goto('https://the-internet.herokuapp.com/')
    time.sleep(2)
    page.click('text="Context Menu"')
    page.locator('#hot-spot').click(button='right')
    time.sleep(3)

        
def test_digest_auth(browser:Browser):
    context=browser.new_context(
        http_credentials={'username':'admin',"password":'admin'},
        no_viewport=True
    )
    auth_page=context.new_page()
    auth_page.goto('https://the-internet.herokuapp.com/digest_auth')
    time.sleep(10)
    print(auth_page.locator('h3').text_content())
    print(auth_page.locator('p').text_content())

def test_dispearing_element(page:Page):
    page.goto('https://the-internet.herokuapp.com/')
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
def test_drag_and_drop(page:Page):
    page.goto('https://the-internet.herokuapp.com/')
    page.click('text="Drag and Drop"')
    time.sleep(2)
    page.drag_and_drop('#column-b', '#column-a')
    time.sleep(3)
    page.go_back()

def test_drop_down(page:Page):
    page.goto('https://the-internet.herokuapp.com/')
    page.click('text="Dropdown"')
    time.sleep(2)
    page.select_option('#dropdown', index=2) 
    time.sleep(2)



def test_dynamic_content(page: Page):
    page.goto('https://the-internet.herokuapp.com/')
    page.get_by_role("link", name="Dynamic Content").click()
    text = page.locator('xpath=//*[@id="content"]/div[1]/div[2]').text_content()
    print('Text : ', text)
    page.reload()
    text = page.locator('xpath=//*[@id="content"]/div[1]/div[2]').text_content()
    print('Text : ', text)
    

def test_dynamic_control(page: Page):
    page.goto('https://the-internet.herokuapp.com/')
    page.get_by_role("link", name="Dynamic Controls").click()
    page.locator('#checkbox').click()
    page.locator('xpath=//*[@id="checkbox-example"]/button').click()
    input_button = page.locator('xpath=//*[@id="input-example"]/button')
    input_button.click()
    input_field = page.locator('xpath=//*[@id="input-example"]/input')
    input_field.fill('Hello Tester')       
    
    page.go_back()

def test_dynamic_loading(page: Page):
    page.goto('https://the-internet.herokuapp.com/')
    page.get_by_role("link", name="Dynamic Loading").click()
    # Example 1
    page.get_by_role("link", name="Example 1: Element on page that is hidden").click()
    page.locator('xpath=//*[@id="start"]/button').click()
    # Wait for the loaded text to become visible
    page.locator('#finish').wait_for(state="visible") 
    page.go_back()
    # Example 2
    page.get_by_role("link", name="Example 2: Element rendered after the fact").click()
    page.locator('xpath=//*[@id="start"]/button').click()
    page.locator('#finish').wait_for(state="visible")
    page.go_back()

def test_entry_ad(page: Page):
    page.goto('https://the-internet.herokuapp.com/')
    page.get_by_role("link", name="Entry Ad").click()
    # Click the "Close" option in the modal
    page.locator('xpath=//*[@id="modal"]/div[2]/div[3]/p').click()
    # Scrape text from tags
    h3 = page.locator('h3').first.text_content()
    p = page.locator('p').first.text_content()
    print(h3)
    print(p)
    page.go_back()

def test_exit_intent(page: Page):
    page.goto('https://the-internet.herokuapp.com/')
    page.get_by_role("link", name="Exit Intent").click()
    h3 = page.locator('h3').first.text_content()
    p = page.locator('p').first.text_content()
    print(h3)
    print(p)
    # Trigger exit intent modal by moving the mouse out of the viewport
    body_element = page.locator('body')
    body_element.click()
    body_element.evaluate("""(element) => {
        const event = new MouseEvent('mouseleave', {
            view: window,
            bubbles: true,
            cancelable: true
        });
        element.dispatchEvent(event);
    }""")
    # Click close on the modal that appears
    page.locator('xpath=//*[@id="ouibounce-modal"]/div[2]/div[3]/p').click()
    page.go_back()


def test_file_download(page: Page):
    page.goto('https://the-internet.herokuapp.com/')
    time.sleep(2)
    page.get_by_role("link", name="File Download").first.click()
    # Locate all link elements
    files = page.locator('a')
    # Print the text of all files listed on the page
    for i in range(files.count()):
        print('file : ', files.nth(i).text_content())
    # FIX: Catch the download event natively in Playwright
    with page.expect_download() as download_info:
        page.get_by_role("link", name="some-file.txt").click() 
    download = download_info.value
    # Optional: If you want to actually save the downloaded file to your machine:
    download.save_as(os.path.join(os.getcwd(), download.suggested_filename))
    print('Test : file download')
    page.go_back()


def test_file_upload(page: Page):
    page.goto('https://the-internet.herokuapp.com/')
    page.get_by_role("link", name="File Upload").click()
    # Create the temporary test file locally
    test_file = os.path.join(os.getcwd(), 'test_upload.txt')
    with open(test_file, 'w') as f:
        f.write('this is test file content')
        
    try:
        # FIX: Use Playwright's set_input_files to upload the file
        page.locator('#file-upload').set_input_files(test_file)
        
        # Click the upload submit button
        page.locator('#file-submit').click()
        print("Test : file upload")
        
    finally:
        # Always clean up and remove the local file even if the test fails
        if os.path.exists(test_file):
            os.remove(test_file)

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


def test_form_auth(page: Page):
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


def test_frames(page: Page):
    page.goto('https://the-internet.herokuapp.com/')
    
    # Use standard text selector instead of get_by_role
    page.click('text="Frames"')
    page.click('text="iFrame"')
    
    frame = page.frame_locator('#mce_0_ifr')
    text = frame.locator('xpath=//*[@id="tinymce"]/p').text_content()
    print('Text:', text)
    
    doc_text = page.locator('xpath=//*[@id="page-footer"]/div/div').text_content()
    print('Text :', doc_text)
    
    page.go_back()
    
    # Use standard text selector here too
    page.click('text="Nested Frames"')
    
    bottom_frame = page.frame_locator('frame[name="frame-bottom"]')
    expect(bottom_frame.locator('body')).to_contain_text("BOTTOM")
    
    page.go_back()
    page.go_back()
    print('Test:Test Frames')

def test_geolocation(page: Page):
    # Enable geolocation permissions inside the browser context
    page.context.grant_permissions(["geolocation"])
    # Set fallback mock coordinates (lat/long)
    page.context.set_geolocation({"latitude": 37.7749, "longitude": -122.4194})
    
    page.goto('https://the-internet.herokuapp.com/')
    page.click('text="Geolocation"')
    
    
    expect(page.locator('body')).to_contain_text("Geolocation")
    page.locator('xpath=/html/body/div[2]/div/div/button').click()
    
    # Grab the coordinates output
    lat_value = page.locator('#lat-value').text_content()
    long_value = page.locator('#long-value').text_content()
    print('Location :', lat_value)
    print('Location :', long_value)
    
    page.go_back()
    print('Test:Test Geolocation')

def test_horizontal_slider(page: Page):
    page.goto('https://the-internet.herokuapp.com/')
    
    page.click('text="Horizontal Slider"')
    slider = page.locator("css=input[type='range']")
    
    # Forward loop (1 to 5)
    for i in range(1, 6):
        slider.evaluate(f"(element) => {{ element.value = '{i}'; element.dispatchEvent(new Event('change')); }}")
        value = page.locator('#range').text_content()
        print('Slider Value :', value)
        
    print('------------------------------------')
    
    # Backward loop (5 to 0)
    for i in range(5, -1, -1):
        slider.evaluate(f"(element) => {{ element.value = '{i}'; element.dispatchEvent(new Event('change')); }}")
        value = page.locator('#range').text_content()
        print('Slider Value :', value)
        
    page.go_back()
    print('Test:Test Horizontal Slider')



# Hovers
def test_hovers(page: Page):
    page.goto('https://the-internet.herokuapp.com/')
    page.click('text="Hovers"')
    for i in range(1, 4):
        img_element = page.locator(f'xpath=//*[@id="content"]/div/div[{i}]/img')
        
        # Hover over the image to reveal details
        img_element.hover()
        print(f'Element: {i}')
        
        expect(page.locator('body')).to_contain_text(f"name: user{i}")
        expect(page.locator('body')).to_contain_text("View profile")
        
        print('Before clicking profile')
        # Click the link that gets revealed on hover
        page.locator(f"xpath=//div[@class='figure'][{i}]//a[contains(text(),'View profile')]").click()
        time.sleep(2)
        page.go_back()
        time.sleep(2)
        
    page.go_back()
    print('Test:Test Hovers')

# Infinite Scroll
def test_infinite_scroll(page: Page):
    page.goto('https://the-internet.herokuapp.com/')
    page.click('text="Infinite Scroll"')
    time.sleep(3)
    initial_count = page.locator('.jscroll-added').count()
    print(f'Initial Count : {initial_count}')
    for i in range(5):
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(1000) 
        new_count = page.locator('.jscroll-added').count()
        print(f'Scroll {i+1}: Content increased from {initial_count} to {new_count}')
        initial_count = new_count
        
    page.go_back()
    print('Test: Test Infinite Scroll')


# Inputs
def test_input(page: Page):
    page.goto('https://the-internet.herokuapp.com/')
    page.click('text="Inputs"')
    # Target the number input element
    input_field = page.locator('css=input[type="number"]')
    # Type '123' into the field
    input_field.fill('123')
    # Fetch headers and descriptions
    title = page.locator('h3').first.text_content()
    para = page.locator('p').first.text_content()
    print(f'\nTitle: {title}')
    print(f'\nParagraph : {para}')
    # Extract value attribute from the input and assert it
    value = input_field.input_value() # Playwright uses .input_value() for text/number fields
    print(value)
    assert value == "123"
    # Press 'ArrowUp' 5 times
    for _ in range(5):
        input_field.press('ArrowUp')
    after_increase_value = input_field.input_value()
    print(f'After Clicking UP arrow Key: {after_increase_value}')
    # Press 'ArrowDown' 6 times
    for _ in range(6):
        input_field.press('ArrowDown')
    after_decrease_value = input_field.input_value()
    print(f'After Clicking DOWN arrow Key: {after_decrease_value}')
    # Clear and type a negative number
    input_field.fill('-456') # .fill() clears the input automatically
    value = input_field.input_value()
    print(value)
    assert value == "-456"
    page.go_back()
    print('Test: Test Input')


# JQuery UI Menus
def test_jquery_ui_menus(page: Page):
    page.goto('https://the-internet.herokuapp.com/')
    page.click('text="JQuery UI Menus"')
    # Hover sequences to expand the dynamic menus
    page.locator('xpath=//*[@id="ui-id-3"]/a').hover()
    page.wait_for_timeout(500) # Give the slide animation a split second
    page.locator('xpath=//*[@id="ui-id-4"]/a').hover()
    page.wait_for_timeout(500)
    time.sleep(2)
    page.locator('xpath=//*[@id="ui-id-6"]/a').hover()
    page.wait_for_timeout(500)
    time.sleep(2)
    # Move back to the top item
    page.locator('xpath=//*[@id="ui-id-3"]/a').hover()
    # Click link to navigate to the intermediate page
    page.click('text="Back to JQuery UI"')
    title = page.locator('h3').first.text_content()
    para = page.locator('p').first.text_content()
    print(f'\nTitle: {title}')
    print(f'\nParagraph : {para}')
    # Click back to the menu
    page.click('text="Menu"')
    time.sleep(2)
    # Go back 3 times to get back to the home page matching your workflow
    page.go_back()
    page.go_back()
    page.go_back()
    print('Test: Test JQuery UI Menus')


# JavaScript Alerts
def test_javascript_alerts(page: Page):
    page.goto('https://the-internet.herokuapp.com/')
    page.click('text="JavaScript Alerts"')
    
    # --- 1. JS Alert (ACCEPT) ---
    # Setup listener to auto-accept
    page.once("dialog", lambda dialog: dialog.accept())
    page.get_by_role("button", name="Click for JS Alert").click()
    
    result = page.locator('#result').text_content()
    print(f'Click for JS Alert : {result}')
    
    # --- 2. JS Confirm (ACCEPT) ---
    page.once("dialog", lambda dialog: dialog.accept())
    page.get_by_role("button", name="Click for JS Confirm").click()
    
    result = page.locator('#result').text_content()
    print(f'Click for JS Confirm(OK) : {result}')
    
    # --- 3. JS Confirm (DISMISS) ---
    page.once("dialog", lambda dialog: dialog.dismiss())
    page.get_by_role("button", name="Click for JS Confirm").click()
    
    result = page.locator('#result').text_content()
    print(f'Click for JS Confirm( DISMISS ) : {result}')
    
    # --- 4. JS Prompt (ACCEPT with Input text) ---
    # lambda dialog: dialog.accept("Hello, Robot") handles both text and confirming
    page.once("dialog", lambda dialog: dialog.accept("Hello, Robot"))
    page.get_by_role("button", name="Click for JS Prompt").click()
    
    result = page.locator('#result').text_content()
    print(f'Click for JS Prompt(OK) : {result}')
    
    # --- 5. JS Prompt (DISMISS) ---
    page.once("dialog", lambda dialog: dialog.dismiss())
    page.get_by_role("button", name="Click for JS Prompt").click()
    
    result = page.locator('#result').text_content()
    print(f'Click for JS Prompt(Cancel) : {result}')
    
    page.go_back()
    print('Test: Test JavaScript Alerts')


# JavaScript onload event error
def test_js_onload_error(page: Page):
    # Setup an array to capture console errors
    errors = []
    page.on("pageerror", lambda err: errors.append(err))
    
    page.goto('https://the-internet.herokuapp.com/')
    page.click('text="JavaScript onload event error"')
    
    # Verify page text content
    expect(page.locator('body')).to_contain_text("This page has a JavaScript error in the onload event.")
    
    # Check that the body element itself exists
    expect(page.locator('body')).to_be_visible()
    
    # Optional print to console showing that you successfully caught the error!
    if errors:
        print(f"\nCaught Browser JS Error: {errors[0]}")
        
    page.go_back()
    print('Test: Test JavaScript onload event error')

# Key Presses
def test_key_presses(page: Page):
    page.goto('https://the-internet.herokuapp.com/')
    page.click('text="Key Presses"')
    
    
    keys_list = ["Tab","Space", "Escape", "Backspace"]
    
    for key in keys_list:
        print(f'Key: {key}')
        page.locator('body').press(key)
        time.sleep(2)
        
    
    input_texts = ["A", "P", "P", "L", "E"]
    target_input = page.locator('#target')
    
    for char in input_texts:
        print(f'Key: {char}')
        target_input.press(char)
        page.wait_for_timeout(100)
        
    # Extract what is currently written in the text box
    value = target_input.input_value()
    print(f'Input Value : {value}')
    assert value == "APPLE"
    
    page.go_back()
    print('Test: Test Key Presses')


# Large & Deep DOM
def test_large_and_deep_dom(page: Page):
    page.goto('https://the-internet.herokuapp.com/')
    page.click('text="Large & Deep DOM"')
    time.sleep(3)
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(3)
    # Count rows and log data
    rows = page.locator('table tr')
    table_rows_count = rows.count()
    print(f'Table Has {table_rows_count} rows')
    time.sleep(3)
    for i in range(table_rows_count):
        row_data = rows.nth(i).text_content()
        print(f'Table Row Data : {row_data.strip()}')
    time.sleep(3)
    page.go_back()
    print('Test: Test Large & Deep DOM')

# Multiple Windows
def test_multiple_windows(page: Page):
    page.goto('https://the-internet.herokuapp.com/')
    page.click('text="Multiple Windows"')
    # FIX: Catch the new tab/window event natively
    with page.context.expect_page() as new_page_info:
        page.click('text="Click Here"') # This link opens a new tab  
    new_tab = new_page_info.value
    new_tab.wait_for_load_state() # Ensure the new page is completely loaded
    # Close the new tab
    new_tab.close()
    # Your execution context is automatically still on the original `page`
    page.go_back()
    print('Test: Test Multiple Windows')


# Nested Frames
def test_nested_frames(page: Page):
    page.goto('https://the-internet.herokuapp.com/')
    page.click('text="Nested Frames"')
    
    frames_list = ["frame-left", "frame-middle", "frame-right"]
    
    for frame_name in frames_list:
        print(frame_name)
        # FIX: Chain frame locators to drill into nested structures
        nested_frame = page.frame_locator('frame[name="frame-top"]').frame_locator(f'frame[name="{frame_name}"]')
        text = nested_frame.locator('body').text_content()
        print(f'Frame Title : {text.strip()}')
        
    # Check the bottom frame (not nested inside frame-top)
    bottom_frame = page.frame_locator('frame[name="frame-bottom"]')
    bottom_text = bottom_frame.locator('body').text_content()
    print(f'Frame Title : {bottom_text.strip()}')
    
    page.go_back()
    print('Test: Test Nested Frames')

# Notification Messages
def test_notification_messages(page: Page):
    page.goto('https://the-internet.herokuapp.com/')
    page.click('text="Notification Messages"')
    
    # Check the initial alert banner (it loads dynamically, could be success or failure text)
    flash_notice = page.locator('#flash')
    expect(flash_notice).to_be_visible()
    print("Initial banner text:", flash_notice.text_content().strip())
    
    # Click to generate a new notification message status
    page.click('text="Click here"')
    
    # Playwright dynamically waits for the flash text to refresh
    expect(flash_notice).to_be_visible()
    print("Updated banner text:", flash_notice.text_content().strip())
    
    page.go_back()
    print('Test: Test Notification Messages')

# Redirect Link
def test_redirect_link(page: Page):
    page.goto('https://the-internet.herokuapp.com/')
    page.click('text="Redirect Link"')
    
    # Click the redirection trigger link
    page.click('text="here"')
    
    status_codes = ["200", "301", "404", "500"]
    
    for code in status_codes:
        page.click(f'text="{code}"')
        
        title = page.locator('h3').first.text_content()
        para = page.locator('p').first.text_content()
        print(f'\nTitle: {title.strip()}')
        print(f'\nParagraph : {para.strip()}')
        
        page.go_back()
        
    page.go_back()
    print('Test: Test Redirect Link')


# Secure File Download
def test_secure_file_download(browser: Browser):
    context=browser.new_context(
        http_credentials={'username':'admin',"password":'admin'},
        no_viewport=True
    )
    auth_page=context.new_page()
    auth_page.goto('https://the-internet.herokuapp.com/download_secure')
    time.sleep(2)
    # Grab the first link pointing to a .txt file
    download_file_locator = auth_page.locator("xpath=//a[contains(@href,'.txt')]").first
    filename = download_file_locator.text_content()
    print(f"Downloading file name: {filename}")
    
    # Capture the download workflow natively
    with auth_page.expect_download() as download_info:
        download_file_locator.click()
        
    download = download_info.value
    print('Test : Secure file download complete')

# Shadow DOM
def test_shadow_dom(page: Page):
    page.goto('https://the-internet.herokuapp.com/')
    page.click('text="Shadow DOM"')
    
    # FIX: Playwright natively pierces the Shadow DOM! 
    # You do not need any complex document.querySelector JavaScript injection.
    shadow_text = page.locator('my-paragraph').first.text_content()
    print(f'Shadow Text : {shadow_text.strip()}')
# Shifting Content
def test_shifting_content(page: Page):
    page.goto('https://the-internet.herokuapp.com/')
    page.click('text="Shifting Content"')
    
    # Example 1: Menu Element
    page.click('text="Example 1: Menu Element"')
    title = page.locator('h3').first.text_content()
    print(f'Menu Element Title : {title}')
    page.go_back()
    
    # Example 2: An image
    page.click('text="Example 2: An image"')
    
    # Loop over shifting paragraph links (Indices 2 through 5)
    for i in range(2, 6):
        page.locator(f'xpath=//*[@id="content"]/div/p[{i}]/a').click()
        print(i)
        page.wait_for_timeout(200) # Quick UI synchronization pause
        
    page.go_back()
    
    # Example 3: List
    page.goto('https://the-internet.herokuapp.com/shifting_content')
    page.click('text="Example 3: List"')
    
    para = page.locator('xpath=//*[@id="content"]/div/div/div').text_content()
    print(f'Para : {para.strip()}')
    
    page.reload()
    
    para = page.locator('xpath=//*[@id="content"]/div/div/div').text_content()
    print(f'Para : {para.strip()}')
    
    page.goto('https://the-internet.herokuapp.com/')

    # Sortable Data Tables
def test_sortable_data_tables(page: Page):
    page.goto('https://the-internet.herokuapp.com/')
    page.click('text="Sortable Data Tables"')
    time.sleep(5)
    # Fetch all table rows on the page
    rows = page.locator('//tr')
    rows_count = rows.count()
    
    for i in range(rows_count):
        row_data = rows.nth(i).text_content()
        # Using .split() cleans up messy vertical alignment spacing inside terminal output
        print(" ".join(row_data.split()))
        
    page.go_back()

# Status Codes
def test_status_codes(page: Page):
    page.goto('https://the-internet.herokuapp.com/')
    page.click('text="Status Codes"')
    
    status_code_links = ["200", "301", "404", "500"]
    
    for link in status_code_links:
        page.click(f'text="{link}"')
        
        title = page.locator('h3').first.text_content()
        para = page.locator('p').first.text_content()
        print(f'\nTitle: {title.strip()}')
        print(f'\nParagraph : {para.strip()}')
        
        page.go_back()
        
    page.go_back()
def test_typos(page: Page):
    page.goto('https://the-internet.herokuapp.com/')
    page.click('text="Typos"')
    
    # Reload the page 5 times and read the shifting text paragraph
    for i in range(5):
        page.reload()
        
        # Target the second paragraph which contains the typo ("won't" vs "wont")
        current_text = page.locator('p').nth(1).text_content()
        print(f'Current Text : {current_text.strip()}')
        print(f'Refresh {i+1}')
        
    page.go_back()
def test_wysiwyg_editor(page: Page):
    page.goto('https://the-internet.herokuapp.com/')
    page.click('text="WYSIWYG Editor"')
    
    # Wait for the editor UI to fully initialize on the page
    page.locator('#mce_0_ifr').wait_for(state="visible")
    
    # 1. Get initial content from the TinyMCE editor using browser execution
    result = page.evaluate("tinymce.activeEditor.getContent({format: 'text'})")
    print(f'Result : {result.strip()}')
    
    # 2. Set new content into the editor
    page.evaluate("tinymce.activeEditor.setContent('This is from automation test')")
    
    # 3. Read the content back out to verify the change
    result_updated = page.evaluate("tinymce.activeEditor.getContent({format: 'text'})")
    print(f'Result 1: {result_updated.strip()}')


def test_resource(page: Page):
    # Start the stopwatch
    start_time = time.time()
    page.goto('https://the-internet.herokuapp.com/slow')
    page.locator('text="Slow Resources"')
    # Stop the stopwatch
    end_time = time.time()
    loading_time = end_time - start_time
    print(f"Total Page Loading Time: {loading_time:.2f} seconds")
    # Assert that the load time must be under 10 seconds
    assert loading_time < 10.0, f"Page load was too slow! Took {loading_time:.2f} seconds."











