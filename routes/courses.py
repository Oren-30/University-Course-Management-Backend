from flask import Blueprint, request, jsonify
from extensions import db
from models import Course

courses_bp = Blueprint("courses", __name__)


# GET all courses
@courses_bp.route("", methods=["GET"])
def get_courses():
    courses = Course.query.all()

    return jsonify([
        {
            "id": course.id,
            "name": course.name,
            "code": course.code,
            "description": course.description
        }
        for course in courses
    ]), 200


# GET one course
@courses_bp.route("/<int:id>", methods=["GET"])
def get_course(id):
    course = Course.query.get_or_404(id)

    return jsonify({
        "id": course.id,
        "name": course.name,
        "code": course.code,
        "description": course.description
    }), 200


# CREATE course
@courses_bp.route("", methods=["POST"])
def create_course():
    data = request.get_json()

    course = Course(
        name=data["name"],
        code=data["code"],
        description=data.get("description")
    )

    db.session.add(course)
    db.session.commit()

    return jsonify({
        "message": "Course created successfully",
        "course": {
            "id": course.id,
            "name": course.name,
            "code": course.code,
            "description": course.description
        }
    }), 201


# UPDATE course
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
        "message": "Course updated successfully"
    }), 200


# DELETE course
@courses_bp.route("/<int:id>", methods=["DELETE"])
def delete_course(id):
    course = Course.query.get_or_404(id)

    db.session.delete(course)
    db.session.commit()

    return jsonify({
        "message": "Course deleted successfully"
    }), 200


# SEARCH courses
@courses_bp.route("/search", methods=["GET"])
def search_courses():
    query = request.args.get("q", "")

    courses = Course.query.filter(
        Course.name.ilike(f"%{query}%")
    ).all()

    return jsonify([
        {
            "id": course.id,
            "name": course.name,
            "code": course.code,
            "description": course.description
        }
        for course in courses
    ]), 200