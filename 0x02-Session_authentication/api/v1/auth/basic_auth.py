#!/usr/bin/env python3
"""
Basic auth
"""
import base64
from api.v1.auth.auth import Auth
from models.user import User
from typing import Tuple, Optional, TypeVar


class BasicAuth(Auth):
    """Auth replica lol
    """
    def extract_base64_authorization_header(
            self,
            authorization_header: str
            ) -> str:
        """Basic - Base64 part
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str
            ) -> str:
        """Basic - Base64 decoding
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_b = base64.b64decode(base64_authorization_header)
            decoded_str = decoded_b.decode('utf-8')
        except Exception:
            return None
        return decoded_str

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
            ) -> Tuple[Optional[str], Optional[str]]:
        """Basic - User Credentials
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        cred = decoded_base64_authorization_header.split(":", 1)
        email = cred[0]
        psswd = cred[1]
        return (email, psswd)

    def user_object_from_credentials(
            self,
            user_email: str, user_pwd: str
            ) -> TypeVar('User'):
        """
        Returns User Instance based on email and password
        """
        if not User:
            return None
        if not isinstance(user_email, str) or user_email is None:
            return None
        if not isinstance(user_pwd, str) or user_pwd is None:
            return None

        users = User.search({"email": user_email})
        if not users:
            return None

        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retreiving a User instance from the request
        """
        # retreiving the authorization header from the request
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        # Extract Base64 part of the authorization header
        b64_auth = self.extract_base64_authorization_header(auth_header)
        if b64_auth is None:
            return None

        # Decode the base64 part
        decode = self.decode_base64_authorization_header(b64_auth)
        if decode is None:
            return None

        # Extract the user credentials from (email, passwd)
        u_email, u_pswd = self.extract_user_credentials(decode)
        if u_email is None or u_pswd is None:
            return None

        # retreiving user instance
        user = self.user_object_from_credentials(u_email, u_pswd)
        return user
