rom flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from extensions import db
from models.student import Student

students_bp = Blueprint(
    "students",
    __name__,
    url_prefix="/students"
)


# Get all students
@students_bp.route("/", methods=["GET"])
@jwt_required()
def get_students():

    students = Student.query.all()

    return jsonify(
        [student.to_dict() for student in students]
    )


# Get one student
@students_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_student(id):

    student = Student.query.get_or_404(id)

    return jsonify(student.to_dict())


# Create student
@students_bp.route("/", methods=["POST"])
@jwt_required()
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


# Update student
@students_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_student(id):

    student = Student.query.get_or_404(id)

    data = request.get_json()
