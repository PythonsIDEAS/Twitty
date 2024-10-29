import sqlite3
from contextlib import contextmanager

class Database:
    def __init__(self, db_name):
        self.db_name = db_name

    @contextmanager
    def connect(self):
        conn = sqlite3.connect(self.db_name)
        try:
            yield conn
        finally:
            conn.close()

    def create_tables(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            # Create tweets table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tweets (
                    id INTEGER PRIMARY KEY,
                    text TEXT NOT NULL
                )
            """)
            # Create users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            """)
            conn.commit()

    def insert_data(self, table_name, data):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO {table_name} (text) VALUES (?)", data)
            conn.commit()

    def get_data(self, table_name):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            return cursor.fetchall()

    def register_user(self, username, email, password):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (username, email, password) VALUES (?, ?, ?)
            """, (username, email, password))
            conn.commit()

    def verify_user(self, username, password):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM users WHERE username = ? AND password = ?
            """, (username, password))
            return cursor.fetchone() is not None

    def search_data(self, table_name, search_term):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name} WHERE text LIKE ?", ('%' + search_term + '%',))
            return cursor.fetchall()
