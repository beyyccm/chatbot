import sqlite3
import datetime

DB_NAME = "obs_chatbot.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    
    # Drop tables to ensure schema update
    c.execute("DROP TABLE IF EXISTS enrollments")
    c.execute("DROP TABLE IF EXISTS courses") # Dependent
    c.execute("DROP TABLE IF EXISTS instructors")
    c.execute("DROP TABLE IF EXISTS students")

    # Students - Added grade_level
    c.execute('''CREATE TABLE IF NOT EXISTS students (
        id TEXT PRIMARY KEY,
        password TEXT,
        name TEXT,
        advisor_id INTEGER,
        department TEXT,
        grade_level INTEGER
    )''')
    
    # Instructors
    c.execute('''CREATE TABLE IF NOT EXISTS instructors (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        office TEXT
    )''')
    
    # Courses - Added credit
    c.execute('''CREATE TABLE IF NOT EXISTS courses (
        code TEXT PRIMARY KEY,
        name TEXT,
        exam_date TEXT,
        schedule TEXT,
        instructor_id INTEGER,
        credit INTEGER,
        FOREIGN KEY(instructor_id) REFERENCES instructors(id)
    )''')
    
    # Enrollments
    c.execute('''CREATE TABLE IF NOT EXISTS enrollments (
        student_id TEXT,
        course_code TEXT,
        midterm INTEGER,
        final INTEGER,
        is_retake INTEGER,
        is_exempt INTEGER,
        attendance_absent INTEGER,
        project_topic TEXT,
        project_deadline TEXT,
        project_note TEXT,
        project_score INTEGER,
        FOREIGN KEY(student_id) REFERENCES students(id),
        FOREIGN KEY(course_code) REFERENCES courses(code)
    )''')
    
    conn.commit()
    seed_data(conn)
    conn.close()

