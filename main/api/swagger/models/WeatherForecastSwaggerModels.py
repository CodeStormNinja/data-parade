from flask_restx import Model, fields

WeatherForecastRequestSwaggerModel = Model("WeatherForecastRequestSwaggerModel", {
    "location": fields.String(required=True, description="Location name", example="São Paulo"),
    "datetime": fields.String(required=True, description="Local ISO datetime", example="2025-09-12T20:00:00Z")
})

WeatherForecastResponseSwaggerModel = Model("WeatherForecastResponseSwaggerModel", {
    "temperature_2m": fields.Float(required=True, description="Temperature in degrees Celsius", example=23.5),
    "relative_humidity_2m": fields.Float(required=True, description="Humidity in percentage", example=78.0),
    "wind_gusts_10m": fields.Float(required=True, description="Wind gusts in kilometers per hour", example=15.0),
    "precipitation": fields.Float(required=True, description="Precipitation in millimeters", example=0.0),
    "pm10": fields.Float(required=True, description="PM10 particulate matter concentration in micrograms per cubic meter", example=12.0),
    "pm2_5": fields.Float(required=True, description="PM2.5 particulate matter concentration in micrograms per cubic meter", example=8.0),
    "us_aqi": fields.Integer(required=True, description="US Air Quality Index", example=42),
    "ozone": fields.Float(required=True, description="Ozone concentration in parts per million", example=0.030)
})