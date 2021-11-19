import allure

from base import Base
from ui_pages.locators.locators import BasePageLocators


class BasePage(Base):
    locators = BasePageLocators()

    @allure.step("Logout")
    def logout(self):
        self.click_by(self.locators.MY_EMAIL_BUTTON)
        self.click_by(self.locators.LOGOUT_BUTTON)
