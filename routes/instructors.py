from flask import Blueprint, request, jsonify

from flask_jwt_extended import jwt_required

from extensions import db

from models.instructor import Instructor

from utils.roles import role_required


instructors_bp = Blueprint(
    "instructors",
    __name__,
    url_prefix="/instructors"
)


# ==========================================
# Get all instructors
# ==========================================
@instructors_bp.route("/", methods=["GET"])
@jwt_required()
def get_instructors():

    instructors = Instructor.query.all()

    return jsonify({
        "success": True,
        "count": len(instructors),
        "instructors": [
            instructor.to_dict()
            for instructor in instructors
        ]
    }), 200


# ==========================================
# Get one instructor
# ==========================================
@instructors_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_instructor(id):

    instructor = Instructor.query.get(id)

    if instructor is None:

        return jsonify({
            "success": False,
            "message": "Instructor not found."
        }), 404

    return jsonify({
        "success": True,
        "instructor": instructor.to_dict()
    }), 200


# ==========================================
# Create instructor
# Admin only
# ==========================================
@instructors_bp.route("/", methods=["POST"])
@role_required("admin")
def create_instructor():

    data = request.get_json()

    required_fields = [
        "first_name",
        "last_name",
        "email",
        "department"
    ]

    for field in required_fields:

        if field not in data or data[field] == "":

            return jsonify({
                "success": False,
                "message": f"{field} is required."
            }), 400

    existing = Instructor.query.filter_by(
        email=data["email"]
    ).first()

    if existing:

        return jsonify({
            "success": False,
            "message": "Instructor already exists."
        }), 409

    instructor = Instructor(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        phone=data.get("phone"),
        department=data["department"],
        office=data.get("office")
    )

    db.session.add(instructor)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Instructor created successfully.",
        "instructor": instructor.to_dict()
    }), 201


# ==========================================
# Update instructor
# Admin only
# ==========================================
@instructors_bp.route("/<int:id>", methods=["PUT"])
@role_required("admin")
def update_instructor(id):

    instructor = Instructor.query.get(id)

    if instructor is None:

        return jsonify({
            "success": False,
            "message": "Instructor not found."
        }), 404

    data = request.get_json()

    if "email" in data:

        existing = Instructor.query.filter(
            Instructor.email == data["email"],
            Instructor.id != id
        ).first()

        if existing:

            return jsonify({
                "success": False,
                "message": "Email already exists."
            }), 409

        instructor.email = data["email"]

    instructor.first_name = data.get(
        "first_name",
        instructor.first_name
    )

    instructor.last_name = data.get(
        "last_name",
        instructor.last_name
    )

    instructor.phone = data.get(
        "phone",
        instructor.phone
    )

    instructor.department = data.get(
        "department",
        instructor.department
    )

    instructor.office = data.get(
        "office",
        instructor.office
    )

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Instructor updated successfully.",
        "instructor": instructor.to_dict()
    }), 200


# ==========================================
# Delete instructor
# Admin only
# ==========================================
@instructors_bp.route("/<int:id>", methods=["DELETE"])
@role_required("admin")
def delete_instructor(id):

    instructor = Instructor.query.get(id)

    if instructor is None:

        return jsonify({
            "success": False,
            "message": "Instructor not found."
        }), 404

    db.session.delete(instructor)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Instructor deleted successfully."
    }), 200


# ==========================================
# Search instructors
# ==========================================
@instructors_bp.route("/search", methods=["GET"])
@jwt_required()
def search_instructors():

    keyword = request.args.get("q", "")

    instructors = Instructor.query.filter(
        Instructor.first_name.ilike(f"%{keyword}%") |
        Instructor.last_name.ilike(f"%{keyword}%") |
        Instructor.email.ilike(f"%{keyword}%") |
        Instructor.department.ilike(f"%{keyword}%")
    ).all()

    return jsonify({
        "success": True,
        "count": len(instructors),
        "instructors": [
            instructor.to_dict()
            for instructor in instructors
        ]
    }), 200