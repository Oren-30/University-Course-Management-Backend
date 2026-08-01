from extensions import db


class Instructor(db.Model):
    __tablename__ = "instructors"

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

    staff_number = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    department = db.Column(
        db.String(100),
        nullable=False
    )

    specialization = db.Column(
        db.String(100),
        nullable=False
    )

    office = db.Column(
        db.String(100)
    )

    phone = db.Column(
        db.String(20)
    )

    # Relationship with User
    user = db.relationship(
        "User",
        back_populates="instructor"
    )

    # Relationship with Course
    courses = db.relationship(
        "Course",
        back_populates="instructor",
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "staff_number": self.staff_number,
            "department": self.department,
            "specialization": self.specialization,
            "office": self.office,
            "phone": self.phone,
            "user": {
                "id": self.user.id,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
                "email": self.user.email,
                "role": self.user.role
            } if self.user else None
        }

    def __repr__(self):
        return f"<Instructor {self.staff_number}>"