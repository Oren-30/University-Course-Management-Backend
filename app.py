from flask import Flask
from flask_cors import CORS

from config import Config
from extensions import db, jwt

from routes.auth import auth_bp
from routes.students import students_bp
from routes.courses import courses_bp
from routes.instructors import instructors_bp
from routes.enrollments import enrollments_bp


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    # Enable CORS for the React frontend
    CORS(app)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(students_bp, url_prefix="/api")
    app.register_blueprint(courses_bp, url_prefix="/api")
    app.register_blueprint(instructors_bp, url_prefix="/api")
    app.register_blueprint(enrollments_bp, url_prefix="/api")

    @app.route("/")
    def home():
        return {
            "message": "University Course Management API Running"
        }

    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)