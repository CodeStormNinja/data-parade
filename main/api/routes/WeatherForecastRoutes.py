from flask import jsonify
from flask_restx import Namespace, Resource, abort
from pydantic import ValidationError

from main.api.swagger.models.WeatherForecastSwaggerModels import WeatherForecastRequestSwaggerModel
from main.domain.dtos.WeatherForecastRequestDto import WeatherForecastRequestDto
from main.domain.services.WeatherForecastService import WeatherForecastService

ns = Namespace("weather-forecast", description="Weather Forecast operations")
for m in [WeatherForecastRequestSwaggerModel]:
    if m.name not in ns.models:
        ns.add_model(m.name, m)

@ns.route("/")
class WeatherForecastResource(Resource):
    
    def __init__(self, api):
        self._weather_forecast_service = WeatherForecastService()
        super().__init__(api)
    
    @ns.expect(WeatherForecastRequestSwaggerModel)
    def post(self):
        
        try:
            dto = WeatherForecastRequestDto.model_validate(ns.payload or {})
        except ValidationError as e:
            abort(400, message="Invalid request body", errors=e.errors())
        
        return jsonify(self._weather_forecast_service.get_forecast(dto.location, dto.datetime))
