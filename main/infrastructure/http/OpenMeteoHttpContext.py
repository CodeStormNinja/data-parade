import os
from flask import current_app

from main.config.HttpConfig import HttpConfig

class OpenMeteoHttpContext:

    base_url = None

    def __init__(self):
        self.session = HttpConfig.create_session()
        self.base_url = current_app.config.get("OPEN_METEO_API_URL")

    def get(self, params):
        response = self.session.get(
            self.base_url,
            params=params,
            timeout=HttpConfig.get_default_timeout()
        )
        response.raise_for_status()
        return response.json()