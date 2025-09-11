from flask import current_app
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class HttpConfig:
    
    _default_timeout = None

    @classmethod
    def get_default_timeout(cls):
        if cls._default_timeout is None:
            cls._default_timeout = float(current_app.config.get("DEFAULT_HTTP_TIMEOUT_SECS"))
        return cls._default_timeout
    
    @staticmethod
    def create_session():
        session = requests.Session()
        session.headers.update({
            "User-Agent": "NasaDataParade/1.0",
            "Accept": "application/json",
        })
        adapter = HTTPAdapter(max_retries=Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[502, 503, 504],
            allowed_methods=["GET"]
        ))
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        return session