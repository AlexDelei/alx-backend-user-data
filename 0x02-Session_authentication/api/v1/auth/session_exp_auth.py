#!/usr/bin/env python3
"""
Creating an expiration period
"""
from datetime import datetime, timedelta
from os import getenv
from api.v1.auth.session_auth import SessionAuth


SESSION_DURATION = getenv('SESSION_DURATION')


class SessionExpAuth(SessionAuth):
    """
    Adding an expiration date to a session id
    """
    def __init__(self):
        """
        Initialization
        """
        if SESSION_DURATION and isinstance(SESSION_DURATION, int):
            self.session_duration = int(SESSION_DURATION)
        self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Overloads create session that
        sets the session to have a timestamp
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        returns the timestamp and compares it
        to current time.
        """
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id.keys():
            return None

        user_id = self.user_id_by_session_id[session_id].get('user_id')
        if self.session_duration <= 0:
            return user_id

        if 'created_at' not in self.user_id_by_session_id[session_id].keys():
            return None
        created_at = self.user_id_by_session_id[session_id].get('created_at')

        current = datetime.now()
        expiry_time = created_at + timedelta(seconds=self.session_duration)

        if current >= expiry_time:
            return None

        return user_id
