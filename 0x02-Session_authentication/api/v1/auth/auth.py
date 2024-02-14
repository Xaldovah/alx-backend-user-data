#!/usr/bin/env python3
"""
This class provides methods for handling
authentication in an API
"""

from flask import request
from typing import List
import os


class Auth:
    """
    Auth class for managing API authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determine if authentication is required for a given path.

        Args:
            path (str): The path of the request.
            excluded_paths (list): List of paths that do not require
            authentication.

        Returns:
        bool: True if authentication is required, False otherwise.
        """
        if not path or not excluded_paths:
            return True

        path = path.rstrip('/') + '/'

        for excluded_path in excluded_paths:
            if path == excluded_path or path.startswith(
                    excluded_path + "*"):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieve the Authorization header from the request.

        Args:
            request (flask.Request, optional): The Flask request object.

        Returns:
        str: The value of the Authorization header, or None if not present.
        """
        if request is None:
            return None

        auth_header = request.headers.get('Authorization')
        return auth_header

    def current_user(self, request=None):
        """
        Retrieve the current user based on the request.

        Args:
            request (flask.Request, optional): The Flask request object.

        Returns:
        TypeVar('User'): The current user, or None if not authenticated.
        """
        return None

    def session_cookie(self, request=None):
        """ Returns a cookie value from a request.

        Args:
            request: The request object.

        Returns:
            str: The value of the cookie named SESSION_NAME from request.
        """
        if request is None:
            return None

        session_name = os.getenv('SESSION_NAME', '_my_session_id')
        return request.cookies.get(session_name)
