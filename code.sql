-- ===========================================
-- DATABASE CREATION
-- ===========================================
CREATE DATABASE CourseManagement;
USE CourseManagement;

-- ===========================================
-- TABLE CREATION
-- ===========================================

-- DEPARTMENT
CREATE TABLE Department (
    Department_ID INT PRIMARY KEY,
    Dept_Name VARCHAR(100) NOT NULL,
    Location VARCHAR(100),
    HOD_Name VARCHAR(100)
);

-- STUDENT
CREATE TABLE Student (
    Student_ID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE,
    Phone VARCHAR(15),
    DOB DATE,
    Year_of_Study INT,
    Department_ID INT,
    FOREIGN KEY (Department_ID) REFERENCES Department(Department_ID)
        ON DELETE SET NULL
);

-- INSTRUCTOR
CREATE TABLE Instructor (
    Instructor_ID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE,
    Phone VARCHAR(15),
    DOJ DATE,
    Qualification VARCHAR(100),
    Department_ID INT,
    FOREIGN KEY (Department_ID) REFERENCES Department(Department_ID)
        ON DELETE SET NULL
);

-- COURSE
CREATE TABLE Course (
    Course_ID INT PRIMARY KEY,
    Course_Name VARCHAR(100) NOT NULL,
    Credits INT,
    Course_Level VARCHAR(20), -- UG / PG
    No_of_Students_Enrolled INT DEFAULT 0,
    Department_ID INT,
    FOREIGN KEY (Department_ID) REFERENCES Department(Department_ID)
        ON DELETE SET NULL
);

-- ENROLLMENT (Associative Entity)
CREATE TABLE Enrollment (
    Enrollment_ID INT PRIMARY KEY,
    Student_ID INT,
    Course_ID INT,
    Semester VARCHAR(20),
    Grade VARCHAR(5),
    FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID)
        ON DELETE CASCADE,
    FOREIGN KEY (Course_ID) REFERENCES Course(Course_ID)
        ON DELETE CASCADE
);

-- TEACHES (Associative Entity)
CREATE TABLE Teaches (
    Teach_ID INT PRIMARY KEY,
    Instructor_ID INT,
    Course_ID INT,
    Semester VARCHAR(20),
    Academic_Year VARCHAR(10),
    FOREIGN KEY (Instructor_ID) REFERENCES Instructor(Instructor_ID)
        ON DELETE CASCADE,
    FOREIGN KEY (Course_ID) REFERENCES Course(Course_ID)
        ON DELETE CASCADE
);

-- CLASSROOM
CREATE TABLE Classroom (
    Room_ID INT PRIMARY KEY,
    Location VARCHAR(100),
    Capacity INT,
    Course_ID INT,
    FOREIGN KEY (Course_ID) REFERENCES Course(Course_ID)
        ON DELETE CASCADE
);


-- ===========================================
-- INSERT DATA
-- ===========================================

-- Departments
INSERT INTO Department (Department_ID, Dept_Name, Location, HOD_Name) VALUES
(1, 'Computer Science', 'Block A', 'Dr. Sharma'),
(2, 'Electronics', 'Block B', 'Dr. Rao'),
(3, 'Mechanical', 'Block C', 'Dr. Verma');

-- Students
INSERT INTO Student (Student_ID, Name, Email, Phone, DOB, Year_of_Study, Department_ID) VALUES
(101, 'Alice', 'alice@uni.edu', '9876543210', '2003-05-12', 2, 1),
(102, 'Bob', 'bob@uni.edu', '9123456789', '2002-10-20', 3, 2),
(103, 'Charlie', 'charlie@uni.edu', '9012345678', '2004-02-28', 1, 1),
(104, 'Diana', 'diana@uni.edu', '9234567890', '2003-09-15', 2, 2),
(105, 'Ethan', 'ethan@uni.edu', '9345678901', '2002-12-05', 4, 3),
(106, 'Fiona', 'fiona@uni.edu', '9456789012', '2003-07-22', 3, 3);

