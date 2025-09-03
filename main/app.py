from flask import Flask
from main.config.Config import Config

def create_app():
    
    # CONFIGURATION
    app = Flask(__name__)
    app.config.from_object(Config())
    app.config.from_object(Config.get_environment_config())

    return app