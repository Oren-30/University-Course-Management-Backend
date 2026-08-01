from extensions import db


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
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

    user = db.relationship(
        "User",
        back_populates="student"
    )

    enrollments = db.relationship(
        "Enrollment",
        back_populates="student",
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "student_number": self.student_number,
            "department": self.department,
            "program": self.program,
            "year_of_study": self.year_of_study,
            "user": {
                "id": self.user.id,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
                "email": self.user.email,
                "role": self.user.role
            } if self.user else None
        }