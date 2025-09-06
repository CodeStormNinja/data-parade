from flask_restful import Resource, reqparse
from ..utils import validate_coords
from ..providers import get_provider

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument("lat", type=float, required=True, location="args", help="lat obrigatória")
parser.add_argument("lon", type=float, required=True, location="args", help="lon obrigatória")

_PROVIDER = get_provider()

class RiskWindResource(Resource):
    def get(self):
        args = parser.parse_args()
        validate_coords(args["lat"], args["lon"])
        resp = _PROVIDER.wind(args["lat"], args["lon"])


        gust = resp["gust_kmh"]
        if gust < 35: level, label = 0, "Baixo"
        elif gust <  55: level, label = 1,"Moderado"
        elif gust < 75: level, label = 2, "Alto"
        else:           level, label = 3, "Crítico"

        resp.update({"level": level, "lebel":label})
        return resp, 200

