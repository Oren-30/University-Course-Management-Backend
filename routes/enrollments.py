from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from extensions import db
from models.enrollment import Enrollment
from models.student import Student
from models.course import Course

enrollments_bp = Blueprint(
    "enrollments",
    __name__,
    url_prefix="/enrollments"
)


# Get all enrollments
@enrollments_bp.route("/", methods=["GET"])
@jwt_required()
def get_enrollments():

    enrollments = Enrollment.query.all()

    return jsonify(
        [enrollment.to_dict() for enrollment in enrollments]
    )


# Get one enrollment
@enrollments_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_enrollment(id):

    enrollment = Enrollment.query.get_or_404(id)

    return jsonify(enrollment.to_dict())


# Create enrollment
@enrollments_bp.route("/", methods=["POST"])
@jwt_required()
def create_enrollment():

    data = request.get_json()

    student = Student.query.get(data["student_id"])
    course = Course.query.get(data["course_id"])

    if student is None:
        return jsonify({"message": "Student not found"}), 404

    if course is None:
        return jsonify({"message": "Course not found"}), 404

    enrollment = Enrollment(
        student_id=data["student_id"],
        course_id=data["course_id"],
        enrollment_date=data["enrollment_date"],
        status=data.get("status", "Active"),
        grade=data.get("grade")
    )

    db.session.add(enrollment)
    db.session.commit()

    return jsonify({
        "message": "Enrollment created successfully",
        "enrollment": enrollment.to_dict()
    }), 201


# Update enrollment
@enrollments_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_enrollment(id):

    enrollment = Enrollment.query.get_or_404(id)

    data = request.get_json()

    if "student_id" in data:
        student = Student.query.get(data["student_id"])

        if student is None:
            return jsonify({"message": "Student not found"}), 404

        enrollment.student_id = data["student_id"]

    if "course_id" in data:
        course = Course.query.get(data["course_id"])

        if course is None:
            return jsonify({"message": "Course not found"}), 404

        enrollment.course_id = data["course_id"]

    enrollment.enrollment_date = data.get(
        "enrollment_date",
        enrollment.enrollment_date
    )

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
        "message": "Enrollment updated successfully",
        "enrollment": enrollment.to_dict()
    })


# Delete enrollment
@enrollments_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_enrollment(id):

    enrollment = Enrollment.query.get_or_404(id)

    db.session.delete(enrollment)
    db.session.commit()

    return jsonify({
        "message": "Enrollment deleted successfully"
    })