import pytest

from clients.api_client import ApiClient
from clients.mysql_client import MysqlORMClient
from constants.app_constants import DefaultUser


class BaseCase:
    api_client = None
    mysql_orm_client = None
    authorized = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client, mysql_orm_client, logger):
        self.api_client: ApiClient = api_client
        self.mysql_orm_client: MysqlORMClient = mysql_orm_client
        self.logger = logger
        if self.authorized:
            res = api_client.login(username=DefaultUser.USERNAME, password=DefaultUser.PASSWORD)
            print(res.status_code)
