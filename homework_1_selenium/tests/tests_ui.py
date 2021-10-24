from random import randint

import pytest

from test_constants import TestConstants
from ui_pages.locators.locators import BasePageLocators, LoginPageLocators


class TestUi:
    @pytest.mark.UI
    @pytest.mark.usefixtures("login")
    def test_valid_login(self, driver):
        assert driver.current_url.startswith(f"{TestConstants.URL_TEST}/dashboard")

    @pytest.mark.UI
    def test_logout(self, login, base_page):
        base_page.logout()
        assert base_page.driver.current_url == f"{TestConstants.URL_TEST}/"
        assert base_page.element_is_presence(LoginPageLocators.TO_COME_BUTTON)

    @pytest.mark.UI
    @pytest.mark.usefixtures("login")
    def test_change_profile_info(self, profile_page):
        new_fio = f"{randint(10000, 9999999999999999999)}"
        profile_page.change_fio_field(new_fio)
        profile_page.driver.refresh()
        assert profile_page.get_fio_text() == new_fio

    @pytest.mark.parametrize("locator, excepted_uri_path",
                             [
                                 (BasePageLocators.SEGMENTS_BUTTON, "/segments/segments_list"),
                                 (BasePageLocators.BALANCE_BUTTON, "/billing"),
                                 (BasePageLocators.STATISTICS_BUTTON, "/statistics/summary"),
                             ])
    @pytest.mark.UI
    @pytest.mark.usefixtures("login")
    def test_change_page(self, base_page, locator, excepted_uri_path):
        base_page.click_by(locator)
        assert base_page.driver.current_url.startswith(f"{TestConstants.URL_TEST}{excepted_uri_path}")
