import pytest
from _pytest.fixtures import FixtureRequest
from selenium.webdriver.remote.webdriver import WebDriver

from clients.api_client import ApiClient
from clients.mysql_client import MysqlORMClient
from ui_pages.pages.login_page import LoginPage
from ui_pages.pages.main_page import MainPage
from ui_pages.pages.register_page import RegisterPage


class BaseCase:
    mysql = None
    api_client = None
    driver = None
    logger = None
    authorized = True

    def prepare(self):
        pass

    @pytest.fixture(scope="function", autouse=True)
    def setup(
            self,
            api_client,
            mysql_orm_client,
            logger,
            driver,
            request: FixtureRequest
    ):
        self.api_client: ApiClient = api_client
        self.mysql: MysqlORMClient = mysql_orm_client
        self.driver: WebDriver = driver
        self.logger = logger
        if self.authorized:
            cookies = request.getfixturevalue('get_cookies')
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()
            self.main_page = MainPage(self.driver)

        else:
            self.login_page: LoginPage = LoginPage(self.driver)
            self.register_page: RegisterPage = RegisterPage(self.driver)

        self.prepare()
