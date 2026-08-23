# test_secure_app.py
import os
import sqlite3
import unittest
import tempfile
import shutil

import secure_user_manager as app

class TestSecureUserManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_dir = tempfile.mkdtemp()
        cls.db_path = os.path.join(cls.test_dir, "test_users.db")
        cls.log_path = os.path.join(cls.test_dir, "test_security.log")
        app.DB_PATH = cls.db_path
        app.LOG_PATH = cls.log_path
        app.init_db()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.test_dir, ignore_errors=True)

    def test_add_and_search_user(self):
        username = "testuser"
        email = "test@example.com"
        password = "strongpassword123"
        ok = app.add_user(username, email, password)
        self.assertTrue(ok)

        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute(
            "SELECT id, username, email, password_hash, salt FROM users WHERE username = ?",
            (username,)
        )
        row = cur.fetchone()
        conn.close()

        self.assertIsNotNone(row)
        db_id, db_user, db_email, pwd_hash, salt = row
        self.assertEqual(db_user, username)
        self.assertEqual(db_email, email)
        self.assertNotEqual(pwd_hash, password)
        self.assertTrue(len(salt) > 0)

    def test_sql_injection_in_add_user(self):
        malicious_username = "'); DROP TABLE users; --"
        email = "attacker@evil.com"
        password = "password123"
        ok = app.add_user(malicious_username, email, password)
        self.assertFalse(ok)

        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
        )
        row = cur.fetchone()
        conn.close()
        self.assertIsNotNone(row)

    def test_sql_injection_in_search(self):
        app.add_user("alice", "alice@example.com", "password123")
        malicious_term = "' OR '1'='1"
        try:
            app.search_users(malicious_term)
        except Exception:
            self.fail("search_users raised an exception on malicious input")

        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM users")
        count = cur.fetchone()[0]
        conn.close()
        self.assertGreater(count, 0)

    def test_weak_password_rejected(self):
        ok = app.add_user("weakuser", "weak@example.com", "123")
        self.assertFalse(ok)

    def test_invalid_email_rejected(self):
        ok = app.add_user("bademail", "not-an-email", "password123")
        self.assertFalse(ok)

if __name__ == "__main__":
    unittest.main()