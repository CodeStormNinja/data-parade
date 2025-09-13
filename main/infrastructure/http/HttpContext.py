from flask import current_app

from main.config.HttpConfig import HttpConfig

class HttpContext:

    def __init__(self):
        HttpConfig()
        self._session = HttpConfig.session

    def get(self, url, timeout=None, params={}, response_type="json"):
        response = self._session.get(
            url,
            params=params,
            timeout=HttpConfig.default_timeout if timeout is None else timeout
        )
        response.raise_for_status()
        if response_type == "json":
            return response.json()
        else:
            return response.text()