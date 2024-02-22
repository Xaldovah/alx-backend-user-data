#!/usr/bin/env python3
"""
Main file
"""
import requests

BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """
    Registers a user with the given email and password.

    Args:
        email (str): The email of the user to register.
        password (str): The password of the user to register.

    Returns:
        None
    """
    response = requests.post(f"{BASE_URL}/users", data={
        "email": email, "password": password})
    assert response.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Attempts to log in with the given email and wrong password.

    Args:
        email (str): The email of the user.
        password (str): The wrong password to use for login.

    Returns:
        None
    """
    response = requests.post(f"{BASE_URL}/sessions", data={
        "email": email, "password": password})
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    Logs in a user with the given email and password.

    Args:
        email (str): The email of the user.
        password (str): The password of the user.

    Returns:
        str: The session ID obtained after successful login.
    """
    response = requests.post(
        f"{BASE_URL}/sessions",
        data={
            "email": email,
            "password": password
        }
    )
    assert response.status_code == 200
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """
    Attempts to access the profile page without logging in.

    Returns:
        None
    """
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 401


def profile_logged(session_id: str) -> None:
    """
    Accesses the profile page with a valid session ID.

    Args:
        session_id (str): The session ID obtained after logging in.

    Returns:
        None
    """
    headers = {"Cookie": f"session_id={session_id}"}
    response = requests.get(f"{BASE_URL}/profile", headers=headers)
    assert response.status_code == 200


def log_out(session_id: str) -> None:
    """
    Logs out a user with the given session ID.

    Args:
        session_id (str): The session ID of the user to log out.

    Returns:
        None
    """
    headers = {"Cookie": f"session_id={session_id}"}
    response = requests.delete(
        f"{BASE_URL}/sessions", headers=headers
    )
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """
    Requests a password reset token for the given email.

    Args:
        email (str): The email for which to request the reset token.

    Returns:
        str: The reset token obtained.
    """
    response = requests.post(
        f"{BASE_URL}/reset_password", data={"email": email})
    assert response.status_code == 200
    return response.json()["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Updates the password for the given email using the reset token.

    Args:
        email (str): The email for which to update the password.
        reset_token (str): The reset token obtained for the email.
        new_password (str): The new password to set for the user.

    Returns: None
    """
    response = requests.put(f"{BASE_URL}/reset_password",
                            data={"email": email,
                                  "reset_token": reset_token,
                                  "new_password": new_passwor
                                  }
                            )
    assert response.status_code == 200


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
