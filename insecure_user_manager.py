# insecure_user_manager.py
import sqlite3

DB_PATH = "users.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            email TEXT,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_user(username, email, password):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    query = f"INSERT INTO users (username, email, password) VALUES ('{username}', '{email}', '{password}')"
    cur.execute(query)
    conn.commit()
    conn.close()
    print("User added successfully.")

def search_users(query_text):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    sql = f"SELECT id, username, email, password FROM users WHERE username LIKE '%{query_text}%' OR email LIKE '%{query_text}%'"
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    if not rows:
        print("No users found.")
        return
    for r in rows:
        print(f"ID: {r[0]}, Username: {r[1]}, Email: {r[2]}, Password: {r[3]}")

def main():
    init_db()
    while True:
        print("\n=== User Data Manager (Insecure) ===")
        print("1. Add user")
        print("2. Search users")
        print("3. Exit")
        choice = input("Enter choice (1/2/3): ").strip()
        if choice == "1":
            username = input("Username: ")
            email = input("Email: ")
            password = input("Password: ")
            try:
                add_user(username, email, password)
            except Exception as e:
                print("Error occurred:", e)
        elif choice == "2":
            q = input("Search term: ")
            try:
                search_users(q)
            except Exception as e:
                print("Error occurred:", e)
        elif choice == "3":
            print("Exiting.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()