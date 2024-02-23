#!/usr/bin/env python3
"""Create a flask app
"""

from flask import Flask, request, jsonify, make_response, abort, redirect
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


@app.route("/sessions", methods=["POST"])
def login():
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


@app.route('/sessions', methods=['DELETE'])
def logout():
    """
    Log out the user by destroying the session
    """
    session_id = request.cookies.get('session_id')
    user = Auth.get_user_from_session_id(session_id)
    if user:
        Auth.destroy_session(user.id)
        return redirect('/')
    else:
        return abort(403)

@app.route('/profile', methods=['GET'])
def profile():
    """Retrieve the user profile information
    """
    session_id = request.cookies.get('session_id')
    user = Auth.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        return abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
