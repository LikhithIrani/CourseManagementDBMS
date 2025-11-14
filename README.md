🚀 Course Management System — DBMS Mini Project
PES University — Department of Computer Science & Engineering

Course Code: UE23CS351A
Tech Used: Python (Tkinter) + MySQL + PyMySQL

📌 Overview

This mini project implements a complete Course Management System integrating:

A complex MySQL database with 12+ tables

A modern Tkinter GUI (multi-tab interface)

Alumni, Placements & Internships support

Stored Procedures, Views, Triggers, Functions

Full CRUD operations for all entities

Real-time MySQL connectivity using PyMySQL

The system resembles a real university ERP module.

🎯 Key Features
🧑‍🎓 Student Management

Add / View / Update / Delete students

Search student by ID, name, email

Track year of study, department, DOB

👨‍🏫 Instructor Management

Add / Edit faculty profiles

Track qualification, department, phone

Automatically updates No_of_Courses_Taught using SQL triggers

📘 Course & Enrollment Management

Manage courses, credits, level

Assign classrooms & instructors

Enroll students with grade tracking

Automatic No_of_Students_Enrolled update via triggers

🧑‍🎓 Alumni Module (NEW)

Store previous student records

Track CGPA, graduation year, notes

Useful for placement & higher-studies analytics

💼 Placement Module (NEW)

Student or Alumni can have placements

Tracks:
✔ Company
✔ Role
✔ Package (LPA)
✔ Offer Date
✔ On-Campus / Off-Campus
✔ Location
✔ Remarks

💻 Internship Module (NEW)

Internship details for Students or Alumni

Tracks duration, stipend, period, mode, company

Research or corporate internships supported

🆘 Placement & Internship Help (NEW)

Inbuilt help resources directly in UI

Roadmaps, resume tips, application guidance etc.

📊 Reports & Views (NEW)

Student performance view

Instructor workload view

Course enrollment analytics view

Alumni placement history

Student internship history

All views accessible directly from UI.

🏛️ Database Design
🧱 Tables Included

Department

Student

Instructor

Course

Enrollment

Teaches

Classroom

Alumni (NEW)

Placement (NEW)

Internship (NEW)

Placement_Help (NEW)

Internship_Help (NEW)

🧩 Advanced SQL Used
Functions:

GetCourseEnrollment()

IsStudentEnrolled()

GetStudentCredits()

IsCourseFull()

Procedures:

AddStudent()

EnrollStudent()

AssignClassroom()

UpdateCourseGrades()

Triggers:

Auto-increment course student count

Prevent delete when department has members

Instructor teaches count update triggers

Views:

v_student_performance

v_instructor_workload

v_course_enrollment

v_alumni_placements

v_student_internships

⚙️ Setup Instructions
1️⃣ Install Required Python Packages
pip install pymysql
pip install cryptography

2️⃣ Import the Database

If you're in terminal:

mysql -u root -p < finalcode.sql


Or open MySQL Workbench → Run entire finalcode.sql file.

3️⃣ Configure the Application

Open course_mgmt_ui.py and set:

DB_BACKEND = "mysql"
MYSQL_CONFIG = {
    "host": "127.0.0.1",
    "user": "cms_user",
    "password": "My$qlStrong2025!",  # Change to your actual password
    "db": "CourseManagement",
    "port": 3306
}

4️⃣ Run the Application
python3 course_mgmt_ui.py


Tkinter UI will launch with all database features enabled.

🖥️ UI Features

✔ Multi-tab layout (Students, Courses, Faculty, Alumni, Placements, Internships, Help)
✔ Modern Tkinter widgets (Treeview tables)
✔ Add / Update / Delete with popups
✔ MySQL connection status indicator
✔ Auto-refresh tables on operation
✔ Built-in Help Section (Placement/Internship)

📂 Repository Structure
CourseManagementDBMS/
│
├── finalcode.sql               # Full database schema + inserts
├── course_mgmt_ui.py           # Tkinter UI (MySQL-connected)
├── README.md                   # Project documentation
└── (optional screenshots)

🏁 Conclusion

This project demonstrates full-stack database application development using:

✔ MySQL (Advanced SQL)
✔ Python (Tkinter GUI)
✔ PyMySQL (DB connector)
✔ Real-world modules: Students, Faculty, Alumni, Placements & Internships
