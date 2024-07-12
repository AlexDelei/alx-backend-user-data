#!/usr/bin/env python3
"""
Creating a new authentication mechanism
"""
import uuid
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """
    New authentication mechanism
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Every user has a session id.

        Args:
            user_id - user's id as a string
        Returns:
            The cls attribute dictionary.
        """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id