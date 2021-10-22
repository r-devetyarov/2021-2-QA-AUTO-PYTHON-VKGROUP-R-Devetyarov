from ui_pages.locators.locators import ProfilePageLocators
from ui_pages.pages.base_page import BasePage


class ProfilePage(BasePage):
    locators = ProfilePageLocators()

    def __init__(self, driver):
        super().__init__(driver)
        self.click_by(self.locators.PROFILE_BUTTON)

    def change_fio_field(self, new_fio: str):
        self.clear_and_send_keys(self.locators.SEND_FIO, new_fio)
        self.click_by(self.locators.SAVE_BUTTON)

    def get_fio_text(self) -> str:
        return self.find(self.locators.GET_FIO).text