-- Instructors
INSERT INTO Instructor (Instructor_ID, Name, Email, Phone, DOJ, Qualification, Department_ID) VALUES
(201, 'Dr. Mehta', 'mehta@uni.edu', '9988776655', '2015-07-01', 'PhD CSE', 1),
(202, 'Dr. Iyer', 'iyer@uni.edu', '8877665544', '2012-08-15', 'PhD ECE', 2),
(203, 'Dr. Kapoor', 'kapoor@uni.edu', '9765432109', '2018-01-12', 'PhD CSE', 1),
(204, 'Dr. Nair', 'nair@uni.edu', '9654321098', '2016-03-23', 'PhD ECE', 2),
(205, 'Dr. Gupta', 'gupta@uni.edu', '9543210987', '2014-05-18', 'PhD ME', 3),
(206, 'Dr. Chawla', 'chawla@uni.edu', '9432109876', '2010-11-30', 'PhD CE', 3);

-- Courses
INSERT INTO Course (Course_ID, Course_Name, Credits, Course_Level, No_of_Students_Enrolled, Department_ID) VALUES
(301, 'Database Systems', 4, 'UG', 0, 1),
(302, 'Digital Circuits', 3, 'UG', 0, 2),
(303, 'Operating Systems', 4, 'UG', 0, 1),
(304, 'Signals and Systems', 3, 'UG', 0, 2),
(305, 'Thermodynamics', 3, 'UG', 0, 3),
(306, 'Structural Analysis', 4, 'UG', 0, 3);

-- Enrollment
INSERT INTO Enrollment (Enrollment_ID, Student_ID, Course_ID, Semester, Grade) VALUES
(401, 101, 301, 'Sem 4', 'A'),
(402, 102, 302, 'Sem 6', 'B'),
(403, 103, 301, 'Sem 2', 'B'),
(404, 104, 302, 'Sem 4', 'A'),
(405, 105, 305, 'Sem 8', 'A'),
(406, 106, 306, 'Sem 6', 'B');

-- Teaches
INSERT INTO Teaches (Teach_ID, Instructor_ID, Course_ID, Semester, Academic_Year) VALUES
(501, 201, 301, 'Sem 4', '2025'),
(502, 202, 302, 'Sem 6', '2025'),
(503, 203, 303, 'Sem 4', '2025'),
(504, 204, 304, 'Sem 6', '2025'),
(505, 205, 305, 'Sem 8', '2025'),
(506, 206, 306, 'Sem 6', '2025');

-- Classrooms
INSERT INTO Classroom (Room_ID, Location, Capacity, Course_ID) VALUES
(601, 'Room 101', 60, 301),
(602, 'Room 202', 50, 302),
(603, 'Room 103', 70, 303),
(604, 'Room 204', 60, 304),
(605, 'Room 305', 80, 305),
(606, 'Room 406', 55, 306);

-- ===========================================
-- UPDATE STATEMENTS
-- ===========================================
UPDATE Student SET Phone = '9000000000' WHERE Student_ID = 101;
UPDATE Instructor SET Qualification = 'PhD in Data Science' WHERE Instructor_ID = 201;
UPDATE Course SET Credits = 5 WHERE Course_ID = 301;
UPDATE Department SET HOD_Name = 'Dr. Menon' WHERE Department_ID = 2;
UPDATE Enrollment SET Grade = 'A+' WHERE Enrollment_ID = 402;
UPDATE Classroom SET Capacity = 75 WHERE Room_ID = 603;

-- ===========================================
-- DELETE STATEMENTS
-- ===========================================
DELETE FROM Student WHERE Student_ID = 106;
DELETE FROM Instructor WHERE Instructor_ID = 206;
DELETE FROM Course WHERE Course_ID = 306;
DELETE FROM Enrollment WHERE Enrollment_ID = 406;
DELETE FROM Teaches WHERE Teach_ID = 506;
DELETE FROM Classroom WHERE Room_ID = 606;

-- ===========================================
-- TRIGGERS
-- ===========================================
-- Auto-update No_of_Students_Enrolled
DELIMITER $$
CREATE TRIGGER trg_enrollment_insert
AFTER INSERT ON Enrollment
FOR EACH ROW
BEGIN
    UPDATE Course
    SET No_of_Students_Enrolled = No_of_Students_Enrolled + 1
    WHERE Course_ID = NEW.Course_ID;
END$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER trg_enrollment_delete
AFTER DELETE ON Enrollment
FOR EACH ROW
BEGIN
    UPDATE Course
    SET No_of_Students_Enrolled = No_of_Students_Enrolled - 1
    WHERE Course_ID = OLD.Course_ID;
END$$
DELIMITER ;

-- Prevent student insert without Department
DELIMITER $$
CREATE TRIGGER trg_student_before_insert
BEFORE INSERT ON Student
FOR EACH ROW
BEGIN
    IF NEW.Department_ID IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Department_ID cannot be NULL';
    END IF;
