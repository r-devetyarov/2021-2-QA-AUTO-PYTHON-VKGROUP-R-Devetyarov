import logging
import os

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from manager import Manager
from test_constants import TestConstants
from ui_pages.pages.login_page import LoginPage


def get_driver(config: dict, download_dir=None):
    browser_name = config["browser"]
    selenoid = config['selenoid']
    vnc = config['vnc']

    if browser_name == 'chrome':
        options = Options()
        if download_dir is not None:
            options.add_experimental_option("prefs", {"download.default_directory": download_dir})

        if selenoid:
            options.add_experimental_option("prefs", {"download.default_directory": '/home/selenium/Downloads'})
            capabilities = {
                'browserName': 'chrome',
                'version': '91.0'
            }
            if vnc:
                capabilities['version'] += '_vnc'
                capabilities['enableVNC'] = True

            browser = webdriver.Remote(selenoid, options=options,
                                       desired_capabilities=capabilities)
        else:
            manager = ChromeDriverManager(version='latest', log_level=logging.CRITICAL)
            browser = webdriver.Chrome(executable_path=manager.install(), options=options)

    elif browser_name == 'firefox':
        manager = GeckoDriverManager(version='latest')
        browser = webdriver.Firefox(executable_path=manager.install())
    else:
        raise RuntimeError(f'Unsupported browser: {browser_name}')

    browser.maximize_window()
    return browser


@pytest.fixture(scope='function')
def driver(config, temp_dir):
    url = config['url']
    with allure.step('Init browser'):
        browser = get_driver(config, download_dir=temp_dir)
        browser.get(url)

    yield browser
    browser.quit()


@pytest.fixture(scope='session')
def cookies(config):
    driver = get_driver(config)
    driver.get(config['url'])
    login_page = LoginPage(driver)
    login_page.login(TestConstants.VALID_LOGIN, TestConstants.VALID_PASSWORD)
    cookies = driver.get_cookies()
    driver.quit()
    return cookies


@pytest.fixture(scope='function', autouse=True)
def ui_report(driver, request, temp_dir):
    failed_tests_count = request.session.testsfailed
    yield
    if request.session.testsfailed > failed_tests_count:
        screenshot = os.path.join(temp_dir, 'failure.png')
        driver.get_screenshot_as_file(screenshot)
        allure.attach.file(screenshot, 'failure.png', attachment_type=allure.attachment_type.PNG)

    browser_log = os.path.join(temp_dir, 'browser.log')
    with open(browser_log, 'w') as f:
        for i in driver.get_log('browser'):
            f.write(f"{i['level']} - {i['source']}\n{i['message']}\n")

    with open(browser_log, 'r') as f:
        allure.attach(f.read(), 'browser.log', attachment_type=allure.attachment_type.TEXT)


@pytest.fixture(scope='function')
def manager(cookies, driver, config, logger):
    return Manager(driver=driver, config=config, logger=logger, cookies=cookies)


@pytest.fixture(scope='function')
def manager_without_login(driver, config, logger):
    return Manager(driver=driver, config=config, logger=logger)
