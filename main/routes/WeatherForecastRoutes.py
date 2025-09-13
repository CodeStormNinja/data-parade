from flask import jsonify
from flask_restx import Namespace, Resource

from main.domain.services.WeatherForecastService import WeatherForecastService

ns = Namespace("weather-forecast", description="Weather Forecast operations")

@ns.route("/")
class WeatherForecastResource(Resource):
    
    def __init__(self, api):
        self._weather_forecast_service = WeatherForecastService()
    
    def post(self):
        
        return jsonify({"result": self._weather_forecast_service.get_forecast("São Paulo", "2025-09-12T20:00:00Z")})
