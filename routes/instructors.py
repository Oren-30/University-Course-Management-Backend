from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from extensions import db
from models.instructor import Instructor

instructors_bp = Blueprint(
    "instructors",
    __name__,
    url_prefix="/instructors"
)


# Get all instructors
@instructors_bp.route("/", methods=["GET"])
@jwt_required()
def get_instructors():

    instructors = Instructor.query.all()

    return jsonify(
        [instructor.to_dict() for instructor in instructors]
    )


# Get one instructor
@instructors_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_instructor(id):

    instructor = Instructor.query.get_or_404(id)

    return jsonify(instructor.to_dict())
# Create instructor
@instructors_bp.route("/", methods=["POST"])
@jwt_required()
def create_instructor():

    data = request.get_json()

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
        "message": "Instructor created successfully",
        "instructor": instructor.to_dict()
    }), 201


# Update instructor
@instructors_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_instructor(id):

    instructor = Instructor.query.get_or_404(id)

    data = request.get_json()

    instructor.first_name = data.get(
        "first_name",
        instructor.first_name
    )

    instructor.last_name = data.get(
        "last_name",
        instructor.last_name
    )

    instructor.email = data.get(
        "email",
        instructor.email
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
        "message": "Instructor updated successfully",
        "instructor": instructor.to_dict()
    })


# Delete instructor
@instructors_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_instructor(id):

    instructor = Instructor.query.get_or_404(id)

    db.session.delete(instructor)
    db.session.commit()

    return jsonify({
        "message": "Instructor deleted successfully"
    })