import os
import importlib

class Config:
        
    def get_environment_config():
        
        env = os.environ.get('FLASK_ENV', 'local').capitalize()
        configModule = importlib.import_module(f'main.config.Config{env}')
        configClass = getattr(configModule, f'Config{env}')
        return configClass()
    
    # HTTP CONFIG
    DEFAULT_HTTP_TIMEOUT_SECS = 5
    
    # EXTERNAL SERVICES
    OPEN_METEO_API_URL = "https://api.open-meteo.com/v1/forecast"
    GEOCODE_API_URL = "https://nominatim.openstreetmap.org/search"
    
    # HEALTH-CHECK
    APPLICATION_STARTED_AT_UTC = None