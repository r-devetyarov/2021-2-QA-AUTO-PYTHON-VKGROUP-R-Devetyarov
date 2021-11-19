import allure
import pytest

from tests.base import ApiBase


@allure.feature("API tests")
class TestApi(ApiBase):

    @allure.title("Test create segment")
    @pytest.mark.API
    def test_create_segment(self, create_new_segment):
        segment = create_new_segment
        self.api_client.check_segment_created(segment)

    @allure.title("Test delete segment")
    @pytest.mark.API
    def test_delete_segment(self):
        segment_id = self.api_client.create_segment().id
        self.api_client.delete_segment(segment_id)
        assert self.api_client.check_segment_deleted(segment_id)

    @allure.title("Test create campaign")
    @pytest.mark.API
    def test_create_campaign(self, create_new_campaign):
        campaign = create_new_campaign
        assert self.api_client.check_camping_created(campaign)
