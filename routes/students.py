from flask import Blueprint, request, jsonify
from extensions import db
from models.student import Student

students_bp = Blueprint("students", __name__)


# ===========================
# GET ALL STUDENTS
# ===========================
@students_bp.route("", methods=["GET"])
def get_students():

    students = Student.query.all()

    return jsonify({
        "students": [
            student.to_dict()
            for student in students
        ]
    }), 200


# ===========================
# GET ONE STUDENT
# ===========================
@students_bp.route("/<int:id>", methods=["GET"])
def get_student(id):

    student = Student.query.get_or_404(id)

    return jsonify({
        "student": student.to_dict()
    }), 200


# ===========================
# CREATE STUDENT
# ===========================
@students_bp.route("", methods=["POST"])
def create_student():

    data = request.get_json()

    student = Student(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        student_number=data["student_number"],
        department=data["department"],
        program=data["program"],
        year_of_study=data["year_of_study"]
    )

    db.session.add(student)
    db.session.commit()

    return jsonify({
        "message": "Student created successfully",
        "student": student.to_dict()
    }), 201


# ===========================
# UPDATE STUDENT
# ===========================
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

    student.student_number = data.get(
        "student_number",
        student.student_number
    )

    student.department = data.get(
        "department",
        student.department
    )

    student.program = data.get(
        "program",
        student.program
    )

    student.year_of_study = data.get(
        "year_of_study",
        student.year_of_study
    )

    db.session.commit()

    return jsonify({
        "message": "Student updated successfully",
        "student": student.to_dict()
    }), 200


# ===========================
# DELETE STUDENT
# ===========================
@students_bp.route("/<int:id>", methods=["DELETE"])
def delete_student(id):

    student = Student.query.get_or_404(id)

    db.session.delete(student)
    db.session.commit()

    return jsonify({
        "message": "Student deleted successfully"
    }), 200


# ===========================
# SEARCH STUDENTS
# ===========================
@students_bp.route("/search", methods=["GET"])
def search_students():

    query = request.args.get("q", "")

    students = Student.query.filter(
        Student.first_name.ilike(f"%{query}%") |
        Student.last_name.ilike(f"%{query}%") |
        Student.student_number.ilike(f"%{query}%")
    ).all()

    return jsonify({
        "students": [
            student.to_dict()
            for student in students
        ]
    }), 200