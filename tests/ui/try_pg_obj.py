import time
import unittest
from selenium import webdriver
from  page_object import page

class Auth(unittest.TestCase):
    """A sample test class to show how page object works"""

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get("http://127.0.0.1:5000")

    def test_login(self):
        # Tests login happy path."""
        login_page = page.LoginPage(self.driver)

        #Checks if the word "Python" is in title
        self.assertTrue(login_page.is_title_matches(), "python.org title doesn't match.")
        time.sleep(1)
        #Sets the text of user textbox to "pycon"
        login_page.username_element = "tom"
        login_page.password_element = "tom1"
        time.sleep(1)
        login_page.click_login_button()

        #Verifies lobby page
        lobby_page = page.LobbyPage(self.driver)
        self.assertTrue(lobby_page.is_title_matches(), "No results found.")
        time.sleep(1)

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()