from selenium.webdriver.common.by import By

from base_page import BasePage


class ProfilePage(BasePage):
    SEND_FIO = (By.XPATH, "//div[@data-name='fio']//input")
    GET_FIO = (By.XPATH, "//div[contains(@class, 'right-module-userNameWrap')]")
    SAVE_BUTTON = (By.XPATH, "//button[@data-class-name='Submit']")

    def change_fio_field(self, new_fio: str):
        self.clear_and_send_keys(self.SEND_FIO, new_fio)
        self.click_by(self.SAVE_BUTTON)

    def get_fio_text(self) -> str:
        return self.find(self.GET_FIO).text
