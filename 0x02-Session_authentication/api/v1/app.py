#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from flask import Flask, jsonify, abort, request, g
from flask_cors import (CORS, cross_origin)
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Lazy import of authentication classes to avoid circular import issues
auth = None
auth_type = getenv("AUTH_TYPE", None)
# print("Authentication Variable: ", auth_type)
if auth_type == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
    # print("Authentication system choosed: ", auth.__class__.__name__)
elif auth_type == 'session_auth':
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
    # print("Authentication systems choosed: ", auth)
else:
    from api.v1.auth.auth import Auth
    auth = Auth()
    # print("Authentication system choosed: ", auth)


@app.before_request
def execute_before_request():
    """
    Request Validation before making any requests
    """
    if auth is None:
        return

    rq_lst = [
        '/api/v1/status/', '/api/v1/unauthorized/',
        '/api/v1/forbidden/', '/api/v1/auth_session/login/'
    ]

    req_auth = auth.require_auth(request.path, rq_lst)

    if req_auth:
        auth_header = auth.authorization_header(request)
        if auth_header is None and auth.session_cookie is None:
            abort(401)
        if not auth.current_user(request):
            abort(403)
        request.current_user = auth.current_user(request)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """Unauthorized error handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbiddenError(error) -> str:
    """Forbidden error handler
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", 5000)
    app.run(host=host, port=port)
