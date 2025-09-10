from flask_restful import Resource, reqparse
from flask import current_app
from datetime import datetime, timezone
import os, time
import requests

_parser = reqparse.RequestParser()
_parser.add_argument("deep", type=int, location="args", choices=(0, 1), default=0)

def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

class HealthResource(Resource):
    def get(self):
        args = _parser.parse_args()

        info = {
            "status": "ok",
            "service": "evento-seguro-api",
            "time_utc": _utc_now_iso(),
            "started_at_utc": current_app.config.get("STARTED_AT_UTC"),
            "uptime_s": round(time.time() - current_app.config.get("STARTED_AT_TS", time.time()), 1),
            "version": os.getenv("APP_VERSION", "dev"),
            "provider_mode": os.getenv("PROVIDER_MODE", "live"),
            "cache_ttl_sec": int(os.getenv("OM_CACHE_TTL_SEC", "900")),
            "debug": bool(current_app.debug),
        }

        if args.deep == 1:
            deps = {}
            try:
                t0 = time.perf_counter()
                r = requests.get(
                    "https://api.open-meteo.com/v1/forecast",
                    params={
                        "latitude": 0, "longitude": 0,
                        "hourly": "temperature_2m",
                        "forecast_days": 1, "timezone": "UTC"
                    },
                    timeout=float(os.getenv("OM_TIMEOUT_SEC", "2"))
                )
                r.raise_for_status()
                deps["open_meteo"] = {
                    "status": "ok",
                    "latency_ms": round((time.perf_counter() - t0) * 1000, 1)
                }
            except Exception as e:
                deps["open_meteo"] = {"status": "fail", "error": type(e).__name__}

            info["deps"] = deps

        return info, 200

"""
/health — health check da API

- Retorna o estado básico do serviço e metadados úteis para observabilidade.
- Opcionalmente executa um "deep check" de dependências externas (Open-Meteo).

Exemplos
- Health rápido:      GET /api/v1/health
- Deep health (dep):  GET /api/v1/health?deep=1

Resposta (200 OK)
{
  "status": "ok",                 # estado lógico da API (processo vivo)
  "service": "evento-seguro-api", # nome do serviço
  "time_utc": "...Z",             # agora em UTC
  "started_at_utc": "...Z",       # quando o app iniciou (UTC)
  "uptime_s": 123.4,              # segundos desde o start
  "version": "dev|x.y.z",         # APP_VERSION
  "provider_mode": "live|mock",   # PROVIDER_MODE
  "cache_ttl_sec": 900,           # OM_CACHE_TTL_SEC
  "debug": true|false,            # Flask debug
  "deps": {                       # só quando deep=1
    "open_meteo": { "status": "ok|fail", "latency_ms": 123.4 | "error": "Timeout" }
  }
}

"""