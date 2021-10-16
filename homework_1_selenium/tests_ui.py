from random import randint

import pytest

from test_constants import TestConstants


class TestUi:
    @pytest.mark.ui
    def test_valid_login(self, driver, login):
        url = driver.current_url
        assert url == f"{TestConstants.URL_TEST}/dashboard"

    @pytest.mark.ui
    def test_logout(self, driver, login, base_page):
        base_page.logout()
        assert driver.current_url == f"{TestConstants.URL_TEST}/"

    @pytest.mark.parametrize(
        "page_name, excepted_uri_path",
        [
            ("segments", "/segments/segments_list"),
            ("balance", "/billing#deposit"),
            ("statistics", "/statistics/summary"),
        ],
    )
    @pytest.mark.ui
    def test_change_page(self, driver, base_page, login, page_name, excepted_uri_path):
        base_page.go_to_page(page_name)
        assert driver.current_url in f"{TestConstants.URL_TEST}{excepted_uri_path}"

    @pytest.mark.ui
    def test_change_profile_info(self, driver, login, profile_page):
        profile_page.go_to_page("profile")
        new_fio = f"{randint(10000, 9999999999999999999)}"
        profile_page.change_fio_field(new_fio)
        driver.refresh()
        assert profile_page.get_fio_text() == new_fio
