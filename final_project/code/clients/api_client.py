import logging
from json import JSONDecodeError
from urllib.parse import urljoin

import allure
import faker
import requests

from constants.app_constants import AppConstants, DefaultUser
from constants.constants_web import ConstantsWeb

logger = logging.getLogger("test")
MAX_RESPONSE_LENGTH = 300


class ResponseErrorException(Exception):
    pass


class ResponseStatusCodeException(Exception):
    pass


def get_status_app():
    return requests.get(url=f"{AppConstants.BASE_URL}/{ConstantsWeb.APP_STATUS_GET}")


class ApiBase:
    def __init__(self, base_url=f"{AppConstants.BASE_URL}"):
        self.base_url = base_url
        self.session = requests.Session()
        self.path = ConstantsWeb
        self.faker = faker.Faker()

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
            check_status_code=None,
            jsonify=True,
            **kwargs,
    ):
        url = urljoin(self.base_url, path)

        self.log_pre(url, headers, data, check_status_code)
        response = self.session.request(
            method, url, headers=headers, data=data, **kwargs
        )
        self.log_post(response)

        if check_status_code:
            if response.status_code != check_status_code:
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


class ApiClient(ApiBase):

    @allure.step("API: send login request")
    def login(self, username, password, set_session: bool = True):
        payload = {
            "username": username,
            "password": password,
            "submit": "Login"
        }
        if set_session:
            res = self.session.post(
                url=f"{self.base_url}{ConstantsWeb.LOGIN_POST}",
                data=payload
            )
        else:
            res = requests.post(url=f"{self.base_url}{ConstantsWeb.LOGIN_POST}",
                                data=payload)

        return res

    def get_cookies(self):
        self.login(
            username=DefaultUser.USERNAME,
            password=DefaultUser.PASSWORD
        )
        resp = self.welcome_get()
        cookie = resp.request.headers["Cookie"].split("=")
        print(cookie)
        cookies = {'httpOnly': True, "name": cookie[0], "value": cookie[1]}
        return cookies

    @allure.step("API: get welcome page")
    def welcome_get(self, expected_rc=None) -> requests.Response:
        return self._request(
            method="GET",
            path=ConstantsWeb.WELCOME_GET,
            check_status_code=expected_rc,
            jsonify=False
        )

    @allure.step("API: add user with creds:\n username: {username}, password: {password}, email: {email}")
    def add_user(self, username: str, password: str, email: str, expected_rc=None):
        return self._request(
            method='POST',
            path=ConstantsWeb.ADD_USER_POST,
            json={"username": username, "password": password, "email": email},
            check_status_code=expected_rc,
            jsonify=False
        )

    @allure.step("API: delete user with username: {username}")
    def delete_user(self, username: str, jsonify=False, expected_rc=None):
        return self._request(
            method='GET',
            path=f'{ConstantsWeb.DELETE_USER_GET}/{username}',
            jsonify=jsonify,
            check_status_code=expected_rc
        )

    @allure.step("API: block user with username: {username}")
    def block_user(self, username: str, jsonify=False, expected_rc=None):
        return self._request(
            method='GET',
            path=f'{ConstantsWeb.BLOCK_USER_GET}/{username}',
            jsonify=jsonify,
            check_status_code=expected_rc
        )

    @allure.step("API: access user with name {username}")
    def access_user(self, username: str, jsonify=False, expected_rc=None):
        return self._request(
            method='GET',
            path=f'{ConstantsWeb.ACCEPT_USER_GET}/{username}',
            jsonify=jsonify,
            check_status_code=expected_rc
        )
