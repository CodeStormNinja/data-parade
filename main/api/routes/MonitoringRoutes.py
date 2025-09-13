from flask_restx import Namespace, Resource
from flask import current_app
import time

from main.common.utils import DateTimeUtils
from main.infrastructure.http.HttpContext import HttpContext

ns = Namespace("health", description="Application Health Check")

@ns.route("/")
class HealthCheckResource(Resource):
    
    def __init__(self, api):
        self._http_context = HttpContext()
        super().__init__(api)
    
    def get(self):
        
        app_started_at_utc = current_app.config.get("APPLICATION_STARTED_AT_UTC")
        geocode_api_url = current_app.config.get("GEOCODE_API_URL")
        weather_forecast_api_url = current_app.config.get("OPEN_METEO_API_URL")

        info = {
            "status": "ok",
            "service": "evento-seguro-api",
            "started_at_utc": app_started_at_utc,
            "requested_at_utc": DateTimeUtils.utc_now_iso(),
            "uptime_s": round(time.time() - DateTimeUtils.utc_to_timestamp(app_started_at_utc), 1),
        }
            
        deps = {}
        
        deps["open_meteo"] = self._test_external_service(weather_forecast_api_url + "/v1/forecast", "get", params={
            "latitude": 0, "longitude": 0,
            "hourly": "temperature_2m",
            "forecast_days": 1, "timezone": "UTC"
        })
        
        deps["geocode"] = self._test_external_service(geocode_api_url + "/search", "get", params={
            "q": "United States", 
            "format": "json", 
            "limit": 1
        })

        info["deps"] = deps
        
        for dep in deps.values():
            if dep["status"] == "fail":
                info["status"] = "fail"
                break

        result_status_code = 200 if info["status"] == "ok" else 503
        return info, result_status_code
    
    def _test_external_service(self, url, method_name, params):
        method = getattr(self._http_context, method_name)
        try:
            t0 = time.perf_counter()
            method(url=url, params=params)
            return {
                "status": "ok",
                "latency_ms": round((time.perf_counter() - t0) * 1000, 1)
            }
        except Exception as e:
            return {
                "status": "fail", 
                "error": type(e).__name__
            }

"""
/health — Health check da API

- Retorna o estado do serviço e metadados úteis para observabilidade.

Exemplos
- Health-check:      GET /api/v1/health

Resposta (200 OK)
{
  "status": "ok",                 # estado lógico da API (processo vivo)
  "service": "evento-seguro-api", # nome do serviço
  "requested_at_utc": "...Z",     # Data-hora da requisição (UTC)
  "started_at_utc": "...Z",       # Data-hora da inicializacação do projeto (UTC)
  "uptime_s": 123.4,              # Segundos desde a inicialização
  "deps": {                       # Dependências externas
    "open_meteo": { 
        "status": "ok|fail", 
        "latency_ms": 123.4,
        "error": "Timeout" 
    },
    "geocode": { 
        "status": "ok|fail", 
        "latency_ms": 123.4,
        "error": "Timeout" 
    }
  }
}

"""