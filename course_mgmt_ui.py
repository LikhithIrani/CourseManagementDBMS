#!/usr/bin/env python3
"""
course_mgmt_ui.py

Tkinter UI for CourseManagement database (students, alumni, placements, internships, etc.)

Default: SQLite backend for easy run. Switch to MySQL by setting DB_BACKEND = "mysql"
and editing MYSQL_CONFIG.

Run:
    python course_mgmt_ui.py
"""

import os
import csv
import sqlite3
import datetime
import pymysql
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog

# =====================
# DATABASE CONFIG
# =====================

# ==== CONFIG ====
DB_BACKEND = "mysql"
MYSQL_CONFIG = {
    "host": "127.0.0.1",        # or "localhost" — both worked for you
    "user": "cms_user",
    "password": "My$qlStrong2025!",
    "db": "CourseManagement",
    "port": 3306,
    "charset": "utf8mb4",
}


# ========================================================================
# DB Layer (abstracts sqlite and mysql)
# ========================================================================
class DB:
    def __init__(self):
        self.backend = DB_BACKEND
        self.conn = None
        if self.backend == "sqlite":
            self.conn = sqlite3.connect(SQLITE_DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
            self.conn.row_factory = sqlite3.Row
        elif self.backend == "mysql":
            try:
                import pymysql
            except Exception as e:
                raise RuntimeError("pymysql required for MySQL backend: pip install pymysql") from e
            # set cursorclass to DictCursor-like if available
            MYSQL_CONFIG["cursorclass"] = pymysql.cursors.DictCursor
            self._pymysql = pymysql
            self.conn = pymysql.connect(**MYSQL_CONFIG)
        else:
            raise RuntimeError("Unsupported DB_BACKEND: " + str(self.backend))

    def cursor(self):
        return self.conn.cursor()

    def execute(self, sql, params=()):
        cur = self.cursor()
        try:
            cur.execute(sql, params)
            # For sqlite, commit below
            return cur
        except Exception:
            cur.close()
            raise

    def executemany(self, sql, seq):
        cur = self.cursor()
        try:
            cur.executemany(sql, seq)
            return cur
        except Exception:
            cur.close()
            raise

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

    def query_all(self, sql, params=()):
        cur = self.execute(sql, params)
        rows = cur.fetchall()
        cur.close()
        # convert sqlite Row to dict-like
        if self.backend == "sqlite":
            return [dict(r) for r in rows]
        else:
            return rows

    def query_one(self, sql, params=()):
        cur = self.execute(sql, params)
        row = cur.fetchone()
        cur.close()
        if self.backend == "sqlite" and row is not None:
            return dict(row)
        return row

# ========================================================================
# Schema creation (for SQLite) - mirrors your final SQL
# ========================================================================
def init_sqlite_schema(db: DB):
    """Create tables if using sqlite backend"""
    # create tables in safe order
    statements = [
        # Department
        """
        CREATE TABLE IF NOT EXISTS Department (
            Department_ID INTEGER PRIMARY KEY,
            Dept_Name TEXT NOT NULL,
            Location TEXT,
            HOD_Name TEXT
        );
        """,
        # Student
        """
        CREATE TABLE IF NOT EXISTS Student (
            Student_ID INTEGER PRIMARY KEY,
            Name TEXT NOT NULL,
            Email TEXT UNIQUE,
            Phone TEXT,
            DOB DATE,
            Year_of_Study INTEGER,
            Department_ID INTEGER,
            FOREIGN KEY(Department_ID) REFERENCES Department(Department_ID) ON DELETE SET NULL
        );
        """,
        # Instructor
        """
        CREATE TABLE IF NOT EXISTS Instructor (
            Instructor_ID INTEGER PRIMARY KEY,
            Name TEXT NOT NULL,
            Email TEXT UNIQUE,
            Phone TEXT,
            DOJ DATE,
            Qualification TEXT,
            Department_ID INTEGER,
            No_of_Courses_Taught INTEGER DEFAULT 0,
            FOREIGN KEY(Department_ID) REFERENCES Department(Department_ID) ON DELETE SET NULL
        );
        """,
        # Course
        """
        CREATE TABLE IF NOT EXISTS Course (
            Course_ID INTEGER PRIMARY KEY,
            Course_Name TEXT NOT NULL,
            Credits INTEGER,
            Course_Level TEXT,
            No_of_Students_Enrolled INTEGER DEFAULT 0,
            Department_ID INTEGER,
            FOREIGN KEY(Department_ID) REFERENCES Department(Department_ID) ON DELETE SET NULL
        );
        """,
        # Classroom
        """
        CREATE TABLE IF NOT EXISTS Classroom (
            Room_ID INTEGER PRIMARY KEY,
            Location TEXT,
            Capacity INTEGER,
            Course_ID INTEGER,
            FOREIGN KEY(Course_ID) REFERENCES Course(Course_ID) ON DELETE CASCADE
        );
        """,
        # Enrollment
        """
        CREATE TABLE IF NOT EXISTS Enrollment (
            Enrollment_ID INTEGER PRIMARY KEY,
            Student_ID INTEGER,
            Course_ID INTEGER,
            Semester TEXT,
            Grade TEXT,
            FOREIGN KEY(Student_ID) REFERENCES Student(Student_ID) ON DELETE CASCADE,
            FOREIGN KEY(Course_ID) REFERENCES Course(Course_ID) ON DELETE CASCADE
        );
        """,
        # Teaches
        """
        CREATE TABLE IF NOT EXISTS Teaches (
            Teach_ID INTEGER PRIMARY KEY,
            Instructor_ID INTEGER,
            Course_ID INTEGER,
            Semester TEXT,
            Academic_Year TEXT,
            FOREIGN KEY(Instructor_ID) REFERENCES Instructor(Instructor_ID) ON DELETE CASCADE,
            FOREIGN KEY(Course_ID) REFERENCES Course(Course_ID) ON DELETE CASCADE
        );
        """,
        # Alumni
        """
        CREATE TABLE IF NOT EXISTS Alumni (
            Alumni_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Email TEXT UNIQUE,
            Phone TEXT,
            DOB DATE,
            Graduation_Year INTEGER,
            CGPA REAL,
            Department_ID INTEGER,
            Notes TEXT,
            FOREIGN KEY(Department_ID) REFERENCES Department(Department_ID) ON DELETE SET NULL
        );
        """,
        # Placement
        """
        CREATE TABLE IF NOT EXISTS Placement (
            Placement_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Student_ID INTEGER,
            Alumni_ID INTEGER,
            Company TEXT NOT NULL,
            Role TEXT,
            Package TEXT,
            Offer_Date DATE,
            On_Campus INTEGER DEFAULT 0,
            Location TEXT,
            Remarks TEXT,
            FOREIGN KEY(Student_ID) REFERENCES Student(Student_ID) ON DELETE SET NULL,
            FOREIGN KEY(Alumni_ID) REFERENCES Alumni(Alumni_ID) ON DELETE SET NULL
        );
        """,
        # Internship
        """
        CREATE TABLE IF NOT EXISTS Internship (
            Internship_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Student_ID INTEGER,
            Alumni_ID INTEGER,
            Company TEXT NOT NULL,
            Role TEXT,
            Duration TEXT,
            Stipend TEXT,
            Start_Date DATE,
            End_Date DATE,
            Mode TEXT,
            Remarks TEXT,
            FOREIGN KEY(Student_ID) REFERENCES Student(Student_ID) ON DELETE SET NULL,
            FOREIGN KEY(Alumni_ID) REFERENCES Alumni(Alumni_ID) ON DELETE SET NULL
        );
        """,
        # Placement_Help
        """
        CREATE TABLE IF NOT EXISTS Placement_Help (
            Help_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Title TEXT,
            Description TEXT,
            Link TEXT,
            Created_On DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """,
        # Internship_Help
        """
        CREATE TABLE IF NOT EXISTS Internship_Help (
            Help_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Title TEXT,
            Description TEXT,
            Link TEXT,
            Created_On DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """,
    ]
    cur = db.cursor()
    try:
        for s in statements:
            cur.execute(s)
        db.commit()
    finally:
        cur.close()

    # Insert some seed data only if empty (safe)
    existing = db.query_one("SELECT COUNT(*) as c FROM Department")
    if existing and existing["c"] == 0:
        seed_departments = [
            (1, 'Computer Science & Engineering', 'Block A', 'Dr. R. S. Menon'),
            (2, 'Electronics & Communication', 'Block B', 'Dr. A. K. Pillai'),
            (3, 'Mechanical Engineering', 'Block C', 'Dr. S. Venkatesh'),
            (4, 'Civil Engineering', 'Block D', 'Dr. N. Chatterjee'),
        ]
        db.executemany("INSERT INTO Department (Department_ID, Dept_Name, Location, HOD_Name) VALUES (?, ?, ?, ?)", seed_departments)
        db.commit()

# ========================================================================
# Utility helpers
# ========================================================================
def to_int(v, default=None):
    try:
        return int(v)
    except Exception:
        return default

def date_or_none(s):
    if not s:
        return None
    try:
        return datetime.date.fromisoformat(s)
    except Exception:
        return None

# export list-of-dicts to CSV
def export_to_csv(rows, columns, filename):
    if not rows:
        raise ValueError("No rows to export")
    with open(filename, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(columns)
        for r in rows:
            w.writerow([r.get(c, "") for c in columns])

# ========================================================================
# Tkinter App
# ========================================================================
class CourseMgmtApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Course Management — Placements & Internships UI")
        self.geometry("1100x700")
        self.minsize(900, 600)

        # DB connection
        try:
            self.db = DB()
        except Exception as e:
            messagebox.showerror("DB error", f"Could not open DB: {e}")
            raise

        if DB_BACKEND == "sqlite":
            init_sqlite_schema(self.db)

        # Build UI
        self._build_main()

    def _build_main(self):
        top = ttk.Frame(self)
        top.pack(side="top", fill="x")

        ttk.Label(top, text="Course Management UI", font=("Segoe UI", 16, "bold")).pack(side="left", padx=12, pady=8)
        ttk.Button(top, text="Export Table CSV", command=self._export_current).pack(side="right", padx=6)
        ttk.Button(top, text="Refresh", command=self.refresh_all).pack(side="right", padx=6)

        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True, padx=8, pady=8)

        # Tabs
        self.tabs = {}
        self._create_tab("Dashboard", self._build_dashboard_tab)
        self._create_tab("Students", self._build_students_tab)
        self._create_tab("Alumni", self._build_alumni_tab)
        self._create_tab("Instructors", self._build_instructors_tab)
        self._create_tab("Courses", self._build_courses_tab)
        self._create_tab("Placements", self._build_placements_tab)
        self._create_tab("Internships", self._build_internships_tab)
        self._create_tab("Help & Resources", self._build_help_tab)
        self._create_tab("Reports", self._build_reports_tab)

    def _create_tab(self, title, builder):
        frame = ttk.Frame(self.nb)
        self.nb.add(frame, text=title)
        self.tabs[title] = frame
        builder(frame)

    def refresh_all(self):
        for name in ("Students", "Alumni", "Instructors", "Courses", "Placements", "Internships", "Help & Resources", "Reports"):
            # call specific refresh functions if exist
            fn = getattr(self, f"refresh_{name.lower().replace(' & ', '_').replace(' ', '_')}", None)
            if callable(fn):
                try:
                    fn()
                except Exception as e:
                    print(f"Refresh {name} failed:", e)

    # -----------------------
    # Dashboard
    # -----------------------
    def _build_dashboard_tab(self, frame):
        f = frame
        ttk.Label(f, text="Overview", font=("Segoe UI", 14)).pack(anchor="w", padx=10, pady=6)
        stats_frame = ttk.Frame(f)
        stats_frame.pack(fill="x", padx=10, pady=6)
        # small stat labels
        self.stat_vars = {}
        for i, (label, query) in enumerate([
            ("Total Students", "SELECT COUNT(*) as c FROM Student"),
            ("Total Alumni", "SELECT COUNT(*) as c FROM Alumni"),
            ("Total Instructors", "SELECT COUNT(*) as c FROM Instructor"),
            ("Total Courses", "SELECT COUNT(*) as c FROM Course"),
            ("Total Placements", "SELECT COUNT(*) as c FROM Placement"),
            ("Total Internships", "SELECT COUNT(*) as c FROM Internship"),
        ]):
            var = tk.StringVar(value="...")
            self.stat_vars[label] = var
            box = ttk.Label(stats_frame, textvariable=var, relief="ridge", padding=8, width=18, anchor="center")
            box.grid(row=0, column=i, padx=6, sticky="nsew")
        ttk.Button(f, text="Refresh Stats", command=self._refresh_stats).pack(anchor="w", padx=10, pady=8)
        self._refresh_stats()

    def _refresh_stats(self):
        for label, q in [
            ("Total Students", "SELECT COUNT(*) as c FROM Student"),
            ("Total Alumni", "SELECT COUNT(*) as c FROM Alumni"),
            ("Total Instructors", "SELECT COUNT(*) as c FROM Instructor"),
            ("Total Courses", "SELECT COUNT(*) as c FROM Course"),
            ("Total Placements", "SELECT COUNT(*) as c FROM Placement"),
            ("Total Internships", "SELECT COUNT(*) as c FROM Internship"),
        ]:
            try:
                row = self.db.query_one(q)
                v = row["c"] if row else 0
            except Exception:
                v = "?"
            self.stat_vars[label].set(f"{label}: {v}")

    # -----------------------
    # STUDENTS TAB
    # -----------------------
    def _build_students_tab(self, frame):
        f = frame
        top = ttk.Frame(f)
        top.pack(fill="x", pady=6, padx=6)
        ttk.Label(top, text="Students", font=("Segoe UI", 12)).pack(side="left")
        search_frame = ttk.Frame(top)
        search_frame.pack(side="right")
        ttk.Label(search_frame, text="Search:").pack(side="left")
        self.student_search_var = tk.StringVar()
        e = ttk.Entry(search_frame, textvariable=self.student_search_var, width=30)
        e.pack(side="left", padx=6)
        ttk.Button(search_frame, text="Go", command=self.refresh_students).pack(side="left")
        ttk.Button(search_frame, text="Add Student", command=self.add_student_dialog).pack(side="left", padx=6)

        cols = ("Student_ID", "Name", "Email", "Phone", "Year_of_Study", "Department_ID")
        tree = ttk.Treeview(f, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=120, anchor="w")
        tree.pack(fill="both", expand=True, padx=6, pady=6)
        tree.bind("<Double-1>", lambda e: self.edit_student_dialog())
        self.students_tree = tree

        bottom = ttk.Frame(f)
        bottom.pack(fill="x", padx=6, pady=6)
        ttk.Button(bottom, text="Edit Selected", command=self.edit_student_dialog).pack(side="left")
        ttk.Button(bottom, text="Delete Selected", command=self.delete_student).pack(side="left", padx=6)
        ttk.Button(bottom, text="Export CSV", command=lambda: self.export_table("Student")).pack(side="right")
        self.refresh_students()

    def refresh_students(self):
        qbase = "SELECT Student_ID, Name, Email, Phone, Year_of_Study, Department_ID FROM Student"
        s = self.student_search_var.get().strip()
        if s:
            q = qbase + " WHERE Name LIKE ? OR Email LIKE ? OR Student_ID LIKE ?"
            params = (f"%{s}%", f"%{s}%", f"%{s}%")
        else:
            q = qbase
            params = ()
        rows = self.db.query_all(q, params)
        self.students_tree.delete(*self.students_tree.get_children())
        for r in rows:
            vals = [r.get(c, "") for c in ("Student_ID", "Name", "Email", "Phone", "Year_of_Study", "Department_ID")]
            self.students_tree.insert("", "end", values=vals)

    def add_student_dialog(self):
        dlg = RecordDialog(self, title="Add Student", fields=[
            ("Student_ID","int"),
            ("Name","text"),
            ("Email","text"),
            ("Phone","text"),
            ("DOB (YYYY-MM-DD)","text"),
            ("Year_of_Study","int"),
            ("Department_ID","int"),
        ])
        if dlg.result:
            vals = dlg.result
            try:
                self.db.execute(
                    "INSERT INTO Student (Student_ID, Name, Email, Phone, DOB, Year_of_Study, Department_ID) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (int(vals["Student_ID"]), vals["Name"], vals["Email"], vals["Phone"], vals.get("DOB (YYYY-MM-DD)"), to_int(vals["Year_of_Study"]), to_int(vals["Department_ID"]))
                )
                self.db.commit()
                messagebox.showinfo("OK", "Student added")
                self.refresh_students()
                self._refresh_stats()
            except Exception as e:
                messagebox.showerror("Error adding student", str(e))

    def edit_student_dialog(self):
        sel = self.students_tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Select a student to edit")
            return
        item = self.students_tree.item(sel[0])["values"]
        sid = item[0]
        row = self.db.query_one("SELECT * FROM Student WHERE Student_ID = ?", (sid,))
        if not row:
            messagebox.showerror("Not found", "Student not found")
            self.refresh_students(); return
        dlg = RecordDialog(self, title="Edit Student", fields=[
            ("Student_ID","int", str(row["Student_ID"])),
            ("Name","text", row["Name"]),
            ("Email","text", row["Email"]),
            ("Phone","text", row["Phone"]),
            ("DOB (YYYY-MM-DD)","text", row.get("DOB") or ""),
            ("Year_of_Study","int", str(row.get("Year_of_Study") or "")),
            ("Department_ID","int", str(row.get("Department_ID") or "")),
        ], readonly_fields=["Student_ID"])
        if dlg.result:
            vals = dlg.result
            try:
                self.db.execute(
                    "UPDATE Student SET Name=?, Email=?, Phone=?, DOB=?, Year_of_Study=?, Department_ID=? WHERE Student_ID = ?",
                    (vals["Name"], vals["Email"], vals["Phone"], vals.get("DOB (YYYY-MM-DD)"), to_int(vals["Year_of_Study"]), to_int(vals["Department_ID"]), int(vals["Student_ID"]))
                )
                self.db.commit()
                messagebox.showinfo("OK", "Student updated")
                self.refresh_students()
            except Exception as e:
                messagebox.showerror("Error updating student", str(e))

    def delete_student(self):
        sel = self.students_tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Select a student to delete")
            return
        sid = self.students_tree.item(sel[0])["values"][0]
        if messagebox.askyesno("Confirm", f"Delete student {sid}? This will cascade delete enrollments."):
            try:
                self.db.execute("DELETE FROM Student WHERE Student_ID = ?", (sid,))
                self.db.commit()
                self.refresh_students(); self._refresh_stats()
            except Exception as e:
                messagebox.showerror("Delete failed", str(e))

    # -----------------------
    # ALUMNI TAB (similar pattern)
    # -----------------------
    def _build_alumni_tab(self, frame):
        f = frame
        top = ttk.Frame(f)
        top.pack(fill="x", pady=6, padx=6)
        ttk.Label(top, text="Alumni (Previous Students)", font=("Segoe UI", 12)).pack(side="left")
        ttk.Button(top, text="Add Alumni", command=self.add_alumni_dialog).pack(side="right")
        ttk.Button(top, text="Export CSV", command=lambda: self.export_table("Alumni")).pack(side="right", padx=6)

        cols = ("Alumni_ID","Name","Email","Phone","Graduation_Year","CGPA","Department_ID")
        tree = ttk.Treeview(f, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=120)
        tree.pack(fill="both", expand=True, padx=6, pady=6)
        tree.bind("<Double-1>", lambda e: self.edit_alumni_dialog())
        self.alumni_tree = tree
        self.refresh_alumni()

    def refresh_alumni(self):
        rows = self.db.query_all("SELECT Alumni_ID, Name, Email, Phone, Graduation_Year, CGPA, Department_ID FROM Alumni")
        self.alumni_tree.delete(*self.alumni_tree.get_children())
        for r in rows:
            self.alumni_tree.insert("", "end", values=[r.get(c,"") for c in ("Alumni_ID","Name","Email","Phone","Graduation_Year","CGPA","Department_ID")])

    def add_alumni_dialog(self):
        dlg = RecordDialog(self, title="Add Alumni", fields=[
            ("Name","text"),
            ("Email","text"),
            ("Phone","text"),
            ("DOB (YYYY-MM-DD)","text"),
            ("Graduation_Year","int"),
            ("CGPA","text"),
            ("Department_ID","int"),
            ("Notes","text"),
        ])
        if dlg.result:
            vals = dlg.result
            try:
                self.db.execute("INSERT INTO Alumni (Name, Email, Phone, DOB, Graduation_Year, CGPA, Department_ID, Notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                (vals["Name"], vals["Email"], vals["Phone"], vals.get("DOB (YYYY-MM-DD)"), to_int(vals["Graduation_Year"]), float(vals["CGPA"]) if vals.get("CGPA") else None, to_int(vals["Department_ID"]), vals.get("Notes")))
                self.db.commit()
                messagebox.showinfo("OK","Alumni added")
                self.refresh_alumni(); self._refresh_stats()
            except Exception as e:
                messagebox.showerror("Error adding alumni", str(e))

    def edit_alumni_dialog(self):
        sel = self.alumni_tree.selection()
        if not sel:
            messagebox.showwarning("Select","Select an alumni to edit")
            return
        aid = self.alumni_tree.item(sel[0])["values"][0]
        row = self.db.query_one("SELECT * FROM Alumni WHERE Alumni_ID = ?", (aid,))
        if not row:
            messagebox.showerror("Not found","Alumni not found"); return
        dlg = RecordDialog(self, title="Edit Alumni", fields=[
            ("Alumni_ID","int", str(row["Alumni_ID"])),
            ("Name","text", row["Name"]),
            ("Email","text", row["Email"]),
            ("Phone","text", row["Phone"]),
            ("DOB (YYYY-MM-DD)","text", row.get("DOB") or ""),
            ("Graduation_Year","int", str(row.get("Graduation_Year") or "")),
            ("CGPA","text", str(row.get("CGPA") or "")),
            ("Department_ID","int", str(row.get("Department_ID") or "")),
            ("Notes","text", row.get("Notes") or ""),
        ], readonly_fields=["Alumni_ID"])
        if dlg.result:
            vals = dlg.result
            try:
                self.db.execute("UPDATE Alumni SET Name=?, Email=?, Phone=?, DOB=?, Graduation_Year=?, CGPA=?, Department_ID=?, Notes=? WHERE Alumni_ID=?",
                                (vals["Name"], vals["Email"], vals["Phone"], vals.get("DOB (YYYY-MM-DD)"), to_int(vals["Graduation_Year"]), float(vals["CGPA"]) if vals.get("CGPA") else None, to_int(vals["Department_ID"]), vals.get("Notes"), int(vals["Alumni_ID"])))
                self.db.commit()
                messagebox.showinfo("OK","Alumni updated"); self.refresh_alumni()
            except Exception as e:
                messagebox.showerror("Error updating alumni", str(e))

    # -----------------------
    # INSTRUCTORS TAB
    # -----------------------
    def _build_instructors_tab(self, frame):
        f = frame
        top = ttk.Frame(f); top.pack(fill="x", pady=6, padx=6)
        ttk.Label(top, text="Instructors", font=("Segoe UI",12)).pack(side="left")
        ttk.Button(top, text="Add Instructor", command=self.add_instructor_dialog).pack(side="right")
        ttk.Button(top, text="Export CSV", command=lambda: self.export_table("Instructor")).pack(side="right", padx=6)

        cols = ("Instructor_ID","Name","Email","Phone","DOJ","Qualification","Department_ID","No_of_Courses_Taught")
        tree = ttk.Treeview(f, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=120)
        tree.pack(fill="both", expand=True, padx=6, pady=6)
        tree.bind("<Double-1>", lambda e: self.edit_instructor_dialog())
        self.instructors_tree = tree
        self.refresh_instructors()

    def refresh_instructors(self):
        rows = self.db.query_all("SELECT Instructor_ID, Name, Email, Phone, DOJ, Qualification, Department_ID, No_of_Courses_Taught FROM Instructor")
        self.instructors_tree.delete(*self.instructors_tree.get_children())
        for r in rows:
            self.instructors_tree.insert("", "end", values=[r.get(c,"") for c in ("Instructor_ID","Name","Email","Phone","DOJ","Qualification","Department_ID","No_of_Courses_Taught")])

    def add_instructor_dialog(self):
        dlg = RecordDialog(self, title="Add Instructor", fields=[
            ("Instructor_ID","int"),
            ("Name","text"),
            ("Email","text"),
            ("Phone","text"),
            ("DOJ (YYYY-MM-DD)","text"),
            ("Qualification","text"),
            ("Department_ID","int"),
            ("No_of_Courses_Taught","int"),
        ])
        if dlg.result:
            vals = dlg.result
            try:
                self.db.execute("INSERT INTO Instructor (Instructor_ID, Name, Email, Phone, DOJ, Qualification, Department_ID, No_of_Courses_Taught) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                (to_int(vals["Instructor_ID"]), vals["Name"], vals["Email"], vals["Phone"], vals.get("DOJ (YYYY-MM-DD)"), vals["Qualification"], to_int(vals["Department_ID"]), to_int(vals.get("No_of_Courses_Taught"))))
                self.db.commit()
                messagebox.showinfo("OK","Instructor added"); self.refresh_instructors(); self._refresh_stats()
            except Exception as e:
                messagebox.showerror("Error adding instructor", str(e))

    def edit_instructor_dialog(self):
        sel = self.instructors_tree.selection()
        if not sel:
            messagebox.showwarning("Select","Select an instructor to edit"); return
        iid = self.instructors_tree.item(sel[0])["values"][0]
        row = self.db.query_one("SELECT * FROM Instructor WHERE Instructor_ID = ?", (iid,))
        if not row:
            messagebox.showerror("Not found","Instructor not found"); return
        dlg = RecordDialog(self, title="Edit Instructor", fields=[
            ("Instructor_ID","int", str(row["Instructor_ID"])),
            ("Name","text", row["Name"]),
            ("Email","text", row["Email"]),
            ("Phone","text", row["Phone"]),
            ("DOJ (YYYY-MM-DD)","text", row.get("DOJ") or ""),
            ("Qualification","text", row.get("Qualification") or ""),
            ("Department_ID","int", str(row.get("Department_ID") or "")),
            ("No_of_Courses_Taught","int", str(row.get("No_of_Courses_Taught") or "0")),
        ], readonly_fields=["Instructor_ID"])
        if dlg.result:
            vals = dlg.result
            try:
                self.db.execute("UPDATE Instructor SET Name=?, Email=?, Phone=?, DOJ=?, Qualification=?, Department_ID=?, No_of_Courses_Taught=? WHERE Instructor_ID=?",
                                (vals["Name"], vals["Email"], vals["Phone"], vals.get("DOJ (YYYY-MM-DD)"), vals.get("Qualification"), to_int(vals["Department_ID"]), to_int(vals.get("No_of_Courses_Taught")), int(vals["Instructor_ID"])))
                self.db.commit(); messagebox.showinfo("OK","Instructor updated"); self.refresh_instructors()
            except Exception as e:
                messagebox.showerror("Error updating instructor", str(e))

    # -----------------------
    # COURSES TAB
    # -----------------------
    def _build_courses_tab(self, frame):
        f = frame
        top = ttk.Frame(f); top.pack(fill="x", padx=6, pady=6)
        ttk.Label(top, text="Courses", font=("Segoe UI",12)).pack(side="left")
        ttk.Button(top, text="Add Course", command=self.add_course_dialog).pack(side="right")
        ttk.Button(top, text="Export CSV", command=lambda: self.export_table("Course")).pack(side="right", padx=6)

        cols = ("Course_ID","Course_Name","Credits","Course_Level","No_of_Students_Enrolled","Department_ID")
        tree = ttk.Treeview(f, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=140)
        tree.pack(fill="both", expand=True, padx=6, pady=6)
        tree.bind("<Double-1>", lambda e: self.edit_course_dialog())
        self.courses_tree = tree
        self.refresh_courses()

    def refresh_courses(self):
        rows = self.db.query_all("SELECT Course_ID, Course_Name, Credits, Course_Level, No_of_Students_Enrolled, Department_ID FROM Course")
        self.courses_tree.delete(*self.courses_tree.get_children())
        for r in rows:
            self.courses_tree.insert("", "end", values=[r.get(c,"") for c in ("Course_ID","Course_Name","Credits","Course_Level","No_of_Students_Enrolled","Department_ID")])

    def add_course_dialog(self):
        dlg = RecordDialog(self, title="Add Course", fields=[
            ("Course_ID","int"),
            ("Course_Name","text"),
            ("Credits","int"),
            ("Course_Level","text"),
            ("Department_ID","int")
        ])
        if dlg.result:
            v = dlg.result
            try:
                self.db.execute("INSERT INTO Course (Course_ID, Course_Name, Credits, Course_Level, Department_ID) VALUES (?, ?, ?, ?, ?)",
                                (to_int(v["Course_ID"]), v["Course_Name"], to_int(v["Credits"]), v["Course_Level"], to_int(v["Department_ID"])))
                self.db.commit(); messagebox.showinfo("OK","Course added"); self.refresh_courses()
            except Exception as e:
                messagebox.showerror("Error adding course", str(e))

    def edit_course_dialog(self):
        sel = self.courses_tree.selection()
        if not sel:
            messagebox.showwarning("Select","Select a course to edit"); return
        cid = self.courses_tree.item(sel[0])["values"][0]
        row = self.db.query_one("SELECT * FROM Course WHERE Course_ID = ?", (cid,))
        if not row: messagebox.showerror("Not found","Course not found"); return
        dlg = RecordDialog(self, title="Edit Course", fields=[
            ("Course_ID","int", str(row["Course_ID"])),
            ("Course_Name","text", row["Course_Name"]),
            ("Credits","int", str(row.get("Credits") or "")),
            ("Course_Level","text", row.get("Course_Level") or ""),
            ("Department_ID","int", str(row.get("Department_ID") or "")),
        ], readonly_fields=["Course_ID"])
        if dlg.result:
            v = dlg.result
            try:
                self.db.execute("UPDATE Course SET Course_Name=?, Credits=?, Course_Level=?, Department_ID=? WHERE Course_ID=?",
                                (v["Course_Name"], to_int(v["Credits"]), v["Course_Level"], to_int(v["Department_ID"]), int(v["Course_ID"])))
                self.db.commit(); messagebox.showinfo("OK","Course updated"); self.refresh_courses()
            except Exception as e:
                messagebox.showerror("Error updating course", str(e))

    # -----------------------
    # PLACEMENTS TAB
    # -----------------------
    def _build_placements_tab(self, frame):
        f = frame
        top = ttk.Frame(f); top.pack(fill="x", padx=6, pady=6)
        ttk.Label(top, text="Placements", font=("Segoe UI",12)).pack(side="left")
        ttk.Button(top, text="Add Placement", command=self.add_placement_dialog).pack(side="right")
        ttk.Button(top, text="Export CSV", command=lambda: self.export_table("Placement")).pack(side="right", padx=6)

        cols = ("Placement_ID","Student_ID","Alumni_ID","Company","Role","Package","Offer_Date","On_Campus","Location")
        tree = ttk.Treeview(f, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=130)
        tree.pack(fill="both", expand=True, padx=6, pady=6)
        tree.bind("<Double-1>", lambda e: self.edit_placement_dialog())
        self.placements_tree = tree
        self.refresh_placements()

    def refresh_placements(self):
        rows = self.db.query_all("SELECT Placement_ID, Student_ID, Alumni_ID, Company, Role, Package, Offer_Date, On_Campus, Location FROM Placement")
        self.placements_tree.delete(*self.placements_tree.get_children())
        for r in rows:
            self.placements_tree.insert("", "end", values=[r.get(c,"") for c in ("Placement_ID","Student_ID","Alumni_ID","Company","Role","Package","Offer_Date","On_Campus","Location")])

    def add_placement_dialog(self):
        dlg = RecordDialog(self, title="Add Placement", fields=[
            ("Student_ID","int"),
            ("Alumni_ID","int"),
            ("Company","text"),
            ("Role","text"),
            ("Package","text"),
            ("Offer_Date (YYYY-MM-DD)","text"),
            ("On_Campus (0/1)","int"),
            ("Location","text"),
            ("Remarks","text"),
        ])
        if dlg.result:
            v = dlg.result
            try:
                self.db.execute("INSERT INTO Placement (Student_ID, Alumni_ID, Company, Role, Package, Offer_Date, On_Campus, Location, Remarks) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                (to_int(v["Student_ID"]), to_int(v["Alumni_ID"]), v["Company"], v.get("Role"), v.get("Package"), v.get("Offer_Date (YYYY-MM-DD)"), to_int(v.get("On_Campus (0/1)")), v.get("Location"), v.get("Remarks")))
                self.db.commit(); messagebox.showinfo("OK","Placement added"); self.refresh_placements(); self._refresh_stats()
            except Exception as e:
                messagebox.showerror("Error adding placement", str(e))

    def edit_placement_dialog(self):
        sel = self.placements_tree.selection()
        if not sel:
            messagebox.showwarning("Select","Select a placement to edit"); return
        pid = self.placements_tree.item(sel[0])["values"][0]
        row = self.db.query_one("SELECT * FROM Placement WHERE Placement_ID = ?", (pid,))
        if not row:
            messagebox.showerror("Not found","Placement not found"); return
        dlg = RecordDialog(self, title="Edit Placement", fields=[
            ("Placement_ID","int", str(row["Placement_ID"])),
            ("Student_ID","int", str(row.get("Student_ID") or "")),
            ("Alumni_ID","int", str(row.get("Alumni_ID") or "")),
            ("Company","text", row.get("Company") or ""),
            ("Role","text", row.get("Role") or ""),
            ("Package","text", row.get("Package") or ""),
            ("Offer_Date (YYYY-MM-DD)","text", row.get("Offer_Date") or ""),
            ("On_Campus (0/1)","int", str(row.get("On_Campus") or "0")),
            ("Location","text", row.get("Location") or ""),
            ("Remarks","text", row.get("Remarks") or ""),
        ], readonly_fields=["Placement_ID"])
        if dlg.result:
            v = dlg.result
            try:
                self.db.execute("UPDATE Placement SET Student_ID=?, Alumni_ID=?, Company=?, Role=?, Package=?, Offer_Date=?, On_Campus=?, Location=?, Remarks=? WHERE Placement_ID=?",
                                (to_int(v["Student_ID"]), to_int(v["Alumni_ID"]), v["Company"], v.get("Role"), v.get("Package"), v.get("Offer_Date (YYYY-MM-DD)"), to_int(v.get("On_Campus (0/1)")), v.get("Location"), v.get("Remarks"), int(v["Placement_ID"])))
                self.db.commit(); messagebox.showinfo("OK","Placement updated"); self.refresh_placements()
            except Exception as e:
                messagebox.showerror("Error updating placement", str(e))

    # -----------------------
    # INTERNSHIPS TAB
    # -----------------------
    def _build_internships_tab(self, frame):
        f = frame
        top = ttk.Frame(f); top.pack(fill="x", padx=6, pady=6)
        ttk.Label(top, text="Internships", font=("Segoe UI",12)).pack(side="left")
        ttk.Button(top, text="Add Internship", command=self.add_intern_dialog).pack(side="right")
        ttk.Button(top, text="Export CSV", command=lambda: self.export_table("Internship")).pack(side="right", padx=6)

        cols = ("Internship_ID","Student_ID","Alumni_ID","Company","Role","Duration","Start_Date","End_Date","Mode")
        tree = ttk.Treeview(f, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=130)
        tree.pack(fill="both", expand=True, padx=6, pady=6)
        tree.bind("<Double-1>", lambda e: self.edit_intern_dialog())
        self.intern_tree = tree
        self.refresh_interns()

    def refresh_interns(self):
        rows = self.db.query_all("SELECT Internship_ID, Student_ID, Alumni_ID, Company, Role, Duration, Start_Date, End_Date, Mode FROM Internship")
        self.intern_tree.delete(*self.intern_tree.get_children())
        for r in rows:
            self.intern_tree.insert("", "end", values=[r.get(c,"") for c in ("Internship_ID","Student_ID","Alumni_ID","Company","Role","Duration","Start_Date","End_Date","Mode")])

    def add_intern_dialog(self):
        dlg = RecordDialog(self, title="Add Internship", fields=[
            ("Student_ID","int"),
            ("Alumni_ID","int"),
            ("Company","text"),
            ("Role","text"),
            ("Duration","text"),
            ("Stipend","text"),
            ("Start_Date (YYYY-MM-DD)","text"),
            ("End_Date (YYYY-MM-DD)","text"),
            ("Mode","text"),
            ("Remarks","text"),
        ])
        if dlg.result:
            v = dlg.result
            try:
                self.db.execute("INSERT INTO Internship (Student_ID, Alumni_ID, Company, Role, Duration, Stipend, Start_Date, End_Date, Mode, Remarks) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                (to_int(v["Student_ID"]), to_int(v["Alumni_ID"]), v["Company"], v.get("Role"), v.get("Duration"), v.get("Stipend"), v.get("Start_Date (YYYY-MM-DD)"), v.get("End_Date (YYYY-MM-DD)"), v.get("Mode"), v.get("Remarks")))
                self.db.commit(); messagebox.showinfo("OK","Internship added"); self.refresh_interns(); self._refresh_stats()
            except Exception as e:
                messagebox.showerror("Error adding internship", str(e))

    def edit_intern_dialog(self):
        sel = self.intern_tree.selection()
        if not sel:
            messagebox.showwarning("Select","Select an internship to edit"); return
        iid = self.intern_tree.item(sel[0])["values"][0]
        row = self.db.query_one("SELECT * FROM Internship WHERE Internship_ID = ?", (iid,))
        if not row:
            messagebox.showerror("Not found","Internship not found"); return
        dlg = RecordDialog(self, title="Edit Internship", fields=[
            ("Internship_ID","int", str(row["Internship_ID"])),
            ("Student_ID","int", str(row.get("Student_ID") or "")),
            ("Alumni_ID","int", str(row.get("Alumni_ID") or "")),
            ("Company","text", row.get("Company") or ""),
            ("Role","text", row.get("Role") or ""),
            ("Duration","text", row.get("Duration") or ""),
            ("Stipend","text", row.get("Stipend") or ""),
            ("Start_Date (YYYY-MM-DD)","text", row.get("Start_Date") or ""),
            ("End_Date (YYYY-MM-DD)","text", row.get("End_Date") or ""),
            ("Mode","text", row.get("Mode") or ""),
            ("Remarks","text", row.get("Remarks") or ""),
        ], readonly_fields=["Internship_ID"])
        if dlg.result:
            v = dlg.result
            try:
                self.db.execute("UPDATE Internship SET Student_ID=?, Alumni_ID=?, Company=?, Role=?, Duration=?, Stipend=?, Start_Date=?, End_Date=?, Mode=?, Remarks=? WHERE Internship_ID=?",
                                (to_int(v["Student_ID"]), to_int(v["Alumni_ID"]), v["Company"], v.get("Role"), v.get("Duration"), v.get("Stipend"), v.get("Start_Date (YYYY-MM-DD)"), v.get("End_Date (YYYY-MM-DD)"), v.get("Mode"), v.get("Remarks"), int(v["Internship_ID"])))
                self.db.commit(); messagebox.showinfo("OK","Internship updated"); self.refresh_interns()
            except Exception as e:
                messagebox.showerror("Error updating internship", str(e))

    # -----------------------
    # Help & Resources Tab
    # -----------------------
    def _build_help_tab(self, frame):
        f = frame
        top = ttk.Frame(f); top.pack(fill="x", pady=6, padx=6)
        ttk.Label(top, text="Help & Resources", font=("Segoe UI",12)).pack(side="left")
        ttk.Button(top, text="Seed Sample Help", command=self.seed_help).pack(side="right")
        ttk.Button(top, text="Export CSV", command=lambda: self.export_table("Placement_Help")).pack(side="right", padx=6)

        cols = ("Help_ID","Title","Description","Link","Created_On")
        tree = ttk.Treeview(f, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=180)
        tree.pack(fill="both", expand=True, padx=6, pady=6)
        self.help_tree = tree
        self.refresh_help()

    def refresh_help(self):
        rows = self.db.query_all("SELECT Help_ID, Title, Description, Link, Created_On FROM Placement_Help")
        self.help_tree.delete(*self.help_tree.get_children())
        for r in rows:
            self.help_tree.insert("", "end", values=[r.get(c,"") for c in ("Help_ID","Title","Description","Link","Created_On")])

    def seed_help(self):
        try:
            self.db.execute("INSERT INTO Placement_Help (Title, Description, Link) VALUES (?, ?, ?)",
                            ("Coding Interview Roadmap", "Systematic roadmap: DS&A -> Mock interviews -> System design basics -> Behavioral preparation", "https://resources.example.com/coding-roadmap"))
            self.db.execute("INSERT INTO Internship_Help (Title, Description, Link) VALUES (?, ?, ?)",
                            ("Where to Find Internships", "College T&P, LinkedIn, Internshala, AngelList, company career pages", "https://resources.example.com/find-interns"))
            self.db.commit()
            messagebox.showinfo("Seeded", "Sample help content added")
            self.refresh_help()
        except Exception as e:
            messagebox.showerror("Seed failed", str(e))

    # -----------------------
    # REPORTS TAB (simple)
    # -----------------------
    def _build_reports_tab(self, frame):
        f = frame
        top = ttk.Frame(f); top.pack(fill="x", padx=6, pady=6)
        ttk.Label(top, text="Reports", font=("Segoe UI",12)).pack(side="left")
        ttk.Button(top, text="Alumni Placements (>= 9.0 CGPA)", command=self.report_top_alumni).pack(side="right")

        self.reports_text = tk.Text(f, height=20)
        self.reports_text.pack(fill="both", expand=True, padx=6, pady=6)

    def report_top_alumni(self):
        rows = self.db.query_all("SELECT a.Alumni_ID, a.Name, a.CGPA, p.Company, p.Role FROM Alumni a LEFT JOIN Placement p ON a.Alumni_ID = p.Alumni_ID WHERE a.CGPA >= ? ORDER BY a.CGPA DESC", (9.0,))
        self.reports_text.delete("1.0", "end")
        if not rows:
            self.reports_text.insert("end", "No alumni with CGPA >= 9.0\n")
            return
        for r in rows:
            self.reports_text.insert("end", f"{r['Alumni_ID']} | {r['Name']} | CGPA: {r['CGPA']} | Company: {r.get('Company') or '-'} | Role: {r.get('Role') or '-'}\n")

    # -----------------------
    # Exports & utilities
    # -----------------------
    def export_table(self, table):
        # select columns
        mapping = {
            "Student": ("Student_ID","Name","Email","Phone","DOB","Year_of_Study","Department_ID"),
            "Alumni": ("Alumni_ID","Name","Email","Phone","DOB","Graduation_Year","CGPA","Department_ID","Notes"),
            "Instructor": ("Instructor_ID","Name","Email","Phone","DOJ","Qualification","Department_ID","No_of_Courses_Taught"),
            "Course": ("Course_ID","Course_Name","Credits","Course_Level","No_of_Students_Enrolled","Department_ID"),
            "Placement": ("Placement_ID","Student_ID","Alumni_ID","Company","Role","Package","Offer_Date","On_Campus","Location","Remarks"),
            "Internship": ("Internship_ID","Student_ID","Alumni_ID","Company","Role","Duration","Stipend","Start_Date","End_Date","Mode","Remarks"),
            "Placement_Help": ("Help_ID","Title","Description","Link","Created_On"),
        }
        cols = mapping.get(table)
        if not cols:
            messagebox.showinfo("Export", "Table export not configured for: " + table); return
        rows = self.db.query_all(f"SELECT {', '.join(cols)} FROM {table}")
        if not rows:
            messagebox.showinfo("Export", "No data to export")
            return
        fn = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")], initialfile=f"{table}.csv")
        if not fn:
            return
        try:
            export_to_csv(rows, cols, fn)
            messagebox.showinfo("Exported", f"Exported {len(rows)} rows to {fn}")
        except Exception as e:
            messagebox.showerror("Export failed", str(e))

    def _export_current(self):
        # pick current tab's name and export mapping
        idx = self.nb.index(self.nb.select())
        title = self.nb.tab(idx, "text")
        map_title = {
            "Students":"Student",
            "Alumni":"Alumni",
            "Instructors":"Instructor",
            "Courses":"Course",
            "Placements":"Placement",
            "Internships":"Internship",
            "Help & Resources":"Placement_Help",
        }.get(title)
        if map_title:
            self.export_table(map_title)
        else:
            messagebox.showinfo("Export", "No export configured for this tab")

# ============================
# Small generic record dialog utility
# ============================
class RecordDialog(simpledialog.Dialog):
    def __init__(self, parent, title=None, fields=None, readonly_fields=None):
        self.fields = fields or []
        self.readonly_fields = set(readonly_fields or [])
        self.result = None
        super().__init__(parent, title=title)

    def body(self, master):
        self.vars = {}
        for r, (label, ftype, *rest) in enumerate([ (f if isinstance(f, tuple) else (f,"text")) for f in self.fields ]):
            default = rest[0] if rest else ""
            ttk.Label(master, text=label).grid(row=r, column=0, sticky="w", padx=6, pady=4)
            v = tk.StringVar(value=default)
            e = ttk.Entry(master, textvariable=v, width=45)
            e.grid(row=r, column=1, sticky="we", padx=6)
            if label in self.readonly_fields:
                e.state(["readonly"])
            self.vars[label] = v
        return list(self.vars.values())[0] if self.vars else None

    def apply(self):
        self.result = {k: v.get().strip() for k, v in self.vars.items()}

# ============================
# Start app
# ============================
def main():
    app = CourseMgmtApp()
    app.refresh_all()
    app.mainloop()
    try:
        app.db.close()
    except Exception:
        pass

if __name__ == "__main__":
    main()
