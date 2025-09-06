from flask import jsonify
from flask_restx import Namespace, Resource

from main.domain.services.WeatherForecastService import WeatherForecastService

weather_forecast_service = WeatherForecastService()

ns = Namespace("weather-forecast", description="Weather Forecast operations")

@ns.route("/")
class WeatherForecastResource(Resource):
    def get(self):
        
        return jsonify({"result": weather_forecast_service.get_forecast("São Paulo")})
