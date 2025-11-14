-- FULL EXECUTABLE SQL SCRIPT
-- Drops existing CourseManagement DB and recreates schema + sample data cleanly.

DROP DATABASE IF EXISTS CourseManagement;
CREATE DATABASE CourseManagement;
USE CourseManagement;

-- ======================
-- TABLES (created in safe order)
-- ======================
CREATE TABLE Department (
    Department_ID INT PRIMARY KEY,
    Dept_Name VARCHAR(100) NOT NULL,
    Location VARCHAR(100),
    HOD_Name VARCHAR(100)
);

CREATE TABLE Student (
    Student_ID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE,
    Phone VARCHAR(15),
    DOB DATE,
    Year_of_Study INT,
    Department_ID INT,
    FOREIGN KEY (Department_ID) REFERENCES Department(Department_ID) ON DELETE SET NULL
);

CREATE TABLE Instructor (
    Instructor_ID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE,
    Phone VARCHAR(15),
    DOJ DATE,
    Qualification VARCHAR(100),
    Department_ID INT,
    No_of_Courses_Taught INT DEFAULT 0,
    FOREIGN KEY (Department_ID) REFERENCES Department(Department_ID) ON DELETE SET NULL
);

CREATE TABLE Course (
    Course_ID INT PRIMARY KEY,
    Course_Name VARCHAR(100) NOT NULL,
    Credits INT,
    Course_Level VARCHAR(20),
    No_of_Students_Enrolled INT DEFAULT 0,
    Department_ID INT,
    FOREIGN KEY (Department_ID) REFERENCES Department(Department_ID) ON DELETE SET NULL
);

CREATE TABLE Classroom (
    Room_ID INT PRIMARY KEY,
    Location VARCHAR(100),
    Capacity INT,
    Course_ID INT,
    FOREIGN KEY (Course_ID) REFERENCES Course(Course_ID) ON DELETE CASCADE
);

CREATE TABLE Enrollment (
    Enrollment_ID INT PRIMARY KEY,
    Student_ID INT,
    Course_ID INT,
    Semester VARCHAR(20),
    Grade VARCHAR(5),
    FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID) ON DELETE CASCADE,
    FOREIGN KEY (Course_ID) REFERENCES Course(Course_ID) ON DELETE CASCADE
);

CREATE TABLE Teaches (
    Teach_ID INT PRIMARY KEY,
    Instructor_ID INT,
    Course_ID INT,
    Semester VARCHAR(20),
    Academic_Year VARCHAR(10),
    FOREIGN KEY (Instructor_ID) REFERENCES Instructor(Instructor_ID) ON DELETE CASCADE,
    FOREIGN KEY (Course_ID) REFERENCES Course(Course_ID) ON DELETE CASCADE
);

CREATE TABLE Alumni (
    Alumni_ID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE,
    Phone VARCHAR(15),
    DOB DATE,
    Graduation_Year INT,
    CGPA DECIMAL(4,2),
    Department_ID INT,
    Notes TEXT,
    FOREIGN KEY (Department_ID) REFERENCES Department(Department_ID) ON DELETE SET NULL
);

CREATE TABLE Placement (
    Placement_ID INT PRIMARY KEY AUTO_INCREMENT,
    Student_ID INT NULL,
    Alumni_ID INT NULL,
    Company VARCHAR(150) NOT NULL,
    Role VARCHAR(150),
    Package VARCHAR(50),
    Offer_Date DATE,
    On_Campus TINYINT(1) DEFAULT 0,
    Location VARCHAR(100),
    Remarks TEXT,
    FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID) ON DELETE SET NULL,
    FOREIGN KEY (Alumni_ID) REFERENCES Alumni(Alumni_ID) ON DELETE SET NULL
);

CREATE TABLE Internship (
    Internship_ID INT PRIMARY KEY AUTO_INCREMENT,
    Student_ID INT NULL,
    Alumni_ID INT NULL,
    Company VARCHAR(150) NOT NULL,
    Role VARCHAR(150),
    Duration VARCHAR(50),
    Stipend VARCHAR(50),
    Start_Date DATE,
    End_Date DATE,
    Mode VARCHAR(20),
    Remarks TEXT,
    FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID) ON DELETE SET NULL,
    FOREIGN KEY (Alumni_ID) REFERENCES Alumni(Alumni_ID) ON DELETE SET NULL
);

