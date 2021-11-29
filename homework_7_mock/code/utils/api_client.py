import logging
from json import JSONDecodeError
from urllib.parse import urljoin

import requests

logger = logging.getLogger("test")
MAX_RESPONSE_LENGTH = 300


class ResponseErrorException(Exception):
    pass


class ResponseStatusCodeException(Exception):
    pass


class Api:
    def __init__(self, base_url):
        self.base_url = base_url

    @staticmethod
    def log_pre(url, data, expected_status):
        logger.info(
            f"Performing request:\n"
            f"URL: {url}\n"
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

    def send_request(self, method, path, expected_status=200, jsonify=True, **kwargs):
        url = urljoin(self.base_url, path)
        self.log_pre(url, kwargs, expected_status)
        response = requests.request(method=method, url=url, **kwargs)

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
                    f"returned JSONDecodeError\n"
                )
        return response
