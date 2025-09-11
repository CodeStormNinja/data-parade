from flask import Flask, Blueprint
from flask_cors import CORS
from flask_restful import Api

def create_app():
    app = Flask(__name__)
    app.config["BUNDLE_ERRORS"] = True
    app.config["ERROR_404_HELP"] = False

    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:8080", "http://127.0.0.1:8080"],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    # (opcional) se você criou o errors.py:
    try:
        from .errors import register_error_handlers
        register_error_handlers(app)
    except Exception:
        pass

    api_bp = Blueprint("api", __name__, url_prefix="/api/v1")
    api = Api(api_bp)

    from .resources.risk_precip import RiskPrecipResource
    from .resources.risk_wind import RiskWindResource
    from .resources.risk_heat import RiskHeatResource
    from .resources.risk_lightning import RiskLightningResource
    from .resources.risk_air import RiskAirResource
    from .resources.geocode import GeocodeResource
    from .errors import register_error_handlers

    api.add_resource(RiskPrecipResource, "/risk/precip")
    api.add_resource(RiskWindResource, "/risk/wind")
    api.add_resource(RiskHeatResource, "/risk/heat")
    api.add_resource(RiskLightningResource, "/risk/lightning")
    api.add_resource(RiskAirResource, "/risk/air")
    api.add_resource(GeocodeResource, "/utils/geocode")

    app.register_blueprint(api_bp)
    return app
