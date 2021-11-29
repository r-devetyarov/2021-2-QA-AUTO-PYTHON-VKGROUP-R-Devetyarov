import logging
import os
import shutil
import signal
import subprocess
import sys
import time
from copy import copy

import pytest
import requests
from requests.exceptions import ConnectionError

import settings
from mock import flask_mock
from utils.api_client import Api

repo_root = os.path.abspath(os.path.join(__file__, os.pardir))


def wait_ready(host, port):
    started = False
    st = time.time()
    while time.time() - st <= 5:
        try:
            requests.get(f'http://{host}:{port}')
            started = True
            break
        except ConnectionError:
            pass

    if not started:
        raise RuntimeError(f'{host}:{port} did not started in 5s!')


def pytest_configure(config):
    if sys.platform.startswith('win'):
        base_dir = 'C:\\tests'
    else:
        base_dir = '/tmp/test'

    if not hasattr(config, 'workerinput'):
        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)

        os.makedirs(base_dir)

        app_path = os.path.join(repo_root, 'application', 'app.py')

        env = copy(os.environ)
        env.update({
            'APP_HOST': settings.APP_HOST,
            'APP_PORT': settings.APP_PORT,
            'EXTERNAL_HOST': settings.MOCK_HOST,
            'EXTERNAL_PORT': settings.MOCK_PORT
        })

        app_logs = open('/tmp/app_logs', 'w')

        app_proc = subprocess.Popen(['python3.8', app_path],
                                    stderr=app_logs, stdout=app_logs,
                                    env=env)
        wait_ready(settings.APP_HOST, settings.APP_PORT)

        config.app_proc = app_proc
        config.app_logs = app_logs

        flask_mock.run_mock()

        wait_ready(settings.MOCK_HOST, settings.MOCK_PORT)

    config.base_temp_dir = base_dir


def pytest_unconfigure(config):
    config.app_proc.send_signal(signal.SIGINT)
    exit_code = config.app_proc.wait()

    assert exit_code == 0, f'app exited abnormally with exit code: {exit_code}'

    config.app_logs.close()
    config.app_proc.wait()

    requests.get(f'http://{settings.MOCK_HOST}:{settings.MOCK_PORT}/shutdown')


@pytest.fixture(scope='function')
def logger(temp_dir):
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


@pytest.fixture(scope='function')
def temp_dir(request):
    test_dir = os.path.join(request.config.base_temp_dir,
                            request._pyfuncitem.nodeid.replace('/', '_').replace(':', '_'))
    os.makedirs(test_dir)
    return test_dir


@pytest.fixture(scope="session")
def api():
    return Api(base_url=f'http://{settings.APP_HOST}:{settings.APP_PORT}')
