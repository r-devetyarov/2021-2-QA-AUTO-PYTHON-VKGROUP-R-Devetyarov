import logging
import os
import time

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

from constants.app_constants import DefaultUser, ProxyAppConstants
from ui_pages.pages.login_page import LoginPage


def get_driver(config: dict):
    browser_name = config["browser"]

    if browser_name == 'chrome':
        options = Options()

        options.add_experimental_option("prefs", {"download.default_directory": '/home/selenium/Downloads'})
        capabilities = {
            'browserName': 'chrome',
            'version': '91.0',
            "enableVNC": True
        }
        capabilities['enableVNC'] = True
        browser = webdriver.Remote(
            command_executor='http://selenoid:4444/wd/hub',
            options=options,
            desired_capabilities=capabilities
        )

    elif browser_name == "local":
        manager = ChromeDriverManager(version='latest', log_level=logging.CRITICAL)
        browser = webdriver.Chrome(executable_path=manager.install())
    else:
        raise RuntimeError(f'Unsupported browser: {browser_name}')

    browser.maximize_window()
    return browser


@pytest.fixture(scope='function')
def driver(config):
    with allure.step('Init browser'):
        browser = get_driver(config)
        # browser.get(AppConstants.BASE_URL)
        # browser.get("http://application:8079")
        # browser.get(ProxyAppConstants.BASE_URL)
        browser.get(ProxyAppConstants.BASE_URL)

    yield browser
    browser.quit()


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


@pytest.fixture(scope="session")
def get_cookies(config):
    driver: WebDriver = get_driver(config)
    try:
        driver.get(ProxyAppConstants.BASE_URL)
        login_page = LoginPage(driver)
        login_page.login(login=DefaultUser.USERNAME, password=DefaultUser.PASSWORD)
        cookies = driver.get_cookies()
        # time.sleep(60)
        driver.quit()
        return cookies
    except Exception as e:
        driver.quit()
        raise e
