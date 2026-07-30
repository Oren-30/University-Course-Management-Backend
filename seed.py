from app import app
from extensions import db, bcrypt

from models.user import User
from models.student import Student
from models.instructor import Instructor
from models.course import Course
from models.enrollment import Enrollment


with app.app_context():
    print("Dropping existing tables...")
    db.drop_all()

    print("Creating tables...")
    db.create_all()

    # -------------------------
    # Users
    # -------------------------
    admin = User(
        first_name="Admin",
        last_name="User",
        email="admin@universitycms.com",
        role="admin",
        password=bcrypt.generate_password_hash("admin123").decode("utf-8")
    )

    lecturer = User(
        first_name="John",
        last_name="Kamau",
        email="john@universitycms.com",
        role="instructor",
        password=bcrypt.generate_password_hash("password123").decode("utf-8")
    )

    student_user = User(
        first_name="Jane",
        last_name="Achieng",
        email="jane@universitycms.com",
        role="student",
        password=bcrypt.generate_password_hash("password123").decode("utf-8")
    )

    db.session.add_all([admin, lecturer, student_user])
    db.session.commit()

    # -------------------------
    # Instructor
    # -------------------------
    instructor = Instructor(
        first_name="John",
        last_name="Kamau",
        email="john@universitycms.com",
        department="Computer Science"
    )

    db.session.add(instructor)
    db.session.commit()

    # -------------------------
    # Students
    # -------------------------
    student1 = Student(
        first_name="Jane",
        last_name="Achieng",
        email="jane@universitycms.com",
        student_number="ST001",
        department="Computer Science",
        program="BSc Computer Science",
        year_of_study=2
    )

    student2 = Student(
        first_name="Peter",
        last_name="Otieno",
        email="peter@universitycms.com",
        student_number="ST002",
        department="Information Technology",
        program="BSc Information Technology",
        year_of_study=3
    )

    db.session.add_all([student1, student2])
    db.session.commit()

    # -------------------------
    # Courses
    # -------------------------
    course1 = Course(
        code="CS101",
        title="Introduction to Programming",
        description="Learn Python programming.",
        credits=3,
        instructor_id=instructor.id
    )

    course2 = Course(
        code="CS201",
        title="Database Systems",
        description="Introduction to SQL and databases.",
        credits=3,
        instructor_id=instructor.id
    )

    db.session.add_all([course1, course2])
    db.session.commit()

    # -------------------------
    # Enrollments
    # -------------------------
    enrollment1 = Enrollment(
        student_id=student1.id,
        course_id=course1.id
    )

    enrollment2 = Enrollment(
        student_id=student1.id,
        course_id=course2.id
    )

    enrollment3 = Enrollment(
        student_id=student2.id,
        course_id=course1.id
    )

    db.session.add_all([enrollment1, enrollment2, enrollment3])
    db.session.commit()

    print("Database seeded successfully!")