#!/usr/bin/env python3
"""Create a flask app
"""

from flask import Flask, request, jsonify
from auth import Auth

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