CREATE TABLE Placement_Help (
    Help_ID INT PRIMARY KEY AUTO_INCREMENT,
    Title VARCHAR(200),
    Description TEXT,
    Link VARCHAR(400),
    Created_On DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Internship_Help (
    Help_ID INT PRIMARY KEY AUTO_INCREMENT,
    Title VARCHAR(200),
    Description TEXT,
    Link VARCHAR(400),
    Created_On DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ======================
-- SAMPLE INSERTS (clean deterministic data)
-- ======================
INSERT INTO Department (Department_ID, Dept_Name, Location, HOD_Name) VALUES
(1, 'Computer Science & Engineering', 'Block A', 'Dr. R. S. Menon'),
(2, 'Electronics & Communication', 'Block B', 'Dr. A. K. Pillai'),
(3, 'Mechanical Engineering', 'Block C', 'Dr. S. Venkatesh'),
(4, 'Civil Engineering', 'Block D', 'Dr. N. Chatterjee');

INSERT INTO Student (Student_ID, Name, Email, Phone, DOB, Year_of_Study, Department_ID) VALUES
(1001, 'Aarav Kumar', 'aarav.kumar@pes.edu', '9845012345', '2003-03-12', 4, 1),
(1002, 'Bhavya Reddy', 'bhavya.reddy@pes.edu', '9881122334', '2004-07-05', 3, 1),
(1003, 'Chirag Patel', 'chirag.patel@pes.edu', '9900011223', '2003-11-22', 4, 2),
(1004, 'Diya Sharma', 'diya.sharma@pes.edu', '9877700112', '2004-01-17', 2, 1),
(1005, 'Eshan Gupta', 'eshan.gupta@pes.edu', '9765432198', '2002-09-30', 4, 3),
(1006, 'Fatima Khan', 'fatima.khan@pes.edu', '9700123456', '2004-05-02', 2, 2);

INSERT INTO Instructor (Instructor_ID, Name, Email, Phone, DOJ, Qualification, Department_ID, No_of_Courses_Taught) VALUES
(2001, 'Dr. R. S. Menon', 'rsmenon@pes.edu', '9440012345', '2010-06-15', 'PhD CSE', 1, 3),
(2002, 'Dr. A. K. Pillai', 'akpillai@pes.edu', '9440023456', '2012-09-01', 'PhD ECE', 2, 2),
(2003, 'Dr. S. Venkatesh', 'svvenkatesh@pes.edu', '9440034567', '2008-01-12', 'PhD ME', 3, 2),
(2004, 'Dr. N. Chatterjee', 'nchatterjee@pes.edu', '9440045678', '2014-03-20', 'PhD CE', 4, 1),
(2005, 'Dr. P. K. Iyer', 'pkiyer@pes.edu', '9440056789', '2016-11-05', 'PhD CSE', 1, 1);

INSERT INTO Course (Course_ID, Course_Name, Credits, Course_Level, No_of_Students_Enrolled, Department_ID) VALUES
(3001, 'Data Structures and Algorithms', 4, 'UG', 0, 1),
(3002, 'Database Management Systems', 4, 'UG', 0, 1),
(3003, 'Digital Electronics', 3, 'UG', 0, 2),
(3004, 'Operating Systems', 4, 'UG', 0, 1),
(3005, 'Thermodynamics', 3, 'UG', 0, 3),
(3006, 'Structural Analysis', 3, 'UG', 0, 4);

INSERT INTO Classroom (Room_ID, Location, Capacity, Course_ID) VALUES
(6001, 'A-101', 80, 3001),
(6002, 'A-102', 60, 3002),
(6003, 'B-201', 50, 3003),
(6004, 'A-201', 70, 3004),
(6005, 'C-301', 90, 3005),
(6006, 'D-101', 40, 3006);

INSERT INTO Enrollment (Enrollment_ID, Student_ID, Course_ID, Semester, Grade) VALUES
(4001, 1001, 3001, 'Sem 8', 'A'),
(4002, 1001, 3002, 'Sem 8', 'A-'),
(4003, 1002, 3001, 'Sem 6', 'B+'),
(4004, 1003, 3003, 'Sem 8', 'A'),
(4005, 1004, 3004, 'Sem 4', 'B'),
(4006, 1005, 3005, 'Sem 8', 'A-'),
(4007, 1006, 3003, 'Sem 4', 'B+');

INSERT INTO Teaches (Teach_ID, Instructor_ID, Course_ID, Semester, Academic_Year) VALUES
(5001, 2001, 3001, 'Sem 8', '2025'),
(5002, 2005, 3002, 'Sem 8', '2025'),
(5003, 2002, 3003, 'Sem 8', '2025'),
(5004, 2001, 3004, 'Sem 4', '2025'),
(5005, 2003, 3005, 'Sem 8', '2025');

-- Insert explicit alumni rows (explicit IDs)
INSERT INTO Alumni (Alumni_ID, Name, Email, Phone, DOB, Graduation_Year, CGPA, Department_ID, Notes) VALUES
(1, 'Gaurav Nair', 'gaurav.nair@alum.pes.edu', '9100001111', '2001-02-10', 2023, 8.95, 1, 'Joined startup as SWE'),
(2, 'Hema Rao', 'hema.rao@alum.pes.edu', '9100002222', '2000-08-24', 2022, 9.18, 1, 'Placed at MNC - Backend'),
(3, 'Ibrahim Sheikh', 'ibrahim.sheikh@alum.pes.edu', '9100003333', '1999-11-12', 2021, 8.40, 2, 'Internship then full-time role'),
(4, 'Jaya Menon', 'jaya.menon@alum.pes.edu', '9100004444', '2000-03-30', 2022, 9.45, 1, 'High CGPA, research internship');

-- Ensure auto_increment for future inserts begins after explicit IDs
ALTER TABLE Alumni AUTO_INCREMENT = 100;

INSERT INTO Placement (Student_ID, Alumni_ID, Company, Role, Package, Offer_Date, On_Campus, Location, Remarks) VALUES
(NULL, 1, 'NexGen Labs', 'Software Engineer', '10 LPA', '2024-07-10', 1, 'Bengaluru', 'On-campus placement'),
(1001, NULL, 'CloudWave', 'SRE Intern (converted)', '8 LPA', '2024-06-15', 0, 'Bengaluru', 'Intern->Full-time'),
(NULL, 2, 'MacroSoft', 'Backend Engineer', '22 LPA', '2023-08-01', 1, 'Hyderabad', 'Offered through drive'),
(NULL, 3, 'Photonics Inc', 'Embedded Systems Engineer', '7 LPA', '2022-11-20', 0, 'Chennai', 'Lateral hire'),
(NULL, 4, 'DeepAI Research', 'Research Engineer', '24 LPA', '2024-09-05', 0, 'Remote', 'Research position');

INSERT INTO Internship (Student_ID, Alumni_ID, Company, Role, Duration, Stipend, Start_Date, End_Date, Mode, Remarks) VALUES
(1002, NULL, 'FinTech Labs', 'ML Intern', '3 months', '25000', '2024-05-01', '2024-07-31', 'Remote', 'Worked on fraud detection prototype'),
(1003, NULL, 'Semicon Solutions', 'Hardware Intern', '2 months', '15000', '2024-06-01', '2024-07-31', 'Onsite', 'PCB testing and verification'),
(NULL, 1, 'NexGen Labs', 'Backend Intern', '6 months', '30000', '2023-01-10', '2023-07-09', 'Hybrid', 'Converted to full-time'),
(1004, NULL, 'OpenSource Org', 'Contributor Intern', '2 months', '0', '2024-04-01', '2024-05-31', 'Remote', 'Open-source contributions'),
(NULL, 4, 'DeepAI Research', 'Research Intern', '12 months', '0', '2023-10-01', '2024-09-30', 'Remote', 'Research on computer vision');

INSERT INTO Placement_Help (Title, Description, Link) VALUES
('Coding Interview Roadmap', 'Systematic roadmap: DS&A -> Mock interviews -> System design basics -> Behavioral preparation', 'https://resources.example.com/coding-roadmap'),
('Building a Strong Resume', 'One-page resume, quantify achievements, include project URLs and GitHub', 'https://resources.example.com/resume-tips'),
('Interview Soft Skills', 'Communication, STAR method for behavioral answers, negotiation basics', 'https://resources.example.com/soft-skills');

INSERT INTO Internship_Help (Title, Description, Link) VALUES
('Where to Find Internships', 'College T&P, LinkedIn, Internshala, AngelList, company career pages', 'https://resources.example.com/find-interns'),
('Internship Application Tips', 'Tailor CV, include cover note, show relevant projects, follow up politely', 'https://resources.example.com/intern-apps'),
('Prepare for Technical Internships', 'Foundations, small projects, coding practice and system basics', 'https://resources.example.com/tech-intern');

-- ======================
-- VIEWS
-- ======================
CREATE OR REPLACE VIEW v_student_performance AS
SELECT s.Student_ID, s.Name, c.Course_Name, e.Semester, e.Grade
FROM Student s
JOIN Enrollment e ON s.Student_ID = e.Student_ID
JOIN Course c ON e.Course_ID = c.Course_ID;

CREATE OR REPLACE VIEW v_instructor_workload AS
SELECT i.Instructor_ID, i.Name AS Instructor_Name, COUNT(t.Course_ID) AS Courses_Taught, GROUP_CONCAT(c.Course_Name) AS Courses
FROM Instructor i
LEFT JOIN Teaches t ON i.Instructor_ID = t.Instructor_ID
LEFT JOIN Course c ON t.Course_ID = c.Course_ID
GROUP BY i.Instructor_ID, i.Name;

CREATE OR REPLACE VIEW v_course_enrollment AS
SELECT c.Course_ID, c.Course_Name, COUNT(e.Student_ID) AS Enrolled_Students, cl.Capacity
FROM Course c
LEFT JOIN Enrollment e ON c.Course_ID = e.Course_ID
LEFT JOIN Classroom cl ON c.Course_ID = cl.Course_ID
GROUP BY c.Course_ID, c.Course_Name, cl.Capacity;

CREATE OR REPLACE VIEW v_alumni_placements AS
SELECT a.Alumni_ID, a.Name, a.Graduation_Year, a.CGPA, p.Company, p.Role, p.Package, p.Offer_Date
FROM Alumni a
LEFT JOIN Placement p ON a.Alumni_ID = p.Alumni_ID;

CREATE OR REPLACE VIEW v_student_internships AS
SELECT s.Student_ID, s.Name, i.Company, i.Role, i.Start_Date, i.End_Date, i.Mode
FROM Student s
LEFT JOIN Internship i ON s.Student_ID = i.Student_ID;

-- ======================
-- FUNCTIONS (drop + create)
-- ======================
DROP FUNCTION IF EXISTS GetCourseEnrollment;
DELIMITER $$
CREATE FUNCTION GetCourseEnrollment(p_Course_ID INT) RETURNS INT DETERMINISTIC
BEGIN
    DECLARE total INT;
    SELECT COUNT(*) INTO total FROM Enrollment WHERE Course_ID = p_Course_ID;
    RETURN IFNULL(total, 0);
END$$
DELIMITER ;

DROP FUNCTION IF EXISTS IsStudentEnrolled;
DELIMITER $$
CREATE FUNCTION IsStudentEnrolled(p_Student_ID INT, p_Course_ID INT) RETURNS VARCHAR(3) DETERMINISTIC
BEGIN
    DECLARE enrolled VARCHAR(3);
    IF EXISTS (SELECT 1 FROM Enrollment WHERE Student_ID = p_Student_ID AND Course_ID = p_Course_ID) THEN
        SET enrolled = 'YES';
    ELSE
        SET enrolled = 'NO';
    END IF;
    RETURN enrolled;
END$$
DELIMITER ;

DROP FUNCTION IF EXISTS GetStudentCredits;
DELIMITER $$
CREATE FUNCTION GetStudentCredits(p_Student_ID INT) RETURNS INT DETERMINISTIC
BEGIN
    DECLARE total_credits INT;
    SELECT SUM(c.Credits) INTO total_credits FROM Enrollment e JOIN Course c ON e.Course_ID = c.Course_ID WHERE e.Student_ID = p_Student_ID;
    RETURN IFNULL(total_credits, 0);
END$$
DELIMITER ;

DROP FUNCTION IF EXISTS IsCourseFull;
DELIMITER $$
CREATE FUNCTION IsCourseFull(p_Course_ID INT) RETURNS VARCHAR(7) DETERMINISTIC
BEGIN
    DECLARE full VARCHAR(7);
    DECLARE enrolled INT;
    DECLARE capacity INT;
    SELECT COUNT(*) INTO enrolled FROM Enrollment WHERE Course_ID = p_Course_ID;
    SELECT Capacity INTO capacity FROM Classroom WHERE Course_ID = p_Course_ID;
    IF capacity IS NULL THEN
        SET full = 'UNKNOWN';
    ELSEIF enrolled >= capacity THEN
        SET full = 'YES';
    ELSE
        SET full = 'NO';
    END IF;
    RETURN full;
END$$
DELIMITER ;

-- ======================
-- PROCEDURES (drop + create)
-- ======================
DROP PROCEDURE IF EXISTS EnrollStudent;
DELIMITER $$
CREATE PROCEDURE EnrollStudent(IN p_Student_ID INT, IN p_Course_ID INT, IN p_Semester VARCHAR(20), IN p_Grade VARCHAR(5))
BEGIN
    IF EXISTS (SELECT 1 FROM Enrollment WHERE Student_ID = p_Student_ID AND Course_ID = p_Course_ID) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Student already enrolled in this course';
    ELSE
        INSERT INTO Enrollment(Student_ID, Course_ID, Semester, Grade) VALUES (p_Student_ID, p_Course_ID, p_Semester, p_Grade);
    END IF;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS UpdateCourseGrades;
DELIMITER $$
CREATE PROCEDURE UpdateCourseGrades(IN p_Course_ID INT, IN p_Semester VARCHAR(20), IN p_New_Grade VARCHAR(5))
BEGIN
    UPDATE Enrollment SET Grade = p_New_Grade WHERE Course_ID = p_Course_ID AND Semester = p_Semester;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS AssignClassroom;
DELIMITER $$
CREATE PROCEDURE AssignClassroom(IN p_Course_ID INT, IN p_Room_ID INT)
BEGIN
    UPDATE Classroom SET Course_ID = p_Course_ID WHERE Room_ID = p_Room_ID;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS AddStudent;
DELIMITER $$
CREATE PROCEDURE AddStudent(IN p_Name VARCHAR(100), IN p_Email VARCHAR(100), IN p_Phone VARCHAR(15), IN p_DOB DATE, IN p_Year INT, IN p_Department_ID INT)
BEGIN
    INSERT INTO Student(Name, Email, Phone, DOB, Year_of_Study, Department_ID) VALUES (p_Name, p_Email, p_Phone, p_DOB, p_Year, p_Department_ID);
END$$
DELIMITER ;

-- ======================
-- TRIGGERS (drop + create)
-- ======================
DROP TRIGGER IF EXISTS trg_enrollment_insert;
DELIMITER $$
CREATE TRIGGER trg_enrollment_insert AFTER INSERT ON Enrollment FOR EACH ROW
BEGIN
    UPDATE Course SET No_of_Students_Enrolled = COALESCE(No_of_Students_Enrolled,0) + 1 WHERE Course_ID = NEW.Course_ID;
END$$
DELIMITER ;

DROP TRIGGER IF EXISTS trg_enrollment_delete;
DELIMITER $$
CREATE TRIGGER trg_enrollment_delete AFTER DELETE ON Enrollment FOR EACH ROW
BEGIN
    UPDATE Course SET No_of_Students_Enrolled = GREATEST(COALESCE(No_of_Students_Enrolled,0) - 1, 0) WHERE Course_ID = OLD.Course_ID;
END$$
DELIMITER ;

DROP TRIGGER IF EXISTS trg_student_before_insert;
DELIMITER $$
CREATE TRIGGER trg_student_before_insert BEFORE INSERT ON Student FOR EACH ROW
BEGIN
    IF NEW.Department_ID IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Department_ID cannot be NULL';
    END IF;
END$$
DELIMITER ;

DROP TRIGGER IF EXISTS trg_department_before_delete;
DELIMITER $$
CREATE TRIGGER trg_department_before_delete BEFORE DELETE ON Department FOR EACH ROW
BEGIN
    IF EXISTS (SELECT 1 FROM Student WHERE Department_ID = OLD.Department_ID) OR EXISTS (SELECT 1 FROM Instructor WHERE Department_ID = OLD.Department_ID) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cannot delete department: students or instructors exist';
    END IF;
END$$
DELIMITER ;

DROP TRIGGER IF EXISTS trg_teaches_insert;
DELIMITER $$
CREATE TRIGGER trg_teaches_insert AFTER INSERT ON Teaches FOR EACH ROW
BEGIN
    UPDATE Instructor SET No_of_Courses_Taught = COALESCE(No_of_Courses_Taught,0) + 1 WHERE Instructor_ID = NEW.Instructor_ID;
END$$
DELIMITER ;

DROP TRIGGER IF EXISTS trg_teaches_delete;
DELIMITER $$
CREATE TRIGGER trg_teaches_delete AFTER DELETE ON Teaches FOR EACH ROW
BEGIN
    UPDATE Instructor SET No_of_Courses_Taught = GREATEST(COALESCE(No_of_Courses_Taught,0) - 1, 0) WHERE Instructor_ID = OLD.Instructor_ID;
END$$
DELIMITER ;

-- ======================
-- Quick checks (sample queries)
-- ======================
SELECT 'Setup completed' AS status;
SELECT GetCourseEnrollment(3001) AS EnrollmentCount;
SELECT IsStudentEnrolled(1001, 3001) AS IsEnrolled;
SELECT * FROM v_student_performance LIMIT 5;
SELECT * FROM v_instructor_workload LIMIT 5;
SELECT * FROM v_alumni_placements LIMIT 5;
SELECT * FROM v_student_internships LIMIT 5;

-- End of script
