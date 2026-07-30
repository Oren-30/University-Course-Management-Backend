from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    first_name = db.Column(
        db.String(100),
        nullable=False
    )

    last_name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(50),
        default="student"
    )


    def set_password(self, password):

        self.password = generate_password_hash(password)


    def check_password(self, password):

        return check_password_hash(
            self.password,
            password
        )


    def to_dict(self):

        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "role": self.role
        }