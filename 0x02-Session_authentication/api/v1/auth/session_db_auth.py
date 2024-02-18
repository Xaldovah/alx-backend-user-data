#!/usr/bin/env python3
"""
This module defines the SessionDBAuth class for session authentication
with database storage.
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime
from flask import request


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth class for session authentication with
    database storage.
    """

    def create_session(self, user_id=None):
        """
        Create a session for the specified user ID and store it in the database

        Args:
            user_id (str): The ID of the user to create a session for.

        Returns:
            str: The session ID created for the user, or None if creation fails
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        new_session = UserSession(user_id=user_id, session_id=session_id)
        new_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieve the user ID associated with a session ID from the database.

        Args:
            session_id (str): The session ID to retrieve the user ID for.

        Returns:
            str: The user ID associated with the session ID, or None
            if not found or expired.
        """
        if session_id is None:
            return None

        session = UserSession.search({'session_id': session_id})
        if not session:
            return None

        session = session[0]
        return super().user_id_for_session_id(session_id)

    def destroy_session(self, request=None):
        """
        Destroy the session associated with the request from the database.

        Args:
            request: The request object containing the session ID
            in the cookies.
        """
        if request is None:
            return

        session_id = request.cookies.get(self.session_name)
        if session_id:
            sessions = UserSession.search({'session_id': session_id})
            for session in sessions:
                session.remove()
