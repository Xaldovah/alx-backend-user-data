#!/usr/bin/env python3
"""
This class handles all routes for the Session authentication.
"""

from flask import request, jsonify, abort
from typing import Tuple
from api.v1.views import app_views
from api.v1.auth import auth
from models.user import User
import os


@app_views.route(
        '/auth_session/login', methods=['POST'], strict_slashes=False)
@app_views.route(
        '/auth_session/login/', methods=['POST'], strict_slashes=False)
def login() -> Tuple[str, int]:
    """Handle user login
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email:
            return jsonify({"error": "email missing"}), 400
        if not password:
            return jsonify({"error": "password missing"}), 400

        user = User.search({"email": email})
        if not user:
            return jsonify({"error": "no user found for this email"}), 404

        user = user[0]
        if not user.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            response_data = user.to_json()
            response = jsonify(response_data)
            response.set_cookie(os.getenv("SESSION_NAME"), session_id)
            return response
        return jsonify({"error": "wrong password"}), 401

    return jsonify({"error": "Method Not Allowed"}), 405


@app_views.route(
        '/auth_session/logout', methods=['DELETE', 'GET'], strict_slashes=False)
@app_views.route(
        '/auth_session/logout/', methods=['DELETE', 'GET'], strict_slashes=False)
def logout():
    """ Handle user logout """
    from api.v1.app import auth
    if request.method == 'DELETE':
        if not auth.destroy_session(request):
            abort(404)
        return jsonify({}), 200
    return jsonify({"error": "Method Not Allowed"}), 405
