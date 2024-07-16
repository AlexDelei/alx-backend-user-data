#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> object:
        """
        Saves a User to the database

        Returns:
            an object with user details
        """
        u_obj = User(email=email, hashed_password=hashed_password)
        self._session.add(u_obj)
        self._session.commit()

        return u_obj

    def reset_schema(self) -> None:
        """
        Initialize or reset the database schema
        """
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