END$$
DELIMITER ;

-- ===========================================
-- STORED PROCEDURES
-- ===========================================
-- Add a new student
DELIMITER $$
CREATE PROCEDURE AddStudent(
    IN p_Name VARCHAR(100),
    IN p_Email VARCHAR(100),
    IN p_Phone VARCHAR(15),
    IN p_DOB DATE,
    IN p_Year INT,
    IN p_Department_ID INT
)
BEGIN
    INSERT INTO Student(Name, Email, Phone, DOB, Year_of_Study, Department_ID)
    VALUES (p_Name, p_Email, p_Phone, p_DOB, p_Year, p_Department_ID);
END$$
DELIMITER ;

-- Update instructor's department
DELIMITER $$
CREATE PROCEDURE UpdateInstructorDept(
    IN p_Instructor_ID INT,
    IN p_NewDept_ID INT
)
BEGIN
    UPDATE Instructor
    SET Department_ID = p_NewDept_ID
    WHERE Instructor_ID = p_Instructor_ID;
END$$
DELIMITER ;

-- ===========================================
-- USER-DEFINED FUNCTIONS
-- ===========================================
-- Get total students in a course
DELIMITER $$
CREATE FUNCTION GetCourseEnrollment(p_Course_ID INT)
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE total INT;
    SELECT COUNT(*) INTO total
    FROM Enrollment
    WHERE Course_ID = p_Course_ID;
    RETURN total;
END$$
DELIMITER ;

-- Check if a student is enrolled in a course
DELIMITER $$
CREATE FUNCTION IsStudentEnrolled(p_Student_ID INT, p_Course_ID INT)
RETURNS VARCHAR(3)
DETERMINISTIC
BEGIN
    DECLARE enrolled VARCHAR(3);
    IF EXISTS (
        SELECT 1 FROM Enrollment
        WHERE Student_ID = p_Student_ID AND Course_ID = p_Course_ID
    ) THEN
        SET enrolled = 'YES';
    ELSE
        SET enrolled = 'NO';
    END IF;
    RETURN enrolled;
END$$
DELIMITER ;

-- ===========================================
-- VIEW TABLE DATA
-- ===========================================
SELECT * FROM Department;
SELECT * FROM Student;
SELECT * FROM Instructor;
SELECT * FROM Course;
SELECT * FROM Enrollment;
SELECT * FROM Teaches;
SELECT * FROM Classroom;

-- ===========================================
-- COMPLEX STORED PROCEDURES
-- ===========================================

-- Procedure to enroll a student in a course
DELIMITER $$
CREATE PROCEDURE EnrollStudent(
    IN p_Student_ID INT,
    IN p_Course_ID INT,
    IN p_Semester VARCHAR(20),
    IN p_Grade VARCHAR(5)
)
BEGIN
    -- Check if student is already enrolled
    IF EXISTS (
        SELECT 1 FROM Enrollment
        WHERE Student_ID = p_Student_ID AND Course_ID = p_Course_ID
    ) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Student already enrolled in this course';
    ELSE
        INSERT INTO Enrollment(Student_ID, Course_ID, Semester, Grade)
        VALUES (p_Student_ID, p_Course_ID, p_Semester, p_Grade);
    END IF;
END$$
DELIMITER ;

-- Procedure to generate student report for a semester
DELIMITER $$
CREATE PROCEDURE GetStudentSemesterReport(
    IN p_Student_ID INT,
    IN p_Semester VARCHAR(20)
)
BEGIN
    SELECT c.Course_Name, e.Grade, i.Name AS Instructor_Name
    FROM Enrollment e
    JOIN Course c ON e.Course_ID = c.Course_ID
    LEFT JOIN Teaches t ON c.Course_ID = t.Course_ID AND t.Semester = e.Semester
    LEFT JOIN Instructor i ON t.Instructor_ID = i.Instructor_ID
    WHERE e.Student_ID = p_Student_ID AND e.Semester = p_Semester;
END$$
DELIMITER ;

-- ===========================================
-- COMPLEX QUERIES: Nested, Join and Aggregate Examples
-- ===========================================

