from flask_restful import Resource, reqparse
from ..utils import validate_coords
from ..providers import get_provider

_parser = reqparse.RequestParser(bundle_errors=True)
_parser.add_argument("lat", type=float, required=True, location="args", help="lat obrigatória")
_parser.add_argument("lon", type=float, required=True, location="args", help="lon obrigatória")

_PROVIDER = get_provider()

class RiskPrecipResource(Resource):
    def get(self):
        args = _parser.parse_args()
        validate_coords(args["lat"], args["lon"])

        resp = _PROVIDER.precip(args["lat"], args["lon"])

        p, inten = resp["p_rain_1h"], resp["intensity_mm_h"]
        if p < 0.2 and inten < 2:   level, label = 0, "Baixo"
        elif p < 0.5 and inten < 5: level, label = 1, "Moderado"
        elif p < 0.7 or inten < 10: level, label = 2, "Alto"
        else:                       level, label = 3, "Crítico"

        resp.update({"level": level, "label": label})
        return resp, 200
