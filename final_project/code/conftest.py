import logging
import os
import shutil
import sys

import allure
import pytest
import utils.utils

from clients.api_client import ApiClient, wait_ready_app
from clients.mysql_client import MysqlORMClient
from constants.app_constants import DbProperty


def pytest_addoption(parser):
    parser.addoption('--browser', default='chrome')


def _is_worker(config) -> bool:
    return hasattr(config, "workerinput")


def pytest_configure(config):
    mysql_orm_client = MysqlORMClient(
        user=DbProperty.DB_USER,
        password=DbProperty.DB_PASS,
        db_name=DbProperty.DB_NAME
    )

    base_dir = log_base_dir()
    if not _is_worker(config):
        wait_ready_app()
        mysql_orm_client.recreate_db()

    mysql_orm_client.connect(db_created=True)

    if not _is_worker(config):
        mysql_orm_client.prepare_create_tables()

        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)

        os.makedirs(base_dir)

    config.base_temp_dir = base_dir
    config.mysql = mysql_orm_client


def pytest_unconfigure(config):
    utils.utils.run_command("chmod -R 777 /tmp/allure")


@pytest.fixture(scope='session')
def mysql_orm_client(request) -> MysqlORMClient:
    client = request.config.mysql
    yield client
    client.connection.close()


@pytest.fixture(scope='session')
def api_client():
    return ApiClient()


@pytest.fixture(scope='session')
def config(request) -> dict:
    browser = request.config.getoption('--browser')
    return {'browser': browser}


@pytest.fixture(scope='function')
def logger(temp_dir, config):
    log_formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
    log_file = os.path.join(temp_dir, 'test.log')
    log_level = logging.INFO

    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    log = logging.getLogger('test')
    log.propagate = False
    log.setLevel(log_level)
    log.addHandler(file_handler)

    yield log

    with open(log_file, 'r') as f:
        allure.attach(f.read(), 'test.log', attachment_type=allure.attachment_type.TEXT)


@pytest.fixture(scope='function')
def temp_dir(request):
    test_dir = os.path.join(request.config.base_temp_dir,
                            request._pyfuncitem.nodeid.replace('/', '_').replace(':', '_'))
    os.makedirs(test_dir)
    return test_dir


def log_base_dir():
    if sys.platform.startswith('win'):
        base_dir = 'C:\\tests'
    else:
        base_dir = '/tmp/tests'
    return base_dir
