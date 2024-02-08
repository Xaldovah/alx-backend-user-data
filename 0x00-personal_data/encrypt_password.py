#!/usr/bin/env python3
"""
This module function returns the log message obfuscated
"""

import bcrypt


def hash_password(password):
    """
    Hashes a password using bcrypt with salt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The hashed password.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


def is_valid(hashed_password, password):
    """
    Validates a password against a hashed password using bcrypt.

    Args:
        hashed_password (bytes): The hashed password.
        password (str): The password to validate.

    Returns:
        bool: True if the password matches the hashed password,
        False otherwise.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
