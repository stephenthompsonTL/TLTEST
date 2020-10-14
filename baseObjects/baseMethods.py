import re
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import pyodbc

from settings.config import settings
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import logging



RunTimeValue = ""

class NoSuchActionExist(Exception):
    print("This action has not been defined")

class AllItemsLoaded(Exception):
    print("All page items loaded")

class BaseMethods:

    def __init__(self):
        self.driver = None

    def attach_driver(self, driver):
        self.driver = driver

    def detach_driver(self):
        self.driver = None

    def _execute_with_wait(self, condition):
        return WebDriverWait(self.driver, 5).until(condition)

    def wait_for_element(self, locator):
        self._execute_with_wait(ec.element_to_be_clickable(locator.l_type, locator.selector))

    def wait_for_items_to_load(self):
        try:
            if (self.driver.find_element("xpath", "//span[text()='Loading menu items...']").is_displayed()) == True:
                time.sleep(30)
        except:
            print("All items loaded")

    def count_all_elements(self, locator):
        return len(self.driver.find_elements(locator.l_type, locator.selector))

    def element_exists(self, locator):
        try:
            time.sleep(1)
            self._execute_with_wait(ec.presence_of_element_located((locator.l_type, locator.selector)))
            return True
        except TimeoutException:
            return False

    def get_element(self, locator, text=""):
        if "ObjectToken" in locator.selector:
            locator.selector = locator.selector.replace("ObjectToken", RunTimeValue)
        isExist = self.element_exists(locator)
        if not isExist:
            raise NoSuchElementException("Could not find ->" + locator.selector)
        return self.driver.find_element(locator.l_type, locator.selector)

    def get_element_text(self, locator):
        if "ObjectToken" in locator.selector:
            locator.selector = locator.selector.replace("ObjectToken", RunTimeValue)
        if not self.element_exists(locator):
            raise NoSuchElementException("Could not find {locator.selector}")
        return self.driver.find_element(locator.l_type, locator.selector).text

    def get_dynamic_text_from_element(self, locator, text):
        global RunTimeValue
        RunTimeValue = text
        dynamic_text = self.get_element(locator, text).text
        locator.selector = re.sub(r"'[A-Z _/a-z]+'", "'ObjectToken'", locator.selector)
        return dynamic_text

    def wait_for_page_load(self):
        self.log.info("Checking if {} page is loaded.".format(self.driver.current_url))
        page_state = self.driver.execute_script('return document.readyState;')
        return page_state == 'complete'

    def enter_text_in_dynamic_field(self, locator, text_to_locate_element, text_to_enter):
        global RunTimeValue
        RunTimeValue = text_to_locate_element
        self.get_element(locator).send_keys(text_to_enter)
        locator.selector = locator.get_original_selector()

    def multi_select_for_dynamic_element(self,main_element,option_to_select):
        ActionChains(self.driver).move_to_element(self.driver.find_element_by_xpath("//div[text()='"+main_element+"']/following-sibling::div//li//span[contains(text(),'"+option_to_select+"')]")).click().perform()

    def perform_action_on_element(self, locator, action: str, text="", text_to_enter=""):
        try:
            global RunTimeValue
            flag = False
            RunTimeValue = text
            action = action.lower()
            if "ObjectToken" in locator.selector:
                flag = True
            if action == "click":
                self.get_element(locator).click()
            elif action == "get_text":
                value = self.get_element_text(locator)
                locator.selector = locator.get_original_selector()
                return value
            elif action == "execute_script_click":
                self.driver.execute_script("arguments[0].click();", self.get_element(locator))
            elif action == "type":
                self.get_element(locator).send_keys(text)
            elif action == "type_with_generic_locator":
                self.get_element(locator).send_keys(text_to_enter)
            elif action == "clear":
                self.get_element(locator).clear()
            elif action == "ctra_delete":
                ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('a').perform()
                ActionChains(self.driver).send_keys(Keys.DELETE).perform()
            elif action == "clickwithactionclass":
                ActionChains(self.driver).move_to_element(self.get_element(locator)).click().perform()
            elif action == "scroll":
                self.driver.execute_script("arguments[0].scrollIntoView(true)", self.get_element(locator))
            elif action == "scroll_into_middle":
                view_port_height = "var viewPortHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);"
                element_top = "var elementTop = arguments[0].getBoundingClientRect().top;"
                js_function = "window.scrollBy(0, elementTop-(viewPortHeight/2));"
                scroll_into_middle = view_port_height + element_top + js_function
                self.driver.execute_script(scroll_into_middle, self.get_element(locator))
            elif action == "switch_tab":
                ActionChains(self.driver).key_down(Keys.CONTROL).key_down(Keys.TAB).key_up(Keys.TAB).key_up(Keys.CONTROL).perform()
            elif action == "press_enter":
                ActionChains(self.driver).key_down(Keys.ENTER).key_up(Keys.ENTER).perform()
            elif action == "press_end":
                ActionChains(self.driver).key_down(Keys.END).key_up(Keys.END).perform()
            elif action == "present":
                try:
                   assert self.get_element(locator).is_displayed()
                except:
                    print(text + " -> Element is not displayed on the page")
                    assert False, text + " Element is not displayed on the page"
            elif action == "not_present":
                if self.count_all_elements(locator)==0:
                    assert True, "User does not have access to current action. PASSED"
                else:
                    assert False, text + " Element is displayed on the page which is invalid in this case. FAILED"
            elif action == "not_display":
                if "ObjectToken" in locator.selector:
                    locator.selector = locator.selector.replace("ObjectToken", RunTimeValue)
                number_of_elements = self.driver.find_elements_by_xpath(locator.selector)
                if(len(number_of_elements)):
                    assert False, "Element is displayed on the page. FAILED"
                else:
                    assert True, "Element is not displayed on the page. PASSED"
            else:
                raise NoSuchActionExist(action)
            if flag:
                locator.selector = locator.get_original_selector()
        except:
            locator.selector = locator.get_original_selector()
            logging.info(action + " on " +str(locator.selector) +" is not working")
            assert False, action +" on " +str(locator.selector) +" is failing"


