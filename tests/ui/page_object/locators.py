from selenium.webdriver.common.by import By

class LoginPageLocators(object):
    """A class for main page locators. All main page locators should come here"""

    LOGIN_BUTTON = (By.NAME, 'login')
    USER_TEXT = (By.NAME, 'username')
    PASSWORD_TEXT = (By.NAME, 'password')
