import allure

from ui_pages.locators.locators import LoginPageLocators
from ui_pages.pages.base_page import BasePage


class LoginPage(BasePage):
    locators = LoginPageLocators()

    @allure.step("Input login {login}")
    def send_login(self, login: str) -> None:
        field = self.find(self.locators.FIELD_INPUT_LOGIN)
        self.logger.info(f"send login in the field {login}")
        field.send_keys(login)

    @allure.step("Input password")
    def send_password(self, password: str) -> None:
        field = self.find(self.locators.FIELD_INPUT_PASSWORD)
        field.send_keys(password)

    @allure.step("Login in the system")
    def login(self, login: str, password: str):
        self.click_by(self.locators.TO_COME_BUTTON)
        self.send_login(login)
        self.send_password(password)
        self.click_by(self.locators.LOGIN_BUTTON_LP)
