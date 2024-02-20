#!/usr/bin/env python3
"""Defines the User model for the users table."""

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Optional


Base = declarative_base()


class User(Base):
    """
    A class to represent a user in the database.

    Attributes:
        id (int): The primary key identifier for the user.
        email (str): The email address of the user.
        hashed_password (str): The hashed password of the user.
        session_id (str, optional): The session ID of the user.
        reset_token (str, optional): The reset token for the user's
            password reset.
    """
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True)
    email: str = Column(String(250), nullable=False)
    hashed_password: str = Column(String(250), nullable=False)
    session_id: Optional[str] = Column(String(250), nullable=True)
    reset_token: Optional[str] = Column(String(250), nullable=True)

    def __repr__(self) -> str:
        """
        Return a string representation of the User object.

        Returns:
            str: A string representation of the User object.
        """
        return f"<User(id={self.id}, email='{self.email}', \
                hashed_password='{self.hashed_password}', \
                session_id='{self.session_id}', \
                reset_token='{self.reset_token}')>"
