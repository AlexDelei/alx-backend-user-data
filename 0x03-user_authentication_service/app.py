#!/usr/bin/env python3
"""
Basic Flask App
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth
import uuid


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=['GET'], strict_slashes=False)
def basic_app():
    """
    Returns a simple payload using jsonify
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def users():
    """
    Endpoint for registering a User
    """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'], strict_slashes=False)
def login():
    """
    Logs In a User and creates a session for it
    """
    email = request.form.get("email")
    password = request.form.get("password")
    valid_user = AUTH.valid_login(email, password)
    if valid_user:
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response
    abort(401)


@app.route("/sessions", methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """
    Logout by deleting user session id
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=['GET'], strict_slashes=False)
def profile() -> str:
    """
    Retreive users session using his session id
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email})


@app.route("/reset_password", methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """
    Get reset token
    """
    email = request.form.get("email")
    user = AUTH._db.find_user_by(email=email)
    if user is not None and email is not None:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token})
    abort(403)


@app.route("/reset_password", methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """
    Update password endpoint
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    user = AUTH._db.find_user_by(email=email)
    user_reset_token = user.reset_token

    try:
        if user_reset_token != reset_token:
            raise ValueError
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
