import pytest


class ApiBase:
    is_authorized = True

    @pytest.fixture(scope="function", autouse=True)
    def setup(self, api_client, logger):
        self.api_client = api_client
        self.logger = logger
        if self.is_authorized:
            self.api_client.post_login()

    @pytest.fixture
    def create_new_segment(self):
        segment_id = self.api_client.create_segment()
        yield
        self.api_client.delete_segment(segment_id)

    @pytest.fixture
    def create_new_campaign(self):
        campaign_id = self.api_client.create_company()
        yield
        self.api_client.delete_campaign(campaign_id)
