from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from extensions import db
from models.user import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# Register
@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "No data provided"
        }), 400

    required = [
        "first_name",
        "last_name",
        "email",
        "password"
    ]

    for field in required:
        if not data.get(field):
            return jsonify({
                "message": f"{field} is required"
            }), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({
            "message": "Email already exists"
        }), 409

    user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        role=data.get("role", "student")
    )

    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully",
        "user": user.to_dict()
    }), 201


# Login
@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "No data provided"
        }), 400

    if not data.get("email") or not data.get("password"):
        return jsonify({
            "message": "Email and password are required"
        }), 400

    user = User.query.filter_by(
        email=data["email"]
    ).first()

    if user is None or not user.check_password(data["password"]):
        return jsonify({
            "message": "Invalid email or password"
        }), 401

    access_token = create_access_token(
        identity=str(user.id)
    )

    return jsonify({
        "access_token": access_token,
        "user": user.to_dict()
    }), 200


# Logged-in User
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():

    user_id = get_jwt_identity()

    user = User.query.get(int(user_id))

    if user is None:
        return jsonify({
            "message": "User not found"
        }), 404

    return jsonify(user.to_dict()), 200