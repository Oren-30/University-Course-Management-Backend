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
        db.String(150),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    credits = db.Column(
        db.Integer,
        nullable=False
    )

    department = db.Column(
        db.String(100),
        nullable=False
    )

    semester = db.Column(
        db.String(20),
        nullable=False
    )

    instructor_id = db.Column(
        db.Integer,
        db.ForeignKey("instructors.id"),
        nullable=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "course_code": self.course_code,
            "course_name": self.course_name,
            "description": self.description,
            "credits": self.credits,
            "department": self.department,
            "semester": self.semester,
            "instructor_id": self.instructor_id
        }