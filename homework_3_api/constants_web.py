class ConstantsWeb:
    ROOT_PATH = "/api/v2/"
    GET_OR_POST_SEGMENTS = f"{ROOT_PATH}remarketing/segments.json"
    DELETE_SEGMENT = lambda segment_id: f"/api/v2/remarketing/segments/{segment_id}.json"
    GET_CAMPAIGNS_LIST = f"{ROOT_PATH}campaigns.json"
    CHANGE_CAMPAIGN_STATUS = f"{ROOT_PATH}campaigns/mass_action.json"
    UPLOAD_CONTENT = f"{ROOT_PATH}content/static.json"
    GET_URL_ID = "/api/v1/urls/"
