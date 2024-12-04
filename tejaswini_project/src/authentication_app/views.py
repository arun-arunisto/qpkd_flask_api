from flask import Blueprint, request, jsonify, make_response, session
from src.authentication_app.models import User, db
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta
import os
from flask_login import login_user, logout_user, login_required, current_user

authentication_bp = Blueprint("authentication", __name__)

#authentication
auth_status = {}

@authentication_bp.route("/api/authentication/signup", methods=["POST"])
def signup():
    """
    For creating a new user account
    accepts name, ,email and password
    email will be unique it will check for the validation with email if the user exists or not
    """
    data = request.get_json()
    print("Data:",request.get_json())
    #gets the name, email and password
    name, email = data.get("name"), data.get("email")
    password = data.get("password")
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(name, email, password)
            db.session.add(user)
            db.session.commit()
            return jsonify({"message":"Signed up successfully!!"}), 201
        else:
            return jsonify({"message":"Already exists please login"}), 400
    except Exception as e:
        return jsonify({"message":str(e)}), 400

@authentication_bp.route("/api/authentication/login", methods=["POST"])
def login():
    """
    To login a user
    accepts email and password 
    it check the hashed password already saved in the database
    """
    auth = request.get_json()
    print("data:",auth)
    email = auth.get("email")
    password = auth.get("password")
    if not auth or not auth.get("email") or not auth.get("password"):
        return jsonify({"message":"All fields required"}), 400
    try:
        user = User.query.filter_by(email=auth.get("email")).first()

        if not user:
            return jsonify({"message":"User does not exist"}), 401
        if check_password_hash(user.password, auth.get("password")):
            login_user(user)
            auth_status["user_public_id"] = user.public_id
            return jsonify({"message":"Login successfully!!"}), 200
        else:
            return jsonify({"message":"Incorrect password!!"}), 401
    except Exception as e:
        print(str(e))
        return jsonify({"message":str(e)}), 400

@authentication_bp.route("/api/authentication/logout", methods=["GET"])
def logout():
    """
    To logout a user already login
    """
    try:
        if not auth_status.get("user_public_id"):
            return jsonify({"status":"Unauthorized"}), 401
        auth_status.clear()
        return jsonify({"message":"Logged out successfully!!"}), 200
    except Exception as e:
        return jsonify({"message":str(e)}), 400