-- Nested query: List students enrolled in courses taught by 'Dr. Mehta'
SELECT s.Student_ID, s.Name
FROM Student s
WHERE s.Student_ID IN (
    SELECT e.Student_ID
    FROM Enrollment e
    JOIN Course c ON e.Course_ID = c.Course_ID
    WHERE c.Course_ID IN (
        SELECT t.Course_ID
        FROM Teaches t
        JOIN Instructor i ON t.Instructor_ID = i.Instructor_ID
        WHERE i.Name = 'Dr. Mehta'
    )
);

-- Join query: Get student details with courses and instructor names
SELECT s.Student_ID, s.Name AS Student_Name, c.Course_Name, i.Name AS Instructor_Name, e.Grade
FROM Student s
JOIN Enrollment e ON s.Student_ID = e.Student_ID
JOIN Course c ON e.Course_ID = c.Course_ID
LEFT JOIN Teaches t ON c.Course_ID = t.Course_ID AND e.Semester = t.Semester
LEFT JOIN Instructor i ON t.Instructor_ID = i.Instructor_ID
ORDER BY s.Name;

-- Aggregate query: Number of students per department
SELECT d.Dept_Name, COUNT(s.Student_ID) AS Number_of_Students
FROM Department d
LEFT JOIN Student s ON d.Department_ID = s.Department_ID
GROUP BY d.Dept_Name;

-- Aggregate query: Average grade point for a course (assuming grades A=4, B=3, C=2, D=1, F=0)
SELECT c.Course_Name,
       AVG(
           CASE e.Grade
               WHEN 'A+' THEN 4.3
               WHEN 'A' THEN 4.0
               WHEN 'B+' THEN 3.3
               WHEN 'B' THEN 3.0
               WHEN 'C+' THEN 2.3
               WHEN 'C' THEN 2.0
               WHEN 'D' THEN 1.0
               WHEN 'F' THEN 0
               ELSE NULL
           END
       ) AS Avg_Grade_Point
FROM Course c
JOIN Enrollment e ON c.Course_ID = e.Course_ID
GROUP BY c.Course_Name;

-- ===========================================
-- DEMONSTRATION OF PROCEDURE AND FUNCTION CALLS
-- ===========================================

-- Enroll student 103 into course 303 for Sem 4 with grade 'B+'
INSERT INTO Enrollment (Student_ID, Course_ID, Semester, Grade)
VALUES (103, 303, 'Sem 4', 'B+');

-- Get report for student 101 for Sem 4
SELECT c.Course_Name, e.Grade, i.Name AS Instructor_Name
FROM Enrollment e
JOIN Course c ON e.Course_ID = c.Course_ID
LEFT JOIN Teaches t ON c.Course_ID = t.Course_ID AND t.Semester = e.Semester
LEFT JOIN Instructor i ON t.Instructor_ID = i.Instructor_ID
WHERE e.Student_ID = 101 AND e.Semester = 'Sem 4';


-- Get total enrollment for course 301 using function
SELECT GetCourseEnrollment(301) AS EnrollmentCount;

-- Check if student 101 is enrolled in course 301
SELECT IsStudentEnrolled(101, 301) AS IsEnrolled;


-- ===========================================
-- ADVANCED TRIGGERS
-- ===========================================

-- Trigger to prevent deletion of department if students or instructors exist
DELIMITER $$
CREATE TRIGGER trg_department_before_delete
BEFORE DELETE ON Department
FOR EACH ROW
BEGIN
    IF EXISTS (SELECT 1 FROM Student WHERE Department_ID = OLD.Department_ID)
    OR EXISTS (SELECT 1 FROM Instructor WHERE Department_ID = OLD.Department_ID) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cannot delete department: students or instructors exist';
    END IF;
END$$
DELIMITER ;

-- Trigger to update the number of courses taught by an instructor
ALTER TABLE Instructor ADD COLUMN No_of_Courses_Taught INT DEFAULT 0;

DELIMITER $$
CREATE TRIGGER trg_teaches_insert
AFTER INSERT ON Teaches
FOR EACH ROW
BEGIN
    UPDATE Instructor
    SET No_of_Courses_Taught = No_of_Courses_Taught + 1
    WHERE Instructor_ID = NEW.Instructor_ID;
END$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER trg_teaches_delete
AFTER DELETE ON Teaches
FOR EACH ROW
BEGIN
    UPDATE Instructor
    SET No_of_Courses_Taught = No_of_Courses_Taught - 1
    WHERE Instructor_ID = OLD.Instructor_ID;
END$$
DELIMITER ;

-- ===========================================
-- ADDITIONAL STORED PROCEDURES
-- ===========================================

