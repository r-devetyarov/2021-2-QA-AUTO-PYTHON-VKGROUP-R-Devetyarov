from pathlib import Path
from typing import Dict

import pytest

from constans import db_constants, constants_for_tests
from log_parser import log_parser
from mysql_orm.mysql_client import MysqlORMClient


def pytest_configure(config):
    mysql_orm_client = MysqlORMClient(
        user=db_constants.DbProperty.DB_USER_ROOT.value,
        password=db_constants.DbProperty.DB_PASSWORD_ROOT.value,
        db_name=db_constants.DbProperty.DB_NAME.value
    )

    if not _is_worker(config):
        mysql_orm_client.recreate_db()

    mysql_orm_client.connect(db_created=True)

    if not _is_worker(config):
        mysql_orm_client.prepare_create_tables()

    config.mysql_orm_client = mysql_orm_client


@pytest.fixture(scope='session')
def mysql_orm_client(request) -> MysqlORMClient:
    client = request.config.mysql_orm_client
    yield client
    client.connection.close()


@pytest.fixture(scope='session')
def log_parser_result() -> Dict:
    return log_parser(path=Path(constants_for_tests.ConstantsForTests.PATH_TO_ACCESS_LOG.value))


def _is_worker(config) -> bool:
    return hasattr(config, "workerinput")
