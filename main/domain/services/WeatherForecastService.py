from datetime import datetime
import pandas as pd

from main.domain.dtos.WeatherForecastResponseDto import WeatherForecastResponseDto
from main.infrastructure.http.GeocodeHttpContext import GeocodeHttpContext
from main.infrastructure.http.WeatherForecastHttpContext import WeatherForecastHttpContext

class WeatherForecastService:
    
    def __init__(self):
        self._weather_forecast_http_context = WeatherForecastHttpContext()
        self._geocode_http_context = GeocodeHttpContext()
    
    def get_forecast(self, location, iso_datetime):
        
        converted_datetime = datetime.fromisoformat(iso_datetime)
        date_string = converted_datetime.date().strftime("%Y-%m-%d")
        
        response_geocode = self._geocode_http_context.get_coordinates_by_location_name(location)
        lat = response_geocode[0]["lat"]
        lon = response_geocode[0]["lon"]
        
        response_forecast = self._weather_forecast_http_context.forecast_by_coordinates_and_period(lat, lon, date_string, date_string)
        forecast_dataframe = pd.DataFrame(response_forecast["hourly"])
        
        response_air_quality = self._weather_forecast_http_context.forecast_air_quality_by_coordinates_and_period(lat, lon, date_string, date_string)
        air_quality_dataframe = pd.DataFrame(response_air_quality["hourly"])
        
        joined_dataframe = pd.merge(forecast_dataframe, air_quality_dataframe, on="time")
        joined_dataframe["time"] = pd.to_datetime(joined_dataframe["time"])
        selected_hour = joined_dataframe.loc[joined_dataframe["time"].dt.hour == converted_datetime.hour]
        response = selected_hour.to_dict(orient="records")[0]
        
        return WeatherForecastResponseDto.model_validate(response)