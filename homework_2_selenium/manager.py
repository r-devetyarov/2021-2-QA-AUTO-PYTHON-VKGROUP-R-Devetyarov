from typing import Dict, Any, List

from selenium import webdriver

from ui_pages.locators.locators import (
    LoginPageLocators,
)
from ui_pages.pages.base_page import BasePage
from ui_pages.pages.login_page import LoginPage
from ui_pages.pages.profile_page import ProfilePage
from ui_pages.pages.segments_page import SegmentsPage


class Manager:
    def __init__(
            self,
            driver: webdriver,
            config: Dict,
            logger,
            cookies: List[Dict[str, Any]] = None,
    ):
        self.driver = driver
        self.config = config
        self.logger = logger
        self.cookies = cookies

        if self.cookies:
            for cookie in self.cookies:
                if "sameSite" in cookie.keys() and cookie["sameSite"] == "None":
                    cookie["sameSite"] = "Lax"
                    self.logger.info(f"изменили куку {cookie}")
                self.driver.add_cookie(cookie)

            self.driver.refresh()
            self.base_page = BasePage(self.driver)
            self.profile_page = ProfilePage
            self.segments_page = SegmentsPage

        else:
            self.login_page = LoginPage(self.driver)
            self.login_page_locators = LoginPageLocators()
