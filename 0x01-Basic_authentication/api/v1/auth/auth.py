#!/usr/bin/env python3
"""
Managing Authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Managing the API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Path authentication
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Authorization header authentication
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Current User authentication
        """
        return None
