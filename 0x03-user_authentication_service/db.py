#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import (
    NoResultFound, InvalidRequestError, ArgumentError
    )

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Saves a User to the database

        Returns:
            an object with user details
        """
        u_obj = User(email=email, hashed_password=hashed_password)
        self._session.add(u_obj)
        self._session.commit()

        return u_obj

    def find_user_by(self, **kwargs) -> User:
        """
        Performs Query and filters down by the
        arguments provided

        Args:
            keyword arguments
        Return:
            User object found
        """
        try:
            u_data = self._session.query(User).filter_by(**kwargs).first()
            if u_data is None:
                raise NoResultFound
            return u_data

        except ArgumentError:
            raise InvalidRequestError
