import allure

from clients.ui_client import UiClient
from ui_pages.locators.locators import MainPageLocators


class MainPage(UiClient):
    locators = MainPageLocators()

    @allure.step("Logout")
    def logout(self):
        self.click_by(self.locators.LOGOUT_BUTTON)

    @allure.step("Open page with scroll: {element_click}")
    def open_page_with_move(self, move_to_element, element_click):
        elem = self.find(move_to_element)
        self.action_chains.move_to_element(elem).perform()
        self.click_by(element_click)
