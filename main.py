"""Student database program for COMP 3005 Assignment 3."""

from datetime import date
from getpass import getpass
import os

import psycopg

# The default port is for the SSH tunnel; local PostgreSQL usually uses 5432.
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", "5433")),
    "dbname": os.getenv("DB_NAME", "assignment3"),
    "user": os.getenv("DB_USER", "postgres"),
    "connect_timeout": 10,
}
DB_PASSWORD = ""


def connect():
    """Open one PostgreSQL connection using the current configuration."""
    return psycopg.connect(**DB_CONFIG, password=DB_PASSWORD)


def getAllStudents():
    """READ: fetch and print every student, ordered by student_id."""
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT student_id, first_name, last_name, email, enrollment_date "
                "FROM students ORDER BY student_id"
            )
            students = cur.fetchall()

    print("\nSTUDENTS TABLE")
    print("-" * 96)
    print(f"{'ID':<6}{'First':<16}{'Last':<16}{'Email':<34}{'Enrollment date'}")
    print("-" * 96)
    for student_id, first_name, last_name, email, enrollment_date in students:
        print(f"{student_id:<6}{first_name:<16}{last_name:<16}{email:<34}{enrollment_date or ''}")
    if not students:
        print("(No students found)")
    print(f"Total: {len(students)} student(s)\n")
    return students


def addStudent(first_name, last_name, email, enrollment_date):
    """CREATE: insert a new student and return its generated primary key."""
    first_name = first_name.strip()
    last_name = last_name.strip()
    email = email.strip()
    if not all((first_name, last_name, email)):
        raise ValueError("First name, last name, and email cannot be empty.")
    if "@" not in email or email.startswith("@") or email.endswith("@"):
        raise ValueError("Email must contain a name and @domain.")
    if isinstance(enrollment_date, str):
        enrollment_date = (date.fromisoformat(enrollment_date.strip())
                           if enrollment_date.strip() else None)
    if enrollment_date is not None and not isinstance(enrollment_date, date):
        raise ValueError("Date must be YYYY-MM-DD or blank.")

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO students (first_name, last_name, email, enrollment_date) "
                "VALUES (%s, %s, %s, %s) RETURNING student_id",
                (first_name, last_name, email, enrollment_date),
            )
            new_id = cur.fetchone()[0]
    print(f"Student added successfully. New student_id: {new_id}")
    return new_id


def updateStudentEmail(student_id, new_email):
    """UPDATE: change the email for the specified student_id."""
    if student_id <= 0:
        raise ValueError("Student ID must be a positive integer.")
    new_email = new_email.strip()
    if "@" not in new_email or new_email.startswith("@") or new_email.endswith("@"):
        raise ValueError("Enter a valid-looking email address.")
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE students SET email = %s WHERE student_id = %s "
                "RETURNING student_id",
                (new_email, student_id),
            )
            row = cur.fetchone()
    if row is None:
        print(f"No student with student_id={student_id} was found.")
        return False
    print(f"Email updated for student_id={student_id}: {new_email}")
    return True


def deleteStudent(student_id):
    """DELETE: remove one student record using its student_id."""
    if student_id <= 0:
        raise ValueError("Student ID must be a positive integer.")
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM students WHERE student_id = %s RETURNING student_id",
                (student_id,),
            )
            row = cur.fetchone()
    if row is None:
        print(f"No student with student_id={student_id} was found.")
        return False
    print(f"Student deleted successfully: student_id={student_id}")
    return True


def ask_student_id():
    """Read a positive integer primary key from the keyboard."""
    student_id = int(input("Student ID: ").strip())
    if student_id <= 0:
        raise ValueError("Student ID must be positive.")
    return student_id


def main():
    """Command-line menu to demonstrate all required database operations."""
    global DB_PASSWORD
    DB_PASSWORD = getpass("PostgreSQL password (typing hidden): ")
    if not DB_PASSWORD:
        print("A database password is required.")
        return

    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT to_regclass('public.students')")
                if cur.fetchone()[0] is None:
                    print("students table not found. Run database/01_create_students.sql first.")
                    return
    except psycopg.Error as exc:
        print(f"Could not connect to PostgreSQL: {exc}")
        print("Check the SSH tunnel, database name, username, and password.")
        return

    print("Connected to the assignment3 database!")
    while True:
        print("\n=== STUDENTS CRUD MENU ===")
        print("1. getAllStudents() — view all students")
        print("2. addStudent() — add a student")
        print("3. updateStudentEmail() — change an email")
        print("4. deleteStudent() — delete a student")
        print("5. Exit")
        choice = input("Enter choice (1–5): ").strip()
        try:
            if choice == "1":
                getAllStudents()
            elif choice == "2":
                addStudent(
                    input("First name: "),
                    input("Last name: "),
                    input("Email: "),
                    input("Enrollment date YYYY-MM-DD (or blank): "),
                )
            elif choice == "3":
                updateStudentEmail(ask_student_id(), input("New email: "))
            elif choice == "4":
                deleteStudent(ask_student_id())
            elif choice == "5":
                print("Goodbye!")
                return
            else:
                print("Choose 1, 2, 3, 4, or 5.")
        except ValueError as exc:
            print(f"Input error: {exc}")
        except psycopg.errors.UniqueViolation:
            print("Database error: that email already exists. Emails must be unique.")
        except psycopg.Error as exc:
            print(f"PostgreSQL error: {exc}")


if __name__ == "__main__":
    main()
