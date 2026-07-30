from extensions import db


class Student(db.Model):

    __tablename__ = "students"

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

    student_number = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    department = db.Column(
        db.String(100),
        nullable=False
    )

    program = db.Column(
        db.String(100),
        nullable=False
    )

    year_of_study = db.Column(
        db.Integer,
        nullable=False
    )

    enrollments = db.relationship(
        "Enrollment",
        backref="student",
        lazy=True,
        cascade="all, delete-orphan"
    )
