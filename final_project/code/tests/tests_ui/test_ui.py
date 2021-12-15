import allure
import pytest

from constants.app_constants import DefaultUser
from tests.tests_ui.base import BaseCase
from ui_pages.locators.locators import MainPageLocators
from utils import utils


@pytest.mark.UI
@allure.feature("UI tests")
class TestUi(BaseCase):
    ''''
    ДОБАВИТЬ:
    повторное создание юзера с существующим юзернейм
    повторное создание юзера с существующим емаил
    при переходе на страницу велком проверку лога браузера - если получится
    логин с пустыми полями
    регистрация с пустыми полями
    регистрация с невалидной длиной пароля
    логин юзером потом меняем access переход куда-нибудь
    '''

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
            (
                    MainPageLocators.PYTHON_BUTTON,
                    MainPageLocators.PYTHON_HISTORY_BTN,
                    "wikipedia.org/wiki/History_of_Python",
            ),
            (
                    MainPageLocators.PYTHON_BUTTON,
                    MainPageLocators.PYTHON_FLASK_BTN,
                    "flask.palletsprojects",
            ),
            (
                    MainPageLocators.LINUX_BUTTON,
                    MainPageLocators.DOWNLOAD_CENTOS_BTN,
                    "/workstation/download",
            ),
            (
                    MainPageLocators.NETWORK_BUTTON,
                    MainPageLocators.WIRESHARK_NEWS_BUTTON,
                    "www.wireshark.org/news",
            ),
            (
                    MainPageLocators.NETWORK_BUTTON,
                    MainPageLocators.WIRESHARK_DOWNLOAD_BUTTON,
                    "wireshark.org/#download",
            ),
            (
                    MainPageLocators.NETWORK_BUTTON,
                    MainPageLocators.TCPDUMP_EXAMPLES_BTN,
                    "tcpdump-examples",
            ),
        ],
    )
    @allure.title("Test open page with move")
    def test_open_page_with_move(self, scroll_to, page_locator, expected_url_path):
        self.main_page.open_page_with_move(
            move_to_element=scroll_to, element_click=page_locator
        )
        urls = self.main_page.get_list_current_urls()
        assert utils.check_contain_in_list(expected_url_path, urls)

    @allure.title("Test current user")
    def test_current_user(self):
        ...

    @allure.title("Test current VK ID")
    def test_current_vk_id(self):
        ...


@pytest.mark.UI
@allure.feature("UI tests")
class TestUiRegistration(BaseCase):
    authorized = False

    def prepare(self):
        self.login_page.open_register_page()

    @allure.title("Test registration valid data")
    @pytest.mark.parametrize("username_len", [6, 8, 16])
    @pytest.mark.parametrize("password_len", [1, 34, 254, 255])
    @pytest.mark.parametrize("email_len", [6, 7, 33, 63, 64])
    def test_register_valid_data(self, username_len, password_len, email_len):
        username = utils.random_string(size=username_len)
        password = utils.random_string(size=password_len)
        email = utils.random_email(size=email_len)
        user_data = self.register_page.register_user(
            username=username,
            email=email,
            password=password,
            confirm_password=password
        )
        assert all(self.mysql.check_user_in_db(username=username, email=user_data[1], password=user_data[2]))

    @allure.title("Test registration invalid username len")
    @pytest.mark.parametrize("username_len", [1, 5, 17, 445])
    def test_invalid_username_len(self, username_len):
        username = utils.random_string(size=username_len)
        self.register_page.register_user(username=username)
        assert self.register_page.element_is_presence(
            self.register_page.locators.INCORRECT_ALERT
        )
        assert not all(self.mysql.check_user_in_db(username=username))

    @allure.title("Test registration invalid email")
    @pytest.mark.parametrize("email_len", [0, 10])
    def test_invalid_email(self, email_len):
        email = utils.random_string(size=email_len)
        user = self.register_page.register_user(email=email)
        assert self.register_page.element_is_presence(
            self.register_page.locators.INCORRECT_ALERT
        )
        assert not all(self.mysql.check_user_in_db(username=user[0]))

    @allure.title("Test registration different passwords")
    def test_diff_pass(self):
        user = self.register_page.register_user(password='123456', confirm_password='gdfgdfg')
        assert self.register_page.element_is_presence(
            self.register_page.locators.INCORRECT_ALERT
        )
        assert not all(self.mysql.check_user_in_db(username=user[0]))

    @allure.title("Test registration don't click on checkbox")
    def test_do_not_click_checkbox(self):
        user = self.register_page.register_user(accept_button=False)
        assert not all(self.mysql.check_user_in_db(username=user[0]))

    @allure.title("Test registration")
    @pytest.mark.parametrize("email_len", [65, 321])
    def test_invalid_email_length(self, email_len):
        email = utils.random_email(size=email_len)
        user = self.register_page.register_user(email=email)
        assert self.register_page.element_is_presence(self.register_page.locators.INCORRECT_ALERT)
        assert not all(self.mysql.check_user_in_db(username=user[0]))


@pytest.mark.UI
@allure.feature("UI tests")
class TestUiLogout(BaseCase):
    authorized = False

    @allure.title("Test logout")
    def test_logout(self, create_user_and_login):
        user = create_user_and_login
        self.main_page.logout()
        assert not self.main_page.element_is_presence(
            self.main_page.locators.LOGOUT_BUTTON,
            timeout=10
        )
        assert all(self.mysql.check_user_in_db(username=user.username, active=0))


@pytest.mark.UI
@allure.feature("UI tests")
class TestUiLogin(BaseCase):
    # TODO добавить проверки с пустыми полями
    authorized = False

    @allure.title("Test login valid creds")
    def test_login_valid_creds(self, create_user_and_login):
        user = create_user_and_login
        assert not self.login_page.element_is_presence(
            self.login_page.locators.FAIL_LOGIN
        )
        assert user[0] in self.main_page.find(
            self.main_page.locators.CURRENT_USER_TEXT
        ).text
        assert all(
            self.mysql.check_user_in_db(
                username=user.username, active=1, start_active_time=utils.get_current_date()
            )
        )

    @allure.title("Test login invalid username")
    def test_login_invalid_username(self):
        self.login_page.login(
            login=self.register_page.builder.user_data().username,
            password=DefaultUser.PASSWORD
        )
        assert self.login_page.element_is_presence(self.login_page.locators.FAIL_LOGIN)

    @allure.title("Test login invalid password")
    def test_login_invalid_password(self):
        self.login_page.login(
            login=DefaultUser.USERNAME,
            password=self.register_page.builder.user_data().password
        )
        assert self.login_page.element_is_presence(self.login_page.locators.FAIL_LOGIN)

    @allure.title("Test login without access")
    def test_login_without_access(self):
        user = self.mysql.add_user(access=0)
        self.login_page.login(
            login=user.username, password=user.password
        )
        assert self.login_page.element_is_presence(self.login_page.locators.FAIL_LOGIN)
