#!/usr/bin/env python3
"""
Creating a new authentication mechanism
"""
import uuid
from api.v1.auth.auth import Auth
from models.user import User


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
            The cls attribute dictionary with each user's
            id value with a key, session_id
        """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retreives a user id based on the session ID

        Args:
            session_id - key for accessing user id
        Return:
            User id
        """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None

        user_id = self.user_id_by_session_id.get(session_id)
    #    print("The dictionary with creds: ", self.user_id_by_session_id)
        return user_id

    def current_user(self, request=None):
        """
        Using Session id to identify a User

        Args:
            request - GET url
        Returns:
            A User retreived from the Database through id
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
    #    print("Session Id: ", session_id)
    #    print("User Id: ", user_id
        user = User.get(user_id)
        if user:
            return user
        return None
