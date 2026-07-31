from functools import wraps

from flask import jsonify

from flask_jwt_extended import (
    verify_jwt_in_request,
    get_jwt,
    get_jwt_identity
)

from models.user import User


def role_required(*allowed_roles):
    """
    Restrict access to users with the specified roles.

    Example:
        @role_required("admin")
        @role_required("admin", "instructor")
    """

    def decorator(fn):

        @wraps(fn)
        def wrapper(*args, **kwargs):

            # Verify JWT exists
            verify_jwt_in_request()

            # Read JWT claims
            claims = get_jwt()

            user_role = claims.get("role")

            if user_role not in allowed_roles:
                return jsonify({
                    "success": False,
                    "message": "Access denied. You do not have permission to perform this action."
                }), 403

            return fn(*args, **kwargs)

        return wrapper

    return decorator


def get_current_user():
    """
    Return the currently logged-in user.
    """

    user_id = get_jwt_identity()

    return User.query.get(user_id)


def is_admin():
    """
    Returns True if the current user is an admin.
    """

    claims = get_jwt()

    return claims.get("role") == "admin"


def is_instructor():
    """
    Returns True if the current user is an instructor.
    """

    claims = get_jwt()

    return claims.get("role") == "instructor"


def is_student():
    """
    Returns True if the current user is a student.
    """

    claims = get_jwt()

    return claims.get("role") == "student"