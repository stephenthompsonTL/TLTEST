import time
from baseObjects.locators import TextView
from baseObjects.baseMethods import BaseMethods


class TextViewPage(BaseMethods):
    instance = None

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = TextViewPage()
        return cls.instance

    def __init__(self):
        super().__init__()

    def click_button_item_from_menu(self):
        super().perform_action_on_element(locator=TextView.ButtonsMenuItem, action="click")

textViewPage = TextViewPage.get_instance()
