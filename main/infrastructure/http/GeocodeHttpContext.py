from flask import current_app

from main.config.HttpConfig import HttpConfig

class GeocodeHttpContext:

    base_url = None

    def __init__(self):
        self.session = HttpConfig.create_session()
        self.base_url = current_app.config.get("GEOCODE_API_URL")

    def get(self, params):
        response = self.session.get(
            self.base_url,
            params=params,
            timeout=HttpConfig.get_default_timeout()
        )
        response.raise_for_status()
        return response.json()