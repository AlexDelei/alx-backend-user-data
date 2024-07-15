#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.auth import Auth
from flask import Flask, jsonify, abort, request, g
from flask_cors import (CORS, cross_origin)

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = getenv("AUTH_TYPE", None)
if auth == 'basic_auth':
    auth = BasicAuth()
elif auth == 'session_auth':
    auth = SessionAuth()
else:
    auth = Auth()


@app.before_request
def execute_before_request():
    """Request Validation
    """
    if auth is None:
        return

    rq_lst = [
        '/api/v1/status/', '/api/v1/unauthorized/',
        '/api/v1/forbidden/', '/api/v1/auth_session/login/'
        ]

    req_auth = auth.require_auth(request.path, rq_lst)
    auth_session_cookie = auth.session_cookie(request)
    auth_header = auth.authorization_header(request)

    if req_auth:
        if not auth_header and not auth_session_cookie:
            abort(401)
        if not auth.current_user(request):
            abort(403)

    g.current_user = auth.current_user(request)


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
    app.run(host=host, port=port, debug=True)
