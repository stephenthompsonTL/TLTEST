import time
from baseObjects.locators import ButtonsView
from baseObjects.baseMethods import BaseMethods


class ButtonsViewPage(BaseMethods):
    instance = None

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = ButtonsViewPage()
        return cls.instance

    def __init__(self):
        super().__init__()

    def verify_buttons_displayed(self):
        super().get_element_text(ButtonsView.NormalButton)


buttonsViewPage = ButtonsViewPage.get_instance()
