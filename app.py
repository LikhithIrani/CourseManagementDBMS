# app.py
"""
Course Management - Tkinter Frontend
Assumes your MySQL DB 'CourseManagement' exists (script from code.sql).
Requires: pymysql

Edit DB connection at DB_CONFIG below, then run: python app.py
"""

import pymysql
from tkinter import *
from tkinter import ttk, messagebox, simpledialog

DB_CONFIG = {
  "host": "localhost",
  "user": "appuser",
  "password": "AppPass123!",
  "database": "CourseManagement",
  "port": 3306
}

# --------------------
# Database helper
# --------------------
class DB:
    def __init__(self, cfg):
        self.cfg = cfg
        self.conn = None
        self.connect()

    def connect(self):
        try:
            self.conn = pymysql.connect(
                host=self.cfg["host"],
                user=self.cfg["user"],
                password=self.cfg["password"],
                database=self.cfg["database"],
                port=self.cfg.get("port", 3306),
                charset="utf8mb4",
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True
            )
        except Exception as e:
            messagebox.showerror("DB Connection Error", f"Could not connect to DB:\n{e}")
            raise

    def query(self, sql, params=None):
        with self.conn.cursor() as cur:
            cur.execute(sql, params or ())
            try:
                return cur.fetchall()
            except:
                return None

    def execute(self, sql, params=None):
        with self.conn.cursor() as cur:
            cur.execute(sql, params or ())
            # autocommit True -> immediate

    def callproc(self, proc_name, params=()):
        with self.conn.cursor() as cur:
            cur.callproc(proc_name, params)
            try:
                return cur.fetchall()
            except:
                return None

