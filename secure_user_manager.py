# secure_user_manager.py
import sqlite3
import os
import hashlib
import re
import logging

DB_PATH = "users_secure.db"
LOG_PATH = "security.log"

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    logger.info("Database initialized.")

def generate_salt() -> str:
    return os.urandom(16).hex()

def hash_password(password: str, salt: str) -> str:
    return hashlib.sha256((password + salt).encode("utf-8")).hexdigest()

def validate_username(username: str) -> bool:
    if not username or len(username) < 3 or len(username) > 30:
        return False
    return re.match(r"^[A-Za-z0-9_-]+$", username) is not None

def validate_email(email: str) -> bool:
    if not email or len(email) > 254:
        return False
    return EMAIL_REGEX.match(email) is not None

def validate_password(password: str) -> bool:
    if not password or len(password) < 8:
        return False
    return True

def add_user(username: str, email: str, password: str) -> bool:
    if not validate_username(username):
        logger.warning(f"Invalid username attempt: {username!r}")
        print("Invalid username. Use 3–30 chars, letters/numbers/_/- only.")
        return False
    if not validate_email(email):
        logger.warning(f"Invalid email attempt: {email!r}")
        print("Invalid email format.")
        return False
    if not validate_password(password):
        logger.warning("Weak password attempt.")
        print("Password must be at least 8 characters.")
        return False

    salt = generate_salt()
    password_hash = hash_password(password, salt)

    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (username, email, password_hash, salt) VALUES (?, ?, ?, ?)",
            (username, email, password_hash, salt)
        )
        conn.commit()
        conn.close()
        logger.info(f"User added: {username}")
        print("User added successfully.")
        return True
    except sqlite3.IntegrityError:
        logger.warning(f"Duplicate user attempt: {username} or {email}")
        print("Username or email already exists.")
        return False
    except Exception as e:
        logger.error(f"Unexpected error in add_user: {e}", exc_info=True)
        print("An unexpected error occurred. Please try again later.")
        return False

def search_users(query_text: str):
    if not query_text or len(query_text) > 50:
        print("Invalid search term.")
        logger.warning(f"Invalid search term: {query_text!r}")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(
            "SELECT id, username, email FROM users WHERE username LIKE ? OR email LIKE ?",
            (f"%{query_text}%", f"%{query_text}%")
        )
        rows = cur.fetchall()
        conn.close()

        if not rows:
            print("No users found.")
            return

        print("Search results:")
        for r in rows:
            print(f"ID: {r[0]}, Username: {r[1]}, Email: {r[2]}")
        logger.info(f"Search performed with term: {query_text!r}, found {len(rows)} rows.")
    except Exception as e:
        logger.error(f"Unexpected error in search_users: {e}", exc_info=True)
        print("An unexpected error occurred while searching.")

def main():
    init_db()
    while True:
        print("\n=== Secure User Data Manager ===")
        print("1. Add user")
        print("2. Search users")
        print("3. Exit")
        choice = input("Enter choice (1/2/3): ").strip()
        if choice == "1":
            username = input("Username: ").strip()
            email = input("Email: ").strip()
            password = input("Password: ").strip()
            add_user(username, email, password)
        elif choice == "2":
            q = input("Search term: ").strip()
            search_users(q)
        elif choice == "3":
            print("Exiting.")
            logger.info("Application exited by user.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()