#!/usr/bin/env python3
"""
BasicAuth class for managing basic authentication.
"""

from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
import base64


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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decode the Base64 authorization header.

        Args:
            base64_authorization_header (str): The Base64 authorization
            header string

        Returns:
            str: The decoded value as a UTF-8 string, or None
            if decoding fails.
        """
        if base64_authorization_header is None or not isinstance(
                base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(
                    base64_authorization_header)
            decoded_string = decoded_bytes.decode('utf-8')
            return decoded_string
        except ValueError:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extract user credentials from the decoded Base64 authorization
        header

        Args:
            decoded_base64_authorization_header (str): The decoded Base64
            authorization header string.

        Returns:
            tuple: A tuple containing user email and password.
        """
        if decoded_base64_authorization_header is None or not isinstance(
                decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        user_email, user_password = decoded_base64_authorization_header.split(
                ':', 1)
        return user_email, user_password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Get the User instance based on email and password.

        Args:
            user_email (str): The user's email.
            user_pwd (str): The user's password.

        Returns:
            User: The User instance if found and password matches, else None.
        """
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        users = User.search({"email": user_email})

        if not users:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Get the User instance for the request.

        Args:
            request (flask.Request): The Flask request object.

        Returns:
            User: The User instance if found and authenticated, else None.
        """
        if request is None:
            return None

        authorization_header = request.header.get('Authorization')
        if authorization_header is None:
            return None

        base64_auth_header = self.extract_base64_authorization_header(
                authorization_header)
        if base64_auth_header is None:
            return None

        decoded_base64_auth_header = self.decode_base64_authorization_header(
                base64_auth_header)
        if decoded_base64_auth_header is None:
            return None

        user_email, user_pwd = self.extract_user_credentials(
                decoded_base64_auth_header)

        if user_email is None or user_pwd is None:
            return None

        return self.user_object_from_credentials(
                user_email, user_pwd)
