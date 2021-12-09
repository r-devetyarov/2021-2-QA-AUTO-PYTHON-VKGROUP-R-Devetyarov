import allure

from clients.ui_client import UiClient
from ui_pages.locators.locators import RegistrationPageLocators
from utils import utils


class RegisterPage(UiClient):
    locators = RegistrationPageLocators()

    @allure.step("Input username {username}")
    def input_username(self, username: str):
        field = self.find(self.locators.FIELD_INPUT_USERNAME)
        self.logger.info(f"send username in the field {username}")
        field.send_keys(username)

    @allure.step("Input password {password}")
    def input_password(self, password: str):
        field = self.find(self.locators.FIELD_INPUT_PASSWORD)
        self.logger.info(f"send password in the field {password}")
        field.send_keys(password)

    @allure.step("Confirm  password {password}")
    def confirm_password(self, password: str):
        field = self.find(self.locators.FIELD_CONFIRM_PASSWORD)
        self.logger.info(f"confirm password in the field {password}")
        field.send_keys(password)

    @allure.step("Input email {email}")
    def input_email(self, email: str):
        field = self.find(self.locators.FIELD_INPUT_EMAIL)
        self.logger.info(f"send email in the field {email}")
        field.send_keys(email)

    @allure.step("Click accept button")
    def click_accept_button(self):
        self.click_by(self.locators.CHECKBOX_ACCEPT)

    @allure.step("Click register button")
    def click_register_button(self):
        self.click_by(self.locators.REGISTER_BUTTON)

    @allure.step("Register new user")
    def register_user(
            self,
            username=None,
            email=None,
            password="123456",
            confirm_password="123456",
            accept_button: bool = True
    ) -> tuple:
        if username is None:
            username = utils.random_string()
        if username is None:
            email = self.faker.ascii_email()
        self.input_username(username)
        self.input_email(email)
        self.input_password(password)
        self.confirm_password(confirm_password)

        if accept_button:
            self.click_accept_button()

        self.click_register_button()
        return username, email, password
