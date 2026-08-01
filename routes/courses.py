from flask import Blueprint, request, jsonify
from extensions import db
from models.course import Course

courses_bp = Blueprint("courses", __name__)


# ==========================================
# GET ALL COURSES
# ==========================================
@courses_bp.route("", methods=["GET"])
def get_courses():

    courses = Course.query.all()

    return jsonify({
        "courses": [
            course.to_dict()
            for course in courses
        ]
    }), 200


# ==========================================
# GET ONE COURSE
# ==========================================
@courses_bp.route("/<int:id>", methods=["GET"])
def get_course(id):

    course = Course.query.get_or_404(id)

    return jsonify({
        "course": course.to_dict()
    }), 200


# ==========================================
# CREATE COURSE
# ==========================================
@courses_bp.route("", methods=["POST"])
def create_course():

    data = request.get_json()

    course = Course(
        name=data["name"],
        code=data["code"],
        description=data.get("description"),
    )

    db.session.add(course)
    db.session.commit()

    return jsonify({
        "message": "Course created successfully",
        "course": course.to_dict()
    }), 201


# ==========================================
# UPDATE COURSE
# ==========================================
@courses_bp.route("/<int:id>", methods=["PUT"])
def update_course(id):

    course = Course.query.get_or_404(id)

    data = request.get_json()

    course.name = data.get("name", course.name)
    course.code = data.get("code", course.code)
    course.description = data.get(
        "description",
        course.description
    )

    db.session.commit()

    return jsonify({
        "message": "Course updated successfully",
        "course": course.to_dict()
    }), 200


# ==========================================
# DELETE COURSE
# ==========================================
@courses_bp.route("/<int:id>", methods=["DELETE"])
def delete_course(id):

    course = Course.query.get_or_404(id)

    db.session.delete(course)
    db.session.commit()

    return jsonify({
        "message": "Course deleted successfully"
    }), 200


# ==========================================
# SEARCH COURSES
# ==========================================
@courses_bp.route("/search", methods=["GET"])
def search_courses():

    query = request.args.get("q", "")

    courses = Course.query.filter(
        Course.name.ilike(f"%{query}%")
    ).all()

    return jsonify({
        "courses": [
            course.to_dict()
            for course in courses
        ]
    }), 200