from flask import Flask
from flask_restx import Api

from main.common.utils import DateTimeUtils
from main.config.Config import Config
from main.api.routes.MonitoringRoutes import ns as monitoring_ns
from main.api.routes.WeatherForecastRoutes import ns as weather_forecast_ns

def create_app():
    
    # CONFIGURATION
    app = Flask(__name__)
    app.config.from_object(Config())
    app.config.from_object(Config.get_environment_config())
    app.config["APPLICATION_STARTED_AT_UTC"] = DateTimeUtils.utc_now_iso()
    
    # SWAGGER
    api = Api(
        app=app, 
        version="1.0", 
        title="NASA Space Apps Challenge 2025 - Will it rain on my parade?", 
        description="Weather Forecast API", 
        doc="/docs"
    )
    
    # ROUTES
    api.add_namespace(monitoring_ns)
    api.add_namespace(weather_forecast_ns)

    return app