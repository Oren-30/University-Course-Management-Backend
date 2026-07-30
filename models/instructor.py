from extensions import db


class Instructor(db.Model):

    __tablename__ = "instructors"

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

    phone = db.Column(
        db.String(20),
        nullable=True
    )

    department = db.Column(
        db.String(100),
        nullable=False
    )

    office = db.Column(
        db.String(100),
        nullable=True
    )

    courses = db.relationship(
        "Course",
        backref="instructor",
        lazy=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "department": self.department,
            "office": self.office
        }