def seed_data(conn):
    c = conn.cursor()
    
    # Clean slate
    c.execute("DELETE FROM students")
    c.execute("DELETE FROM instructors")
    c.execute("DELETE FROM courses")
    c.execute("DELETE FROM enrollments")

    print("Seeding database with grade levels and comprehensive data...")
    
    # --- INSTRUCTORS ---
    instructors = [
        (101, "Dr. Ahmet Yılmaz", "ahmet.yilmaz@atauni.edu.tr", "Mühendislik B-204"),
        (102, "Prof. Dr. Leyla Kaya", "leyla.kaya@atauni.edu.tr", "Mimarlık A-101"),
        (103, "Prof. Dr. Kemal Can", "kemal.can@atauni.edu.tr", "Tıp Fakültesi C-Block"),
        (104, "Doç. Dr. Selin Demir", "selin.demir@atauni.edu.tr", "Hukuk Fakültesi H-302"),
        (105, "Dr. Zeynep İngilizceci", "zeynep.lang@atauni.edu.tr", "Yabancı Diller YD-101"),
        (106, "Prof. Dr. Tarihçi Baba", "tarih.baba@atauni.edu.tr", "Edebiyat Fak. E-505"),
        (107, "Dr. Matematikçi Ali", "ali.math@atauni.edu.tr", "Fen Fak. F-103"),
        (108, "Dr. Fizikçi Ayşe", "ayse.fizik@atauni.edu.tr", "Fen Fak. F-202"),
    ]
    c.executemany("INSERT INTO instructors VALUES (?,?,?,?)", instructors)
    
    # --- STUDENTS ---
    # Added Grade Levels: 3, 2, 1, 4
    students = [
        ("21010101", "12345", "Ayşe Yılmaz", 101, "Bilgisayar Mühendisliği", 3),
        ("21010102", "12345", "Mehmet Öz", 102, "Mimarlık", 2),
        ("21010103", "12345", "Zeynep Kaya", 103, "Tıp Fakültesi", 1),
        ("21010104", "12345", "Ali Vural", 104, "Hukuk Fakültesi", 4)
    ]
    c.executemany("INSERT INTO students VALUES (?,?,?,?,?,?)", students)
    
    # --- COURSES (Added Credits) ---
    courses = [
        # Common / Basic
        ("ENG101", "İngilizce I", "2025-01-02 10:00", "Pazartesi 13:00-15:00", 105, 2),
        ("TURK101", "Türk Dili I", "2025-01-03 14:00", "Perşembe 10:00-12:00", 106, 2),
        ("MATH101", "Matematik I", "2025-01-04 09:00", "Pazartesi 09:00-12:00", 107, 6),
        ("PHYS101", "Fizik I", "2025-01-05 13:00", "Salı 09:00-12:00", 108, 6),
        
        # Comp Eng
        ("CS101", "Bilgisayar Bilimlerine Giriş", "2025-01-06 10:00", "Çarşamba 09:00-12:00", 101, 5),
        ("CS302", "Yapay Zeka", "2025-01-12 14:00", "Salı 13:00-16:00", 101, 7),
        ("CS305", "Web Programlama", "2025-01-15 09:00", "Çarşamba 13:00-16:00", 101, 6),
        ("CS201", "Veri Yapıları", "2025-01-08 11:00", "Cuma 09:00-12:00", 101, 6),

        # Arch
        ("ARCH101", "Temel Tasarım", "2025-01-07 09:00", "Pazartesi 09:00-13:00", 102, 8),
        ("ARCH201", "Mimari Tasarım", "2025-01-20 09:00", "Salı 13:00-17:00", 102, 8),
        ("ARCH205", "Mimarlık Tarihi", "2025-01-18 10:00", "Çarşamba 10:00-12:00", 106, 4),
        ("ARCH302", "Yapı Statiği", "2025-01-14 14:00", "Perşembe 14:00-16:00", 102, 5),
        ("ART101", "Sanat Tarihi", "2025-01-16 11:00", "Cuma 10:00-12:00", 102, 3),

        # Med
        ("MED101", "Anatomi", "2025-01-10 09:00", "Pazartesi 08:00-12:00", 103, 10),
        ("MED104", "Biyokimya", "2025-01-14 13:00", "Salı 09:00-12:00", 103, 8),
        ("MED201", "Fizyoloji", "2025-01-12 10:00", "Çarşamba 08:00-12:00", 103, 9),
        ("MED106", "Tıbbi Biyoloji", "2025-01-09 14:00", "Perşembe 13:00-15:00", 103, 6),
        ("MED303", "Patoloji", "2025-01-19 13:00", "Cuma 13:00-16:00", 103, 9),

        # Law
        ("LAW101", "Anayasa Hukuku", "2025-01-11 10:00", "Pazartesi 10:00-13:00", 104, 7),
        ("LAW105", "Roma Hukuku", "2025-01-16 14:00", "Salı 14:00-16:00", 104, 6),
        ("LAW202", "Ceza Hukuku", "2025-01-13 10:00", "Çarşamba 10:00-13:00", 104, 7),
        ("LAW301", "Medeni Hukuk", "2025-01-17 09:00", "Perşembe 09:00-12:00", 104, 7),
        ("LAW404", "İdare Hukuku", "2025-01-21 11:00", "Cuma 14:00-17:00", 104, 6)
    ]
    c.executemany("INSERT INTO courses VALUES (?,?,?,?,?,?)", courses)
    
    # --- ENROLLMENTS ---
    # Added project_score as last column
    enrollments = []
    
    # 1. Ayşe (Comp Eng) - Scores added to projects
    enrollments.extend([
        ("21010101", "ENG101", None, None, 0, 1, 0, None, None, None, None), 
        ("21010101", "TURK101", 88, 90, 0, 0, 0, None, None, None, None), 
        ("21010101", "MATH101", 75, 80, 0, 0, 1, None, None, None, None), 
        ("21010101", "PHYS101", 70, 75, 0, 0, 2, "Fizik Lab Raporu", "2025-01-10", "Deney sonuçları", 85), 
        ("21010101", "CS101", 95, 92, 0, 0, 0, None, None, None, None), 
        ("21010101", "CS305", 85, None, 0, 0, 1, "E-Ticaret Sitesi", "2025-01-20", "API tamamlanmalı", 90), 
        ("21010101", "CS302", 70, None, 0, 0, 2, "Satranç Botu", "2025-01-25", "Algoritma optimize edilecek", None) # Not graded yet
    ])

    # 2. Mehmet (Arch)
    enrollments.extend([
        ("21010102", "ENG101", 50, 60, 0, 0, 1, None, None, None, None), 
        ("21010102", "TURK101", 65, 70, 0, 0, 0, None, None, None, None), 
        ("21010102", "ARCH101", 70, 75, 0, 0, 1, "Temel Tasarım Paftası", "2025-01-12", "Eksik çizimler var", 70), 
        ("21010102", "ARCH201", 60, None, 0, 0, 2, "Kültür Merkezi Maketi", "2025-01-22", "Ölçek hatalı", None), # Ongoing
        ("21010102", "ARCH205", 40, None, 1, 0, 4, None, None, None, None), 
        ("21010102", "ARCH302", 45, None, 0, 0, 3, None, None, None, None), 
        ("21010102", "ART101", 80, 85, 0, 0, 0, "Rönesans Sanatı Sunumu", "2025-01-18", "Hazır", 95) 
    ])

    # 3. Zeynep (Med)
    enrollments.extend([
        ("21010103", "MED101", 90, None, 0, 0, 1, None, None, None, None), 
        ("21010103", "MED104", 88, None, 0, 0, 0, None, None, None, None), 
        ("21010103", "MED201", 92, None, 0, 0, 0, None, None, None, None), 
        ("21010103", "MED106", 85, 87, 0, 0, 1, None, None, None, None), 
        ("21010103", "MED303", 89, None, 0, 0, 0, None, None, None, None), 
        ("21010103", "ENG101", 95, 98, 0, 0, 0, None, None, None, None), 
        ("21010103", "TURK101", 90, 92, 0, 0, 0, None, None, None, None) 
    ])

    # 4. Ali (Law)
    enrollments.extend([
        ("21010104", "LAW101", 35, 40, 1, 0, 5, None, None, None, None), # Retake (Failed previously)
        ("21010104", "LAW105", 65, None, 0, 0, 1, "Roma Hukukunda Mülkiyet Sunumu", "2025-01-15", "Slaytlar yüklenecek", 65), 
        ("21010104", "LAW202", 40, 45, 1, 0, 0, None, None, None, None), # Retake
        ("21010104", "LAW301", 50, 55, 0, 0, 4, "Boşanma Davası Analizi", "2025-01-19", "Araştırma devam ediyor", None), # Ongoing
        ("21010104", "LAW404", 70, 72, 0, 0, 2, None, None, None, None), 
        ("21010104", "ENG101", 45, 50, 1, 0, 6, None, None, None, None), # Retake
        ("21010104", "TURK101", 60, 65, 0, 0, 2, None, None, None, None) 
    ])
    
    # 1. Ayşe (Comp Eng) - Add a retake
    enrollments.append(("21010101", "PHYS101", 30, 48, 1, 0, 4, None, None, None, None)) # Retake Physics

    c.executemany("INSERT INTO enrollments VALUES (?,?,?,?,?,?,?,?,?,?,?)", enrollments)
    
    conn.commit()

# Query Helpers
def get_student(student_id):
    conn = get_db_connection()
    student = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    conn.close()
    return student

def get_student_details_full(student_id):
    conn = get_db_connection()
    c = conn.cursor()
    
    # Advisor
    advisor = c.execute('''
        SELECT i.name, i.email, i.office 
        FROM students s 
        JOIN instructors i ON s.advisor_id = i.id 
        WHERE s.id = ?
    ''', (student_id,)).fetchone()
    
    # Courses with Instructor Info
    rows = c.execute('''
        SELECT c.name, c.code, c.exam_date, c.schedule, c.credit,
               e.midterm, e.final, e.is_retake, e.is_exempt, e.attendance_absent,
               e.project_topic, e.project_deadline, e.project_note, e.project_score,
               i.name as instructor_name, i.office as instructor_office, i.email as instructor_email
        FROM enrollments e
        JOIN courses c ON e.course_code = c.code
        JOIN instructors i ON c.instructor_id = i.id
        WHERE e.student_id = ?
    ''', (student_id,)).fetchall()
    
    conn.close()
    return advisor, rows
