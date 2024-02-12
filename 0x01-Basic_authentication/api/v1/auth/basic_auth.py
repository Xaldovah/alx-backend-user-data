#!/usr/bin/env python3
"""
BasicAuth class for managing basic authentication.
"""

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    This class provides methods for handling
    basic authentication in an API.
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Extract the Base64 part of the Authorization header for Basic
        Authentication.

        Args:
            authorization_header (str): The Authorization header string.

        Returns:
        str: The Base64 part of the Authorization header, or None if not
        found.
        """
        if authorization_header is None or not isinstance(
                authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header.split(" ")[1]
