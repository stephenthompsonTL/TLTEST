from appium.webdriver.common.mobileby import MobileBy


class Locator:
    def __init__(self, l_type, selector):
        self.l_type = l_type
        self.selector = selector
        self._original_selector = selector

    def parameterize(self, *args):
        self.selector = self.selector.format(*args)

    def set_original_selector(self, value):
        _original_selector = value

    def get_original_selector(self):
        return self._original_selector


class Home:
    TextMenuItem = Locator(MobileBy.ACCESSIBILITY_ID, "Text")
    ViewsMenuItem = Locator(MobileBy.ACCESSIBILITY_ID, "Views")


class TextView:
    ButtonsMenuItem = Locator(MobileBy.ACCESSIBILITY_ID, "Buttons")


class ButtonsView:
    NormalButton = Locator(MobileBy.ACCESSIBILITY_ID, "Normal")
    SmallButton = Locator(MobileBy.ACCESSIBILITY_ID, "Small")
    ToggleButton = Locator(MobileBy.ACCESSIBILITY_ID, "Toggle")
