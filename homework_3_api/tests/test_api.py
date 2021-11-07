import allure
import pytest

from tests.base import ApiBase


@allure.feature("API tests")
class TestApi(ApiBase):

    @allure.title("Test create segment")
    @pytest.mark.API
    def test_create_segment(self, create_new_segment):
        pass

    @allure.title("Test delete segment")
    @pytest.mark.API
    def test_delete_segment(self):
        segment_id = self.api_client.create_segment()
        self.api_client.delete_segment(segment_id)

    @allure.title("Test create campaign")
    @pytest.mark.API
    def test_create_campaign(self, create_new_campaign):
        pass
