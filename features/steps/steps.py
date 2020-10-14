from behave import *
from time import sleep
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException
from pages.home_page import homePage
from pages.buttons_view_page import buttonsViewPage
from pages.text_view_page import textViewPage

@given('the Android app is launched')
def step_impl(context):
    pass


@then('we can click the text item in the Android app')
def step_impl(context):

    homePage.attach_driver(context.driver)
    homePage.click_text_item_from_menu()
    sleep(3)


@given('the iOS app is launched')
def step_impl(context):
    pass


@then('we can click the item in the iOS app')
def step_impl(context):
    try:
        element = context.driver.find_element_by_accessibility_id('Text Fields')
    except NoSuchElementException:
        raise
    finally:
        sleep(3)

@then('we can click the views item in the screen')
def step_impl(context):

    homePage.attach_driver(context.driver)
    homePage.click_views_item_from_menu()
    sleep(3)


@then('we can click the buttons item in the screen')
def step_impl(context):

    textViewPage.attach_driver(context.driver)
    textViewPage.click_button_item_from_menu()
    sleep(3)


@then('buttons will display')
def step_impl(context):

    buttonsViewPage.attach_driver(context.driver)
    buttonsViewPage.verify_buttons_displayed()
    sleep(3)