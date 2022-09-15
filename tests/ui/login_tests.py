import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Firefox()
driver.implicitly_wait(5) # seconds
driver.get("http://127.0.0.1:5000")
assert "Fistfight!" in driver.title


def enter_field_by_name(name, value, action=None):
    elem = driver.find_element(by=By.NAME, value=name)
    elem.clear()
    elem.send_keys(value)
    if action : elem.send_keys(action)


def verify_error(msg):
    elem = driver.find_element(by=By.CLASS_NAME, value="flashes")
    elems = elem.find_elements(by=By.CSS_SELECTOR, value="li")
    for el in elems:
        print(el.text)
        if msg in el.text:
            return True
    return False

enter_field_by_name("username", "pycon", Keys.RETURN)
assert verify_error("Invalid username")
time.sleep(1)

enter_field_by_name("username", "tom")
enter_field_by_name("password", "fooby", Keys.RETURN)
time.sleep(1)
assert verify_error("Invalid password")

link = driver.find_element(by=By.LINK_TEXT, value="Register")
link.click()
assert "Fistfight!" in driver.title

enter_field_by_name("username", "pycon", Keys.RETURN)
assert verify_error("Password is required")
time.sleep(1)

enter_field_by_name("password", "fooby", Keys.RETURN)
time.sleep(1)
assert verify_error("Username is required")

enter_field_by_name("username", "pycon")
enter_field_by_name("password", "fooby", Keys.RETURN)


# driver.close()


