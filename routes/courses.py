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
    )


# Get one course
@courses_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_course(id):

    course = Course.query.get_or_404(id)

    return jsonify(course.to_dict())


# Create a course
@courses_bp.route("/", methods=["POST"])
@jwt_required()
def create_course():

    data = request.get_json()

    instructor = Instructor.query.get(data["instructor_id"])

    if instructor is None:
        return jsonify({
            "message": "Instructor not found"
        }), 404

    course = Course(
        course_code=data["course_code"],
        course_name=data["course_name"],
        description=data.get("description"),
        credit_hours=data["credit_hours"],
        instructor_id=data["instructor_id"]
    )

    db.session.add(course)
    db.session.commit()

    return jsonify({
        "message": "Course created successfully",
        "course": course.to_dict()
    }), 201

# Update a course
@courses_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_course(id):

    course = Course.query.get_or_404(id)

    data = request.get_json()

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

    course.credit_hours = data.get(
        "credit_hours",
        course.credit_hours
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
    })


# Delete a course
@courses_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_course(id):

    course = Course.query.get_or_404(id)

    db.session.delete(course)
    db.session.commit()

    return jsonify({
        "message": "Course deleted successfully"
    })