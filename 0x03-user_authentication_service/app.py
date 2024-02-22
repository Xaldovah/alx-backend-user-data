#!/usr/bin/env python3
"""Create a flask app
"""

from flask import Flask, request, jsonify, make_response, abort
from auth import Auth
from typing import Union

app = Flask(__name__)
Auth = Auth()


@app.route("/")
def welcome():
    """
    Route to return a welcome message
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """
    Register a new user.

    Expect two form data fields: "email" and "password".
    If the user does not exist, register it and respond with a success message.
    If the user is already registered, respond with an error message and a 400
    status code.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        Auth.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login() -> Union[str, make_response]:
    """
    Log in the user.

    This function handles POST requests to the '/sessions' route to
    authenticate users and create a new session for them.

    Returns:
        Response: A response with JSON data indicating the login status.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not Auth.valid_login(email, password):
        abort(401)

    session_id = Auth.create_session(email)

    response = make_response(jsonify({'email': email, 'message': 'logged in'}))
    response.set_cookie('session_id', session_id)

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
