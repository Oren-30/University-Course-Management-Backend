from extensions import db


class Enrollment(db.Model):

    __tablename__ = "enrollments"

    id = db.Column(db.Integer, primary_key=True)

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

    enrollment_date = db.Column(
        db.Date,
        nullable=False
    )

    status = db.Column(
        db.String(50),
        default="Active"
    )

    grade = db.Column(
        db.String(5),
        nullable=True
    )

    course = db.relationship(
        "Course",
        backref=db.backref("enrollments", lazy=True)
    )

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "course_id": self.course_id,
            "enrollment_date": self.enrollment_date.isoformat() if self.enrollment_date else None,
            "status": self.status,
            "grade": self.grade
        }