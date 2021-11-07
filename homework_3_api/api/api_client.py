import logging
import os
from json import JSONDecodeError
from typing import Dict, List, Union, Optional, Any
from urllib.parse import urljoin

import allure
import faker
import requests
from PIL import Image

from constants_web import ConstantsWeb

fake = faker.Faker()
logger = logging.getLogger("test")
MAX_RESPONSE_LENGTH = 300


class ResponseErrorException(Exception):
    pass


class ResponseStatusCodeException(Exception):
    pass


class GetCsrfTokenError(Exception):
    pass


class ApiBase:
    def __init__(self, base_url, user, password):
        self.base_url = base_url
        self.user = user
        self.password = password
        self.session = requests.Session()
        self.headers = self.post_headers
        self.path = ConstantsWeb
        self.faker = faker.Faker()

    @property
    def post_headers(self):
        return {
            "Referer": "https://target.my.com/",
        }

    @staticmethod
    def log_pre(url, headers, data, expected_status):
        logger.info(
            f"Performing request:\n"
            f"URL: {url}\n"
            f"HEADERS: {headers}\n"
            f"DATA: {data}\n\n"
            f"expected status: {expected_status}\n\n"
        )

    @staticmethod
    def log_post(response):
        log_str = "Got response:\n" f"RESPONSE STATUS: {response.status_code}"

        if len(response.text) > MAX_RESPONSE_LENGTH:
            if logger.level == logging.INFO:
                logger.info(
                    f"{log_str}\n"
                    f"RESPONSE CONTENT: COLLAPSED due to response size > {MAX_RESPONSE_LENGTH}. "
                    f"Use DEBUG logging.\n\n"
                    f"{response.text[:MAX_RESPONSE_LENGTH]}"
                )
            elif logger.level == logging.DEBUG:
                logger.info(f"{log_str}\n" f"RESPONSE CONTENT: {response.text}\n\n")
        else:
            logger.info(f"{log_str}\n" f"RESPONSE CONTENT: {response.text}\n\n")

    def _request(
            self,
            method,
            path,
            headers=None,
            data=None,
            expected_status=200,
            jsonify=True,
            **kwargs,
    ):
        url = urljoin(self.base_url, path)
        if headers is None:
            headers = self.headers

        self.log_pre(url, headers, data, expected_status)
        response = self.session.request(
            method, url, headers=headers, data=data, **kwargs
        )
        self.log_post(response)

        if response.status_code != expected_status:
            raise ResponseStatusCodeException(
                f'Got {response.status_code} {response.request} for URL "{url}"'
            )

        if jsonify:
            try:
                json_response = response.json()
                if "error" in json_response:
                    raise ResponseErrorException(
                        f'Request url: "{url}"'
                        f'returned error {json_response["error"]}'
                    )
                return json_response
            except JSONDecodeError:
                raise ResponseErrorException(
                    f'Request url: "{url}"\n'
                    f"Method: {method}\n"
                    f"Body: {data}\n"
                    f"returned JSONDecodeError\n"
                )
        return response

    def post_login(self, set_session: bool = True):
        data = {
            "email": self.user,
            "password": self.password,
            "continue": "https://target.my.com/auth/mycom?state=target_login%3D1%26ignore_opener%3D1#email",
            "failure": "https://account.my.com/login/",
        }
        res = self.session.post(
            "https://auth-ac.my.com/auth?lang=en&nosavelogin=0",
            headers=self.post_headers,
            data=data,
        )
        response = self._request("GET", "gettoken/", expected_status=404, jsonify=False)
        csrf_token = [
            header
            for header in response.headers["Set-Cookie"].split(";")
            if "csrftoken" in header
        ][0]
        if len(csrf_token) == 0:
            raise GetCsrfTokenError(
                f"Doesn't have csrf token in cookies: {response.headers['Set-Cookie']}"
            )
        csrf_token = csrf_token.split("=")[-1]
        if set_session:
            self.headers["X-CSRFToken"] = csrf_token

        return res

    @allure.step("API: get all segments")
    def get_all_segments(
            self, limit: str = "500"
    ) -> List[Dict[str, Union[int, str, List]]]:
        params = {"limit": limit}
        return self._request("GET", path=self.path.GET_OR_POST_SEGMENTS, params=params)[
            "items"
        ]

    @allure.step("API: create segment with name {segment_name}")
    def create_segment(
            self,
            segment_name: str = f"New segment {fake.lexify(text='???????#???#???')}",
            pass_condition: int = 1,
            object_type: str = "remarketing_player",
    ) -> str:
        payload = {
            "name": f"{segment_name}",
            "pass_condition": pass_condition,
            "relations": [
                {
                    "object_type": object_type,
                    "params": {"right": 0, "type": "positive", "left": 365},
                }
            ],
        }
        logger.info(f"Create segment with name {segment_name}")
        response = self._request(
            "POST", path=self.path.GET_OR_POST_SEGMENTS, json=payload
        )
        all_segments = self.get_all_segments()
        segment = [
            segment for segment in all_segments if response["id"] == segment["id"]
        ]
        assert segment
        assert segment[0]["name"] == segment_name
        assert segment[0]["pass_condition"] == pass_condition
        return response["id"]

    @allure.step("API: delete segment with id {segment_id}")
    def delete_segment(self, segment_id: str):
        logger.info(f"Delete segment with id {segment_id}")
        self._request(
            "DELETE",
            path=self.path.DELETE_SEGMENT(segment_id),
            headers=self.headers,
            expected_status=204,
            jsonify=False,
        )
        assert int(segment_id) not in [segment["id"] for segment in self.get_all_segments()], "Segment not deleted"

    def gel_all_campaigns(self, status_filer: str = None) -> List[Dict]:
        """"
        status_filer: available status "active", "blocked", "deleted"
        """
        params: Dict[str, Any] = {"limit": 250}
        if status_filer:
            params["_status"] = status_filer

        return self._request("GET", path=self.path.GET_CAMPAIGNS_LIST, params=params)["items"]

    def _upload_image_content(self, size: tuple = (240, 400)):
        image_name = f"test_image_{fake.lexify(text='??????')}.png"
        try:
            img = Image.new('RGB', size, color="black")
            img.save(image_name)
            with open(image_name, 'rb') as file:
                response = self._request("POST",
                                         path=self.path.UPLOAD_CONTENT,
                                         files={"file": file, "filename": image_name})
            return response["id"]
        finally:
            os.remove(image_name)

    def _get_url_id(self, url: str = f"www.test_url_{fake.lexify(text='????')}.com") -> int:
        response = self._request("GET", path=self.path.GET_URL_ID, params={"url": url})
        return response["id"]

    def create_company(
            self,
            payload: Optional[Dict[str, Union[None, str, int, List, Dict]]] = None,
            campaign_name: str = f"111111_New company {fake.lexify(text='???????#???#???')}",
    ) -> int:
        if payload is None:
            pass
        payload = {
            "name": campaign_name,
            "read_only": False,
            "conversion_funnel_id": None,
            "objective": "traffic",
            "enable_offline_goals": False,
            "targetings": {
                "split_audience": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                "sex": ["male", "female"],
                "age": {
                    "age_list": [48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62],
                    "expand": True,
                },
                "geo": {"regions": [188]},
                "interests_soc_dem": [],
                "segments": [],
                "interests": [],
                "fulltime": {
                    "flags": ["use_holidays_moving", "cross_timezone"],
                    "mon": [0, 1, 2, 3, 4, 5, 6],
                    "tue": [0, 1],
                    "wed": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                    "thu": [23],
                    "fri": [0, 1],
                    "sat": [0, 1],
                    "sun": [0, 1, 2, ],
                },
                "pads": [102643],
                "mobile_types": ["tablets", "smartphones"],
                "mobile_vendors": [],
                "mobile_operators": [],
            },
            "age_restrictions": None,
            "date_start": None,
            "date_end": None,
            "autobidding_mode": "second_price_mean",
            "budget_limit_day": None,
            "budget_limit": None,
            "mixing": "fastest",
            "utm": None,
            "enable_utm": True,
            "price": "3.61",
            "max_price": "0",
            "package_id": 961,
            "banners": [
                {
                    "urls": {"primary": {"id": self._get_url_id()}},
                    "textblocks": {},
                    "content": {"image_240x400": {"id": self._upload_image_content()}},
                    "name": "",
                }
            ],
        }

        response = self._request(
            "POST", path=self.path.GET_CAMPAIGNS_LIST, json=payload
        )
        assert "id" in response
        campaign_id = response["id"]

        all_campaigns = self.gel_all_campaigns()
        assert campaign_id in [campaign["id"] for campaign in all_campaigns]
        assert payload["name"] in [campaign["name"] for campaign in all_campaigns]

        return campaign_id

    def delete_campaign(self, campaign_id: int) -> None:
        payload = [{"id": campaign_id, "status": "deleted"}]
        self._request("POST",
                      path=self.path.CHANGE_CAMPAIGN_STATUS,
                      json=payload,
                      jsonify=False,
                      expected_status=204)
        assert campaign_id not in [campaign["id"] for campaign in self.gel_all_campaigns(status_filer="active")]
        assert campaign_id in [campaign["id"] for campaign in self.gel_all_campaigns(status_filer="deleted")]
