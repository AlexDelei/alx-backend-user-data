#!/usr/bin/env python3
"""
Basic auth
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Auth replica lol
    """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """Basic - Base64 part
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header[len("Basic "):]
