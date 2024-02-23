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

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Retrieve the user corresponding to the given session ID.
        """
        if session_id is None:
            return None

        return self._db.find_user_by(session_id=session_id)

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy the session of the user with the given user ID.
        """
        user = self._db.find_user_by(id=user_id)
        if user:
            user.session_id = None
            self._db.commit()

    def get_reset_password_token(self, email: str) -> str:
        """
        Generate a reset password token for the user with the given email.
        """
        user = self._db.find_user_by(email=email)
        if not user:
            raise ValueError

        reset_token = str(uuid.uuid4())
        user.reset_token = reset_token
        self._db.commit()

        return reset_token

    def update_password(self, reset_token: str, new_password: str) -> None:
        """
        Update the password of the user corresponding to the reset token.
        """
        user = self._db.find_user_by(reset_token=reset_token)
        if not user:
            raise ValueError

        hashed_password = _hash_password(new_password)
        user.hashed_password = hashed_password
        user.reset_token = None
        self._db.commit()
