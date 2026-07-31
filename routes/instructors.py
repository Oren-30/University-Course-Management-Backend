from flask import Blueprint, request, jsonify
from extensions import db
from models import Instructor

instructors_bp = Blueprint("instructors", __name__)


# GET all instructors
@instructors_bp.route("", methods=["GET"])
def get_instructors():
    instructors = Instructor.query.all()

    return jsonify([
        {
            "id": instructor.id,
            "name": instructor.name,
            "email": instructor.email,
            "department": instructor.department
        }
        for instructor in instructors
    ]), 200


# GET one instructor
@instructors_bp.route("/<int:id>", methods=["GET"])
def get_instructor(id):
    instructor = Instructor.query.get_or_404(id)

    return jsonify({
        "id": instructor.id,
        "name": instructor.name,
        "email": instructor.email,
        "department": instructor.department
    }), 200


# CREATE instructor
@instructors_bp.route("", methods=["POST"])
def create_instructor():
    data = request.get_json()

    instructor = Instructor(
        name=data["name"],
        email=data["email"],
        department=data.get("department")
    )

    db.session.add(instructor)
    db.session.commit()

    return jsonify({
        "message": "Instructor created successfully",
        "instructor": {
            "id": instructor.id,
            "name": instructor.name,
            "email": instructor.email,
            "department": instructor.department
        }
    }), 201


# UPDATE instructor
@instructors_bp.route("/<int:id>", methods=["PUT"])
def update_instructor(id):
    instructor = Instructor.query.get_or_404(id)

    data = request.get_json()

    instructor.name = data.get(
        "name",
        instructor.name
    )

    instructor.email = data.get(
        "email",
        instructor.email
    )

    instructor.department = data.get(
        "department",
        instructor.department
    )

    db.session.commit()

    return jsonify({
        "message": "Instructor updated successfully"
    }), 200


# DELETE instructor
@instructors_bp.route("/<int:id>", methods=["DELETE"])
def delete_instructor(id):
    instructor = Instructor.query.get_or_404(id)

    db.session.delete(instructor)
    db.session.commit()

    return jsonify({
        "message": "Instructor deleted successfully"
    }), 200


# SEARCH instructors
@instructors_bp.route("/search", methods=["GET"])
def search_instructors():
    query = request.args.get("q", "")

    instructors = Instructor.query.filter(
        Instructor.name.ilike(f"%{query}%")
    ).all()

    return jsonify([
        {
            "id": instructor.id,
            "name": instructor.name,
            "email": instructor.email,
            "department": instructor.department
        }
        for instructor in instructors
    ]), 200