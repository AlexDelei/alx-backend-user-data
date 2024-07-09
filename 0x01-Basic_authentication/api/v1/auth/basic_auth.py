#!/usr/bin/env python3
"""
Basic auth
"""
import base64
from api.v1.auth.auth import Auth


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
            ) -> (str, str):
        """Basic - User Credentials
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        user = decoded_base64_authorization_header.split(':')[0]
        email = decoded_base64_authorization_header.split(':')[1]
        return (user, email)
