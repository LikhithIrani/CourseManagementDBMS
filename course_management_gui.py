import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
from datetime import datetime

class CourseManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Course Management System")
        self.root.geometry("1200x700")
        self.root.configure(bg='#f0f0f0')
        
        # Database configuration - Update these with your MySQL credentials
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'Likhith@123',  # Update with your MySQL password
            'database': 'CourseManagement'
        }
        
        self.connection = None
        self.connect_to_database()
        
        # Create main notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_students_tab()
        self.create_instructors_tab()
        self.create_courses_tab()
        self.create_enrollments_tab()
        self.create_placements_tab()
        self.create_internships_tab()
        self.create_reports_tab()
        self.create_functions_tab()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def connect_to_database(self):
        """Connect to MySQL database"""
        try:
            self.connection = mysql.connector.connect(**self.db_config)
            if self.connection.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            messagebox.showerror("Database Error", f"Error connecting to MySQL: {e}")
            self.root.quit()
    
    def execute_query(self, query, params=None, fetch=True):
        """Execute a query and return results"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch:
                results = cursor.fetchall()
                cursor.close()
                return results
            else:
                self.connection.commit()
                cursor.close()
                return True
        except Error as e:
            messagebox.showerror("Database Error", f"Error executing query: {e}")
            return None
    
    def create_dashboard_tab(self):
        """Create dashboard tab with statistics"""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="Dashboard")
        
        # Title
        title_label = tk.Label(dashboard_frame, text="Course Management System Dashboard", 
                              font=("Arial", 18, "bold"), bg='#f0f0f0')
        title_label.pack(pady=20)
        
        # Statistics frame
        stats_frame = tk.Frame(dashboard_frame, bg='#f0f0f0')
        stats_frame.pack(pady=20)
        
        # Get statistics
        stats = self.get_statistics()
        
        # Create stat cards
        stat_cards = [
            ("Total Students", stats.get('students', 0), "#4CAF50"),
            ("Total Instructors", stats.get('instructors', 0), "#2196F3"),
            ("Total Courses", stats.get('courses', 0), "#FF9800"),
            ("Total Enrollments", stats.get('enrollments', 0), "#9C27B0")
        ]
        
        for i, (label, value, color) in enumerate(stat_cards):
            card = tk.Frame(stats_frame, bg=color, width=250, height=150)
            card.pack(side=tk.LEFT, padx=10, pady=10)
            card.pack_propagate(False)
            
            label_widget = tk.Label(card, text=label, font=("Arial", 12), bg=color, fg='white')
            label_widget.pack(pady=20)
            
            value_widget = tk.Label(card, text=str(value), font=("Arial", 24, "bold"), bg=color, fg='white')
            value_widget.pack(pady=10)
        
        # Refresh button
        refresh_btn = tk.Button(dashboard_frame, text="Refresh Statistics", 
                               command=lambda: self.refresh_dashboard(dashboard_frame),
                               bg="#2196F3", fg="white", font=("Arial", 12), padx=20, pady=10)
        refresh_btn.pack(pady=20)
    
    def get_statistics(self):
        """Get dashboard statistics"""
        stats = {}
        
        # Count students
        result = self.execute_query("SELECT COUNT(*) as count FROM Student")
        stats['students'] = result[0]['count'] if result else 0
        
        # Count instructors
        result = self.execute_query("SELECT COUNT(*) as count FROM Instructor")
        stats['instructors'] = result[0]['count'] if result else 0
        
        # Count courses
        result = self.execute_query("SELECT COUNT(*) as count FROM Course")
        stats['courses'] = result[0]['count'] if result else 0
        
        # Count enrollments
        result = self.execute_query("SELECT COUNT(*) as count FROM Enrollment")
        stats['enrollments'] = result[0]['count'] if result else 0
        
        return stats
    
    def refresh_dashboard(self, frame):
        """Refresh dashboard statistics"""
        for widget in frame.winfo_children():
            widget.destroy()
        self.create_dashboard_tab()
    
    def create_students_tab(self):
        """Create students management tab"""
        students_frame = ttk.Frame(self.notebook)
        self.notebook.add(students_frame, text="Students")
        
        # Title
        title_label = tk.Label(students_frame, text="Student Management", 
                              font=("Arial", 16, "bold"), bg='#f0f0f0')
        title_label.pack(pady=10)
        
        # Buttons frame
        btn_frame = tk.Frame(students_frame, bg='#f0f0f0')
        btn_frame.pack(pady=10)
        
        add_btn = tk.Button(btn_frame, text="Add Student", command=self.open_add_student_window,
                           bg="#4CAF50", fg="white", font=("Arial", 11), padx=15, pady=5)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = tk.Button(btn_frame, text="Refresh", command=lambda: self.refresh_students_table(tree),
                               bg="#2196F3", fg="white", font=("Arial", 11), padx=15, pady=5)
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        verify_btn = tk.Button(btn_frame, text="Verify Database", command=self.verify_database_connection,
                              bg="#FF9800", fg="white", font=("Arial", 11), padx=15, pady=5)
        verify_btn.pack(side=tk.LEFT, padx=5)
        
        # Treeview for students
        tree_frame = tk.Frame(students_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        scrollbar_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        
        tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Email", "Phone", "DOB", "Year", "Department"),
                           show="headings", yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        scrollbar_y.config(command=tree.yview)
        scrollbar_x.config(command=tree.xview)
        
        # Configure columns
        tree.heading("ID", text="Student ID")
        tree.heading("Name", text="Name")
        tree.heading("Email", text="Email")
        tree.heading("Phone", text="Phone")
        tree.heading("DOB", text="Date of Birth")
        tree.heading("Year", text="Year of Study")
        tree.heading("Department", text="Department")
        
        tree.column("ID", width=100)
        tree.column("Name", width=150)
        tree.column("Email", width=200)
        tree.column("Phone", width=120)
        tree.column("DOB", width=120)
        tree.column("Year", width=100)
        tree.column("Department", width=200)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Store tree reference for refresh
        students_frame.tree = tree
        
        # Load students
        self.load_students(tree)
    
    def load_students(self, tree):
        """Load students into treeview"""
        # Clear existing items
        for item in tree.get_children():
            tree.delete(item)
        
        query = """
        SELECT s.Student_ID, s.Name, s.Email, s.Phone, s.DOB, s.Year_of_Study, d.Dept_Name
        FROM Student s
        LEFT JOIN Department d ON s.Department_ID = d.Department_ID
        ORDER BY s.Student_ID
        """
        
        students = self.execute_query(query)
        if students:
            for student in students:
                dob = student['DOB'].strftime('%Y-%m-%d') if student['DOB'] else ''
                tree.insert("", tk.END, values=(
                    student['Student_ID'],
                    student['Name'],
                    student['Email'] or '',
                    student['Phone'] or '',
                    dob,
                    student['Year_of_Study'],
                    student['Dept_Name'] or ''
                ))
    
    def refresh_students_table(self, tree):
        """Refresh students table"""
        self.load_students(tree)
    
    def verify_database_connection(self):
        """Verify database connection and show current data"""
        try:
            # Check connection
            if not self.connection or not self.connection.is_connected():
                messagebox.showerror("Error", "Database connection is not active!")
                return
            
            # Get total count of students
            result = self.execute_query("SELECT COUNT(*) as total FROM Student")
            total_students = result[0]['total'] if result else 0
            
            # Get last 5 students added
            recent_students = self.execute_query(
                "SELECT Student_ID, Name, Department_ID, Year_of_Study FROM Student ORDER BY Student_ID DESC LIMIT 5"
            )
            
            # Format recent students
            recent_text = ""
            if recent_students:
                for student in recent_students:
                    # Get department name
                    dept_result = self.execute_query(
                        "SELECT Dept_Name FROM Department WHERE Department_ID = %s",
                        (student['Department_ID'],)
                    )
                    dept_name = dept_result[0]['Dept_Name'] if dept_result else 'Unknown'
                    
                    recent_text += f"ID: {student['Student_ID']} - {student['Name']} (Year {student['Year_of_Study']}, {dept_name})\n"
            else:
                recent_text = "No students found"
            
            messagebox.showinfo("Database Verification", 
                f"✓ Database Connection: Active\n\n"
                f"Total Students in Database: {total_students}\n\n"
                f"Recent Students (Last 5):\n{recent_text}")
        except Error as e:
            messagebox.showerror("Error", f"Database verification failed: {e}")
    
    def open_add_student_window(self):
        """Open window to add new student"""
        window = tk.Toplevel(self.root)
        window.title("Add New Student")
        window.geometry("400x500")
        window.configure(bg='#f0f0f0')
        
        # Form fields
        tk.Label(window, text="Student ID *", bg='#f0f0f0', font=("Arial", 10)).pack(pady=5)
        student_id_entry = tk.Entry(window, font=("Arial", 10), width=30)
        student_id_entry.pack(pady=5)
        
        tk.Label(window, text="Name *", bg='#f0f0f0', font=("Arial", 10)).pack(pady=5)
        name_entry = tk.Entry(window, font=("Arial", 10), width=30)
        name_entry.pack(pady=5)
        
        tk.Label(window, text="Email", bg='#f0f0f0', font=("Arial", 10)).pack(pady=5)
        email_entry = tk.Entry(window, font=("Arial", 10), width=30)
        email_entry.pack(pady=5)
        
        tk.Label(window, text="Phone", bg='#f0f0f0', font=("Arial", 10)).pack(pady=5)
        phone_entry = tk.Entry(window, font=("Arial", 10), width=30)
        phone_entry.pack(pady=5)
        
        tk.Label(window, text="Date of Birth (YYYY-MM-DD)", bg='#f0f0f0', font=("Arial", 10)).pack(pady=5)
        dob_entry = tk.Entry(window, font=("Arial", 10), width=30)
        dob_entry.pack(pady=5)
        
        tk.Label(window, text="Year of Study *", bg='#f0f0f0', font=("Arial", 10)).pack(pady=5)
        year_entry = tk.Entry(window, font=("Arial", 10), width=30)
        year_entry.pack(pady=5)
        
        tk.Label(window, text="Department *", bg='#f0f0f0', font=("Arial", 10)).pack(pady=5)
        dept_var = tk.StringVar()
        dept_combo = ttk.Combobox(window, textvariable=dept_var, width=27, state="readonly")
        dept_combo.pack(pady=5)
        
        # Load departments
        departments = self.execute_query("SELECT Department_ID, Dept_Name FROM Department")
        if departments:
            dept_dict = {dept['Dept_Name']: dept['Department_ID'] for dept in departments}
            dept_combo['values'] = list(dept_dict.keys())
        
        def add_student():
            """Add student using AddStudent procedure or direct insert"""
            try:
                student_id = student_id_entry.get().strip()
                name = name_entry.get().strip()
                email = email_entry.get().strip() or None
                phone = phone_entry.get().strip() or None
                dob = dob_entry.get().strip() or None
                year = year_entry.get().strip()
                dept_name = dept_var.get()
                
                if not student_id or not name or not year or not dept_name:
                    messagebox.showerror("Error", "Please fill all required fields (*)")
                    return
                
                dept_id = dept_dict.get(dept_name)
                
                # Use AddStudent procedure (it doesn't take Student_ID, so use direct insert)
                query = """
                INSERT INTO Student (Student_ID, Name, Email, Phone, DOB, Year_of_Study, Department_ID)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                params = (int(student_id), name, email, phone, dob if dob else None, int(year), dept_id)
                
                if self.execute_query(query, params, fetch=False):
                    # Verify the student was added to database
                    verify_query = "SELECT * FROM Student WHERE Student_ID = %s"
                    verify_result = self.execute_query(verify_query, (int(student_id),))
                    
                    if verify_result:
                        student_data = verify_result[0]
                        messagebox.showinfo("Success", 
                            f"Student added successfully!\n\n"
                            f"Verification:\n"
                            f"Student ID: {student_data['Student_ID']}\n"
                            f"Name: {student_data['Name']}\n"
                            f"Department ID: {student_data['Department_ID']}\n"
                            f"Year of Study: {student_data['Year_of_Study']}\n\n"
                            f"✓ Record found in database!")
                    else:
                        messagebox.showwarning("Warning", "Student added but could not verify in database.")
                    
                    window.destroy()
                    # Refresh students table
                    for tab_id in range(self.notebook.index("end")):
                        tab = self.notebook.nametowidget(self.notebook.tabs()[tab_id])
                        if hasattr(tab, 'tree'):
                            self.load_students(tab.tree)
                    # Refresh dashboard
                    self.refresh_dashboard(self.notebook.nametowidget(self.notebook.tabs()[0]))
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Student ID and Year must be numbers.")
            except Error as e:
                messagebox.showerror("Error", f"Error adding student: {e}")
        
        submit_btn = tk.Button(window, text="Add Student", command=add_student,
                              bg="#4CAF50", fg="white", font=("Arial", 11), padx=20, pady=10)
        submit_btn.pack(pady=20)
    
    def create_instructors_tab(self):
        """Create instructors tab"""
        instructors_frame = ttk.Frame(self.notebook)
        self.notebook.add(instructors_frame, text="Instructors")
        
        title_label = tk.Label(instructors_frame, text="Instructor Management", 
                              font=("Arial", 16, "bold"), bg='#f0f0f0')
        title_label.pack(pady=10)
        
        tree_frame = tk.Frame(instructors_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Email", "Phone", "DOJ", "Qualification", "Department", "Courses"),
                           show="headings", yscrollcommand=scrollbar.set)
        
        scrollbar.config(command=tree.yview)
        
        tree.heading("ID", text="Instructor ID")
        tree.heading("Name", text="Name")
        tree.heading("Email", text="Email")
        tree.heading("Phone", text="Phone")
        tree.heading("DOJ", text="Date of Joining")
        tree.heading("Qualification", text="Qualification")
        tree.heading("Department", text="Department")
        tree.heading("Courses", text="Courses Taught")
        
        tree.column("ID", width=100)
        tree.column("Name", width=150)
        tree.column("Email", width=200)
        tree.column("Phone", width=120)
        tree.column("DOJ", width=120)
        tree.column("Qualification", width=150)
        tree.column("Department", width=200)
        tree.column("Courses", width=100)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load instructors
        query = """
        SELECT i.Instructor_ID, i.Name, i.Email, i.Phone, i.DOJ, i.Qualification, 
               d.Dept_Name, i.No_of_Courses_Taught
        FROM Instructor i
        LEFT JOIN Department d ON i.Department_ID = d.Department_ID
        ORDER BY i.Instructor_ID
        """
        
        instructors = self.execute_query(query)
        if instructors:
            for instructor in instructors:
                doj = instructor['DOJ'].strftime('%Y-%m-%d') if instructor['DOJ'] else ''
                tree.insert("", tk.END, values=(
                    instructor['Instructor_ID'],
                    instructor['Name'],
                    instructor['Email'] or '',
                    instructor['Phone'] or '',
                    doj,
                    instructor['Qualification'] or '',
                    instructor['Dept_Name'] or '',
                    instructor['No_of_Courses_Taught'] or 0
                ))
    
    def create_courses_tab(self):
        """Create courses tab"""
        courses_frame = ttk.Frame(self.notebook)
        self.notebook.add(courses_frame, text="Courses")
        
        title_label = tk.Label(courses_frame, text="Course Management", 
                              font=("Arial", 16, "bold"), bg='#f0f0f0')
        title_label.pack(pady=10)
        
        tree_frame = tk.Frame(courses_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Credits", "Level", "Department", "Enrolled", "Room", "Capacity"),
                           show="headings", yscrollcommand=scrollbar.set)
        
        scrollbar.config(command=tree.yview)
        
        tree.heading("ID", text="Course ID")
        tree.heading("Name", text="Course Name")
        tree.heading("Credits", text="Credits")
        tree.heading("Level", text="Level")
        tree.heading("Department", text="Department")
        tree.heading("Enrolled", text="Enrolled")
        tree.heading("Room", text="Room Location")
        tree.heading("Capacity", text="Capacity")
        
        tree.column("ID", width=100)
        tree.column("Name", width=200)
        tree.column("Credits", width=80)
        tree.column("Level", width=80)
        tree.column("Department", width=200)
        tree.column("Enrolled", width=80)
        tree.column("Room", width=120)
        tree.column("Capacity", width=80)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load courses
        query = """
        SELECT c.Course_ID, c.Course_Name, c.Credits, c.Course_Level, d.Dept_Name,
               c.No_of_Students_Enrolled, cl.Location AS Room_Location, cl.Capacity
        FROM Course c
        LEFT JOIN Department d ON c.Department_ID = d.Department_ID
        LEFT JOIN Classroom cl ON c.Course_ID = cl.Course_ID
        ORDER BY c.Course_ID
        """
        
        courses = self.execute_query(query)
        if courses:
            for course in courses:
                tree.insert("", tk.END, values=(
                    course['Course_ID'],
                    course['Course_Name'],
                    course['Credits'],
                    course['Course_Level'],
                    course['Dept_Name'] or '',
                    course['No_of_Students_Enrolled'] or 0,
                    course['Room_Location'] or '',
                    course['Capacity'] or ''
                ))
    
    def create_enrollments_tab(self):
        """Create enrollments tab with EnrollStudent procedure"""
        enrollments_frame = ttk.Frame(self.notebook)
        self.notebook.add(enrollments_frame, text="Enrollments")
        
        title_label = tk.Label(enrollments_frame, text="Enrollment Management", 
                              font=("Arial", 16, "bold"), bg='#f0f0f0')
        title_label.pack(pady=10)
        
        btn_frame = tk.Frame(enrollments_frame, bg='#f0f0f0')
        btn_frame.pack(pady=10)
        
        add_btn = tk.Button(btn_frame, text="Enroll Student", command=self.open_enroll_student_window,
                           bg="#4CAF50", fg="white", font=("Arial", 11), padx=15, pady=5)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = tk.Button(btn_frame, text="Refresh", command=lambda: self.refresh_enrollments_table(tree),
                               bg="#2196F3", fg="white", font=("Arial", 11), padx=15, pady=5)
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        tree_frame = tk.Frame(enrollments_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        tree = ttk.Treeview(tree_frame, columns=("ID", "Student", "Course", "Semester", "Grade"),
                           show="headings", yscrollcommand=scrollbar.set)
        
        scrollbar.config(command=tree.yview)
        
        tree.heading("ID", text="Enrollment ID")
        tree.heading("Student", text="Student Name")
        tree.heading("Course", text="Course Name")
        tree.heading("Semester", text="Semester")
        tree.heading("Grade", text="Grade")
        
        tree.column("ID", width=120)
        tree.column("Student", width=200)
        tree.column("Course", width=250)
        tree.column("Semester", width=100)
        tree.column("Grade", width=80)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        enrollments_frame.tree = tree
        
        # Load enrollments
        self.load_enrollments(tree)
    
    def load_enrollments(self, tree):
        """Load enrollments into treeview"""
        for item in tree.get_children():
            tree.delete(item)
        
        query = """
        SELECT e.Enrollment_ID, s.Name AS Student_Name, c.Course_Name, e.Semester, e.Grade
        FROM Enrollment e
        JOIN Student s ON e.Student_ID = s.Student_ID
        JOIN Course c ON e.Course_ID = c.Course_ID
        ORDER BY e.Enrollment_ID
        """
        
        enrollments = self.execute_query(query)
        if enrollments:
            for enrollment in enrollments:
                tree.insert("", tk.END, values=(
                    enrollment['Enrollment_ID'],
                    enrollment['Student_Name'],
                    enrollment['Course_Name'],
                    enrollment['Semester'],
                    enrollment['Grade'] or ''
                ))
    
    def refresh_enrollments_table(self, tree):
        """Refresh enrollments table"""
        self.load_enrollments(tree)
    
    def open_enroll_student_window(self):
        """Open window to enroll student using EnrollStudent procedure"""
        window = tk.Toplevel(self.root)
        window.title("Enroll Student in Course")
        window.geometry("400x400")
        window.configure(bg='#f0f0f0')
        
        tk.Label(window, text="Enrollment ID *", bg='#f0f0f0', font=("Arial", 10)).pack(pady=5)
        enroll_id_entry = tk.Entry(window, font=("Arial", 10), width=30)
        enroll_id_entry.pack(pady=5)
        
        tk.Label(window, text="Student *", bg='#f0f0f0', font=("Arial", 10)).pack(pady=5)
        student_var = tk.StringVar()
        student_combo = ttk.Combobox(window, textvariable=student_var, width=27, state="readonly")
        student_combo.pack(pady=5)
        
        students = self.execute_query("SELECT Student_ID, Name FROM Student ORDER BY Name")
        if students:
            student_dict = {f"{s['Name']} (ID: {s['Student_ID']})": s['Student_ID'] for s in students}
            student_combo['values'] = list(student_dict.keys())
        
        tk.Label(window, text="Course *", bg='#f0f0f0', font=("Arial", 10)).pack(pady=5)
        course_var = tk.StringVar()
        course_combo = ttk.Combobox(window, textvariable=course_var, width=27, state="readonly")
        course_combo.pack(pady=5)
        
        courses = self.execute_query("SELECT Course_ID, Course_Name FROM Course ORDER BY Course_Name")
        if courses:
            course_dict = {f"{c['Course_Name']} (ID: {c['Course_ID']})": c['Course_ID'] for c in courses}
            course_combo['values'] = list(course_dict.keys())
        
        tk.Label(window, text="Semester *", bg='#f0f0f0', font=("Arial", 10)).pack(pady=5)
        semester_entry = tk.Entry(window, font=("Arial", 10), width=30)
        semester_entry.pack(pady=5)
        
        tk.Label(window, text="Grade", bg='#f0f0f0', font=("Arial", 10)).pack(pady=5)
        grade_entry = tk.Entry(window, font=("Arial", 10), width=30)
        grade_entry.pack(pady=5)
        
        def enroll_student():
            """Enroll student using EnrollStudent procedure"""
            try:
                enroll_id = enroll_id_entry.get().strip()
                student_name = student_var.get()
                course_name = course_var.get()
                semester = semester_entry.get().strip()
                grade = grade_entry.get().strip() or None
                
                if not enroll_id or not student_name or not course_name or not semester:
                    messagebox.showerror("Error", "Please fill all required fields (*)")
                    return
                
                student_id = student_dict.get(student_name)
                course_id = course_dict.get(course_name)
                
                # Use EnrollStudent procedure via direct insert (since procedure doesn't take Enrollment_ID)
                # The trigger will update No_of_Students_Enrolled automatically
                query = """
                INSERT INTO Enrollment (Enrollment_ID, Student_ID, Course_ID, Semester, Grade)
                VALUES (%s, %s, %s, %s, %s)
                """
                params = (int(enroll_id), student_id, course_id, semester, grade)
                
                if self.execute_query(query, params, fetch=False):
                    messagebox.showinfo("Success", "Student enrolled successfully!")
                    window.destroy()
                    # Refresh enrollments table
                    for tab_id in range(self.notebook.index("end")):
                        tab = self.notebook.nametowidget(self.notebook.tabs()[tab_id])
                        if hasattr(tab, 'tree'):
                            self.load_enrollments(tab.tree)
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Enrollment ID must be a number.")
            except Error as e:
                messagebox.showerror("Error", f"Error enrolling student: {e}")
        
        submit_btn = tk.Button(window, text="Enroll Student", command=enroll_student,
                              bg="#4CAF50", fg="white", font=("Arial", 11), padx=20, pady=10)
        submit_btn.pack(pady=20)
    
    def create_placements_tab(self):
        """Create placements tab"""
        placements_frame = ttk.Frame(self.notebook)
        self.notebook.add(placements_frame, text="Placements")
        
        title_label = tk.Label(placements_frame, text="Placement Records", 
                              font=("Arial", 16, "bold"), bg='#f0f0f0')
        title_label.pack(pady=10)
        
        tree_frame = tk.Frame(placements_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Type", "Company", "Role", "Package", "Date", "Location"),
                           show="headings", yscrollcommand=scrollbar.set)
        
        scrollbar.config(command=tree.yview)
        
        tree.heading("ID", text="Placement ID")
        tree.heading("Name", text="Person Name")
        tree.heading("Type", text="Type")
        tree.heading("Company", text="Company")
        tree.heading("Role", text="Role")
        tree.heading("Package", text="Package")
        tree.heading("Date", text="Offer Date")
        tree.heading("Location", text="Location")
        
        tree.column("ID", width=100)
        tree.column("Name", width=150)
        tree.column("Type", width=80)
        tree.column("Company", width=150)
        tree.column("Role", width=150)
        tree.column("Package", width=100)
        tree.column("Date", width=120)
        tree.column("Location", width=120)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load placements
        query = """
        SELECT p.Placement_ID, 
               COALESCE(s.Name, a.Name) AS Person_Name,
               CASE WHEN p.Student_ID IS NOT NULL THEN 'Student' ELSE 'Alumni' END AS Person_Type,
               p.Company, p.Role, p.Package, p.Offer_Date, p.Location
        FROM Placement p
        LEFT JOIN Student s ON p.Student_ID = s.Student_ID
        LEFT JOIN Alumni a ON p.Alumni_ID = a.Alumni_ID
        ORDER BY p.Placement_ID
        """
        
        placements = self.execute_query(query)
        if placements:
            for placement in placements:
                offer_date = placement['Offer_Date'].strftime('%Y-%m-%d') if placement['Offer_Date'] else ''
                tree.insert("", tk.END, values=(
                    placement['Placement_ID'],
                    placement['Person_Name'] or '',
                    placement['Person_Type'],
                    placement['Company'],
                    placement['Role'] or '',
                    placement['Package'] or '',
                    offer_date,
                    placement['Location'] or ''
                ))
    
    def create_internships_tab(self):
        """Create internships tab"""
        internships_frame = ttk.Frame(self.notebook)
        self.notebook.add(internships_frame, text="Internships")
        
        title_label = tk.Label(internships_frame, text="Internship Records", 
                              font=("Arial", 16, "bold"), bg='#f0f0f0')
        title_label.pack(pady=10)
        
        tree_frame = tk.Frame(internships_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Type", "Company", "Role", "Duration", "Stipend", "Start", "Mode"),
                           show="headings", yscrollcommand=scrollbar.set)
        
        scrollbar.config(command=tree.yview)
        
        tree.heading("ID", text="Internship ID")
        tree.heading("Name", text="Person Name")
        tree.heading("Type", text="Type")
        tree.heading("Company", text="Company")
        tree.heading("Role", text="Role")
        tree.heading("Duration", text="Duration")
        tree.heading("Stipend", text="Stipend")
        tree.heading("Start", text="Start Date")
        tree.heading("Mode", text="Mode")
        
        tree.column("ID", width=100)
        tree.column("Name", width=150)
        tree.column("Type", width=80)
        tree.column("Company", width=150)
        tree.column("Role", width=150)
        tree.column("Duration", width=100)
        tree.column("Stipend", width=100)
        tree.column("Start", width=120)
        tree.column("Mode", width=100)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load internships
        query = """
        SELECT i.Internship_ID,
               COALESCE(s.Name, a.Name) AS Person_Name,
               CASE WHEN i.Student_ID IS NOT NULL THEN 'Student' ELSE 'Alumni' END AS Person_Type,
               i.Company, i.Role, i.Duration, i.Stipend, i.Start_Date, i.Mode
        FROM Internship i
        LEFT JOIN Student s ON i.Student_ID = s.Student_ID
        LEFT JOIN Alumni a ON i.Alumni_ID = a.Alumni_ID
        ORDER BY i.Internship_ID
        """
        
        internships = self.execute_query(query)
        if internships:
            for internship in internships:
                start_date = internship['Start_Date'].strftime('%Y-%m-%d') if internship['Start_Date'] else ''
                tree.insert("", tk.END, values=(
                    internship['Internship_ID'],
                    internship['Person_Name'] or '',
                    internship['Person_Type'],
                    internship['Company'],
                    internship['Role'] or '',
                    internship['Duration'] or '',
                    internship['Stipend'] or '',
                    start_date,
                    internship['Mode'] or ''
                ))
    
    def create_reports_tab(self):
        """Create reports tab with all database views"""
        reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(reports_frame, text="Reports")
        
        title_label = tk.Label(reports_frame, text="Database Views & Reports", 
                              font=("Arial", 16, "bold"), bg='#f0f0f0')
        title_label.pack(pady=10)
        
        # Notebook for different views
        view_notebook = ttk.Notebook(reports_frame)
        view_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Student Performance View
        self.create_view_tab(view_notebook, "Student Performance", "v_student_performance",
                            ["Student_ID", "Name", "Course_Name", "Semester", "Grade"])
        
        # Instructor Workload View
        self.create_view_tab(view_notebook, "Instructor Workload", "v_instructor_workload",
                            ["Instructor_ID", "Instructor_Name", "Courses_Taught", "Courses"])
        
        # Course Enrollment View
        self.create_view_tab(view_notebook, "Course Enrollment", "v_course_enrollment",
                            ["Course_ID", "Course_Name", "Enrolled_Students", "Capacity"])
        
        # Alumni Placements View
        self.create_view_tab(view_notebook, "Alumni Placements", "v_alumni_placements",
                            ["Alumni_ID", "Name", "Graduation_Year", "CGPA", "Company", "Role", "Package", "Offer_Date"])
        
        # Student Internships View
        self.create_view_tab(view_notebook, "Student Internships", "v_student_internships",
                            ["Student_ID", "Name", "Company", "Role", "Start_Date", "End_Date", "Mode"])
    
    def create_view_tab(self, notebook, title, view_name, columns):
        """Create a tab for a database view"""
        view_frame = ttk.Frame(notebook)
        notebook.add(view_frame, text=title)
        
        tree_frame = tk.Frame(view_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        scrollbar_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings",
                           yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        scrollbar_y.config(command=tree.yview)
        scrollbar_x.config(command=tree.xview)
        
        # Configure columns
        for col in columns:
            tree.heading(col, text=col.replace("_", " "))
            tree.column(col, width=120)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Load view data
        query = f"SELECT * FROM {view_name}"
        results = self.execute_query(query)
        
        if results:
            for row in results:
                values = tuple(str(row.get(col, '')) if row.get(col) is not None else '' 
                              for col in columns)
                # Handle date objects
                formatted_values = []
                for val in values:
                    if isinstance(val, str) and len(val) > 10:
                        try:
                            dt = datetime.strptime(val, '%Y-%m-%d %H:%M:%S')
                            formatted_values.append(dt.strftime('%Y-%m-%d'))
                        except:
                            formatted_values.append(val)
                    else:
                        formatted_values.append(val)
                tree.insert("", tk.END, values=tuple(formatted_values))
    
    def create_functions_tab(self):
        """Create functions tab to test SQL functions"""
        functions_frame = ttk.Frame(self.notebook)
        self.notebook.add(functions_frame, text="Functions")
        
        title_label = tk.Label(functions_frame, text="SQL Functions Testing", 
                              font=("Arial", 16, "bold"), bg='#f0f0f0')
        title_label.pack(pady=10)
        
        # Function 1: GetCourseEnrollment
        func1_frame = tk.LabelFrame(functions_frame, text="GetCourseEnrollment", 
                                    font=("Arial", 12, "bold"), bg='#f0f0f0', padx=20, pady=20)
        func1_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(func1_frame, text="Course ID:", bg='#f0f0f0', font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
        course_id_entry = tk.Entry(func1_frame, font=("Arial", 10), width=20)
        course_id_entry.pack(side=tk.LEFT, padx=10)
        
        result_label1 = tk.Label(func1_frame, text="Result: -", bg='#f0f0f0', font=("Arial", 10, "bold"))
        result_label1.pack(side=tk.LEFT, padx=20)
        
        def get_course_enrollment():
            try:
                course_id = int(course_id_entry.get())
                query = "SELECT GetCourseEnrollment(%s) AS EnrollmentCount"
                result = self.execute_query(query, (course_id,))
                if result:
                    count = result[0]['EnrollmentCount']
                    result_label1.config(text=f"Result: {count} students enrolled")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid Course ID")
        
        tk.Button(func1_frame, text="Get Enrollment", command=get_course_enrollment,
                 bg="#2196F3", fg="white", font=("Arial", 10), padx=15, pady=5).pack(side=tk.LEFT, padx=10)
        
        # Function 2: IsStudentEnrolled
        func2_frame = tk.LabelFrame(functions_frame, text="IsStudentEnrolled", 
                                    font=("Arial", 12, "bold"), bg='#f0f0f0', padx=20, pady=20)
        func2_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(func2_frame, text="Student ID:", bg='#f0f0f0', font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
        student_id_entry = tk.Entry(func2_frame, font=("Arial", 10), width=20)
        student_id_entry.pack(side=tk.LEFT, padx=10)
        
        tk.Label(func2_frame, text="Course ID:", bg='#f0f0f0', font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
        course_id_entry2 = tk.Entry(func2_frame, font=("Arial", 10), width=20)
        course_id_entry2.pack(side=tk.LEFT, padx=10)
        
        result_label2 = tk.Label(func2_frame, text="Result: -", bg='#f0f0f0', font=("Arial", 10, "bold"))
        result_label2.pack(side=tk.LEFT, padx=20)
        
        def check_enrollment():
            try:
                student_id = int(student_id_entry.get())
                course_id = int(course_id_entry2.get())
                query = "SELECT IsStudentEnrolled(%s, %s) AS IsEnrolled"
                result = self.execute_query(query, (student_id, course_id))
                if result:
                    enrolled = result[0]['IsEnrolled']
                    result_label2.config(text=f"Result: {enrolled}")
            except ValueError:
                messagebox.showerror("Error", "Please enter valid IDs")
        
        tk.Button(func2_frame, text="Check Enrollment", command=check_enrollment,
                 bg="#2196F3", fg="white", font=("Arial", 10), padx=15, pady=5).pack(side=tk.LEFT, padx=10)
        
        # Function 3: GetStudentCredits
        func3_frame = tk.LabelFrame(functions_frame, text="GetStudentCredits", 
                                    font=("Arial", 12, "bold"), bg='#f0f0f0', padx=20, pady=20)
        func3_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(func3_frame, text="Student ID:", bg='#f0f0f0', font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
        student_id_entry3 = tk.Entry(func3_frame, font=("Arial", 10), width=20)
        student_id_entry3.pack(side=tk.LEFT, padx=10)
        
        result_label3 = tk.Label(func3_frame, text="Result: -", bg='#f0f0f0', font=("Arial", 10, "bold"))
        result_label3.pack(side=tk.LEFT, padx=20)
        
        def get_credits():
            try:
                student_id = int(student_id_entry3.get())
                query = "SELECT GetStudentCredits(%s) AS TotalCredits"
                result = self.execute_query(query, (student_id,))
                if result:
                    credits = result[0]['TotalCredits']
                    result_label3.config(text=f"Result: {credits} credits")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid Student ID")
        
        tk.Button(func3_frame, text="Get Credits", command=get_credits,
                 bg="#2196F3", fg="white", font=("Arial", 10), padx=15, pady=5).pack(side=tk.LEFT, padx=10)
        
        # Function 4: IsCourseFull
        func4_frame = tk.LabelFrame(functions_frame, text="IsCourseFull", 
                                    font=("Arial", 12, "bold"), bg='#f0f0f0', padx=20, pady=20)
        func4_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(func4_frame, text="Course ID:", bg='#f0f0f0', font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
        course_id_entry4 = tk.Entry(func4_frame, font=("Arial", 10), width=20)
        course_id_entry4.pack(side=tk.LEFT, padx=10)
        
        result_label4 = tk.Label(func4_frame, text="Result: -", bg='#f0f0f0', font=("Arial", 10, "bold"))
        result_label4.pack(side=tk.LEFT, padx=20)
        
        def check_full():
            try:
                course_id = int(course_id_entry4.get())
                query = "SELECT IsCourseFull(%s) AS IsFull"
                result = self.execute_query(query, (course_id,))
                if result:
                    is_full = result[0]['IsFull']
                    result_label4.config(text=f"Result: {is_full}")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid Course ID")
        
        tk.Button(func4_frame, text="Check if Full", command=check_full,
                 bg="#2196F3", fg="white", font=("Arial", 10), padx=15, pady=5).pack(side=tk.LEFT, padx=10)
    
    def on_closing(self):
        """Handle window close"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = CourseManagementSystem(root)
    root.mainloop()


if __name__ == "__main__":
    main()

