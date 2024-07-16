#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError, ArgumentError

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
        Retreives a user from the db

        Args:
            kwargs - key-value arguments to be used to filter
        Return:
            A user object
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound
        except InvalidRequestError:
            raise InvalidRequestError
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Locates the user to update using the user_id arg

        Args:
            user_id - a user id
            kwargs - key-value data for updating
        Returns:
            A user object
        """
        try:
            user = self.find_user_by(id=user_id)
            user = kwargs
        except ArgumentError:
            raise ValueError
        
        return None
