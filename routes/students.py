from flask import Blueprint, request, jsonify

from flask_jwt_extended import jwt_required

from extensions import db

from models.student import Student

from utils.roles import role_required


students_bp = Blueprint(
    "students",
    __name__,
    url_prefix="/students"
)


# ==========================================
# Get all students
# ==========================================
@students_bp.route("/", methods=["GET"])
@jwt_required()
def get_students():

    students = Student.query.all()

    return jsonify({
        "success": True,
        "count": len(students),
        "students": [
            student.to_dict() for student in students
        ]
    }), 200


# ==========================================
# Get one student
# ==========================================
@students_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_student(id):

    student = Student.query.get(id)

    if student is None:

        return jsonify({
            "success": False,
            "message": "Student not found."
        }), 404

    return jsonify({
        "success": True,
        "student": student.to_dict()
    }), 200


# ==========================================
# Create student (Admin only)
# ==========================================
@students_bp.route("/", methods=["POST"])
@role_required("admin")
def create_student():

    data = request.get_json()

    required_fields = [
        "first_name",
        "last_name",
        "email",
        "student_number",
        "department",
        "program",
        "year_of_study"
    ]

    for field in required_fields:

        if field not in data or data[field] == "":
            return jsonify({
                "success": False,
                "message": f"{field} is required."
            }), 400

    existing_student = Student.query.filter(
        (Student.email == data["email"]) |
        (Student.student_number == data["student_number"])
    ).first()

    if existing_student:

        return jsonify({
            "success": False,
            "message": "Student already exists."
        }), 409

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
        "success": True,
        "message": "Student created successfully.",
        "student": student.to_dict()
    }), 201


# ==========================================
# Update student (Admin only)
# ==========================================
@students_bp.route("/<int:id>", methods=["PUT"])
@role_required("admin")
def update_student(id):

    student = Student.query.get(id)

    if student is None:

        return jsonify({
            "success": False,
            "message": "Student not found."
        }), 404

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
        "success": True,
        "message": "Student updated successfully.",
        "student": student.to_dict()
    }), 200


# ==========================================
# Delete student (Admin only)
# ==========================================
@students_bp.route("/<int:id>", methods=["DELETE"])
@role_required("admin")
def delete_student(id):

    student = Student.query.get(id)

    if student is None:

        return jsonify({
            "success": False,
            "message": "Student not found."
        }), 404

    db.session.delete(student)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Student deleted successfully."
    }), 200


# ==========================================
# Search students
# ==========================================
@students_bp.route("/search", methods=["GET"])
@jwt_required()
def search_students():

    keyword = request.args.get("q", "")

    students = Student.query.filter(
        Student.first_name.ilike(f"%{keyword}%") |
        Student.last_name.ilike(f"%{keyword}%") |
        Student.student_number.ilike(f"%{keyword}%") |
        Student.email.ilike(f"%{keyword}%")
    ).all()

    return jsonify({
        "success": True,
        "count": len(students),
        "students": [
            student.to_dict() for student in students
        ]
    }), 200