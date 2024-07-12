#!/usr/bin/env python3
"""
Bringing Session authentication together
"""
import os
from api.v1.app import auth
from api.v1.views import app_views
from flask import request, jsonify
from models.user import User


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
    from api.v1.auth.session_auth import SessionAuth
    session_id = SessionAuth.create_session(user_id)

    # cookie = os.getenv("SESSION_NAME")
    # cookie.set_cookie(user_data.to_json())

    return user_data.to_json()
