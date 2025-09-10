from flask_restful import Resource, reqparse
import os, requests

_parser = reqparse.RequestParser(bundle_errors=True)
_parser.add_argument("q", type=str, required=True, location="args", help="query address is required")
_parser.add_argument("limit", type=int, required=False, location="args", default=1)

class GeocodeResource(Resource):
    def get(self):
        args = _parser.parse_args()
        headers = {
            "User-Agent": os.getenv("GEOCODE_USER_AGENT", "evento-seguro-api/1.0 (contact: team@example.com)")
        }
        r = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": args["q"], "format": "json", "limit": args["limit"]},
            headers=headers, timeout=10
        )
        r.raise_for_status()
        data = r.json()
        if not data:
            return {"results": []}, 200
        # normaliza
        results = [
            {
                "lat": float(item["lat"]),
                "lon": float(item["lon"]),
                "display_name": item.get("display_name"),
            }
            for item in data
        ]
        return {"results": results}, 200

"""
/utils/geocode — utilitário de geocodificação (Nominatim/OSM)

O que faz
- Converte texto (endereço, ponto de interesse, cidade) em coordenadas {lat, lon}.
- Usa **Nominatim**, a API pública de geocodificação do **OpenStreetMap** (é uma API
  externa, **diferente** da nossa API de riscos).


1) GET /api/v1/utils/geocode?q=Praça da Sé, São Paulo&limit=1
2) Ler results[0].lat e results[0].lon (se existir)
3) Chamar /api/v1/risk/* com esses lat/lon (ex.: /risk/precip?lat={lat}&lon={lon})

Parâmetros
- q (obrigatório): texto para geocodificar
- limit (opcional): número de resultados (padrão 1)

Resposta (200)
{ "results": [ { "lat": -23.55, "lon": -46.63, "display_name": "..." } ] }
- Sem correspondência: "results": []
- Erros: 400 se faltar 'q'; 502 se a API externa falhar/timeout

"""