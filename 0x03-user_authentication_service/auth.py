#!/usr/bin/env python3
"""takes in a password string arguments and returns bytes"""

import bcrypt


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
