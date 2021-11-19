from typing import Dict

import pytest
from mysql_orm.client import MysqlORMClient

from models.model import Student


class MysqlBase:
    def __init__(self, mysql=None, log_parser_result=None):
        self.mysql = mysql
        self.log_parser_result = log_parser_result

    def prepare(self):
        pass

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_orm_client, log_parser_result):
        self.mysql: MysqlORMClient = mysql_orm_client
        self.log_parser_result: Dict = log_parser_result
        self.prepare()

    def get_students(self, prepod_id=None):
        self.mysql.session.commit()  # need to expire current models and get updated data from MySQL
        students = self.mysql.session.query(Student)

        # additionally filter by prepod_id
        if prepod_id is not None:
            students = students.filter_by(prepod_id=prepod_id)
        return students.all()
