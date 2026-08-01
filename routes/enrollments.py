from flask import Blueprint, request, jsonify
from extensions import db
from models.enrollment import Enrollment

enrollments_bp = Blueprint("enrollments", __name__)


# ==========================================
# GET ALL ENROLLMENTS
# ==========================================
@enrollments_bp.route("", methods=["GET"])
def get_enrollments():

    enrollments = Enrollment.query.all()

    return jsonify({
        "enrollments": [
            enrollment.to_dict()
            for enrollment in enrollments
        ]
    }), 200


# ==========================================
# GET ONE ENROLLMENT
# ==========================================
@enrollments_bp.route("/<int:id>", methods=["GET"])
def get_enrollment(id):

    enrollment = Enrollment.query.get_or_404(id)

    return jsonify({
        "enrollment": enrollment.to_dict()
    }), 200


# ==========================================
# CREATE ENROLLMENT
# ==========================================
@enrollments_bp.route("", methods=["POST"])
def create_enrollment():

    data = request.get_json()

    enrollment = Enrollment(
        student_id=data["student_id"],
        course_id=data["course_id"],
        semester=data["semester"],
        academic_year=data["academic_year"],
        grade=data.get("grade"),
        status=data.get("status", "Active")
    )

    db.session.add(enrollment)
    db.session.commit()

    return jsonify({
        "message": "Enrollment created successfully",
        "enrollment": enrollment.to_dict()
    }), 201


# ==========================================
# UPDATE ENROLLMENT
# ==========================================
@enrollments_bp.route("/<int:id>", methods=["PUT"])
def update_enrollment(id):

    enrollment = Enrollment.query.get_or_404(id)

    data = request.get_json()

    enrollment.student_id = data.get(
        "student_id",
        enrollment.student_id
    )

    enrollment.course_id = data.get(
        "course_id",
        enrollment.course_id
    )

    enrollment.semester = data.get(
        "semester",
        enrollment.semester
    )

    enrollment.academic_year = data.get(
        "academic_year",
        enrollment.academic_year
    )

    enrollment.grade = data.get(
        "grade",
        enrollment.grade
    )

    enrollment.status = data.get(
        "status",
        enrollment.status
    )

    db.session.commit()

    return jsonify({
        "message": "Enrollment updated successfully",
        "enrollment": enrollment.to_dict()
    }), 200


# ==========================================
# DELETE ENROLLMENT
# ==========================================
@enrollments_bp.route("/<int:id>", methods=["DELETE"])
def delete_enrollment(id):

    enrollment = Enrollment.query.get_or_404(id)

    db.session.delete(enrollment)
    db.session.commit()

    return jsonify({
        "message": "Enrollment deleted successfully"
    }), 200


# ==========================================
# SEARCH ENROLLMENTS
# ==========================================
@enrollments_bp.route("/search", methods=["GET"])
def search_enrollments():

    query = request.args.get("q", "")

    enrollments = Enrollment.query.filter(
        (Enrollment.student_id == query) |
        (Enrollment.course_id == query)
    ).all()

    return jsonify({
        "enrollments": [
            enrollment.to_dict()
            for enrollment in enrollments
        ]
    }), 200