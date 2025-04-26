import sqlite3
from datetime import datetime

def get_connection():
    conn = sqlite3.connect('vg_tutor.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_tutor INTEGER NOT NULL
        )
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            tutor_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            subject TEXT,
            FOREIGN KEY(student_id) REFERENCES users(id),
            FOREIGN KEY(tutor_id) REFERENCES users(id)
        )
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER NOT NULL,
            receiver_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY(sender_id) REFERENCES users(id),
            FOREIGN KEY(receiver_id) REFERENCES users(id)
        )
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reviewer_id INTEGER NOT NULL,
            tutor_id INTEGER NOT NULL,
            rating INTEGER NOT NULL,
            comment TEXT,
            timestamp TEXT NOT NULL,
            FOREIGN KEY(reviewer_id) REFERENCES users(id),
            FOREIGN KEY(tutor_id) REFERENCES users(id)
        )
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reporter_id INTEGER NOT NULL,
            reported_id INTEGER NOT NULL,
            reason TEXT,
            evidence_path TEXT,
            timestamp TEXT NOT NULL,
            FOREIGN KEY(reporter_id) REFERENCES users(id),
            FOREIGN KEY(reported_id) REFERENCES users(id)
        )
        """)
        conn.commit()

# User operations
def add_user(username, password_hash, is_tutor):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (username, password, is_tutor)
                VALUES (?, ?, ?)
            """, (username, password_hash, is_tutor))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False

def get_user_by_username(username):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        return cursor.fetchone()

def get_user_by_id(user_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()

def get_all_users():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()

def get_tutors():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE is_tutor = 1")
        return cursor.fetchall()

# Booking operations
def add_booking(student_id, tutor_id, date, time, subject):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO bookings (student_id, tutor_id, date, time, subject)
            VALUES (?, ?, ?, ?, ?)
        """, (student_id, tutor_id, date, time, subject))
        conn.commit()

def get_bookings_for_student(student_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bookings WHERE student_id = ?", (student_id,))
        return cursor.fetchall()

def get_bookings_for_tutor(tutor_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bookings WHERE tutor_id = ?", (tutor_id,))
        return cursor.fetchall()

# Message operations
def add_message(sender_id, receiver_id, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO messages (sender_id, receiver_id, message, timestamp)
            VALUES (?, ?, ?, ?)
        """, (sender_id, receiver_id, message, timestamp))
        conn.commit()

def get_messages_between(user1_id, user2_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM messages
            WHERE (sender_id = ? AND receiver_id = ?)
               OR (sender_id = ? AND receiver_id = ?)
            ORDER BY timestamp
        """, (user1_id, user2_id, user2_id, user1_id))
        return cursor.fetchall()

# Review operations
def add_review(reviewer_id, tutor_id, rating, comment):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO reviews (reviewer_id, tutor_id, rating, comment, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (reviewer_id, tutor_id, rating, comment, timestamp))
        conn.commit()

def get_reviews_for_tutor(tutor_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reviews WHERE tutor_id = ?", (tutor_id,))
        return cursor.fetchall()

# Report operations
def add_report(reporter_id, reported_id, reason, evidence_path=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO reports (reporter_id, reported_id, reason, evidence_path, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (reporter_id, reported_id, reason, evidence_path, timestamp))
        conn.commit()

def get_reports_for_user(user_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reports WHERE reported_id = ?", (user_id,))
        return cursor.fetchall()
