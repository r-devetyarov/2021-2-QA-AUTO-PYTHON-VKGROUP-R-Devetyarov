from typing import Tuple

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

CLICK_RETRY = 3
TIMEOUT = 5


class WebDriverWaitingException(Exception):
    pass


class Base:
    def __init__(self, driver):
        self.driver = driver

    def find(self, locator: Tuple[By, str]):
        try:
            self.wait().until(EC.presence_of_element_located(locator))
            return self.driver.find_element(*locator)
        except TimeoutException:
            raise WebDriverWaitingException(f"Element {locator[1]} not presence after {TIMEOUT}sec")

    def click_by(self, locator: Tuple[By, str]) -> None:
        for i in range(CLICK_RETRY):
            try:
                self.find(locator)
                elem = self.wait().until(EC.element_to_be_clickable(locator))
                elem.click()
                return
            except StaleElementReferenceException:
                if i == CLICK_RETRY - 1:
                    raise
            except TimeoutException:
                raise WebDriverWaitingException(f"Element {locator[1]} not clickable after {TIMEOUT}sec")

    def clear_and_send_keys(self, locator: Tuple[By, str], text: str):
        locator = self.find(locator)
        locator.clear()
        locator.send_keys(text)

    def wait(self, timeout=TIMEOUT):
        return WebDriverWait(self.driver, timeout=timeout)
