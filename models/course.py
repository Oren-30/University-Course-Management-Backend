from extensions import db


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    course_code = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    course_name = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.Text
    )

    credits = db.Column(
        db.Integer,
        nullable=False
    )

    instructor_id = db.Column(
        db.Integer,
        db.ForeignKey("instructors.id"),
        nullable=False
    )

    instructor = db.relationship(
        "Instructor",
        back_populates="courses"
    )

    enrollments = db.relationship(
        "Enrollment",
        back_populates="course",
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "course_code": self.course_code,
            "course_name": self.course_name,
            "description": self.description,
            "credits": self.credits,
            "instructor_id": self.instructor_id
        }

    def __repr__(self):
        return f"<Course {self.course_code}>"