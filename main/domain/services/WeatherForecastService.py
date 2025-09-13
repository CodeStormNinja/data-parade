from datetime import datetime

from main.infrastructure.http.GeocodeHttpContext import GeocodeHttpContext
from main.infrastructure.http.WeatherForecastHttpContext import WeatherForecastHttpContext

class WeatherForecastService:
    
    def __init__(self):
        self._weather_forecast_http_context = WeatherForecastHttpContext()
        self._geocode_http_context = GeocodeHttpContext()
    
    def get_forecast(self, location, iso_datetime):
        
        response_geocode = self._geocode_http_context.get_coordinates_by_location_name(location)
        lat = response_geocode[0]["lat"]
        lon = response_geocode[0]["lon"]
        
        converted_datetime = datetime.fromisoformat(iso_datetime)
        date_string = converted_datetime.date().strftime("%Y-%m-%d")
        response_forecast = self._weather_forecast_http_context.forecast_by_coordinates_and_period(lat, lon, date_string, date_string)
        response_air_quality = self._weather_forecast_http_context.forecast_air_quality_by_coordinates_and_period(lat, lon, date_string, date_string)
        
        return response_air_quality