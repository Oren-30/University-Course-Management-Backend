from datetime import datetime

from flask import Blueprint, request, jsonify

from flask_jwt_extended import jwt_required

from extensions import db

from models.enrollment import Enrollment
from models.student import Student
from models.course import Course

from utils.roles import role_required


enrollments_bp = Blueprint(
    "enrollments",
    __name__,
    url_prefix="/enrollments"
)


# ==========================================
# Get all enrollments
# ==========================================
@enrollments_bp.route("/", methods=["GET"])
@jwt_required()
def get_enrollments():

    enrollments = Enrollment.query.all()

    return jsonify({
        "success": True,
        "count": len(enrollments),
        "enrollments": [
            enrollment.to_dict()
            for enrollment in enrollments
        ]
    }), 200


# ==========================================
# Get one enrollment
# ==========================================
@enrollments_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_enrollment(id):

    enrollment = Enrollment.query.get(id)

    if enrollment is None:

        return jsonify({
            "success": False,
            "message": "Enrollment not found."
        }), 404

    return jsonify({
        "success": True,
        "enrollment": enrollment.to_dict()
    }), 200


# ==========================================
# Create enrollment
# Admin only
# ==========================================
@enrollments_bp.route("/", methods=["POST"])
@role_required("admin")
def create_enrollment():

    data = request.get_json()

    required_fields = [
        "student_id",
        "course_id"
    ]

    for field in required_fields:

        if field not in data:

            return jsonify({
                "success": False,
                "message": f"{field} is required."
            }), 400

    student = Student.query.get(
        data["student_id"]
    )

    if student is None:

        return jsonify({
            "success": False,
            "message": "Student not found."
        }), 404

    course = Course.query.get(
        data["course_id"]
    )

    if course is None:

        return jsonify({
            "success": False,
            "message": "Course not found."
        }), 404

    existing = Enrollment.query.filter_by(
        student_id=data["student_id"],
        course_id=data["course_id"]
    ).first()

    if existing:

        return jsonify({
            "success": False,
            "message": "Student is already enrolled in this course."
        }), 409

    enrollment = Enrollment(
        student_id=data["student_id"],
        course_id=data["course_id"],
        enrollment_date=datetime.utcnow().date(),
        status=data.get("status", "Active"),
        grade=data.get("grade")
    )

    db.session.add(enrollment)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Enrollment created successfully.",
        "enrollment": enrollment.to_dict()
    }), 201


# ==========================================
# Update enrollment
# Admin & Instructor
# ==========================================
@enrollments_bp.route("/<int:id>", methods=["PUT"])
@role_required("admin", "instructor")
def update_enrollment(id):

    enrollment = Enrollment.query.get(id)

    if enrollment is None:

        return jsonify({
            "success": False,
            "message": "Enrollment not found."
        }), 404

    data = request.get_json()

    if "student_id" in data:

        student = Student.query.get(
            data["student_id"]
        )

        if student is None:

            return jsonify({
                "success": False,
                "message": "Student not found."
            }), 404

        enrollment.student_id = data["student_id"]

    if "course_id" in data:

        course = Course.query.get(
            data["course_id"]
        )

        if course is None:

            return jsonify({
                "success": False,
                "message": "Course not found."
            }), 404

        enrollment.course_id = data["course_id"]

    if "enrollment_date" in data:

        enrollment.enrollment_date = datetime.strptime(
            data["enrollment_date"],
            "%Y-%m-%d"
        ).date()

    enrollment.status = data.get(
        "status",
        enrollment.status
    )

    enrollment.grade = data.get(
        "grade",
        enrollment.grade
    )

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Enrollment updated successfully.",
        "enrollment": enrollment.to_dict()
    }), 200


# ==========================================
# Delete enrollment
# Admin only
# ==========================================
@enrollments_bp.route("/<int:id>", methods=["DELETE"])
@role_required("admin")
def delete_enrollment(id):

    enrollment = Enrollment.query.get(id)

    if enrollment is None:

        return jsonify({
            "success": False,
            "message": "Enrollment not found."
        }), 404

    db.session.delete(enrollment)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Enrollment deleted successfully."
    }), 200


# ==========================================
# Search enrollments
# ==========================================
@enrollments_bp.route("/search", methods=["GET"])
@jwt_required()
def search_enrollments():

    keyword = request.args.get("q", "")

    enrollments = Enrollment.query.filter(
        Enrollment.status.ilike(f"%{keyword}%") |
        Enrollment.grade.ilike(f"%{keyword}%")
    ).all()

    return jsonify({
        "success": True,
        "count": len(enrollments),
        "enrollments": [
            enrollment.to_dict()
            for enrollment in enrollments
        ]
    }), 200
