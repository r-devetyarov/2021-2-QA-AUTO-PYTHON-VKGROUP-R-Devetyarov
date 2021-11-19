import allure

from helpers import random_string
from ui_pages.locators.locators import CompanyPageLocators
from ui_pages.pages.base_page import BasePage


class SegmentsPage(BasePage):
    locators = CompanyPageLocators

    def __init__(self, driver):
        super().__init__(driver)
        self.click_by(self.locators.COMPANY_BUTTON)

    @allure.step("Create new company with name {company_name}")
    def create_company(self, company_name: str = f"new_segment_name_{random_string()}"):
        self.click_by(self.locators.CREATE_COMPANY_NOT_FIRST)

    @allure.step("Get id company via name: {company_name}")
    def get_id_segment_via_name(self, company_name: str) -> str:
        locator = self.locators.company_name_title(company_name)
        self.logger.info(f"Find locator {locator}")
        id_company = self.get_attribute_by_name(locator=locator, attribute_name="href").split("/")[-1].split("?")[0]
        self.logger.info(f"Get id segment {id_company}")
        return id_company

    @allure.step("Delete company with id: {segment_id}")
    def delete_company(self, company_id: str) -> None:
        self.click_by(self.locators.settings_company(company_id))
        self.click_by(self.locators.DELETE_COMPANY_BUTTON)
        self.refresh_page()
