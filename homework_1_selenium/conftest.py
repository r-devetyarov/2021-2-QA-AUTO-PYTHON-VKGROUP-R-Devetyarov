import pytest
from selenium import webdriver

from test_constants import TestConstants
from ui_pages.pages.base_page import BasePage
from ui_pages.pages.login_page import LoginPage
from ui_pages.pages.profile_page import ProfilePage


@pytest.fixture(scope="function")
def driver() -> webdriver:
    driver = webdriver.Chrome(executable_path=TestConstants.PATH_TO_DRIVER_CHROME)
    driver.maximize_window()
    driver.get(TestConstants.URL_TEST)
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def login(driver):
    login_page = LoginPage(driver)
    login_page.login(
        login=TestConstants.VALID_LOGIN, password=TestConstants.VALID_PASSWORD
    )


@pytest.fixture(scope="function")
def logout_teardown(driver):
    yield
    base_page = BasePage(driver)
    base_page.logout()


@pytest.fixture(scope="function")
def base_page(driver):
    return BasePage(driver)


@pytest.fixture(scope="function")
def profile_page(driver):
    return ProfilePage(driver)
