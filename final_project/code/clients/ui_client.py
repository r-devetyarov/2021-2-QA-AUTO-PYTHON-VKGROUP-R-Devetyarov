import logging
from typing import Tuple

import allure
import faker
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

CLICK_RETRY = 3
TIMEOUT = 5


class WebDriverWaitingException(Exception):
    pass


class UiClient:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.logger = logging.getLogger('test')
        self.faker = faker.Faker()

    @allure.step("Find element with locator {locator}")
    def find(self, locator: Tuple[By, str]):
        try:
            self.wait().until(EC.presence_of_element_located(locator))
            return self.driver.find_element(*locator)
        except TimeoutException:
            raise WebDriverWaitingException(f"Element {locator[1]} not presence after {TIMEOUT}sec")

    @allure.step("Clicking element {locator}")
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

    @allure.step("CLear and send keys {locator}")
    def clear_and_send_keys(self, locator: Tuple[By, str], text: str):
        self.logger.info(f"Send text {text} in field {locator}")
        locator = self.find(locator)
        locator.clear()
        locator.send_keys(text)

    def wait(self, timeout=TIMEOUT):
        return WebDriverWait(self.driver, timeout=timeout)

    @allure.step("Get element {locator} is presence in DOM")
    def element_is_presence(self, locator: Tuple[By, str], timeout: int = 3) -> bool:
        try:
            self.wait(timeout=timeout).until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    @allure.step("Find elements {locator}")
    def find_elements_by(self, locator: Tuple[By, str]):
        try:
            self.wait().until(EC.presence_of_element_located(locator))
            return self.driver.find_elements(*locator)
        except TimeoutException:
            raise WebDriverWaitingException(f"Element {locator[1]} not presence after {TIMEOUT}sec")

    @allure.step("Get attribute {attribute_name} from {locator}")
    def get_attribute_by_name(self, locator, attribute_name: str) -> str:

        attribute = self.find(locator).get_attribute(attribute_name)
        self.logger.info(f"Got attribute {attribute} from element {locator}")
        return attribute

    @allure.step("Refresh page")
    def refresh_page(self):
        self.driver.refresh()

    @property
    def action_chains(self):
        return ActionChains(self.driver)

    @allure.step("Get list current urls")
    def get_list_current_urls(self):
        urls = []
        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)
            urls.append(self.driver.current_url)
        print(urls)
        return urls
