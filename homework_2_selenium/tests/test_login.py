import allure
import pytest

from helpers import random_string, random_email
from test_constants import TestConstants


@allure.feature("UI tests")
@allure.story("Logins tests")
class TestLoginUi:

    @allure.title("Login use valid cred")
    @pytest.mark.UI
    def test_valid_login(self, manager):
        assert manager.driver.current_url.startswith(
            f"{TestConstants.URL_TEST}/dashboard"
        )

    @allure.title("Login use invalid username")
    @pytest.mark.UI
    def test_login_invalid_login(self, manager_without_login):
        manager = manager_without_login
        manager.login_page.login(login=random_email(), password=TestConstants.VALID_PASSWORD)
        assert manager.login_page.element_is_presence(
            manager.login_page_locators.FORGOT_PASSWORD
        )

    @allure.title("Login use invalid password")
    @pytest.mark.UI
    def test_login_invalid_password(self, manager_without_login):
        manager = manager_without_login
        manager.login_page.login(login=TestConstants.VALID_LOGIN, password=random_string())
        assert manager.login_page.element_is_presence(
            manager.login_page_locators.FORGOT_PASSWORD
        )
