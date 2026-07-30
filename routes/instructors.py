from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from extensions import db
from models.instructor import Instructor

instructors_bp = Blueprint(
    "instructors",
    __name__,
    url_prefix="/instructors"
)


# Get all instructors
@instructors_bp.route("/", methods=["GET"])
@jwt_required()
def get_instructors():

    instructors = Instructor.query.all()

    return jsonify(
        [instructor.to_dict() for instructor in instructors]
    )


# Get one instructor
@instructors_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_instructor(id):

    instructor = Instructor.query.get_or_404(id)

    return jsonify(instructor.to_dict())