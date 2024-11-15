from database import connect_db, get_cursor
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, username, user_id=None):
        self.username = username
        self.user_id = user_id

    @staticmethod
    def create_user(username, password):
        conn = connect_db()
        cursor = get_cursor(conn)
        password_hash = generate_password_hash(password)
        try:
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return User(username, user_id)
        except sqlite3.IntegrityError:
            conn.close()
            return None

    @staticmethod
    def authenticate(username, password):
        conn = connect_db()
        cursor = get_cursor(conn)
        cursor.execute(
            "SELECT id, password_hash FROM users WHERE username = ?",
            (username,)
        )
        result = cursor.fetchone()
        conn.close()

        if result and check_password_hash(result[1], password):
            return User(username, result[0])
        return None

    @staticmethod
    def get_by_id(user_id):
        conn = connect_db()
        cursor = get_cursor(conn)
        cursor.execute(
            "SELECT username FROM users WHERE id = ?",
            (user_id,)
        )
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return User(result[0], user_id)
        return None