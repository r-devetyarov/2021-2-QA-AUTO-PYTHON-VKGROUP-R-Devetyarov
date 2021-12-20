import allure

from clients.ui_client import UiClient
from ui_pages.locators.locators import RegistrationPageLocators
from utils.builder import Builder


class RegisterPage(UiClient):
    locators = RegistrationPageLocators()
    builder = Builder()

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
            password=None,
            confirm_password=None,
            accept_button: bool = True
    ):
        user = self.builder.user_data(
            username=username,
            email=email,
            password=password,
            confirm_password=confirm_password
        )

        self.input_username(user.username)
        self.input_email(user.email)
        self.input_password(user.password)
        self.confirm_password(user.confirm_password)

        if accept_button:
            self.click_accept_button()

        self.click_register_button()
        return user
