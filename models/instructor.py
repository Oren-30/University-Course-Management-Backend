from flask import Blueprint, jsonify
from models.instructor import Instructor

instructors_bp = Blueprint("instructors", __name__)


# GET all instructors
@instructors_bp.route("", methods=["GET"])
def get_instructors():

    instructors = Instructor.query.all()

    return jsonify({
        "instructors": [
            instructor.to_dict()
            for instructor in instructors
        ]
    }), 200


# GET one instructor
@instructors_bp.route("/<int:id>", methods=["GET"])
def get_instructor(id):

    instructor = Instructor.query.get_or_404(id)

    return jsonify({
        "instructor": instructor.to_dict()
    }), 200