from flask import Blueprint, request, jsonify, make_response
from src.authentication_app.models import User, db
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta
import os

authentication_bp = Blueprint("authentication", __name__)

@authentication_bp.route("/api/authentication/signup", methods=["POST"])
def signup():
    data = request.form

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
    auth = request.form
    email = auth.get("email")
    password = auth.get("password")
    if not auth or not auth.get("email") or not auth.get("password"):
        return jsonify({"message":"All fields required"}), 400
    try:
        user = User.query.filter_by(email=auth.get("email")).first()

        if not user:
            return jsonify({"message":"User does not exist"}), 401
        if check_password_hash(user.password, auth.get("password")):
            return jsonify({"message":"Login successfully!!"}), 200
        else:
            return jsonify({"message":"Incorrect password!!"}), 401
    except Exception as e:
        return jsonify({"message":str(e)}), 400