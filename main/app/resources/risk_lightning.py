from flask_restful import Resource, reqparse
from ..utils import validate_coords
from ..providers import get_provider

_parser = reqparse.RequestParser(bundle_errors=True)
_parser.add_argument("lat", type=float, required=True, location="args", help="lat obrigatória")
_parser.add_argument("lon", type=float, required=True, location="args", help="lon obrigatória")

_PROVIDER = get_provider()

class RiskLightningResource(Resource):
    def get(self):
        args = _parser.parse_args()
        validate_coords(args["lat"], args["lon"])

        resp = _PROVIDER.lightning(args["lat"], args["lon"])

        prob = resp["p_cg_1h"]
        if prob < 0.2:      level, label = 0, "Baixo"
        elif prob < 0.4:    level, label = 1, "Moderado"
        elif prob < 0.6:    level, label = 2, "Alto"
        else:               level, label = 3, "Crítico"

        resp.update({"level": level, "label": label})
        return resp, 200
