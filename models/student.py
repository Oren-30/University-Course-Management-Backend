from flask import Blueprint, request, jsonify
from extensions import db
from models.student import Student

students_bp = Blueprint("students", __name__)


# ==========================================
# GET ALL STUDENTS
# ==========================================
@students_bp.route("", methods=["GET"])
def get_students():

    students = Student.query.all()

    return jsonify({
        "students": [
            student.to_dict()
            for student in students
        ]
    }), 200


# ==========================================
# GET ONE STUDENT
# ==========================================
@students_bp.route("/<int:id>", methods=["GET"])
def get_student(id):

    student = Student.query.get_or_404(id)

    return jsonify({
        "student": student.to_dict()
    }), 200


# ==========================================
# CREATE STUDENT
# ==========================================
@students_bp.route("", methods=["POST"])
def create_student():

    data = request.get_json()

    student = Student(
        user_id=data["user_id"],
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


# ==========================================
# UPDATE STUDENT
# ==========================================
@students_bp.route("/<int:id>", methods=["PUT"])
def update_student(id):

    student = Student.query.get_or_404(id)

    data = request.get_json()

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


# ==========================================
# DELETE STUDENT
# ==========================================
@students_bp.route("/<int:id>", methods=["DELETE"])
def delete_student(id):

    student = Student.query.get_or_404(id)

    db.session.delete(student)
    db.session.commit()

    return jsonify({
        "message": "Student deleted successfully"
    }), 200


# ==========================================
# SEARCH STUDENTS
# ==========================================
@students_bp.route("/search", methods=["GET"])
def search_students():

    query = request.args.get("q", "")

    students = Student.query.join(Student.user).filter(
        db.or_(
            Student.student_number.ilike(f"%{query}%"),
            Student.department.ilike(f"%{query}%")
        )
    ).all()

    return jsonify({
        "students": [
            student.to_dict()
            for student in students
        ]
    }), 200