import time
from baseObjects.locators import Home
from baseObjects.baseMethods import BaseMethods


class HomePage(BaseMethods):
    instance = None

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = HomePage()
        return cls.instance

    def __init__(self):
        super().__init__()

    def click_text_item_from_menu(self):
        super().perform_action_on_element(locator=Home.TextMenuItem, action="click")

    def click_views_item_from_menu(self):
        super().perform_action_on_element(locator=Home.ViewsMenuItem, action="click")

homePage = HomePage.get_instance()
