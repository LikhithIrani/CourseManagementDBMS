# Course Management System - Python GUI (Tkinter)

A comprehensive desktop application for managing course information, students, instructors, enrollments, and more using Python Tkinter and MySQL.

## Features

- 📊 **Dashboard**: Statistics overview of students, instructors, courses, and enrollments
- 👥 **Student Management**: Add and view students with full information
- 🎓 **Instructor Management**: View instructor details and workload
- 📚 **Course Management**: View all courses with enrollment and capacity information
- ✅ **Enrollment Management**: Enroll students in courses (uses `EnrollStudent` procedure)
- 💼 **Placement Tracking**: View student and alumni placements
- 🏢 **Internship Tracking**: Track student and alumni internships
- 📈 **Reports & Views**: Access all database views:
  - Student Performance
  - Instructor Workload
  - Course Enrollment
  - Alumni Placements
  - Student Internships
- 🔧 **SQL Functions**: Test all database functions:
  - `GetCourseEnrollment(course_id)` - Get enrollment count for a course
  - `IsStudentEnrolled(student_id, course_id)` - Check if student is enrolled
  - `GetStudentCredits(student_id)` - Get total credits for a student
  - `IsCourseFull(course_id)` - Check if course is at capacity

## Prerequisites

- Python 3.7 or higher
- MySQL 8.0 or higher
- Tkinter (usually included with Python)

## Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd DBMS_MINIPROJECT1
   ```

2. **Install required Python packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the MySQL database**
   - Open MySQL and run the `finalcode.sql` file:
   ```bash
   mysql -u root -p < finalcode.sql
   ```
   Or manually execute the SQL file in your MySQL client.

4. **Configure database connection**
   - Open `course_management_gui.py`
   - Update the database configuration (lines 18-24) with your MySQL credentials:
   ```python
   self.db_config = {
       'host': 'localhost',
       'user': 'root',
       'password': 'your_password',  # Update this
       'database': 'CourseManagement'
   }
   ```

## Running the Application

1. **Run the Python script**
   ```bash
   python course_management_gui.py
   ```
   
   Or on some systems:
   ```bash
   python3 course_management_gui.py
   ```

2. **The GUI window will open** with tabs for different sections

## Application Structure

The application has the following tabs:

1. **Dashboard**: Overview statistics
2. **Students**: View and add students
3. **Instructors**: View instructor information
4. **Courses**: View all courses
5. **Enrollments**: View and create enrollments
6. **Placements**: View placement records
7. **Internships**: View internship records
8. **Reports**: Access all database views
9. **Functions**: Test SQL functions

## Using the Application

### Adding a Student

1. Go to the **Students** tab
2. Click **Add Student** button
3. Fill in the required fields:
   - Student ID (must be unique)
   - Name
   - Email (optional)
   - Phone (optional)
   - Date of Birth (optional, format: YYYY-MM-DD)
   - Year of Study (1-4)
   - Department (select from dropdown)
4. Click **Add Student**
5. The student will be added using the `AddStudent` procedure (or direct insert with Student_ID)

### Enrolling a Student

1. Go to the **Enrollments** tab
2. Click **Enroll Student** button
3. Fill in the required fields:
   - Enrollment ID
   - Select Student from dropdown
   - Select Course from dropdown
   - Enter Semester
   - Enter Grade (optional)
4. Click **Enroll Student**
5. The enrollment will use the `EnrollStudent` procedure
6. Triggers will automatically update the course enrollment count

### Using SQL Functions

1. Go to the **Functions** tab
2. Enter the required IDs in the function sections
3. Click the respective button to execute the function
4. Results will be displayed in the result label

### Viewing Reports

1. Go to the **Reports** tab
2. Select a sub-tab for the view you want to see:
   - Student Performance
   - Instructor Workload
   - Course Enrollment
   - Alumni Placements
   - Student Internships
3. The data will be displayed in a table format

## Active Triggers

The following triggers from your SQL file are active and will execute automatically:

1. **trg_enrollment_insert**: Updates `No_of_Students_Enrolled` when a student enrolls
2. **trg_enrollment_delete**: Decreases `No_of_Students_Enrolled` when enrollment is deleted
3. **trg_student_before_insert**: Validates that `Department_ID` is not NULL
4. **trg_teaches_insert**: Updates `No_of_Courses_Taught` when an instructor is assigned
5. **trg_teaches_delete**: Decreases `No_of_Courses_Taught` when assignment is removed

## Active Procedures

The following stored procedures can be used:

1. **EnrollStudent**: Enrolled via direct insert (procedure doesn't accept Enrollment_ID)
2. **UpdateCourseGrades**: Update grades for all students in a course/semester
3. **AssignClassroom**: Assign a classroom to a course
4. **AddStudent**: Add a new student (used when Student_ID is not provided)

## Troubleshooting

**Database Connection Error:**
- Verify MySQL is running
- Check database credentials in `course_management_gui.py`
- Ensure the `CourseManagement` database exists

**Import Error for mysql-connector-python:**
- Run: `pip install mysql-connector-python`
- Or: `pip3 install mysql-connector-python`

**Tkinter Import Error:**
- On Ubuntu/Debian: `sudo apt-get install python3-tk`
- On macOS: Usually included with Python
- On Windows: Usually included with Python

**Procedure/Trigger Not Working:**
- Ensure `finalcode.sql` was executed completely
- Check MySQL error logs
- Verify the database contains all triggers and procedures

## Notes

- All database operations use prepared statements for security
- The application maintains a persistent database connection
- Triggers execute automatically when data is inserted/updated/deleted
- Views are read-only and show real-time data from the database

## License

This project is for educational purposes.


