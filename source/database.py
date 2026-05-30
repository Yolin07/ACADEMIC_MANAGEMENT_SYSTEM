import hashlib
import secrets
import sqlite3
from pathlib import Path


class Database:
    def __init__(self, db_name=None):
        default_db_path = Path(__file__).with_name("secured_academic.db")
        self.db_name = str(default_db_path if db_name is None else db_name)
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # SQL TABLE 1: Teachers
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS teachers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    recovery_question TEXT NOT NULL,
                    recovery_answer TEXT NOT NULL
                )
            """)

            # SQL TABLE 2: Folders
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS folders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    teacher_id INTEGER NOT NULL,
                    folder_name TEXT NOT NULL,
                    educational_level TEXT NOT NULL,
                    UNIQUE(teacher_id, folder_name),
                    FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE CASCADE
                )
            """)

            # SQL TABLE 3: Grades
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS student_grades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    folder_id INTEGER NOT NULL,
                    semester_segment TEXT NOT NULL,
                    student_number TEXT NOT NULL,
                    student_name TEXT NOT NULL,
                    subject_name TEXT NOT NULL,
                    period_name TEXT NOT NULL,
                    numeric_grade REAL NOT NULL,
                    UNIQUE(folder_id, semester_segment, student_number, subject_name, period_name),
                    FOREIGN KEY (folder_id) REFERENCES folders(id) ON DELETE CASCADE
                )
            """)
            conn.commit()

    def _hash_data(self, plaintext: str, salt: str = None) -> str:
        if not salt:
            salt = secrets.token_hex(16)
        dk = hashlib.pbkdf2_hmac("sha256", plaintext.encode(), salt.encode(), 100_000)
        return f"{salt}${dk.hex()}"

    def _verify_hash(self, plaintext: str, stored_hash: str) -> bool:
        try:
            salt, _ = stored_hash.split("$", 1)
            return self._hash_data(plaintext, salt) == stored_hash
        except (ValueError, AttributeError):
            return False

    def register(self, username, password, question, answer) -> bool:
        try:
            hashed_password = self._hash_data(password)
            hashed_answer = self._hash_data(answer.strip().lower())
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO teachers (username, password, recovery_question, recovery_answer) VALUES (?, ?, ?, ?)",
                    (username, hashed_password, question, hashed_answer)
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False

    def authenticate(self, username, password) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM teachers WHERE username = ?", (username,))
            row = cursor.fetchone()
            if row:
                return self._verify_hash(password, row[0])
        return False

    def get_teacher_id(self, username):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM teachers WHERE username = ?", (username,))
            row = cursor.fetchone()
            return row[0] if row else None

    def get_recovery_question(self, username):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT recovery_question FROM teachers WHERE username = ?", (username,))
            row = cursor.fetchone()
            return row[0] if row else None

    def verify_recovery(self, username, answer) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT recovery_answer FROM teachers WHERE username = ?", (username,))
            row = cursor.fetchone()
            if row:
                return self._verify_hash(answer.strip().lower(), row[0])
        return False

    def reset_password(self, username, new_password):
        hashed_password = self._hash_data(new_password)
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE teachers SET password = ? WHERE username = ?", (hashed_password, username))
            conn.commit()

    def get_folders(self, teacher_id):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT folder_name, educational_level FROM folders WHERE teacher_id = ?", (teacher_id,))
            return {row[0]: {"level": row[1]} for row in cursor.fetchall()}

    def add_folder(self, teacher_id, name, level) -> bool:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO folders (teacher_id, folder_name, educational_level) VALUES (?, ?, ?)",
                               (teacher_id, name, level))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False

    def delete_folder(self, teacher_id, name):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM folders WHERE teacher_id = ? AND folder_name = ?", (teacher_id, name))
            conn.commit()

    def get_folder_id(self, teacher_id, folder_name):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM folders WHERE teacher_id = ? AND folder_name = ?", (teacher_id, folder_name))
            row = cursor.fetchone()
            return row[0] if row else None

    def save_grade(self, folder_id, semester, student_id, name, subject, period, grade):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO student_grades (folder_id, semester_segment, student_number, student_name, subject_name, period_name, numeric_grade)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(folder_id, semester_segment, student_number, subject_name, period_name) DO UPDATE SET
                    student_name = excluded.student_name,
                    numeric_grade = excluded.numeric_grade
            """, (folder_id, semester, student_id, name, subject, period, grade))
            conn.commit()

    def delete_student(self, folder_id, semester, student_id):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM student_grades WHERE folder_id = ? AND semester_segment = ? AND student_number = ?",
                           (folder_id, semester, student_id))
            conn.commit()

    def get_semester_records(self, folder_id, semester):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT student_number, student_name, subject_name, period_name, numeric_grade
                FROM student_grades
                WHERE folder_id = ? AND semester_segment = ?
            """, (folder_id, semester))

            structured_data = {}
            for s_num, s_name, sub, prd, grd in cursor.fetchall():
                if s_num not in structured_data:
                    structured_data[s_num] = {"name": s_name, "grades": {}, "raw_list": []}
                col_key = f"[{prd}] {sub}"
                structured_data[s_num]["grades"][col_key] = grd
                structured_data[s_num]["raw_list"].append(grd)
            return structured_data
