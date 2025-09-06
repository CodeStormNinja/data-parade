from flask import Flask
from flask_restx import Api, Namespace

from main.config.Config import Config
from main.routes.WeatherForecastRoute import ns as weather_forecast_ns

def create_app():
    
    # CONFIGURATION
    app = Flask(__name__)
    app.config.from_object(Config())
    app.config.from_object(Config.get_environment_config())
    
    # SWAGGER
    api = Api(
        app=app, 
        version="1.0", 
        title="NASA Space Apps Challenge 2025 - Will it rain on my parade?", 
        description="Weather Forecast API", 
        doc="/docs"
    )
    
    # ROUTES
    api.add_namespace(weather_forecast_ns)

    return app