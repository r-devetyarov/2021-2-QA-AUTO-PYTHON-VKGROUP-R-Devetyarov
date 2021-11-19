from random import randint

import allure
import pytest

from test_constants import TestConstants
from ui_pages.locators.locators import BasePageLocators, LoginPageLocators


@allure.feature("UI tests")
@allure.story("Another tests")
class TestUI:

    @allure.title("Logout")
    @pytest.mark.UI
    def test_logout(self, manager):
        manager.base_page.logout()
        manager.base_page.element_is_presence(LoginPageLocators.TO_COME_BUTTON)

    @allure.title("Change profile info")
    @pytest.mark.UI
    def test_change_profile_info(self, manager):
        profile_page = manager.profile_page(manager.driver)
        new_fio = f"{randint(10000, 9999999999999999999)}"
        profile_page.change_fio_field(new_fio)
        profile_page.driver.refresh()
        assert profile_page.get_fio_text() == new_fio

    @allure.title("Change current page on {excepted_uri_path}")
    @pytest.mark.parametrize("locator, excepted_uri_path",
                             [
                                 (BasePageLocators.SEGMENTS_BUTTON, "/segments"),
                                 (BasePageLocators.BALANCE_BUTTON, "/billing"),
                                 (BasePageLocators.STATISTICS_BUTTON, "/statistics"),
                             ])
    @pytest.mark.UI
    def test_change_page(self, manager, locator, excepted_uri_path):
        manager.base_page.click_by(locator)
        assert manager.driver.current_url.startswith(f"{TestConstants.URL_TEST}{excepted_uri_path}")
