from flask_restful import Resource, reqparse
from ..utils import validate_coords
from ..providers import get_provider

_parser = reqparse.RequestParser(bundle_errors=True)
_parser.add_argument("lat", type=float, required=True, location="args", help="lat obrigatória")
_parser.add_argument("lon", type=float, required=True, location="args", help="lon obrigatória")

_PROVIDER = get_provider()

class RiskHeatResource(Resource):
    def get(self):
        args = _parser.parse_args()
        validate_coords(args["lat"], args["lon"])

        resp = _PROVIDER.heat(args["lat"], args["lon"])

        utci = resp["utci"]
        if utci < 26:       level, label = 0, "Baixo"
        elif utci < 32:     level, label = 1, "Moderado"
        elif utci < 38:     level, label = 2, "Alto"
        else:               level, label = 3, "Crítico"

        resp.update({"level": level, "label": label})
        return resp, 200
