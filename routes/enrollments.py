from flask import Blueprint, request, jsonify
from extensions import db
from models import Enrollment

enrollments_bp = Blueprint("enrollments", __name__)


# GET all enrollments
@enrollments_bp.route("", methods=["GET"])
def get_enrollments():
    enrollments = Enrollment.query.all()

    return jsonify([
        {
            "id": enrollment.id,
            "student_id": enrollment.student_id,
            "course_id": enrollment.course_id
        }
        for enrollment in enrollments
    ]), 200


# GET one enrollment
@enrollments_bp.route("/<int:id>", methods=["GET"])
def get_enrollment(id):
    enrollment = Enrollment.query.get_or_404(id)

    return jsonify({
        "id": enrollment.id,
        "student_id": enrollment.student_id,
        "course_id": enrollment.course_id
    }), 200


# CREATE enrollment
@enrollments_bp.route("", methods=["POST"])
def create_enrollment():
    data = request.get_json()

    enrollment = Enrollment(
        student_id=data["student_id"],
        course_id=data["course_id"]
    )

    db.session.add(enrollment)
    db.session.commit()

    return jsonify({
        "message": "Enrollment created successfully",
        "enrollment": {
            "id": enrollment.id,
            "student_id": enrollment.student_id,
            "course_id": enrollment.course_id
        }
    }), 201


# UPDATE enrollment
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

    db.session.commit()

    return jsonify({
        "message": "Enrollment updated successfully"
    }), 200


# DELETE enrollment
@enrollments_bp.route("/<int:id>", methods=["DELETE"])
def delete_enrollment(id):
    enrollment = Enrollment.query.get_or_404(id)

    db.session.delete(enrollment)
    db.session.commit()

    return jsonify({
        "message": "Enrollment deleted successfully"
    }), 200


# SEARCH enrollments
@enrollments_bp.route("/search", methods=["GET"])
def search_enrollments():
    query = request.args.get("q", "")

    enrollments = Enrollment.query.filter(
        (Enrollment.student_id == query)
        |
        (Enrollment.course_id == query)
    ).all()

    return jsonify([
        {
            "id": enrollment.id,
            "student_id": enrollment.student_id,
            "course_id": enrollment.course_id
        }
        for enrollment in enrollments
    ]), 200