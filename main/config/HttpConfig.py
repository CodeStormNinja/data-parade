from flask import current_app
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class HttpConfig:
    
    default_timeout = None
    session = None
    
    def __init__(self):
        
        if HttpConfig.session is None:
            session = requests.Session()
            session.headers.update({
                "User-Agent": "nasa-data-parade/1.0",
                "Accept": "application/json",
            })
            adapter = HTTPAdapter(max_retries=Retry(
                total=3,
                backoff_factor=1,
                status_forcelist=[502, 503, 504],
                allowed_methods=["GET"]
            ))
            session.mount("https://", adapter)
            HttpConfig.session = session
        
        if HttpConfig.default_timeout is None:
            HttpConfig.default_timeout = float(current_app.config.get("DEFAULT_HTTP_TIMEOUT_SECS"))