from flask import Blueprint, request, jsonify
from extensions import db
from models.instructor import Instructor

instructors_bp = Blueprint("instructors", __name__)


# ==========================================
# GET ALL INSTRUCTORS
# ==========================================
@instructors_bp.route("", methods=["GET"])
def get_instructors():

    instructors = Instructor.query.all()

    return jsonify({
        "instructors": [
            instructor.to_dict()
            for instructor in instructors
        ]
    }), 200


# ==========================================
# GET ONE INSTRUCTOR
# ==========================================
@instructors_bp.route("/<int:id>", methods=["GET"])
def get_instructor(id):

    instructor = Instructor.query.get_or_404(id)

    return jsonify({
        "instructor": instructor.to_dict()
    }), 200


# ==========================================
# CREATE INSTRUCTOR
# ==========================================
@instructors_bp.route("", methods=["POST"])
def create_instructor():

    data = request.get_json()

    instructor = Instructor(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        department=data["department"],
        specialization=data.get("specialization")
    )

    db.session.add(instructor)
    db.session.commit()

    return jsonify({
        "message": "Instructor created successfully",
        "instructor": instructor.to_dict()
    }), 201


# ==========================================
# UPDATE INSTRUCTOR
# ==========================================
@instructors_bp.route("/<int:id>", methods=["PUT"])
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

    instructor.department = data.get(
        "department",
        instructor.department
    )

    instructor.specialization = data.get(
        "specialization",
        instructor.specialization
    )

    db.session.commit()

    return jsonify({
        "message": "Instructor updated successfully",
        "instructor": instructor.to_dict()
    }), 200


# ==========================================
# DELETE INSTRUCTOR
# ==========================================
@instructors_bp.route("/<int:id>", methods=["DELETE"])
def delete_instructor(id):

    instructor = Instructor.query.get_or_404(id)

    db.session.delete(instructor)
    db.session.commit()

    return jsonify({
        "message": "Instructor deleted successfully"
    }), 200


# ==========================================
# SEARCH INSTRUCTORS
# ==========================================
@instructors_bp.route("/search", methods=["GET"])
def search_instructors():

    query = request.args.get("q", "")

    instructors = Instructor.query.filter(
        Instructor.first_name.ilike(f"%{query}%") |
        Instructor.last_name.ilike(f"%{query}%")
    ).all()

    return jsonify({
        "instructors": [
            instructor.to_dict()
            for instructor in instructors
        ]
    }), 200