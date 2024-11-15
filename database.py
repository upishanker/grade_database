import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def connect_db():
    conn = sqlite3.connect('grades.db')
    return conn

def get_cursor(conn):
    return conn.cursor()

def create_tables():
    conn = connect_db()
    cursor = get_cursor(conn)

  # Users table with password
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username TEXT NOT NULL UNIQUE,
      password_hash TEXT NOT NULL
  )
  """)

  # Rest of the tables remain the same
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      hours INTEGER NOT NULL,
      user_id INTEGER,
      FOREIGN KEY (user_id) REFERENCES users (id)
  )
  """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assignments (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      grade REAL,
      weight REAL NOT NULL,
      course_id INTEGER,
      FOREIGN KEY (course_id) REFERENCES courses (id)
  )
  """)

    conn.commit()
    conn.close()

def init_db():
    create_tables()