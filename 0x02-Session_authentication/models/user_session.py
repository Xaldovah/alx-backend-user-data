#!/usr/bin/env python3
""" UserSession module
"""
from models.base import Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(Base):
    """ UserSession class
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        UserSession model to store session IDs in the database.
        """
        __tablename__ = 'user_sessions'

        user_id = Column(String(60), nullable=False)
        session_id = Column(String(60), nullable=False)
