import pytest
from playwright.sync_api import sync_playwright, Page
import time 


@pytest.fixture(scope="module")
def shared_page():
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=False,args=["--start-maximized"])
        context=browser.new_context(no_viewport=True)
        page=context.new_page()
        yield page
        context.close()
        browser.close()


def test_01_open_browser(shared_page: Page):
    shared_page.goto('https://www.saucedemo.com/')
    assert "Swag Labs" in shared_page.title()


@pytest.mark.parametrize("username,password", [
    ("standard_user", ""),
    ("locked_out_user", "secret_sauce"),
    ("", "secret_sauce"),
    ("standard_user", "secret_sauce"),
])
def test_login(shared_page: Page,username,password):
    shared_page.locator('#user-name').fill(username)
    time.sleep(3)
    password_field = shared_page.locator('#password')
    password_field.fill(password)
    # shared_page.locator('#login-button').click()
    password_field.press('Enter')
    time.sleep(3)
    shared_page.reload()

def test_sort_products(shared_page: Page):
    select= shared_page.locator('.product_sort_container')
    select.select_option(value="za")
    time.sleep(2)
    select.select_option(label="Price (low to high)")
    time.sleep(2)
    select.select_option(index=0)   # selects the third option
    time.sleep(2)
    shared_page.select_option('.product_sort_container', label="Price (low to high)")
    time.sleep(2)
    shared_page.select_option('.product_sort_container', value="za")
    time.sleep(2)
    shared_page.select_option('.product_sort_container', index=1)  


def test_add_to_cart(shared_page:Page):
    l=[
        'add-to-cart-sauce-labs-backpack',
        'add-to-cart-sauce-labs-bike-light',
        'add-to-cart-sauce-labs-bolt-t-shirt',
        'add-to-cart-sauce-labs-fleece-jacket',
        'add-to-cart-sauce-labs-onesie',
        # 'add-to-cart-test\.allthethings\(\)-t-shirt-\(red\)'
        ]
    time.sleep(3)
    for add_id in l:
        id=f'#{add_id}'
        shared_page.locator(id).click()
        time.sleep(2)
    add_button = shared_page.locator('[id="add-to-cart-test.allthethings()-t-shirt-(red)"]')
    add_button.click()
    
def test_remove_cart_data(shared_page:Page):
    l=[
        'remove-sauce-labs-backpack',
        'remove-sauce-labs-bolt-t-shirt',
        'remove-sauce-labs-onesie'
        ]
    time.sleep(3)
    for add_id in l:
        id=f'#{add_id}'
        shared_page.locator(id).click()
        time.sleep(2)

def test_detail(shared_page: Page):
    product_names = [
        "Sauce Labs Backpack",
        "Sauce Labs Bike Light",
        "Sauce Labs Bolt T-Shirt"
    ]
    for name in product_names:
        shared_page.locator('.inventory_item_name', has_text=name).click()
        shared_page.wait_for_load_state("networkidle")
        assert "inventory-item.html" in shared_page.url
        shared_page.go_back()
        time.sleep(2)
        shared_page.wait_for_load_state("networkidle")

def test_view_cart(shared_page: Page):
    time.sleep(2)
    shared_page.locator('.shopping_cart_link').click() 
    shared_page.locator('#item_3_title_link').click()
    
    title = shared_page.locator('.inventory_details_name.large_size').text_content()
    assert "Red" in title
    
    shared_page.locator('.shopping_cart_link').click()
    time.sleep(3)


def test_check_out(shared_page: Page):
    shared_page.locator('#checkout').click()
    shared_page.locator('#first-name').fill("QA")
    shared_page.locator('#last-name').fill("Testing") 
    shared_page.locator('#postal-code').fill("123")
    shared_page.locator("#continue").click()
    time.sleep(3)

def test_check_total(shared_page: Page):
    price_elements = shared_page.locator(".inventory_item_price")
    prices = [float(el.inner_text().replace("$", "")) for el in price_elements.all()]
    subtotal = sum(prices)

    tax_element = shared_page.locator(".summary_tax_label")
    tax_text = tax_element.inner_text()
    tax = float(tax_text.split("$")[1])

    total_element = shared_page.locator(".summary_total_label")
    total_text = total_element.inner_text()
    displayed_total = float(total_text.split("$")[1])

    calculated_total = subtotal + tax

    print(subtotal,tax,calculated_total)
    assert abs(calculated_total - displayed_total) < 0.01, "Total mismatch"

    time.sleep(2)
    shared_page.locator('#finish').click()

    
def test_logout(shared_page:Page):
    shared_page.locator('#react-burger-menu-btn').click()
    shared_page.locator("text=Logout").click()
    time.sleep(3)
