from flask import Blueprint, request, jsonify
from extensions import db
from models.student import Student

students_bp = Blueprint("students", __name__)


def student_response(student):
    return {
        "id": student.id,
        "name": f"{student.first_name} {student.last_name}",
        "email": student.email
    }


# GET all students
@students_bp.route("", methods=["GET"])
def get_students():
    students = Student.query.all()

    return jsonify([
        student_response(student)
        for student in students
    ]), 200


# GET one student
@students_bp.route("/<int:id>", methods=["GET"])
def get_student(id):
    student = Student.query.get_or_404(id)

    return jsonify(
        student_response(student)
    ), 200


# CREATE student
@students_bp.route("", methods=["POST"])
def create_student():
    data = request.get_json()

    student = Student(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"]
    )

    db.session.add(student)
    db.session.commit()

    return jsonify({
        "message": "Student created successfully",
        "student": student_response(student)
    }), 201


# UPDATE student
@students_bp.route("/<int:id>", methods=["PUT"])
def update_student(id):
    student = Student.query.get_or_404(id)

    data = request.get_json()

    student.first_name = data.get(
        "first_name",
        student.first_name
    )

    student.last_name = data.get(
        "last_name",
        student.last_name
    )

    student.email = data.get(
        "email",
        student.email
    )

    db.session.commit()

    return jsonify({
        "message": "Student updated successfully"
    }), 200


# DELETE student
@students_bp.route("/<int:id>", methods=["DELETE"])
def delete_student(id):
    student = Student.query.get_or_404(id)

    db.session.delete(student)
    db.session.commit()

    return jsonify({
        "message": "Student deleted successfully"
    }), 200


# SEARCH students
@students_bp.route("/search", methods=["GET"])
def search_students():
    query = request.args.get("q", "")

    students = Student.query.filter(
        Student.first_name.ilike(f"%{query}%") |
        Student.last_name.ilike(f"%{query}%")
    ).all()

    return jsonify([
        student_response(student)
        for student in students
    ]), 200