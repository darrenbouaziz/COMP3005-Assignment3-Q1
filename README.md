# COMP 3005 - Assignment 3 Q1

This is a Python program that connects to PostgreSQL and lets you view, add, update, and delete student records.

## Files

- `main.py` - Python program with the four student functions and a menu
- `01_create_students.sql` - SQL script to create the table and insert the three starting students
- `requirements.txt` - Python package needed for the database connection

## Database setup

1. Open PostgreSQL in pgAdmin and create a database named `assignment3`.
2. Select the `assignment3` database and open **Tools > Query Tool**.
3. Run the SQL in `01_create_students.sql`.
4. Check the students table in pgAdmin. It should include John Doe, Jane Smith, and Jim Beam.

The table uses an automatically generated primary key (`student_id`), required first and last names, a unique email, and an enrollment date.

## Running the program

Install Python 3.10 or newer. Open PowerShell in the project folder, then run:

```powershell
py -m pip install -r requirements.txt
```

I used the PostgreSQL database on my course VM. With the Carleton VPN connected, I started an SSH tunnel in a separate PowerShell window:

```powershell
ssh -N -L 127.0.0.1:5433:127.0.0.1:5432 student@<VM_IP_ADDRESS>
```

Replace `<VM_IP_ADDRESS>` with the VM's floating IP and leave that PowerShell window open. The Python program uses `127.0.0.1` and port `5433` by default.

If PostgreSQL is running locally on port `5432`, run this before starting Python:

```powershell
$env:DB_PORT = "5432"
```

Start the program with:

```powershell
py main.py
```

Enter the PostgreSQL password when prompted. The menu has these options:

1. `getAllStudents()` - Displays all students.
2. `addStudent(first_name, last_name, email, enrollment_date)` - Adds a new student.
3. `updateStudentEmail(student_id, new_email)` - Changes a student's email.
4. `deleteStudent(student_id)` - Removes a student by ID.
5. Exit.

## Demo video

[Assignment 3 Q1 demonstration](https://youtu.be/SbVGQabpXFU)
