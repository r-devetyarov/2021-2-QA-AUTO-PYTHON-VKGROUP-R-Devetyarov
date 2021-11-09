import allure
import pytest

from tests.base import ApiBase


@allure.feature("API tests")
class TestApi(ApiBase):

    @allure.title("Test create segment")
    @pytest.mark.API
    def test_create_segment(self, create_new_segment):
        segment = create_new_segment
        all_segments = self.api_client.get_all_segments()
        segments = [
            item for item in all_segments if segment.id == item["id"]
        ]
        assert segments
        assert segments[0]["name"] == segment.name
        assert segments[0]["pass_condition"] == segment.pass_condition

    @allure.title("Test delete segment")
    @pytest.mark.API
    def test_delete_segment(self):
        segment_id = self.api_client.create_segment().id
        self.api_client.delete_segment(segment_id)
        assert int(segment_id) not in [segment["id"] for segment in self.api_client.get_all_segments()]

    @allure.title("Test create campaign")
    @pytest.mark.API
    def test_create_campaign(self, create_new_campaign):
        campaign = create_new_campaign
        all_campaigns = self.api_client.gel_all_campaigns()
        assert campaign.id in [item["id"] for item in all_campaigns]
        assert campaign.name in [item["name"] for item in all_campaigns]
