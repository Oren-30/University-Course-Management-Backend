from extensions import db


class Enrollment(db.Model):
    __tablename__ = "enrollments"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("courses.id"),
        nullable=False
    )

    semester = db.Column(
        db.String(20),
        nullable=False
    )

    academic_year = db.Column(
        db.String(20),
        nullable=False
    )

    enrollment_date = db.Column(
        db.Date,
        nullable=False,
        server_default=db.func.current_date()
    )

    grade = db.Column(
        db.String(2)
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="Active"
    )

    # Relationships
    student = db.relationship(
        "Student",
        back_populates="enrollments"
    )

    course = db.relationship(
        "Course",
        back_populates="enrollments"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "course_id": self.course_id,
            "semester": self.semester,
            "academic_year": self.academic_year,
            "enrollment_date": (
                self.enrollment_date.isoformat()
                if self.enrollment_date else None
            ),
            "grade": self.grade,
            "status": self.status
        }

    def __repr__(self):
        return (
            f"<Enrollment Student:{self.student_id} "
            f"Course:{self.course_id}>"
        )