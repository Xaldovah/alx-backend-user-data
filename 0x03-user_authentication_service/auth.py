#!/usr/bin/env python3
"""takes in a password string arguments and returns bytes"""

import bcrypt
import uuid
from db import DB
from user import Base, User


def _hash_password(password: str) -> bytes:
    """
    Hashes the input password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The salted hash of the input password.
    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed


def _generate_uuid() -> str:
    """
    Generate a new UUID string representation.

    Returns:
        str: A string representation of a new UUID.
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user.

        Args:
            email (str): The email address of the user.
            password (str): The password of the user.

        Returns:
            User: The created User object.

        Raises:
            ValueError: If a user with the provided email already exists.
        """
        existing_user = self._db.find_user_by(email=email)
        if existing_user:
            raise ValueError(f"User {email} already exists")

        hashed_password = _hash_password(password)
        user = self._db.add_user(email, hashed_password)
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate the user's login credentials.

        Args:
            email (str): The email address of the user.
            password (str): The password of the user.

        Returns:
        bool: True if the login credentials are valid, False otherwise.
        """
        user = self._db.find_user_by(email=email)

        if user:
            hashed_password = user.hashed_password
            user_pass = password.encode('utf-8')
            if bcrypt.checkpw(user_pass, hashed_password):
                return True
        return False

    def create_session(self, email: str) -> str:
        """
        Create a new session for the user.

        Args:
            email (str): The email address of the user.

        Returns:
            str: The session ID.
        """
        user = self._db.find_user_by(email=email)
        if user:
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        return None
