import allure

from tests.tests_api.base import BaseCase


@allure.feature("API tests")
class TestApi(BaseCase):
    def test_1(self):
        # res = self.api_client.add_user("qweqweqwe", "123456", "wewewe@bk.ru")
        res = self.api_client.get_cookies()


@allure.feature("API tests without authorize")
class TestApiWithoutAuth:
    ...
