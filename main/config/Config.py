import os
import importlib

class Config:
        
    def get_environment_config():
        
        env = os.environ.get('FLASK_ENV', 'local').capitalize()
        configModule = importlib.import_module(f'main.config.Config{env}')
        configClass = getattr(configModule, f'Config{env}')
        return configClass()