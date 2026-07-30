from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db
from models.user import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# Register
@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    if not data:
        return jsonify({"message": "No data provided"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message": "Email already exists"}), 409

    user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        role=data.get("role", "student"),
        password=generate_password_hash(data["password"])
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully"
    }), 201


# Login
@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    user = User.query.filter_by(
        email=data["email"]
    ).first()

    if user is None:
        return jsonify({
            "message": "Invalid email or password"
        }), 401

    if not check_password_hash(
        user.password,
        data["password"]
    ):
        return jsonify({
            "message": "Invalid email or password"
        }), 401

    access_token = create_access_token(
        identity=user.id
    )

    return jsonify({
        "token": access_token,
        "user": user.to_dict()
    })


# Logged-in user profile
@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():

    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if user is None:
        return jsonify({
            "message": "User not found"
        }), 404

    return jsonify(user.to_dict())