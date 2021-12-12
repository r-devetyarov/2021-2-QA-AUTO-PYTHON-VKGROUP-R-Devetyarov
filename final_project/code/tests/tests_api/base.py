import pytest

from clients.api_client import ApiClient
from clients.mysql_client import MysqlORMClient
from constants.app_constants import DefaultUser


class BaseCase:
    api_client = None
    mysql = None
    logger = None
    authorized = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client, mysql_orm_client, logger):
        self.api_client: ApiClient = api_client
        self.mysql: MysqlORMClient = mysql_orm_client
        self.logger = logger
        if self.authorized:
            api_client.login(username=DefaultUser.USERNAME, password=DefaultUser.PASSWORD)

    @pytest.fixture
    def create_user(self):
        user_data = self.api_client.builder.user_data()
        self.api_client.add_user(
            username=user_data.username,
            password=user_data.password,
            email=user_data.email
        )
        return user_data
