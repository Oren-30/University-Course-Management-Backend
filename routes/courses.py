from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from extensions import db
from models.course import Course
from models.instructor import Instructor

courses_bp = Blueprint(
    "courses",
    __name__,
    url_prefix="/courses"
)


# Get all courses
@courses_bp.route("/", methods=["GET"])
@jwt_required()
def get_courses():

    courses = Course.query.all()

    return jsonify(
        [course.to_dict() for course in courses]
    ), 200


# Get one course
@courses_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_course(id):

    course = Course.query.get_or_404(id)

    return jsonify(course.to_dict()), 200


# Create course
@courses_bp.route("/", methods=["POST"])
@jwt_required()
def create_course():

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "No data provided"
        }), 400

    required = [
        "course_code",
        "course_name",
        "credits",
        "department",
        "semester",
        "instructor_id"
    ]

    for field in required:
        if not data.get(field):
            return jsonify({
                "message": f"{field} is required"
            }), 400

    if Course.query.filter_by(
        course_code=data["course_code"]
    ).first():
        return jsonify({
            "message": "Course code already exists"
        }), 409

    instructor = Instructor.query.get(
        data["instructor_id"]
    )

    if instructor is None:
        return jsonify({
            "message": "Instructor not found"
        }), 404

    course = Course(
        course_code=data["course_code"],
        course_name=data["course_name"],
        description=data.get("description"),
        credits=data["credits"],
        department=data["department"],
        semester=data["semester"],
        instructor_id=data["instructor_id"]
    )

    db.session.add(course)
    db.session.commit()

    return jsonify({
        "message": "Course created successfully",
        "course": course.to_dict()
    }), 201


# Update course
@courses_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_course(id):

    course = Course.query.get_or_404(id)

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "No data provided"
        }), 400

    if "course_code" in data:
        existing = Course.query.filter_by(
            course_code=data["course_code"]
        ).first()

        if existing and existing.id != course.id:
            return jsonify({
                "message": "Course code already exists"
            }), 409

    course.course_code = data.get(
        "course_code",
        course.course_code
    )

    course.course_name = data.get(
        "course_name",
        course.course_name
    )

    course.description = data.get(
        "description",
        course.description
    )

    course.credits = data.get(
        "credits",
        course.credits
    )

    course.department = data.get(
        "department",
        course.department
    )

    course.semester = data.get(
        "semester",
        course.semester
    )

    if "instructor_id" in data:

        instructor = Instructor.query.get(
            data["instructor_id"]
        )

        if instructor is None:
            return jsonify({
                "message": "Instructor not found"
            }), 404

        course.instructor_id = data["instructor_id"]

    db.session.commit()

    return jsonify({
        "message": "Course updated successfully",
        "course": course.to_dict()
    }), 200


# Delete course
@courses_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_course(id):

    course = Course.query.get_or_404(id)

    db.session.delete(course)
    db.session.commit()

    return jsonify({
        "message": "Course deleted successfully"
    }), 200