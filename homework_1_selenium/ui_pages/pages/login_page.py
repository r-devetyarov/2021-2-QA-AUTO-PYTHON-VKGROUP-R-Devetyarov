from ui_pages.locators.locators import LoginPageLocators
from ui_pages.pages.base_page import BasePage


class LoginPage(BasePage):
    locators = LoginPageLocators()

    def send_login(self, login: str) -> None:
        field = self.find(self.locators.FIELD_INPUT_LOGIN)

        field.send_keys(login)

    def send_password(self, password: str) -> None:
        field = self.find(self.locators.FIELD_INPUT_PASSWORD)
        field.send_keys(password)

    def login(self, login: str, password: str):
        self.click_by(self.locators.TO_COME_BUTTON)
        self.send_login(login)
        self.send_password(password)
        self.click_by(self.locators.LOGIN_BUTTON_LP)
