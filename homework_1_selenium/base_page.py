import time

from selenium.webdriver.common.by import By

from base import Base


class BasePage(Base):
    MY_EMAIL_BUTTON = (By.XPATH, "//div[contains(@class, 'right-module-rightButton')]")
    LOGOUT_BUTTON = (By.XPATH, "//a[@href='/logout']")
    SEGMENTS_BUTTON = (By.XPATH, "//a[@href='/segments']")
    BALANCE_BUTTON = (By.XPATH, "//a[@href='/billing']")
    STATISTICS_BUTTON = (By.XPATH, "//a[@href='/statistics']")
    PROFILE_BUTTON = (By.XPATH, "//a[@href='/profile']")

    def logout(self):
        self.click_by(self.MY_EMAIL_BUTTON)
        time.sleep(2)
        self.click_by(self.LOGOUT_BUTTON)

    def go_to_page(self, page_name: str):
        page_name = page_name.lower()
        if page_name in ("segments", "аудитории"):
            locator = self.SEGMENTS_BUTTON
        elif page_name in ("balance", "баланс"):
            locator = self.BALANCE_BUTTON
        elif page_name in ("statistics", "статистика"):
            locator = self.STATISTICS_BUTTON
        elif page_name in ("profile", "профиль"):
            locator = self.PROFILE_BUTTON
        else:
            raise RuntimeError(f"This page not found: {page_name}")
        self.click_by(locator)
