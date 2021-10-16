from selenium.webdriver.common.by import By

from base_page import BasePage


class LoginPage(BasePage):
    TO_COME_BUTTON = (By.XPATH, "//div[contains(@class, 'responseHead-module-button')]")
    FIELD_INPUT_LOGIN = (By.NAME, "email")
    FIELD_INPUT_PASSWORD = (By.NAME, "password")
    LOGIN_BUTTON_LP = (By.XPATH, '//div[contains(@class, "authForm-module-button")]')

    def send_login(self, login: str) -> None:
        field = self.find(self.FIELD_INPUT_LOGIN)

        field.send_keys(login)

    def send_password(self, password: str) -> None:
        field = self.find(self.FIELD_INPUT_PASSWORD)
        field.send_keys(password)

    def login(self, login: str, password: str):
        self.click_by(self.TO_COME_BUTTON)
        self.send_login(login)
        self.send_password(password)
        self.click_by(self.LOGIN_BUTTON_LP)
