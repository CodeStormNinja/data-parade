from flask import current_app

from main.infrastructure.http.HttpContext import HttpContext

class WeatherForecastHttpContext:

    def __init__(self):
        self._http_context = HttpContext()
        self.base_url = current_app.config.get("OPEN_METEO_API_URL") + "/v1"
        self.base_air_quality_url = current_app.config.get("OPEN_METEO_AIR_QUALITY_API_URL") + "/v1"

    def forecast_by_coordinates_and_period(self, latitude, longitude, start_date, end_date):
        return self._http_context.get(self.base_url + "/forecast", params={
            "latitude": latitude,
            "longitude": longitude,
            "hourly": ",".join([
                "temperature_2m",       # ºC
                "relative_humidity_2m", # %
                "precipitation",        # mm
                "wind_gusts_10m"        # km/h
            ]),
            "start_date": start_date,
            "end_date": end_date,
            "timezone": "auto"
        })
        
    def forecast_air_quality_by_coordinates_and_period(self, latitude, longitude, start_date, end_date):
        return self._http_context.get(self.base_air_quality_url + "/air-quality", params={
            "latitude": latitude,
            "longitude": longitude,
            "hourly": ",".join([
                "pm10",
                "pm2_5",
                "us_aqi",
                "ozone"
            ]),
            "start_date": start_date,
            "end_date": end_date,
            "timezone": "auto"
        })