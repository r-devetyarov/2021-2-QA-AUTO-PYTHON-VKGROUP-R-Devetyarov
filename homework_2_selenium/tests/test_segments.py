import allure
import pytest


@pytest.fixture
def create_segment(manager) -> str:
    segments_page = manager.segments_page(manager.driver)
    return segments_page.create_segment()


@pytest.fixture
def delete_segment_td(manager, create_segment):
    yield
    segments_page = manager.segments_page(manager.driver)
    segment_id = segments_page.get_id_segment_via_name(segment_name=create_segment)
    segments_page.delete_segment(segment_id=segment_id)


@allure.feature("UI tests")
@allure.story("Segments tests")
class TestUiSegments:

    @allure.title("Create segment")
    def test_create_valid_segment(self, manager, create_segment, delete_segment_td):
        segments_page = manager.segments_page(manager.driver)
        assert segments_page.element_is_presence(segments_page.locators.segment_name_title(create_segment))

    @allure.title("Delete segment")
    def test_delete_segment(self, manager, create_segment):
        segments_page = manager.segments_page(manager.driver)
        segment_id = segments_page.get_id_segment_via_name(segment_name=create_segment)
        segments_page.delete_segment(segment_id=segment_id)
        assert not segments_page.element_is_presence(
            segments_page.locators.segment_name_title(segment_name=create_segment))
