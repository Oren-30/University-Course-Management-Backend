from datetime import date

from app import app
from extensions import db

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
        role="admin"
    )
    admin.set_password("admin123")

    lecturer = User(
        first_name="John",
        last_name="Kamau",
        email="john@universitycms.com",
        role="instructor"
    )
    lecturer.set_password("password123")

    student_user = User(
        first_name="Jane",
        last_name="Achieng",
        email="jane@universitycms.com",
        role="student"
    )
    student_user.set_password("password123")

    db.session.add_all([admin, lecturer, student_user])
    db.session.commit()

    # -------------------------
    # Instructor
    # -------------------------
    instructor = Instructor(
        first_name="John",
        last_name="Kamau",
        email="john.lecturer@universitycms.com",
        phone="+254700123456",
        department="Computer Science",
        office="Block A - Room 203"
    )

    db.session.add(instructor)
    db.session.commit()

    # -------------------------
    # Students
    # -------------------------
    student1 = Student(
        first_name="Jane",
        last_name="Achieng",
        email="jane.student@universitycms.com",
        student_number="ST001",
        department="Computer Science",
        program="BSc Computer Science",
        year_of_study=2
    )

    student2 = Student(
        first_name="Peter",
        last_name="Otieno",
        email="peter.student@universitycms.com",
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
        course_code="CS101",
        course_name="Introduction to Programming",
        description="Learn Python programming.",
        credits=3,
        department="Computer Science",
        semester="Semester 1",
        instructor_id=instructor.id
    )

    course2 = Course(
        course_code="CS201",
        course_name="Database Systems",
        description="Introduction to SQL and Database Design.",
        credits=3,
        department="Computer Science",
        semester="Semester 2",
        instructor_id=instructor.id
    )

    db.session.add_all([course1, course2])
    db.session.commit()

    # -------------------------
    # Enrollments
    # -------------------------
    enrollment1 = Enrollment(
        student_id=student1.id,
        course_id=course1.id,
        enrollment_date=date.today(),
        status="Active",
        grade=None
    )

    enrollment2 = Enrollment(
        student_id=student1.id,
        course_id=course2.id,
        enrollment_date=date.today(),
        status="Active",
        grade=None
    )

    enrollment3 = Enrollment(
        student_id=student2.id,
        course_id=course1.id,
        enrollment_date=date.today(),
        status="Active",
        grade=None
    )

    db.session.add_all([enrollment1, enrollment2, enrollment3])
    db.session.commit()

    print("=" * 50)
    print("Database seeded successfully!")
    print("=" * 50)
    print("Users: 3")
    print("Instructor: 1")
    print("Students: 2")
    print("Courses: 2")
    print("Enrollments: 3")