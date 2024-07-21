#!/usr/bin/env python3
"""
Session Authentication
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
        Creating a session id
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retreiving the user id using the
        session id as the key
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        user = self.user_id_by_session_id.get(session_id)
        return user
