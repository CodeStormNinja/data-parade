# app/providers.py
import json, time, hashlib, os  # noqa: E401
from pathlib import Path
from typing import Dict, Any, Optional
import requests
from math import isfinite

# -------- cache config --------
CACHE_TTL_SEC = int(os.getenv("OM_CACHE_TTL_SEC", "900"))  # 15 min
CACHE_DIR = Path("./.cache")
CACHE_DIR.mkdir(exist_ok=True)

# -------- helpers --------
def _round(x: float, nd: int = 2) -> float:
    return round(x, nd) if (x is not None and isfinite(x)) else 0.0

def _ck(name: str, lat: float, lon: float) -> Path:
    raw = f"{name}:{_round(lat)}:{_round(lon)}"
    h = hashlib.sha1(raw.encode()).hexdigest()[:16]
    return CACHE_DIR / f"{name}_{h}.json"

def _get_cache(p: Path) -> Optional[Dict[str, Any]]:
    if p.exists() and (time.time() - p.stat().st_mtime) < CACHE_TTL_SEC:
        return json.loads(p.read_text(encoding="utf-8"))
    return None

def _set_cache(p: Path, data: Dict[str, Any]) -> Dict[str, Any]:
    p.write_text(json.dumps(data), encoding="utf-8")
    return data

def _first(seq, default=None):
    try:
        return seq[0]
    except (IndexError, TypeError):
        return default

# -------- provider --------
class OpenMeteoProvider:
    """Cliente simples para /v1/forecast e /v1/air-quality (sem API key)."""
    BASE = "https://api.open-meteo.com/v1/forecast"
    AIR  = "https://air-quality-api.open-meteo.com/v1/air-quality"

    def __init__(self, session: Optional[requests.Session] = None):
        self.http = session or requests.Session()
        self.timeout = float(os.getenv("OM_TIMEOUT_SEC", "10"))

    # ---------- forecast ----------
    def _fetch(self, lat: float, lon: float) -> Dict[str, Any]:
        p = _ck("om_forecast", lat, lon)
        cached = _get_cache(p)
        if cached:
            return cached

        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": ",".join([
                "precipitation",          # mm
                "wind_gusts_10m",         # km/h
                "temperature_2m",         # °C
                "relative_humidity_2m",   # %
            ]),
            "forecast_days": 2,
            "timezone": "auto",
        }
        r = self.http.get(self.BASE, params=params, timeout=self.timeout)
        r.raise_for_status()
        return _set_cache(p, r.json())

    # ---------- mapeamentos p/ contrato ----------
    def precip(self, lat: float, lon: float) -> Dict[str, Any]:
        data = self._fetch(lat, lon)
        h = data.get("hourly", {})
        pr = float(_first(h.get("precipitation"), 0.0))  # mm/h
        p = min(1.0, pr / 5.0)                           # heurística simples
        return {
            "lat": lat, "lon": lon,
            "p_rain_1h": round(p, 2),
            "intensity_mm_h": round(pr, 1),
            "source": "open-meteo",
            "updated_at": _first(h.get("time")) or data.get("timezone", ""),
        }

    def wind(self, lat: float, lon: float) -> Dict[str, Any]:
        data = self._fetch(lat, lon)
        h = data.get("hourly", {})
        gust = float(_first(h.get("wind_gusts_10m"), 0.0))  # km/h
        return {
            "lat": lat, "lon": lon,
            "p_gust_1h": round(min(1.0, gust / 80.0), 2),
            "gust_kmh": int(gust),
            "sustained_kmh": max(0, int(gust) - 25),
            "source": "open-meteo",
            "updated_at": _first(h.get("time")) or data.get("timezone", ""),
        }

    def heat(self, lat: float, lon: float) -> Dict[str, Any]:
        data = self._fetch(lat, lon)
        h = data.get("hourly", {})
        t  = float(_first(h.get("temperature_2m"), 0.0))       # °C
        rh = float(_first(h.get("relative_humidity_2m"), 50))  # %

        wbgt = t - 2.5
        utci = t + 0.2 * max(0.0, (rh - 50.0) / 10.0)
        return {
            "lat": lat, "lon": lon,
            "wbgt": round(wbgt, 1),
            "utci": round(utci, 1),
            "p_heat_stress_1h": round(max(0.0, (utci - 26.0) / 14.0), 2),
            "source": "open-meteo",
            "updated_at": _first(h.get("time")) or data.get("timezone", ""),
        }

    def lightning(self, lat: float, lon: float) -> Dict[str, Any]:
        w = self.wind(lat, lon)
        p = self.precip(lat, lon)
        prob = round(min(1.0, 0.5 * p["p_rain_1h"] + 0.5 * w["p_gust_1h"]), 2)
        return {
            "lat": lat, "lon": lon,
            "p_cg_1h": prob,
            "within_10km": prob > 0.6,
            "source": "proxy(open-meteo)",
            "updated_at": w["updated_at"],
        }

    # ---------- air quality ----------
    def air(self, lat: float, lon: float) -> Dict[str, Any]:
        p = _ck("om_air", lat, lon)
        cached = _get_cache(p)
        if cached:
            return cached

        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": "pm2_5,pm10,ozone,us_aqi",
            "forecast_days": 2,
            "timezone": "auto",
        }
        r = self.http.get(self.AIR, params=params, timeout=self.timeout)
        r.raise_for_status()
        data = r.json()
        h = data.get("hourly", {})
        aqi  = int(_first(h.get("us_aqi"), 0))
        pm25 = float(_first(h.get("pm2_5"), 0.0))
        pm10 = float(_first(h.get("pm10"), 0.0))
        o3   = float(_first(h.get("ozone"), 0.0))
        cat = ("Good" if aqi <= 50 else
               "Moderate" if aqi <= 100 else
               "USG" if aqi <= 150 else
               "Unhealthy" if aqi <= 200 else
               "Very Unhealthy" if aqi <= 300 else "Hazardous")
        return _set_cache(p, {
            "lat": lat, "lon": lon,
            "us_aqi": aqi, "pm2_5": round(pm25, 1), "pm10": round(pm10, 1), "o3": round(o3, 1),
            "category": cat, "source": "open-meteo-air",
            "updated_at": _first(h.get("time")) or data.get("timezone", ""),
        })


def get_provider():
    return OpenMeteoProvider()
