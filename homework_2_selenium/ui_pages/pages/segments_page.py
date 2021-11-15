import allure

from helpers import random_string
from ui_pages.locators.locators import SegmentsPageLocators
from ui_pages.pages.base_page import BasePage


class SegmentsPage(BasePage):
    locators = SegmentsPageLocators

    def __init__(self, driver):
        super().__init__(driver)
        self.click_by(self.locators.SEGMENTS_BUTTON)

    @allure.step("Create new segment with name: {segment_name}")
    def create_segment(self, segment_name: str = f"new_segment_name_{random_string()}") -> str:
        self.logger.info(f"Create segment with name: {segment_name}")
        if self.element_is_presence(self.locators.SEGMENT_ID):
            self.click_by(self.locators.CREATE_SEGMENT_NOT_FIRST)
        else:
            self.click_by(self.locators.CREATE_SEGMENT_FIRST)

        self.click_by(self.locators.CREATE_ITEM_GAMES_SN)
        self.click_by(self.locators.CREATE_ITEMS_GAMES_CHECKBOX)
        self.click_by(self.locators.ADD_SEGMENT_BUTTON)
        self.clear_and_send_keys(self.locators.CREATE_SEGMENT_NAME_FILED, text=segment_name)
        self.click_by(self.locators.BUTTON_SUBMIT)
        assert self.element_is_presence(self.locators.segment_name_title(segment_name), timeout=7), "Segment not added"
        return segment_name

    @allure.step("Get id segment via name: {segment_name}")
    def get_id_segment_via_name(self, segment_name: str) -> str:
        locator = self.locators.segment_name_title(segment_name)
        self.logger.info(f"Find locator {locator}")
        id_segment = self.get_attribute_by_name(locator=locator, attribute_name="href").split("/")[-1]
        self.logger.info(f"Get id segment {id_segment}")
        return id_segment

    @allure.step("Delete segment with id: {segment_id}")
    def delete_segment(self, segment_id: str) -> None:
        self.click_by(self.locators.delete_segment_id_button(segment_id))
        self.click_by(self.locators.CONFIRM_DELETE)
        self.refresh_page()


