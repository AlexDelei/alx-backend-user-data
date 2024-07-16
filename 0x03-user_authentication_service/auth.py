#!/usr/bin/env python3
"""
Authentication systems
"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    Salts and hashes an input password

    Args:
        password - input password for hashing
    Returns:
        a byte string of the hashed password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(14))


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register's a user if does not exist in our
        database

        Args:
            email - user email, wil be used for validation
            password - user password
        Returns:
            Saved user object
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user
        raise ValueError("User <user's email> already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """
        Credentials Validation

        Args:
            email - used to locate the user
            password - validate this password
        Returns:
            True if password matches
        """
        try:
            user = self._db.find_user_by(email=email)
            hashed_pswd = user.hashed_password
            return bcrypt.checkpw(password.encode('utf-8'), hashed_pswd)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        Finds the user using the email, generates
        uuid and stores it in the db

        Args:
            email - user email
        Returns:
            users session id
        """
        try:
            user = self._db.find_user_by(email=email)
            user_session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=user_session_id)
            return str(user_session_id)
        except NoResultFound:
            return None


def _generate_uuid() -> str:
    """
    Generate and return UUID
    """
    return str(uuid.uuid4())