-- Procedure to update grades of all students in a course and semester
DELIMITER $$
CREATE PROCEDURE UpdateCourseGrades(
    IN p_Course_ID INT,
    IN p_Semester VARCHAR(20),
    IN p_New_Grade VARCHAR(5)
)
BEGIN
    UPDATE Enrollment
    SET Grade = p_New_Grade
    WHERE Course_ID = p_Course_ID AND Semester = p_Semester;
END$$
DELIMITER ;

-- Procedure to assign/change classroom for a course
DELIMITER $$
CREATE PROCEDURE AssignClassroom(
    IN p_Course_ID INT,
    IN p_Room_ID INT
)
BEGIN
    UPDATE Classroom
    SET Course_ID = p_Course_ID
    WHERE Room_ID = p_Room_ID;
END$$
DELIMITER ;

-- ===========================================
-- ADDITIONAL USER-DEFINED FUNCTIONS
-- ===========================================

-- Function to calculate total credits taken by a student
DELIMITER $$
CREATE FUNCTION GetStudentCredits(p_Student_ID INT)
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE total_credits INT;
    SELECT SUM(c.Credits) INTO total_credits
    FROM Enrollment e
    JOIN Course c ON e.Course_ID = c.Course_ID
    WHERE e.Student_ID = p_Student_ID;
    RETURN IFNULL(total_credits, 0);
END$$
DELIMITER ;

-- Function to check if a course is full (enrollment >= classroom capacity)
DELIMITER $$
CREATE FUNCTION IsCourseFull(p_Course_ID INT)
RETURNS VARCHAR(3)
DETERMINISTIC
BEGIN
    DECLARE full VARCHAR(3);
    DECLARE enrolled INT;
    DECLARE capacity INT;

    SELECT COUNT(*) INTO enrolled FROM Enrollment WHERE Course_ID = p_Course_ID;
    SELECT Capacity INTO capacity FROM Classroom WHERE Course_ID = p_Course_ID;

    IF enrolled >= capacity THEN
        SET full = 'YES';
    ELSE
        SET full = 'NO';
    END IF;
    RETURN full;
END$$
DELIMITER ;

-- ===========================================
-- USEFUL VIEWS FOR REPORTING
-- ===========================================

-- View: Student performance summary
CREATE OR REPLACE VIEW v_student_performance AS
SELECT
    s.Student_ID,
    s.Name,
    c.Course_Name,
    e.Semester,
    e.Grade
FROM Student s
JOIN Enrollment e ON s.Student_ID = e.Student_ID
JOIN Course c ON e.Course_ID = c.Course_ID;

-- View: Instructor workload summary
CREATE OR REPLACE VIEW v_instructor_workload AS
SELECT
    i.Instructor_ID,
    i.Name AS Instructor_Name,
    COUNT(t.Course_ID) AS Courses_Taught,
    GROUP_CONCAT(c.Course_Name) AS Courses
FROM Instructor i
LEFT JOIN Teaches t ON i.Instructor_ID = t.Instructor_ID
LEFT JOIN Course c ON t.Course_ID = c.Course_ID
GROUP BY i.Instructor_ID, i.Name;

-- View: Course Enrollment Summary
CREATE OR REPLACE VIEW v_course_enrollment AS
SELECT
    c.Course_ID,
    c.Course_Name,
    COUNT(e.Student_ID) AS Enrolled_Students,
    cl.Capacity
FROM Course c
LEFT JOIN Enrollment e ON c.Course_ID = e.Course_ID
LEFT JOIN Classroom cl ON c.Course_ID = cl.Course_ID
GROUP BY c.Course_ID, c.Course_Name, cl.Capacity;

-- ===========================================
-- SAMPLE INVOCATIONS
-- ===========================================

-- Get total credits for student 101
SELECT GetStudentCredits(101) AS TotalCredits;

-- Check if 'Database Systems' course (301) is full
SELECT IsCourseFull(301) AS IsFull;

-- View summaries
SELECT * FROM v_student_performance;
SELECT * FROM v_instructor_workload;
SELECT * FROM v_course_enrollment;

-- Update grades of all students in course 301 for Sem 4 to 'A'
UPDATE Enrollment
SET Grade = 'A'
WHERE Course_ID = 301 AND Semester = 'Sem 4';

-- Assign course 303 to Room 603
UPDATE Classroom
SET Course_ID = 303
WHERE Room_ID = 603;


