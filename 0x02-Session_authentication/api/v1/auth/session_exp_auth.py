#!/usr/bin/env python3
"""
This module provides an extension of the SessionAuth class
with session expiration functionality.
"""

from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """
    This class extends SessionAuth with session expiration functionality.
    """

    def __init__(self):
        """
        Initialize the SessionExpAuth instance.

        Sets the session duration based on the SESSION_DURATION environment
        variable.
        """
        super().__init__()
        self.session_duration = int(os.getenv('SESSION_DURATION', 0))

    def create_session(self, user_id=None):
        """
        Create a session for the specified user ID.

        Args:
            user_id (str): The ID of the user to create a
            session for.

        Returns:
            str: The session ID created for the user, or None
            if creation fails.
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        self.user_id_by_session_id[session_id] = {
                'user_id': user_id,
                'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieve the user ID associated with a session ID.

        Args:
            session_id (str): The session ID to retrieve the user ID for.

        Returns:
            str: The user ID associated with the session ID, or None
            if not found or expired.
        """
        if session_id is None:
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None

        if self.session_duration <= 0:
            return session_dict.get('user_id')

        created_at = session_dict.get('created_at')
        if created_at is None:
            return None

        expiration_time = created_at + timedelta(
                seconds=self.session_duration)
        if datetime.now() > expiration_time:
            return None

        return session_dict.get('user_id')
