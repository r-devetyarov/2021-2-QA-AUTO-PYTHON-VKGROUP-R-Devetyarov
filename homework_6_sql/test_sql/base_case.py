from typing import Dict, Callable

import pytest
from mysql_orm.mysql_client import MysqlORMClient
from models.model import LineCount, MethodsCount, MostCommonUrl, BadRequestTopMaxSize, ServerErrorTopIp


class InsertDataError(Exception):
    pass


class MysqlBase:

    def prepare(self):
        pass

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_orm_client, log_parser_result):
        self.mysql: MysqlORMClient = mysql_orm_client
        self.log_parser_result: Dict = log_parser_result

        self.prepare()

    def all_query(self, model: Callable):
        self.mysql.session.commit()
        all_records = self.mysql.session.query(model).all()
        print(all_records)
        return all_records



