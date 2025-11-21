DBMS MINI PROJECT
COURSE MANAGEMENT SYSTEM WITH PLACEMENTS & INTERNSHIPS

LIKHITH M IRANI – PES1UG23CS329
LIKHITH U SHETTY - PES1UG23CS331

1. Abstract

This mini-project implements a Course Management System as a database-driven desktop application for managing academic and placement-related data at the department level. The system stores and manages information about departments, students, instructors, courses, classrooms, enrollments, alumni, placements, internships and help resources.

The backend is implemented in MySQL using a well-designed schema with foreign keys, views, stored functions, stored procedures and triggers to maintain data integrity and automate counts. The frontend is built using Python’s Tkinter library, providing tabs for dashboard statistics, student management, course and instructor viewing, enrollments, placements, internships, reports (views) and function testing. Real-time statistics such as course enrollment counts and instructor workload are automatically updated using triggers and are visualized through the GUI.

2. User Requirement Specification
2.1 Purpose

The purpose of the system is to automate manual processes of maintaining student, course, faculty, alumni, internship and placement records in a department. By integrating a relational database with a graphical user interface, the system reduces human error, supports fast querying and ensures referential integrity across all related entities. 

finalcode

2.2 Scope

Supports multiple departments within an institute.

Handles core academic data: students, instructors, courses, classrooms and enrollments.

Extends the scope to alumni, placements and internships to help the department track outcomes.

Provides reports using SQL views (student performance, instructor workload, course enrollment, alumni placements, student internships).

Allows interactive testing of key SQL functions from the UI (e.g., course enrollment count, whether a course is full, total credits of a student).

Can be extended in future to include attendance, marks, web interface, export/import features and authentication.

2.3 Functional Requirements
Functionality	Description
Manage Students	Add new students and view all student records from the GUI.
View Instructors	View instructor details and number of courses taught.
View Courses & Classrooms	View course details, enrolled count and classroom capacity.
Manage Enrollments	Enroll students into courses via a form and view all enrollments.
Placements Module	View placement records for students/alumni with company, role, package.
Internships Module	View internship records for students/alumni with duration, stipend, mode.
Reports (Views)	View data from SQL views (performance, workload, enrollment, outcomes).
Function Testing	Call SQL functions from UI (enrollment count, credits, full course, etc.)
Data Integrity	Enforced through foreign keys, triggers, functions and procedures.

3. Tools and Technologies Used
Component	Technology / Tool
Programming Language	Python 3.10
GUI Framework	Tkinter + ttk (Notebook, Treeview, dialogs)
Database	MySQL 8.10
Python–MySQL Connector	mysql-connector-python
ER / Schema Design	MySQL Workbench / Draw.io
IDE	VS Code / PyCharm
Operating System	Windows / macOS (development and testing)

4. System Design
4.1 ER Diagram (Logical Description)

Entities:
Department, Student, Instructor, Course, Classroom, Enrollment, Teaches, Alumni, Placement, Internship, Placement_Help, Internship_Help. 

finalcode

Main Relationships:

Department → Student (1 : N)

Department → Instructor (1 : N)

Department → Course (1 : N)

Student ↔ Course (M : N via Enrollment)

Instructor ↔ Course (M : N via Teaches)

Course → Classroom (1 : 0/1)

Alumni → Placement (1 : N; also Placement can refer to Student)

Alumni → Internship (1 : N; also Internship can refer to Student)

Placement_Help, Internship_Help are independent resource entities.

This ER structure supports both current students and passed-out alumni, letting the department track academic and career outcomes in a single integrated system. 

finalcode

4.2 Relational Schema

Key relations (simplified from the SQL script): 

finalcode

Department(Department_ID PK, Dept_Name, Location, HOD_Name)

Student(Student_ID PK, Name, Email, Phone, DOB, Year_of_Study, Department_ID FK)

Instructor(Instructor_ID PK, Name, Email, Phone, DOJ, Qualification, Department_ID FK, No_of_Courses_Taught)

Course(Course_ID PK, Course_Name, Credits, Course_Level, No_of_Students_Enrolled, Department_ID FK)

Classroom(Room_ID PK, Location, Capacity, Course_ID FK)

Enrollment(Enrollment_ID PK, Student_ID FK, Course_ID FK, Semester, Grade)

