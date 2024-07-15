#!/usr/bin/env python3
"""
Bringing Session authentication together
"""
import os
from api.v1.app import auth
from api.v1.views import app_views
from flask import request, jsonify, session, abort
from models.user import User


cookie = os.getenv("SESSION_NAME")


@app_views.route(
        '/auth_session/login/',
        methods=['POST'],
        strict_slashes=False
        )
def session_authentication():
    """
    Handles all authentications in one route
    """
    user_email = request.form.get("email")
    user_psswd = request.form.get("password")

    if user_email is None or user_email == '':
        return jsonify({"error": "email missing"}), 400

    if user_psswd is None or user_psswd == '':
        return jsonify({"error": "password missing"}), 400

    valid_user = User.search({"email": user_email})
    if not valid_user:
        return jsonify({"error": "no user found for this email"}), 404

    user_ = valid_user[0]
    if not user_.is_valid_password(user_psswd):
        return jsonify({"error": "wrong password"}), 401

    user_data = valid_user[0]
    user_id = user_data.id

    user_id = user_data.id
    from api.v1.app import auth
    print("This is the Authetication system: ", auth)
    session_id = auth.create_session(user_id)
    user_session = jsonify(user_data.to_json())
    user_session.set_cookie(cookie, session_id)

    return user_session


@app_views.route(
    '/api/v1/auth_session/logout',
    methods=['DELETE'],
    strict_slashes=False
    )
def logout():
    """
    Logouts out a user by deleting user's instance
    """
    from api.v1.app import auth

    destroy = auth.destroy_session(request)
    if destroy:
        return jsonify({}), 200
    abort(404)