# --------------------
# Main Application
# --------------------
class App:
    def __init__(self, root, db: DB):
        self.root = root
        self.db = db
        root.title("Course Management System")
        root.geometry("1000x620")
        self.style = ttk.Style(root)
        # Tabs
        self.nb = ttk.Notebook(root)
        self.nb.pack(fill=BOTH, expand=True)

        # Prepare tabs
        self.student_tab = Frame(self.nb)
        self.instructor_tab = Frame(self.nb)
        self.course_tab = Frame(self.nb)
        self.enroll_tab = Frame(self.nb)
        self.report_tab = Frame(self.nb)

        self.nb.add(self.student_tab, text="Students")
        self.nb.add(self.instructor_tab, text="Instructors")
        self.nb.add(self.course_tab, text="Courses")
        self.nb.add(self.enroll_tab, text="Enrollment")
        self.nb.add(self.report_tab, text="Reports")

        # Build each tab
        self.build_students_tab()
        self.build_instructors_tab()
        self.build_courses_tab()
        self.build_enroll_tab()
        self.build_report_tab()

    # --------------------
    # Students Tab
    # --------------------
    def build_students_tab(self):
        frame = self.student_tab

        left = Frame(frame, padx=8, pady=8)
        left.pack(side=LEFT, fill=Y)

        Label(left, text="Add / Update Student", font=("Arial", 12, "bold")).pack(anchor=W, pady=(0,8))
        self.s_id_var = StringVar()
        self.s_name_var = StringVar()
        self.s_email_var = StringVar()
        self.s_phone_var = StringVar()
        self.s_dob_var = StringVar()
        self.s_year_var = StringVar()
        self.s_dept_var = StringVar()

        entries = [
            ("Student ID", self.s_id_var),
            ("Name", self.s_name_var),
            ("Email", self.s_email_var),
            ("Phone", self.s_phone_var),
            ("DOB (YYYY-MM-DD)", self.s_dob_var),
            ("Year", self.s_year_var),
            ("Department ID", self.s_dept_var)
        ]
        for lbl, var in entries:
            Frame(left).pack(fill=X, pady=2)
            Label(left, text=lbl).pack(anchor=W)
            Entry(left, textvariable=var).pack(fill=X)

        btn_frame = Frame(left, pady=8)
        btn_frame.pack(fill=X)
        Button(btn_frame, text="Add Student", command=self.add_student).pack(side=LEFT, padx=4)
        Button(btn_frame, text="Update Student", command=self.update_student).pack(side=LEFT, padx=4)
        Button(btn_frame, text="Delete Student", command=self.delete_student).pack(side=LEFT, padx=4)
        Button(btn_frame, text="Clear Fields", command=self.clear_student_fields).pack(side=LEFT, padx=4)

        # Right pane - list
        right = Frame(frame, padx=8, pady=8)
        right.pack(side=LEFT, fill=BOTH, expand=True)
        Label(right, text="Students List", font=("Arial", 12, "bold")).pack(anchor=W)
        cols = ("Student_ID", "Name", "Email", "Phone", "DOB", "Year_of_Study", "Department_ID")
        self.student_tree = ttk.Treeview(right, columns=cols, show="headings")
        for c in cols:
            self.student_tree.heading(c, text=c)
            self.student_tree.column(c, width=120, anchor=W)
        self.student_tree.pack(fill=BOTH, expand=True)
        self.student_tree.bind("<<TreeviewSelect>>", self.on_student_select)

        Button(right, text="Refresh", command=self.load_students).pack(pady=6)
        self.load_students()

    def load_students(self):
        self.student_tree.delete(*self.student_tree.get_children())
        rows = self.db.query("SELECT * FROM Student ORDER BY Student_ID")
        for r in rows:
            self.student_tree.insert("", END, values=(r["Student_ID"], r["Name"], r["Email"], r["Phone"], str(r["DOB"]), r["Year_of_Study"], r["Department_ID"]))

    def clear_student_fields(self):
        for v in [self.s_id_var, self.s_name_var, self.s_email_var, self.s_phone_var, self.s_dob_var, self.s_year_var, self.s_dept_var]:
            v.set("")

    def on_student_select(self, event):
        sel = self.student_tree.selection()
        if not sel:
            return
        vals = self.student_tree.item(sel[0], "values")
        self.s_id_var.set(vals[0])
        self.s_name_var.set(vals[1])
        self.s_email_var.set(vals[2])
        self.s_phone_var.set(vals[3])
        self.s_dob_var.set(vals[4])
        self.s_year_var.set(vals[5])
        self.s_dept_var.set(vals[6])

    def add_student(self):
        try:
            name = self.s_name_var.get().strip()
            email = self.s_email_var.get().strip()
            if not name:
                messagebox.showwarning("Validation", "Name is required")
                return
            sql = "INSERT INTO Student (Student_ID, Name, Email, Phone, DOB, Year_of_Study, Department_ID) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            sid = self.s_id_var.get().strip()
            if not sid:
                # allow DB to auto-generate? In schema Student_ID is PK with no auto-increment.
                messagebox.showwarning("Validation", "Student_ID is required (enter unique int)")
                return
            params = (int(sid), name, email or None, self.s_phone_var.get() or None, self.s_dob_var.get() or None, int(self.s_year_var.get()) if self.s_year_var.get() else None, int(self.s_dept_var.get()) if self.s_dept_var.get() else None)
            self.db.execute(sql, params)
            messagebox.showinfo("Success", "Student added")
            self.load_students()
            self.clear_student_fields()
        except Exception as e:
            messagebox.showerror("Error adding student", str(e))

    def update_student(self):
        try:
            sid = self.s_id_var.get().strip()
            if not sid:
                messagebox.showwarning("Validation", "Select a student or provide Student_ID")
                return
            sql = "UPDATE Student SET Name=%s, Email=%s, Phone=%s, DOB=%s, Year_of_Study=%s, Department_ID=%s WHERE Student_ID=%s"
            params = (self.s_name_var.get() or None, self.s_email_var.get() or None, self.s_phone_var.get() or None, self.s_dob_var.get() or None, int(self.s_year_var.get()) if self.s_year_var.get() else None, int(self.s_dept_var.get()) if self.s_dept_var.get() else None, int(sid))
            self.db.execute(sql, params)
            messagebox.showinfo("Success", "Student updated")
            self.load_students()
            self.clear_student_fields()
        except Exception as e:
            messagebox.showerror("Error updating student", str(e))

    def delete_student(self):
        try:
            sid = self.s_id_var.get().strip()
            if not sid:
                messagebox.showwarning("Validation", "Select student to delete")
                return
            if not messagebox.askyesno("Confirm", f"Delete student {sid}?"):
                return
            self.db.execute("DELETE FROM Student WHERE Student_ID=%s", (int(sid),))
            messagebox.showinfo("Deleted", "Student deleted")
            self.load_students()
            self.clear_student_fields()
        except Exception as e:
            messagebox.showerror("Error deleting student", str(e))

    # --------------------
    # Instructors Tab
    # --------------------
    def build_instructors_tab(self):
        frame = self.instructor_tab
        left = Frame(frame, padx=8, pady=8)
        left.pack(side=LEFT, fill=Y)

        Label(left, text="Add / Update Instructor", font=("Arial", 12, "bold")).pack(anchor=W, pady=(0,8))
        self.i_id_var = StringVar()
        self.i_name_var = StringVar()
        self.i_email_var = StringVar()
        self.i_phone_var = StringVar()
        self.i_doj_var = StringVar()
        self.i_qual_var = StringVar()
        self.i_dept_var = StringVar()

        entries = [
            ("Instructor ID", self.i_id_var),
            ("Name", self.i_name_var),
            ("Email", self.i_email_var),
            ("Phone", self.i_phone_var),
            ("DOJ (YYYY-MM-DD)", self.i_doj_var),
            ("Qualification", self.i_qual_var),
            ("Department ID", self.i_dept_var)
        ]
        for lbl, var in entries:
            Frame(left).pack(fill=X, pady=2)
            Label(left, text=lbl).pack(anchor=W)
            Entry(left, textvariable=var).pack(fill=X)

        btn_frame = Frame(left, pady=8)
        btn_frame.pack(fill=X)
        Button(btn_frame, text="Add Instructor", command=self.add_instructor).pack(side=LEFT, padx=4)
        Button(btn_frame, text="Update Instructor", command=self.update_instructor).pack(side=LEFT, padx=4)
        Button(btn_frame, text="Delete Instructor", command=self.delete_instructor).pack(side=LEFT, padx=4)
        Button(btn_frame, text="Clear", command=self.clear_instructor_fields).pack(side=LEFT, padx=4)

        right = Frame(frame, padx=8, pady=8)
        right.pack(side=LEFT, fill=BOTH, expand=True)
        Label(right, text="Instructors List", font=("Arial", 12, "bold")).pack(anchor=W)
        cols = ("Instructor_ID", "Name", "Email", "Phone", "DOJ", "Qualification", "Department_ID", "No_of_Courses_Taught")
        self.instructor_tree = ttk.Treeview(right, columns=cols, show="headings")
        for c in cols:
            self.instructor_tree.heading(c, text=c)
            self.instructor_tree.column(c, width=120, anchor=W)
        self.instructor_tree.pack(fill=BOTH, expand=True)
        self.instructor_tree.bind("<<TreeviewSelect>>", self.on_instructor_select)
        Button(right, text="Refresh", command=self.load_instructors).pack(pady=6)
        self.load_instructors()

    def load_instructors(self):
        self.instructor_tree.delete(*self.instructor_tree.get_children())
        rows = self.db.query("SELECT * FROM Instructor ORDER BY Instructor_ID")
        for r in rows:
            # No_of_Courses_Taught might be NULL if not added; default to 0
            noc = r.get("No_of_Courses_Taught", 0)
            self.instructor_tree.insert("", END, values=(r["Instructor_ID"], r["Name"], r["Email"], r["Phone"], str(r["DOJ"]), r["Qualification"], r["Department_ID"], noc))

    def clear_instructor_fields(self):
        for v in [self.i_id_var, self.i_name_var, self.i_email_var, self.i_phone_var, self.i_doj_var, self.i_qual_var, self.i_dept_var]:
            v.set("")

    def on_instructor_select(self, event):
        sel = self.instructor_tree.selection()
        if not sel:
            return
        vals = self.instructor_tree.item(sel[0], "values")
        self.i_id_var.set(vals[0])
        self.i_name_var.set(vals[1])
        self.i_email_var.set(vals[2])
        self.i_phone_var.set(vals[3])
        self.i_doj_var.set(vals[4])
        self.i_qual_var.set(vals[5])
        self.i_dept_var.set(vals[6])

    def add_instructor(self):
        try:
            if not self.i_id_var.get().strip() or not self.i_name_var.get().strip():
                messagebox.showwarning("Validation", "Instructor ID and Name required")
                return
            sql = "INSERT INTO Instructor (Instructor_ID, Name, Email, Phone, DOJ, Qualification, Department_ID) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            params = (int(self.i_id_var.get()), self.i_name_var.get(), self.i_email_var.get() or None, self.i_phone_var.get() or None, self.i_doj_var.get() or None, self.i_qual_var.get() or None, int(self.i_dept_var.get()) if self.i_dept_var.get() else None)
            self.db.execute(sql, params)
            messagebox.showinfo("Success", "Instructor added")
            self.load_instructors()
            self.clear_instructor_fields()
        except Exception as e:
            messagebox.showerror("Error adding instructor", str(e))

    def update_instructor(self):
        try:
            if not self.i_id_var.get().strip():
                messagebox.showwarning("Validation", "Select an instructor or provide ID")
                return
            sql = "UPDATE Instructor SET Name=%s, Email=%s, Phone=%s, DOJ=%s, Qualification=%s, Department_ID=%s WHERE Instructor_ID=%s"
            params = (self.i_name_var.get() or None, self.i_email_var.get() or None, self.i_phone_var.get() or None, self.i_doj_var.get() or None, self.i_qual_var.get() or None, int(self.i_dept_var.get()) if self.i_dept_var.get() else None, int(self.i_id_var.get()))
            self.db.execute(sql, params)
            messagebox.showinfo("Success", "Instructor updated")
            self.load_instructors()
            self.clear_instructor_fields()
        except Exception as e:
            messagebox.showerror("Error updating instructor", str(e))

    def delete_instructor(self):
        try:
            if not self.i_id_var.get().strip():
                messagebox.showwarning("Validation", "Select instructor to delete")
                return
            if not messagebox.askyesno("Confirm", f"Delete instructor {self.i_id_var.get()}?"):
                return
            self.db.execute("DELETE FROM Instructor WHERE Instructor_ID=%s", (int(self.i_id_var.get()),))
            messagebox.showinfo("Deleted", "Instructor deleted")
            self.load_instructors()
            self.clear_instructor_fields()
        except Exception as e:
            messagebox.showerror("Error deleting instructor", str(e))

    # --------------------
    # Courses Tab
    # --------------------
    def build_courses_tab(self):
        frame = self.course_tab
        left = Frame(frame, padx=8, pady=8)
        left.pack(side=LEFT, fill=Y)

        Label(left, text="Add / Update Course", font=("Arial", 12, "bold")).pack(anchor=W, pady=(0,8))
        self.c_id_var = StringVar()
        self.c_name_var = StringVar()
        self.c_credits_var = StringVar()
        self.c_level_var = StringVar()
        self.c_dept_var = StringVar()

        entries = [
            ("Course ID", self.c_id_var),
            ("Course Name", self.c_name_var),
            ("Credits", self.c_credits_var),
            ("Course Level (UG/PG)", self.c_level_var),
            ("Department ID", self.c_dept_var)
        ]
        for lbl, var in entries:
            Frame(left).pack(fill=X, pady=2)
            Label(left, text=lbl).pack(anchor=W)
            Entry(left, textvariable=var).pack(fill=X)

        btn_frame = Frame(left, pady=8)
        btn_frame.pack(fill=X)
        Button(btn_frame, text="Add Course", command=self.add_course).pack(side=LEFT, padx=4)
        Button(btn_frame, text="Update Course", command=self.update_course).pack(side=LEFT, padx=4)
        Button(btn_frame, text="Delete Course", command=self.delete_course).pack(side=LEFT, padx=4)
        Button(btn_frame, text="Clear", command=self.clear_course_fields).pack(side=LEFT, padx=4)

        right = Frame(frame, padx=8, pady=8)
        right.pack(side=LEFT, fill=BOTH, expand=True)
        Label(right, text="Courses List", font=("Arial", 12, "bold")).pack(anchor=W)
        cols = ("Course_ID", "Course_Name", "Credits", "Course_Level", "No_of_Students_Enrolled", "Department_ID")
        self.course_tree = ttk.Treeview(right, columns=cols, show="headings")
        for c in cols:
            self.course_tree.heading(c, text=c)
            self.course_tree.column(c, width=140, anchor=W)
        self.course_tree.pack(fill=BOTH, expand=True)
        self.course_tree.bind("<<TreeviewSelect>>", self.on_course_select)
        Button(right, text="Refresh", command=self.load_courses).pack(pady=6)
        self.load_courses()

    def load_courses(self):
        self.course_tree.delete(*self.course_tree.get_children())
        rows = self.db.query("SELECT * FROM Course ORDER BY Course_ID")
        for r in rows:
            self.course_tree.insert("", END, values=(r["Course_ID"], r["Course_Name"], r["Credits"], r["Course_Level"], r["No_of_Students_Enrolled"], r["Department_ID"]))

    def clear_course_fields(self):
        for v in [self.c_id_var, self.c_name_var, self.c_credits_var, self.c_level_var, self.c_dept_var]:
            v.set("")

    def on_course_select(self, event):
        sel = self.course_tree.selection()
        if not sel:
            return
        vals = self.course_tree.item(sel[0], "values")
        self.c_id_var.set(vals[0])
        self.c_name_var.set(vals[1])
        self.c_credits_var.set(vals[2])
        self.c_level_var.set(vals[3])
        # no_of_students read-only
        self.c_dept_var.set(vals[5])

    def add_course(self):
        try:
            if not self.c_id_var.get().strip() or not self.c_name_var.get().strip():
                messagebox.showwarning("Validation", "Course ID and Name required")
                return
            sql = "INSERT INTO Course (Course_ID, Course_Name, Credits, Course_Level, No_of_Students_Enrolled, Department_ID) VALUES (%s,%s,%s,%s,%s,%s)"
            params = (int(self.c_id_var.get()), self.c_name_var.get(), int(self.c_credits_var.get()) if self.c_credits_var.get() else None, self.c_level_var.get() or None, 0, int(self.c_dept_var.get()) if self.c_dept_var.get() else None)
            self.db.execute(sql, params)
            messagebox.showinfo("Success", "Course added")
            self.load_courses()
            self.clear_course_fields()
        except Exception as e:
            messagebox.showerror("Error adding course", str(e))

    def update_course(self):
        try:
            if not self.c_id_var.get().strip():
                messagebox.showwarning("Validation", "Select a course or enter Course ID")
                return
            sql = "UPDATE Course SET Course_Name=%s, Credits=%s, Course_Level=%s, Department_ID=%s WHERE Course_ID=%s"
            params = (self.c_name_var.get() or None, int(self.c_credits_var.get()) if self.c_credits_var.get() else None, self.c_level_var.get() or None, int(self.c_dept_var.get()) if self.c_dept_var.get() else None, int(self.c_id_var.get()))
            self.db.execute(sql, params)
            messagebox.showinfo("Success", "Course updated")
            self.load_courses()
            self.clear_course_fields()
        except Exception as e:
            messagebox.showerror("Error updating course", str(e))

    def delete_course(self):
        try:
            if not self.c_id_var.get().strip():
                messagebox.showwarning("Validation", "Select course to delete")
                return
            if not messagebox.askyesno("Confirm", f"Delete course {self.c_id_var.get()}?"):
                return
            self.db.execute("DELETE FROM Course WHERE Course_ID=%s", (int(self.c_id_var.get()),))
            messagebox.showinfo("Deleted", "Course deleted")
            self.load_courses()
            self.clear_course_fields()
        except Exception as e:
            messagebox.showerror("Error deleting course", str(e))

    # --------------------
    # Enrollment Tab
    # --------------------
    def build_enroll_tab(self):
        frame = self.enroll_tab
        top = Frame(frame, padx=8, pady=8)
        top.pack(side=TOP, fill=X)
        Label(top, text="Enroll / Unenroll Student", font=("Arial", 12, "bold")).pack(anchor=W)
        f = Frame(top)
        f.pack(fill=X, pady=(6,0))

        Label(f, text="Student ID").grid(row=0, column=0, sticky=W, padx=4, pady=2)
        Label(f, text="Course ID").grid(row=0, column=2, sticky=W, padx=4, pady=2)
        Label(f, text="Semester").grid(row=0, column=4, sticky=W, padx=4, pady=2)
        Label(f, text="Grade").grid(row=0, column=6, sticky=W, padx=4, pady=2)

        self.en_sid = StringVar()
        self.en_cid = StringVar()
        self.en_sem = StringVar()
        self.en_grade = StringVar()

        Entry(f, textvariable=self.en_sid, width=12).grid(row=0, column=1, padx=4)
        Entry(f, textvariable=self.en_cid, width=12).grid(row=0, column=3, padx=4)
        Entry(f, textvariable=self.en_sem, width=12).grid(row=0, column=5, padx=4)
        Entry(f, textvariable=self.en_grade, width=8).grid(row=0, column=7, padx=4)

        btn_frame = Frame(top)
        btn_frame.pack(fill=X, pady=6)
        Button(btn_frame, text="Enroll Student", command=self.enroll_student).pack(side=LEFT, padx=6)
        Button(btn_frame, text="Unenroll (Delete)", command=self.unenroll_student).pack(side=LEFT, padx=6)
        Button(btn_frame, text="Show Enrollments for Course", command=self.show_course_enrollments).pack(side=LEFT, padx=6)

        # List enrollments for selected course
        bottom = Frame(frame, padx=8, pady=8)
        bottom.pack(fill=BOTH, expand=True)
        Label(bottom, text="Enrollments", font=("Arial", 12, "bold")).pack(anchor=W)
        cols = ("Enrollment_ID", "Student_ID", "Course_ID", "Semester", "Grade")
        self.enroll_tree = ttk.Treeview(bottom, columns=cols, show="headings")
        for c in cols:
            self.enroll_tree.heading(c, text=c)
            self.enroll_tree.column(c, width=120)
        self.enroll_tree.pack(fill=BOTH, expand=True)
        Button(bottom, text="Refresh All Enrollments", command=self.load_enrollments).pack(pady=6)
        self.load_enrollments()

    def load_enrollments(self):
        self.enroll_tree.delete(*self.enroll_tree.get_children())
        rows = self.db.query("SELECT * FROM Enrollment ORDER BY Enrollment_ID")
        for r in rows:
            self.enroll_tree.insert("", END, values=(r["Enrollment_ID"], r["Student_ID"], r["Course_ID"], r["Semester"], r["Grade"]))

    def enroll_student(self):
        try:
            sid = self.en_sid.get().strip()
            cid = self.en_cid.get().strip()
            sem = self.en_sem.get().strip() or "Sem 1"
            grade = self.en_grade.get().strip() or None
            if not sid or not cid:
                messagebox.showwarning("Validation", "Student ID and Course ID required")
                return
            # Use stored procedure EnrollStudent if present:
            try:
                self.db.callproc("EnrollStudent", (int(sid), int(cid), sem, grade))
                messagebox.showinfo("Success", "Student enrolled via stored procedure")
            except Exception as e:
                # fallback to direct insert (in case SP not present)
                self.db.execute("INSERT INTO Enrollment (Student_ID, Course_ID, Semester, Grade) VALUES (%s,%s,%s,%s)", (int(sid), int(cid), sem, grade))
                messagebox.showinfo("Success", "Student enrolled (direct insert)")
            self.load_enrollments()
            self.load_courses()  # to refresh No_of_Students_Enrolled (trigger)
        except Exception as e:
            messagebox.showerror("Enrollment Error", str(e))

    def unenroll_student(self):
        try:
            sid = self.en_sid.get().strip()
            cid = self.en_cid.get().strip()
            if not sid or not cid:
                messagebox.showwarning("Validation", "Student ID and Course ID required")
                return
            # find enrollment id(s)
            rows = self.db.query("SELECT Enrollment_ID FROM Enrollment WHERE Student_ID=%s AND Course_ID=%s", (int(sid), int(cid)))
            if not rows:
                messagebox.showinfo("Info", "No matching enrollment found")
                return
            # confirm deletion
            if not messagebox.askyesno("Confirm", f"Delete {len(rows)} enrollment(s) for Student {sid} in Course {cid}?"):
                return
            for r in rows:
                self.db.execute("DELETE FROM Enrollment WHERE Enrollment_ID=%s", (r["Enrollment_ID"],))
            messagebox.showinfo("Success", "Enrollment(s) deleted")
            self.load_enrollments()
            self.load_courses()
        except Exception as e:
            messagebox.showerror("Unenroll Error", str(e))

    def show_course_enrollments(self):
        cid = self.en_cid.get().strip()
        if not cid:
            messagebox.showwarning("Validation", "Enter Course ID to list enrollments")
            return
        rows = self.db.query("SELECT e.Enrollment_ID, s.Student_ID, s.Name, e.Semester, e.Grade FROM Enrollment e JOIN Student s ON e.Student_ID = s.Student_ID WHERE e.Course_ID=%s", (int(cid),))
        # show results in a temporary dialog
        if not rows:
            messagebox.showinfo("No rows", "No enrollments for this course")
            return
        dlg = Toplevel(self.root)
        dlg.title(f"Enrollments for Course {cid}")
        cols = ("Enrollment_ID", "Student_ID", "Name", "Semester", "Grade")
        tree = ttk.Treeview(dlg, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=120)
        tree.pack(fill=BOTH, expand=True)
        for r in rows:
            tree.insert("", END, values=(r["Enrollment_ID"], r["Student_ID"], r["Name"], r["Semester"], r["Grade"]))
        Button(dlg, text="Close", command=dlg.destroy).pack(pady=6)

    # --------------------
    # Reports Tab
    # --------------------
    def build_report_tab(self):
        frame = self.report_tab
        left = Frame(frame, padx=8, pady=8)
        left.pack(side=LEFT, fill=Y)

        Label(left, text="Reports / Stored Proc Calls", font=("Arial", 12, "bold")).pack(anchor=W, pady=(0,8))

        # Get student semester report
        Label(left, text="Student Semester Report").pack(anchor=W, pady=(4,0))
        self.r_student_id = StringVar()
        self.r_semester = StringVar()
        Entry(left, textvariable=self.r_student_id).pack(fill=X, pady=2)
        Entry(left, textvariable=self.r_semester).pack(fill=X, pady=(0,6))
        Button(left, text="Get Student Semester Report", command=self.get_student_sem_report).pack(fill=X, pady=(0,8))

        # Get course enrollment count (function)
        Label(left, text="Course Enrollment Count (function GetCourseEnrollment)").pack(anchor=W, pady=(4,0))
        self.r_course_id = StringVar()
        Entry(left, textvariable=self.r_course_id).pack(fill=X, pady=2)
        Button(left, text="Get Course Enrollment Count", command=self.get_course_enrollment_count).pack(fill=X, pady=(0,8))

        # IsCourseFull
        Label(left, text="Check if Course is Full (function IsCourseFull)").pack(anchor=W, pady=(4,0))
        self.r_course_full_id = StringVar()
        Entry(left, textvariable=self.r_course_full_id).pack(fill=X, pady=2)
        Button(left, text="Is Course Full?", command=self.is_course_full).pack(fill=X, pady=(0,8))

        # Output area
        right = Frame(frame, padx=8, pady=8)
        right.pack(side=LEFT, fill=BOTH, expand=True)
        Label(right, text="Report Output", font=("Arial", 12, "bold")).pack(anchor=W)
        self.report_tree = ttk.Treeview(right, columns=("c1","c2","c3","c4","c5"), show="headings")
        for i in range(1,6):
            self.report_tree.heading(f"c{i}", text=f"C{i}")
            self.report_tree.column(f"c{i}", width=180)
        self.report_tree.pack(fill=BOTH, expand=True)
        Button(right, text="Clear Output", command=lambda: self.report_tree.delete(*self.report_tree.get_children())).pack(pady=6)

    def get_student_sem_report(self):
        sid = self.r_student_id.get().strip()
        sem = self.r_semester.get().strip()
        if not sid or not sem:
            messagebox.showwarning("Validation", "Student ID and Semester required")
            return
        try:
            # Use stored procedure if available
            rows = None
            try:
                rows = self.db.callproc("GetStudentSemesterReport", (int(sid), sem))
            except Exception:
                # fallback to select
                rows = self.db.query("""
                    SELECT c.Course_Name, e.Grade, i.Name AS Instructor_Name
                    FROM Enrollment e
                    JOIN Course c ON e.Course_ID = c.Course_ID
                    LEFT JOIN Teaches t ON c.Course_ID = t.Course_ID AND t.Semester = e.Semester
                    LEFT JOIN Instructor i ON t.Instructor_ID = i.Instructor_ID
                    WHERE e.Student_ID = %s AND e.Semester = %s
                """, (int(sid), sem))
            self.report_tree.delete(*self.report_tree.get_children())
            if not rows:
                messagebox.showinfo("No data", "No report rows")
                return
            # normalize rows which may be dicts or tuples
            for r in rows:
                if isinstance(r, dict):
                    vals = list(r.values())
                else:
                    vals = list(r)
                # slice or pad to 5
                vals = (vals + [""]*5)[:5]
                self.report_tree.insert("", END, values=vals)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def get_course_enrollment_count(self):
        cid = self.r_course_id.get().strip()
        if not cid:
            messagebox.showwarning("Validation", "Course ID required")
            return
        try:
            # call function - MySQL functions must be in SELECT
            r = self.db.query("SELECT GetCourseEnrollment(%s) AS EnrollmentCount", (int(cid),))
            self.report_tree.delete(*self.report_tree.get_children())
            if r:
                self.report_tree.insert("", END, values=(f"Course {cid}", f"EnrollmentCount: {r[0].get('EnrollmentCount')}", "", "", ""))
            else:
                messagebox.showinfo("No data", "Function returned no rows")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def is_course_full(self):
        cid = self.r_course_full_id.get().strip()
        if not cid:
            messagebox.showwarning("Validation", "Course ID required")
            return
        try:
            r = self.db.query("SELECT IsCourseFull(%s) AS IsFull", (int(cid),))
            self.report_tree.delete(*self.report_tree.get_children())
            if r:
                self.report_tree.insert("", END, values=(f"Course {cid}", f"IsFull: {r[0].get('IsFull')}", "", "", ""))
            else:
                messagebox.showinfo("No data", "Function returned no rows")
        except Exception as e:
            messagebox.showerror("Error", str(e))


# --------------------
# Run
# --------------------
def main():
    root = Tk()
    try:
        db = DB(DB_CONFIG)
    except Exception:
        return
    app = App(root, db)
    root.mainloop()

if __name__ == "__main__":
    main()

