import time

import allure
import pytest
from constants.app_constants import DefaultUser
from ui_pages.locators.locators import MainPageLocators
from tests.tests_ui.base import BaseCase
from utils import utils


class TestUi(BaseCase):
    def test_logout(self):
        self.main_page.logout()
        assert not self.main_page.element_is_presence(self.main_page.locators.LOGOUT_BUTTON)

    @pytest.mark.parametrize(
        "page_locator, expected_url_path",
        [
            (MainPageLocators.HOME_BUTTON, "welcome"),
            (MainPageLocators.PYTHON_BUTTON, "python.org"),
            (MainPageLocators.WHAT_IS_API_BTN, "wikipedia.org/wiki/API"),
            (MainPageLocators.FUTURE_OF_INTERNET_BTN, "future-of-the-internet"),
            (MainPageLocators.LETS_ABOUT_SMTP_BTN, "wiki/SMTP"),
        ]
    )
    @allure.title("Test open page {page_locator[1]}")
    def test_open_pages(self, page_locator, expected_url_path):
        self.main_page.click_by(page_locator)
        urls = self.main_page.get_list_current_urls()
        assert utils.check_contain_in_list(expected_url_path, urls)

    @pytest.mark.parametrize(
        "scroll_to, page_locator, expected_url_path",
        [
            (MainPageLocators.PYTHON_BUTTON, MainPageLocators.PYTHON_HISTORY_BTN, "wikipedia.org/wiki/History_of_Python"),
            (MainPageLocators.PYTHON_BUTTON, MainPageLocators.PYTHON_FLASK_BTN, "flask.palletsprojects"),
            (MainPageLocators.LINUX_BUTTON, MainPageLocators.DOWNLOAD_CENTOS_BTN, "/workstation/download"),
            (MainPageLocators.NETWORK_BUTTON, MainPageLocators.WIRESHARK_NEWS_BUTTON, "www.wireshark.org/news"),
            (MainPageLocators.NETWORK_BUTTON, MainPageLocators.WIRESHARK_DOWNLOAD_BUTTON, "wireshark.org/#download"),
            (MainPageLocators.NETWORK_BUTTON, MainPageLocators.TCPDUMP_EXAMPLES_BTN, " tcpdump-examples"),
        ]
    )
    @allure.title("Test open page with move")
    def test_open_page_with_move(self, scroll_to, page_locator, expected_url_path):
        self.main_page.open_page_with_move(move_to_element=scroll_to, element_click=page_locator)
        urls = self.main_page.get_list_current_urls()
        assert utils.check_contain_in_list(expected_url_path, urls)


@allure.feature("UI tests: registration")
class TestUiRegistration(BaseCase):
    authorized = False

    def prepare(self):
        self.login_page.open_register_page()

    @allure.title("Test registration valid")
    @pytest.mark.parametrize("username_len", [6, 8, 16])
    def test_register_valid_data(self, username_len):
        username = utils.random_string(size=username_len)
        user_data = self.register_page.register_user(username=username)
        assert all(self.mysql.check_user_in_db(username=username, email=user_data[1], password=user_data[2]))

    @allure.title("Test registration invalid username len")
    @pytest.mark.parametrize("username_len", [0, 5, 17])
    def test_invalid_username(self, username_len):
        username = utils.random_string(size=username_len)
        self.register_page.register_user(username=username)
        assert self.register_page.element_is_presence(self.register_page.locators.INCORRECT_USERNAME_ALERT)
        assert not all(self.mysql.check_user_in_db(username=username))


@allure.feature("UI tests: login")
class TestUiLogin(BaseCase):
    authorized = False

    @allure.title("Test login valid creds")
    def test_login_valid_creds(self):
        self.login_page.login(login=DefaultUser.USERNAME, password=DefaultUser.PASSWORD)
        assert not self.login_page.element_is_presence(self.login_page.locators.FAIL_LOGIN)

    @allure.title("Test login invalid username")
    def test_login_invalid_username(self):
        self.login_page.login(login=self.api_client.faker.user_name(), password=DefaultUser.PASSWORD)
        assert self.login_page.element_is_presence(self.login_page.locators.FAIL_LOGIN)

    @allure.title("Test login invalid password")
    def test_login_invalid_password(self):
        self.login_page.login(login=DefaultUser.USERNAME, password=self.api_client.faker.user_name())
        assert self.login_page.element_is_presence(self.login_page.locators.FAIL_LOGIN)
