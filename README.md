#  Course Management System — DBMS Mini Project (UE23CS351A)

###  PES University, Ring Road Campus  
**Department of Computer Science and Engineering**  
**Course Code:** UE23CS351A — Database Management Systems  

---

##  Overview

The **Course Management System** is a database-driven application developed using **Python (Tkinter)** and **MySQL**.  
It simplifies the management of students, instructors, departments, and courses in an educational environment.  

The system performs **CRUD operations** through a Tkinter GUI and ensures data consistency using SQL **triggers**, **stored procedures**, and **user-defined functions**.

---

##  Features

 CRUD operations for:
- Students  
- Instructors  
- Courses  
- Enrollments  

 Automated data integrity using:
- Triggers for enrollment count updates  
- Validation triggers for student and department insertion  

 Advanced SQL usage:
- Stored Procedures (`EnrollStudent`, `AddStudent`, `GetStudentSemesterReport`)  
- User Defined Functions (`GetCourseEnrollment`, `IsCourseFull`)  
- Views for reporting and analytics  

 GUI Highlights:
- Tkinter-based desktop interface  
- Separate tabs for Students, Instructors, Courses, Enrollments, and Reports  
- Integrated search and refresh options  
- Dynamic report generation through stored procedure calls  

---

##  Tools & Technologies

| Component | Technology |
|------------|-------------|
| Programming Language | Python 3.10 |
| GUI Framework | Tkinter |
| Database | MySQL 8.x |
| Database Connector | PyMySQL |
| Additional Library | Cryptography |
| IDE | VS Code |
| OS | macOS (Apple M3) |

---

##  Database Design

### **Entities**
- Department  
- Student  
- Instructor  
- Course  
- Enrollment  
- Teaches  
- Classroom  

### **Relationships**
- Department → Student (1:N)  
- Department → Instructor (1:N)  
- Department → Course (1:N)  
- Student ↔ Course (M:N via Enrollment)  
- Instructor ↔ Course (M:N via Teaches)  

### **Relational Schema**
```sql
Department(Department_ID PK, Dept_Name, Location, HOD_Name)
Student(Student_ID PK, Name, Email, Phone, DOB, Year_of_Study, Department_ID FK)
Instructor(Instructor_ID PK, Name, Email, Phone, DOJ, Qualification, Department_ID FK, No_of_Courses_Taught)
Course(Course_ID PK, Course_Name, Credits, Course_Level, No_of_Students_Enrolled, Department_ID FK)
Enrollment(Enrollment_ID PK, Student_ID FK, Course_ID FK, Semester, Grade)
Teaches(Teach_ID PK, Instructor_ID FK, Course_ID FK, Semester, Academic_Year)
Classroom(Room_ID PK, Location, Capacity, Course_ID FK)


-----------------------------------------------------------------------------------


Setup Instructions

1. Import Database

Open MySQL and run:
	SOURCE path/to/code.sql;

2. Install Dependencies
	pip install pymysql cryptography
 
3. Configure Database Credentials

Edit the DB_CONFIG section in app.py:
	DB_CONFIG = {
	    "host": "localhost",
	    "user": "appuser",
	    "password": "AppPass123!",
	    "database": "CourseManagement",
	    "port": 3306
	}

4. Run the Application
	python3 app.py

