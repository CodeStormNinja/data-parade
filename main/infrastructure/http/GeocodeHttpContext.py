from flask import current_app

from main.infrastructure.http.HttpContext import HttpContext

class GeocodeHttpContext:

    def __init__(self):
        self._base_url = current_app.config.get("GEOCODE_API_URL")
        self._http_context = HttpContext()

    def get_coordinates_by_location_name(self, location_name):
        return self._http_context.get(self._base_url + "/search", params={
            "q": location_name, 
            "format": "json", 
            "limit": 1
        })