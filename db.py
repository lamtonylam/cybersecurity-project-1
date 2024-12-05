import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


class Database:
    def __init__(self, db_name="notes.db"):
        self.db_name = db_name
        self.init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        conn = self.get_connection()
        c = conn.cursor()
        # create user table and notes table
        c.execute(
            """CREATE TABLE IF NOT EXISTS users
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     username TEXT UNIQUE NOT NULL,
                     password TEXT NOT NULL,
                     admin INTEGER DEFAULT 0)"""
        )
        c.execute(
            """CREATE TABLE IF NOT EXISTS notes
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     user_id INTEGER,
                     content TEXT NOT NULL,
                     FOREIGN KEY (user_id) REFERENCES users (id))"""
        )
        # add admin user
        c.execute(
            """INSERT OR IGNORE INTO users (username, password, admin)
                    VALUES (?, ?, 1)""",
            ("admin", generate_password_hash("iamadmin")),
        )
        conn.commit()
        conn.close()

    def register_user(self, username, password):
        conn = self.get_connection()
        c = conn.cursor()

        if c.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone():
            conn.close()
            return False

        c.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, generate_password_hash(password)),
        )
        conn.commit()
        conn.close()
        return True

    def authenticate_user(self, username, password):
        conn = self.get_connection()
        c = conn.cursor()
        user = c.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            return dict(user)
        return None

    def add_note(self, user_id, content):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute(
            "INSERT INTO notes (user_id, content) VALUES (?, ?)", (user_id, content)
        )
        conn.commit()
        conn.close()
        return True

    def get_user_notes(self, user_id):
        conn = self.get_connection()
        c = conn.cursor()
        notes = c.execute(
            "SELECT * FROM notes WHERE user_id = ?", (user_id,)
        ).fetchall()
        conn.close()
        return [dict(note) for note in notes]

    def get_all_notes(self):
        conn = self.get_connection()
        c = conn.cursor()
        notes = c.execute("SELECT * FROM notes").fetchall()
        conn.close()
        return [dict(note) for note in notes]

    def is_admin(self, user_id):
        conn = self.get_connection()
        c = conn.cursor()
        user = c.execute("SELECT admin FROM users WHERE id = ?", (user_id,)).fetchone()
        conn.close()
        return bool(user and user["admin"])
