from .element import BasePageElement
from .locators import LoginPageLocators

class UserTextElement(BasePageElement):
    """This class gets the search text from the specified locator"""

    #The locator for search box where search string is entered
    locator = 'username'


class PasswordTextElement(BasePageElement):
    """This class gets the search text from the specified locator"""

    #The locator for search box where search string is entered
    locator = 'password'


class BasePage(object):
    """Base class to initialize the base page that will be called from all
    pages"""

    def __init__(self, driver):
        self.driver = driver


class LoginPage(BasePage):
    username_element = UserTextElement()
    password_element = PasswordTextElement()

    def is_title_matches(self):
        """Verifies that the hardcoded text "Python" appears in page title"""

        return "Fistfight!" in self.driver.title

    def click_login_button(self):
        """Triggers the search"""
        element = self.driver.find_element(*LoginPageLocators.LOGIN_BUTTON)
        element.click()
