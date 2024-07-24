#!/usr/bin/env python3
"""
New View for session authentication
"""
from flask import request, jsonify, abort
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route(
        '/auth_session/login',
        methods=['POST'],
        strict_slashes=False
        )
def login():
    """
    login functionality
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or email is None:
        return jsonify({"error": "email missing"}), 400
    if not password or password is None:
        return jsonify({"error": "password missing"}), 400

    user = User.search({'email': email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    u_user = user[0]
    if not u_user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(u_user.id)
    response = jsonify(u_user.to_json())
    response.set_cookie(getenv('SESSION_NAME'), session_id)
    return response


@app_views.route(
    '/auth_session/logout',
    methods=['DELETE'],
    strict_slashes=False
    )
def logout():
    """
    Logout by deleting current user session
    """
    from api.v1.app import auth
    destroy = auth.destroy_session(request)

    if destroy:
        return jsonify({}), 200
    abort(404)
