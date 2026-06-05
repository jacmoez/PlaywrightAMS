import time
import pytest
from playwright.sync_api import Page,Browser

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
