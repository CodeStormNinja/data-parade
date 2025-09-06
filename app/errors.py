from flask import jsonify
from werkzeug.exceptions import HTTPException, BadRequest
import requests

def register_error_handlers(app):
    @app.errorhandler(BadRequest)
    def handle_bad_request(e):
        return jsonify(error={"code": 400, "name": "Bad Request", "message": e.description}), 400

    @app.errorhandler(HTTPException)
    def handle_http_exception(e: HTTPException):
        return jsonify(error={"code": e.code, "name": e.name, "message": e.description}), e.code

    @app.errorhandler((requests.Timeout, requests.ConnectionError, requests.RequestException))
    def handle_upstream(e):
        return jsonify(error={"code": 502, "name": "Upstream Error", "message": str(e)}), 502

    @app.errorhandler(Exception)
    def handle_generic(e):
        app.logger.exception("unexpected_error")
        return jsonify(error={"code": 500, "name": "Internal Server Error", "message": "unexpected_error"}), 500
