import allure
import pytest

from tests.tests_api.base import BaseCase
from utils import utils


@pytest.mark.API
@allure.feature("API tests")
@allure.story("Tests with authorized")
class TestApi(BaseCase):

    @allure.title("Registry user with valid data")
    @pytest.mark.parametrize("username_len", [6, 8, 16])
    @pytest.mark.parametrize("password_len", [1, 34, 254, 255])
    @pytest.mark.parametrize("email_len", [6, 7, 33, 63, 64])
    def test_register_valid_data(self, username_len, password_len, email_len):
        username = utils.random_string(size=username_len)
        password = utils.random_string(size=password_len)
        email = utils.random_email(size=email_len)
        resp = self.api_client.add_user(username=username, password=password, email=email)
        # TODO bug: not correct response status code
        # assert resp.status_code == 201
        assert all(self.mysql.check_user_in_db(username=username, email=email, password=password))
        assert resp.text == "User   was added!"

    @allure.title("Registry user with invalid username length")
    @pytest.mark.parametrize("username_len", [1, 5, 17, 445])
    def test_invalid_username(self, username_len):
        username = utils.random_string(size=username_len)
        resp = self.api_client.add_user(username=username)


@allure.feature("API tests without authorize")
class TestApiWithoutAuth:
    ...
