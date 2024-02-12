#!/usr/bin/env python3
"""
This class provides methods for handling
authentication in an API
"""

from flask import request
from typing import List


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
        return False

    def authorization_header(self, request=None) -> str:
        """
        Retrieve the Authorization header from the request.

        Args:
            request (flask.Request, optional): The Flask request object.

        Returns:
        str: The value of the Authorization header, or None if not present.
        """
        return None

    def current_user(self, request=None):
        """
        Retrieve the current user based on the request.

        Args:
            request (flask.Request, optional): The Flask request object.

        Returns:
        TypeVar('User'): The current user, or None if not authenticated.
        """
        return None
