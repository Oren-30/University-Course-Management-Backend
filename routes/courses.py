from flask import Blueprint, request, jsonify

from flask_jwt_extended import jwt_required

from extensions import db

from models.course import Course
from models.instructor import Instructor

from utils.roles import role_required


courses_bp = Blueprint(
    "courses",
    __name__,
    url_prefix="/courses"
)


# ==========================================
# Get all courses
# ==========================================
@courses_bp.route("/", methods=["GET"])
@jwt_required()
def get_courses():

    courses = Course.query.all()

    return jsonify({
        "success": True,
        "count": len(courses),
        "courses": [
            course.to_dict() for course in courses
        ]
    }), 200


# ==========================================
# Get one course
# ==========================================
@courses_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_course(id):

    course = Course.query.get(id)

    if course is None:

        return jsonify({
            "success": False,
            "message": "Course not found."
        }), 404

    return jsonify({
        "success": True,
        "course": course.to_dict()
    }), 200


# ==========================================
# Create course
# Admin & Instructor
# ==========================================
@courses_bp.route("/", methods=["POST"])
@role_required("admin", "instructor")
def create_course():

    data = request.get_json()

    required_fields = [
        "course_code",
        "course_name",
        "credits",
        "department",
        "semester",
        "instructor_id"
    ]

    for field in required_fields:

        if field not in data or data[field] == "":
            return jsonify({
                "success": False,
                "message": f"{field} is required."
            }), 400

    existing_course = Course.query.filter_by(
        course_code=data["course_code"]
    ).first()

    if existing_course:

        return jsonify({
            "success": False,
            "message": "Course code already exists."
        }), 409

    instructor = Instructor.query.get(
        data["instructor_id"]
    )

    if instructor is None:

        return jsonify({
            "success": False,
            "message": "Instructor not found."
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
        "success": True,
        "message": "Course created successfully.",
        "course": course.to_dict()
    }), 201


# ==========================================
# Update course
# Admin & Instructor
# ==========================================
@courses_bp.route("/<int:id>", methods=["PUT"])
@role_required("admin", "instructor")
def update_course(id):

    course = Course.query.get(id)

    if course is None:

        return jsonify({
            "success": False,
            "message": "Course not found."
        }), 404

    data = request.get_json()

    if "course_code" in data:

        existing = Course.query.filter(
            Course.course_code == data["course_code"],
            Course.id != id
        ).first()

        if existing:

            return jsonify({
                "success": False,
                "message": "Course code already exists."
            }), 409

        course.course_code = data["course_code"]

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
                "success": False,
                "message": "Instructor not found."
            }), 404

        course.instructor_id = data["instructor_id"]

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Course updated successfully.",
        "course": course.to_dict()
    }), 200


# ==========================================
# Delete course
# Admin only
# ==========================================
@courses_bp.route("/<int:id>", methods=["DELETE"])
@role_required("admin")
def delete_course(id):

    course = Course.query.get(id)

    if course is None:

        return jsonify({
            "success": False,
            "message": "Course not found."
        }), 404

    db.session.delete(course)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Course deleted successfully."
    }), 200


# ==========================================
# Search courses
# ==========================================
@courses_bp.route("/search", methods=["GET"])
@jwt_required()
def search_courses():

    keyword = request.args.get("q", "")

    courses = Course.query.filter(
        Course.course_code.ilike(f"%{keyword}%") |
        Course.course_name.ilike(f"%{keyword}%") |
        Course.department.ilike(f"%{keyword}%") |
        Course.semester.ilike(f"%{keyword}%")
    ).all()

    return jsonify({
        "success": True,
        "count": len(courses),
        "courses": [
            course.to_dict() for course in courses
        ]
    }), 200