Teaches(Teach_ID PK, Instructor_ID FK, Course_ID FK, Semester, Academic_Year)

Alumni(Alumni_ID PK, Name, Email, Phone, DOB, Graduation_Year, CGPA, Department_ID FK, Notes)

Placement(Placement_ID PK, Student_ID FK NULL, Alumni_ID FK NULL, Company, Role, Package, Offer_Date, On_Campus, Location, Remarks)

Internship(Internship_ID PK, Student_ID FK NULL, Alumni_ID FK NULL, Company, Role, Duration, Stipend, Start_Date, End_Date, Mode, Remarks)

Placement_Help(Help_ID PK, Title, Description, Link, Created_On)

Internship_Help(Help_ID PK, Title, Description, Link, Created_On)

5. DDL and DML Commands
5.1 DDL

All DDL is centralized in finalcode.sql, which: 

finalcode

Drops and recreates the CourseManagement database.

Creates all tables in dependency order (Department → Student/Instructor/Course → Classroom/Enrollment/Teaches → Alumni → Placement/Internship → Help tables).

Defines primary keys, foreign keys and default values.

Example (simplified) DDL:

CREATE TABLE Course (
    Course_ID INT PRIMARY KEY,
    Course_Name VARCHAR(100) NOT NULL,
    Credits INT,
    Course_Level VARCHAR(20),
    No_of_Students_Enrolled INT DEFAULT 0,
    Department_ID INT,
    FOREIGN KEY (Department_ID) REFERENCES Department(Department_ID) ON DELETE SET NULL
);

5.2 DML (Sample CRUD)

Sample inserts (provided in the script) add initial departments, students, instructors, courses, classrooms, enrollments, alumni, placements, internships and help resources for testing. 

finalcode

Examples:

-- Insert a student
INSERT INTO Student (Student_ID, Name, Email, Phone, DOB, Year_of_Study, Department_ID)
VALUES (1007, 'New Student', 'new.student@pes.edu', '9999999999', '2004-02-10', 2, 1);

-- Update a course's credits
UPDATE Course SET Credits = 5 WHERE Course_ID = 3002;

-- Delete an enrollment (triggers will update count)
DELETE FROM Enrollment WHERE Enrollment_ID = 4001;

6. GUI

The GUI is implemented in course_management_gui.py using Tkinter and ttk’s Notebook for multiple tabs. 

course_management_gui

Main Tabs:

Dashboard

Displays total counts of students, instructors, courses and enrollments using colored “cards”.

A “Refresh Statistics” button re-queries the database and updates the cards.

Students

Shows a Treeview of all students with ID, name, email, phone, DOB, year of study and department.

“Add Student” button opens a form to insert a new student record into the database.

“Verify Database” button runs simple checks (total students and last few students) and shows them in a message box.

Instructors

Displays instructor details including No_of_Courses_Taught, which is automatically maintained by triggers when Teaches rows are inserted/deleted.

Courses

Shows courses with credits, level, department, enrolled count and classroom capacity, combining Course and Classroom data.

Enrollments

Lists all enrollments with student name, course name, semester and grade.

“Enroll Student” opens a form to add a new enrollment; the trigger updates No_of_Students_Enrolled in Course.

Placements

Displays placement records with person name (student or alumni), type, company, role, package, offer date and location.

Internships

Displays internship records with person name, type (student/alumni), company, role, duration, stipend, start date and mode.

Reports

Contains sub-tabs for all major SQL views (student performance, instructor workload, course enrollment, alumni placements, student internships).

Functions

Provides input boxes and buttons to call SQL functions like GetCourseEnrollment, IsStudentEnrolled, GetStudentCredits, and IsCourseFull and shows results directly in the UI.

7. Triggers, Procedures and Functions

All advanced DBMS features are defined in finalcode.sql and are actively used by the GUI.

7.1 Triggers

trg_enrollment_insert (AFTER INSERT on Enrollment)

Increments Course.No_of_Students_Enrolled whenever a new enrollment is added.

Used indirectly when the user enrolls a student via the Enrollments tab.

trg_enrollment_delete (AFTER DELETE on Enrollment)

Decrements the student count, ensuring it never goes below 0.

