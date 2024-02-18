#!/usr/bin/env python3
"""
This module defines the UserSession model for storing session IDs
in the database.
"""
from models.base import Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class UserSession(Base):
    """
    UserSession model to store session IDs in the database.
    """

    __tablename__ = 'user_sessions'

    id = Column(String(60), primary_key=True)
    user_id = Column(String(60), nullable=False)
    session_id = Column(String(60), nullable=False)

    def __init__(self, *args: list, **kwargs: dict):
        """
        Initialize a new UserSession instance.

        Args:
            args (list): Positional arguments.
        kwargs (dict): Keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id', '')
        self.session_id = kwargs.get('session_id', '')

    def __str__(self):
        """
        Return a string representation of the UserSession instance.
        """
        return f"<UserSession(id='{self.id}', user_id='{self.user_id}', \
                session_id='{self.session_id}')>"
