import pytest
from playwright.sync_api import sync_playwright, Page

# --- FIXTURE ---

@pytest.fixture(scope="module")
def shared_page():
    """Sets up a shared browser session for the entire testing sequence."""
    with sync_playwright() as p:
        # Launching Chromium (Can swap to p.firefox or p.webkit)
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        context = browser.new_context(no_viewport=True) # Uses full screen space natively
        page = context.new_page()
        
        yield page
        
        context.close()
        browser.close()


# --- INDIVIDUAL TEST CASES ---

def test_01_open_browser(shared_page: Page):
    shared_page.goto("https://testautomationpractice.blogspot.com/")
    print("Open Browser Success")


def test_02_input_text(shared_page: Page):
    # Fill, clear, and re-fill text field
    name_field = shared_page.locator('#name')
    name_field.fill("မောင်မောင်")
    name_field.clear()

    # Fill sequential inputs using placeholder start attributes (^=)
    user_data = ['မေမြတ်', '၀၉၆၆၅၅၄၄၃၃', 'qa@ams.com']
    input_fields = shared_page.locator('input[placeholder^="Enter"]').all()
    
    for i, data in enumerate(user_data):
        if i < len(input_fields):
            input_fields[i].fill(data)
            
    shared_page.locator('#textarea').fill('ဘန်ကောက်၊ ထိုင်း။')


def test_03_check_box(shared_page: Page):
    # Select Gender Radio
    shared_page.locator('#female').check()

    # Iterate and check specific checkboxes
    days = ['tuesday', 'sunday', 'friday']
    for day in days:
        shared_page.locator(f'#{day}').check()


def test_04_select_box(shared_page: Page):
    # Playwright natively handles dropdown selections via .select_option() using values
    shared_page.locator("#country").select_option(value="australia")
    shared_page.locator("#colors").select_option(value="blue")
    shared_page.locator("#animals").select_option(value="deer")


def test_05_date_picker(shared_page: Page):
    # Type directly into the date components
    shared_page.locator("#datepicker").fill("09/06/2025")
    shared_page.locator("#txtDate").fill("09/09/2025")
    shared_page.locator("#start-date").fill("09/06/2025")
    shared_page.locator("#end-date").fill("09/09/2025")
    
    shared_page.locator(".submit-btn").click()
    
    result = shared_page.locator("#result").text_content()
    print("Result : ", result)


# def test_06_file_upload(shared_page: Page):
#     # Provide local mock file paths or ensure these paths exist locally
#     img1 = "/Users/amsltd/Downloads/flower2.jpeg"
#     img2 = "/Users/amsltd/Downloads/flower1.jpeg"
    
#     # Single file upload
#     shared_page.locator("#singleFileInput").set_input_files(img1)
#     shared_page.locator('#singleFileForm >> button:has-text("Upload Single File")').click()
    
#     # Multiple files upload (Passed effortlessly as an array)
#     shared_page.locator("#multipleFilesInput").set_input_files([img1, img2])
#     shared_page.locator('#multipleFilesForm >> button:has-text("Upload Multiple Files")').click()


def test_07_table(shared_page: Page):
    # Grab all rows inside the target Book Table
    rows = shared_page.locator("table[name='BookTable'] tr").all()
    table_data = []

    for index, row in enumerate(rows):
        # Read table headers (th) on the first loop, otherwise read columns (td)
        cell_selector = "th" if index == 0 else "td"
        cells = row.locator(cell_selector).all_text_contents()
        table_data.append(cells)
        
    print("\n--- Book Table Data ---")
    for row in table_data:
        print("\t".join(row))


def test_08_pagination_table(shared_page: Page):
    print("\n--- Product Pagination Table Data ---")
    
    for i in range(1, 5):
        # Click through pagination numbers
        shared_page.locator(f'//*[@id="pagination"]/li[{i}]/a').click()
        
        # Pull rows out of the target table element
        rows = shared_page.locator("#productTable tr").all()
        table_data = []
        
        for index, row in enumerate(rows):
            cell_selector = "th" if index == 0 else "td"
            cells = row.locator(cell_selector).all_text_contents()
            table_data.append(cells)
            
        print(f"------------ Page {i} ---------")
        for row in table_data:
            print("\t".join(row))