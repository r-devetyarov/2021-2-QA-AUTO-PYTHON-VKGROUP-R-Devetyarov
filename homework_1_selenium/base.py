import time
from typing import Tuple

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

CLICK_RETRY = 10
TIMEOUT = 20


class Base:
    def __init__(self, driver):
        self.driver = driver

    def find(self, locator: Tuple[By, str]):
        WebDriverWait(self.driver, TIMEOUT).until(
            EC.presence_of_element_located(locator)
        )
        return self.driver.find_element(*locator)

    def click_by(self, locator: Tuple[By, str]) -> None:
        self.wait_for_clickable(locator)
        for i in range(CLICK_RETRY):
            element = self.find(locator)
            try:
                element.click()
                return
            except StaleElementReferenceException:
                time.sleep(0.5)
                if i == CLICK_RETRY:
                    raise

    def wait_for_clickable(self, locator: Tuple[By, str], timeout=TIMEOUT):
        WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))

    def clear_and_send_keys(self, locator: Tuple[By, str], text: str):
        locator = self.find(locator)
        locator.clear()
        locator.send_keys(text)
