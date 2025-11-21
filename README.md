📘 Course Management System (DBMS Project)

This project is a Course Management System built using Python (Tkinter UI) and MySQL.
It supports managing students, courses, faculty, enrollments, and includes views, triggers, functions, and stored procedures to make database operations efficient and secure.

🚀 Features
✔ Student Management

Add, view, update, delete student records

Fetch student details using stored procedures

✔ Course Management

Add, update, delete courses

Auto-check course availability with triggers

✔ Faculty Management

Assign courses

Manage relationships between faculty and departments

✔ Enrollment Management

Enroll students into courses

Automatic seat checks using triggers

Views to list enrolled students

✔ MySQL Integration

Uses:

Views for simplified read-only combined data

Triggers for automatic updates

Functions for reusable logic

Stored Procedures for UI operations

✔ Modern UI (Tkinter)

Light/Dark mode support

Clean buttons

Database-connected forms

Error popups

Success notifications

🛠️ Tech Stack
Component	Technology Used
Frontend	Python (Tkinter)
Backend	MySQL 8+
Connector	PyMySQL
Database Logic	Procedures, Functions, Triggers, Views
📂 Project Structure
CourseManagementDBMS/
│── app.py / student_ui.py / course_mgmt_ui.py
│── db/
│   ├── finalcode.sql        # Complete DB schema + triggers + views + procedures
│── assets/
│   ├── icons, images
│── README.md

🧪 Database Objects Used
1️⃣ Views

Used for:

Listing students with course details

Creating complex join results for UI display

Example:

CREATE VIEW student_course_view AS
SELECT s.student_id, s.name, c.course_name
FROM students s
JOIN enrollments e ON s.student_id = e.student_id
JOIN courses c ON e.course_id = c.course_id;

2️⃣ Triggers

Used for:

Auto-updating seat count when student enrolls

Preventing over-enrollment

Logging operations

Example:

CREATE TRIGGER reduce_seat
AFTER INSERT ON enrollments
FOR EACH ROW
UPDATE courses SET seats = seats - 1 WHERE course_id = NEW.course_id;

3️⃣ Functions

Used for validating data before inserting.

Example:

CREATE FUNCTION check_seats(cid INT)
RETURNS INT
RETURN (SELECT seats FROM courses WHERE course_id = cid);

4️⃣ Stored Procedures

Used for:

Adding new student

Editing student info

Inserting course

Registering student into course

Example:

CREATE PROCEDURE add_student(IN sname VARCHAR(50), IN semail VARCHAR(50))
BEGIN
    INSERT INTO students(name, email) VALUES(sname, semail);
END;

▶️ How to Run
1. Install dependencies
pip install pymysql

2. Import the SQL file

Open MySQL Workbench → Import → run finalcode.sql

3. Configure Database in UI

Inside course_mgmt_ui.py:

DB_CONFIG = {
    "host": "localhost",
    "user": "cms_user",
    "password": "YourPassword",
    "database": "cms_db",
}

4. Run the application
python course_mgmt_ui.py

📸 Screenshots

(Add your UI images here)

![Student UI](assets/student_ui.png)
![Course UI](assets/course_ui.png)

👨‍💻 Author

Likhith M Irani
PES University
B.Tech – Computer Science
