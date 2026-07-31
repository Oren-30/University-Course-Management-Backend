from flask import Blueprint, request, jsonify

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from extensions import db
from models.user import User


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)


# ==========================================
# Register
# ==========================================
@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "No data provided."
        }), 400

    required_fields = [
        "first_name",
        "last_name",
        "email",
        "password"
    ]

    for field in required_fields:

        if field not in data or not data[field]:

            return jsonify({
                "success": False,
                "message": f"{field} is required."
            }), 400

    existing_user = User.query.filter_by(
        email=data["email"]
    ).first()

    if existing_user:

        return jsonify({
            "success": False,
            "message": "Email already exists."
        }), 409

    user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        password=generate_password_hash(data["password"]),
        role=data.get("role", "student")
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "User registered successfully.",
        "user": user.to_dict()
    }), 201


# ==========================================
# Login
# ==========================================
@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "No data provided."
        }), 400

    user = User.query.filter_by(
        email=data.get("email")
    ).first()

    if user is None:

        return jsonify({
            "success": False,
            "message": "Invalid email or password."
        }), 401

    if not check_password_hash(
        user.password,
        data.get("password")
    ):

        return jsonify({
            "success": False,
            "message": "Invalid email or password."
        }), 401

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "role": user.role
        }
    )

    return jsonify({
        "success": True,
        "message": "Login successful.",
        "access_token": access_token,
        "user": user.to_dict()
    }), 200


# ==========================================
# Logged-in User Profile
# ==========================================
@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():

    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if user is None:

        return jsonify({
            "success": False,
            "message": "User not found."
        }), 404

    return jsonify({
        "success": True,
        "user": user.to_dict()
    })


# ==========================================
# Update Profile
# ==========================================
@auth_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():

    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if user is None:

        return jsonify({
            "success": False,
            "message": "User not found."
        }), 404

    data = request.get_json()

    user.first_name = data.get(
        "first_name",
        user.first_name
    )

    user.last_name = data.get(
        "last_name",
        user.last_name
    )

    user.email = data.get(
        "email",
        user.email
    )

    if "password" in data and data["password"]:

        user.password = generate_password_hash(
            data["password"]
        )

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Profile updated successfully.",
        "user": user.to_dict()
    })


# ==========================================
# Verify Token
# ==========================================
@auth_bp.route("/verify", methods=["GET"])
@jwt_required()
def verify():

    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if user is None:

        return jsonify({
            "success": False,
            "message": "Invalid token."
        }), 401

    return jsonify({
        "success": True,
        "message": "Token is valid.",
        "user": user.to_dict()
    })