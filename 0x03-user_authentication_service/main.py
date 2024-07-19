#!/usr/bin/env python3
"""
Will run tests on our implemented functions
"""
import requests
from auth import Auth

AUTH = Auth()


def register_user(email: str, password: str) -> None:
    """
    Saves a user to the database.
    Expected result:
        - A json response object
    """
    url = "http://0.0.0.0:5000/users"
    data = {"email": email, "password": password}
    reg_user = requests.post(url, data=data)

    expected = {'email': email, 'message': 'user created'}
    assert reg_user.status_code == 200
    assert reg_user.json() == expected


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Validate wrong passwords

    Expected result:
        - a 401 status code
    """
    url = "http://0.0.0.0:5000/sessions"
    data = {"email": email, "password": password}
    invalid_login = requests.post(url, data=data)

    assert invalid_login.status_code == 401


def profile_unlogged() -> None:
    """
    Invalid profile login

    Expected:
        - A 403 status code
    """
    url = "http://0.0.0.0:5000/profile"
    cookies = {"session_id": ""}
    req = requests.get(url, cookies=cookies)
    assert req.status_code == 403


def log_in(email: str, password: str) -> str:
    """
    Login with correct credentials

    Expected:
        - a json object response
        - a 200 http status code
    """
    expected = {"email": email, "message": "logged in"}
    url = "http://0.0.0.0:5000/sessions"
    data = {"email": email, "password": password}
    req = requests.post(url, data=data)

    assert req.status_code == 200
    assert req.json() == expected
    return req.cookies.get("session_id")


def profile_logged(session_id: str) -> None:
    """
    When successfully logged in, a session id
    is created and now you can view profile.

    Expected:
        - User's email in a json object
        - a 200 http status code
    """
    url = "http://0.0.0.0:5000/profile"
    cookies = {"session_id": session_id}
    req = requests.get(url, cookies=cookies)

    assert req.status_code == 200


def log_out(session_id: str) -> None:
    """
    Destroys a user's session id

    Expected:
        - A redirect http status code
    """
    url = "http://0.0.0.0:5000/sessions"
    cookies = {"session_id": session_id}
    req = requests.delete(url, cookies=cookies)

    assert req.status_code == 200


def reset_password_token(email: str) -> str:
    """
    Perform a password reset request

    Expected:
        -   A reset_token
    """
    url = "http://0.0.0.0:5000/reset_password"
    data = {"email": email}
    req = requests.post(url, data=data)

    assert req.status_code == 200

    return req.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Update the password through the reset_token

    Expected:
        -   A json response object
    """
    expected = {"email": email, "message": "Password updated"}
    url = "http://0.0.0.0:5000/reset_password"
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
        }
    req = requests.put(url, data=data)

    assert req.status_code == 200
    assert req.json() == expected


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
