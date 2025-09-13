from flask_restx import Model, fields

WeatherForecastRequestSwaggerModel = Model("WeatherForecastRequestSwaggerModel", {
    "location": fields.String(required=True, description="Location name", example="São Paulo"),
    "datetime": fields.String(required=True, description="Local ISO datetime", example="2025-09-12T20:00:00Z")
})