trg_student_before_insert (BEFORE INSERT on Student)

Prevents insertion of a student without a valid Department_ID.

Guarantees that the Students tab will never show “orphan” students.

trg_department_before_delete (BEFORE DELETE on Department)

Blocks deletion of a department if students or instructors still reference it, preventing referential problems.

trg_teaches_insert / trg_teaches_delete (AFTER INSERT/DELETE on Teaches)

Automatically maintain Instructor.No_of_Courses_Taught.

This count is displayed in the Instructors tab without needing manual updates.

7.2 Stored Functions

GetCourseEnrollment(p_Course_ID)

Returns the number of students enrolled in a course (COUNT over Enrollment).

Called from the “Functions” tab to display enrollment count.

IsStudentEnrolled(p_Student_ID, p_Course_ID)

Returns 'YES' or 'NO' depending on whether the student is enrolled in the given course.

Tested interactively from the GUI.

GetStudentCredits(p_Student_ID)

Sums the credits of all courses the student is enrolled in.

Helps quickly check academic load/coursework.

IsCourseFull(p_Course_ID)

Compares number of enrolled students with classroom capacity and returns 'YES', 'NO' or 'UNKNOWN'.

Useful for deciding if more students can be added.

7.3 Stored Procedures

EnrollStudent(p_Student_ID, p_Course_ID, p_Semester, p_Grade)

Checks if the student is already enrolled; if yes, raises an error using SIGNAL.

Otherwise inserts a new row into Enrollment.

UpdateCourseGrades(p_Course_ID, p_Semester, p_New_Grade)

Bulk updates grades for a specific course and semester.

AssignClassroom(p_Course_ID, p_Room_ID)

Assigns a classroom to a course by updating the Classroom table.

AddStudent(p_Name, p_Email, p_Phone, p_DOB, p_Year, p_Department_ID)

Inserts a new student record with given details.

The GUI mainly uses direct INSERT/SELECT statements, but the logic is compatible with these procedures and demonstrates how business logic can be moved to the database layer.

8. Complex Queries

Some example complex queries and how they are used:

Join Queries (Views):

v_student_performance joins Student, Enrollment and Course to show each student’s performance per course and semester.

v_instructor_workload joins Instructor, Teaches and Course and aggregates courses taught using GROUP_CONCAT and COUNT.

v_course_enrollment joins Course, Enrollment and Classroom to show enrolled students vs capacity.

Aggregate Queries:

Counting students per course, total credits per student (GetStudentCredits), number of courses per instructor (No_of_Courses_Taught).

Nested / Conditional Queries:

Functions like IsCourseFull internally compare aggregate enrollment counts with capacity.

Placement and internship queries can filter by graduation year, company, or department to analyze outcomes.

9. List of Functionalities
Functionality	Description
Student Management	View all students; add new students via a form.
Instructor Management	View instructors with qualification, department and courses taught.
Course Management	View courses with credits, level, department, enrolled count and classroom.
Enrollment Management	Enroll students into courses and view all enrollments.
Alumni Management	Store and use alumni data in placements/internships tables.
Placement Tracking	Track company, role, package, location and mode for student/alumni offers.
Internship Tracking	Track duration, stipend, mode and role for internships.
Dashboard Statistics	Show counts of students, instructors, courses and enrollments.
Report Views	Use SQL views to show performance, workload, enrollment and outcomes.
Function Testing	Call SQL functions from the GUI and display results to the user.
Automatic Counts	Use triggers to auto-update student counts per course and courses per instructor.
10. GitHub Repository

GitHub Link (project code and SQL scripts):

https://github.com/LikhithIrani/CourseManagementDBMS

11. Conclusion

This Course Management System mini-project demonstrates how DBMS concepts can be applied to a realistic academic setting. A normalized MySQL schema with foreign keys ensures referential integrity across departments, students, instructors, courses, classrooms, alumni, placements and internships. Triggers, stored procedures and functions encapsulate business rules in the database, while views provide ready-made reports for analysis.

The Python Tkinter GUI connects to this backend and offers a user-friendly interface to view and insert data, visualize statistics and test SQL functions in real time. Future enhancements could include editing and deleting records from the UI, attendance and marks modules, CSV export/import, user authentication and migration to a web framework such as Flask or Django.
