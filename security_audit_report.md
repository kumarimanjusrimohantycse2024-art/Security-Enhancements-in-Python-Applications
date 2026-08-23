# Security Audit Report  
**Project:** Secure User Data Manager (Python CLI Application)  
**Author:** Manjusri Mohanty  
**Date:** 2026-08-16  

## 1. Application Overview

CLI app that stores users (username, email, password) in SQLite, allows adding and searching users.  
Two versions: `insecure_user_manager.py` (vulnerable) and `secure_user_manager.py` (fixed).

## 2. Vulnerabilities in Insecure Version

### 2.1 SQL Injection in add_user

- Code: `query = f"INSERT INTO users ... VALUES ('{username}', '{email}', '{password}')"`
- Risk: Attacker can run arbitrary SQL (e.g. drop tables).
- Fix: Use parameterized query with `?` placeholders.

### 2.2 SQL Injection in search_users

- Code: `sql = f"SELECT ... WHERE username LIKE '%{query_text}%'"`
- Risk: Attacker can retrieve all rows or modify data.
- Fix: Use parameterized query.

### 2.3 Plain-text Password Storage

- Passwords stored as-is in DB.
- Risk: DB leak → all passwords exposed.
- Fix: Store salted hash (`SHA256(password + salt)`).

### 2.4 Error Messages Leak Info

- Code: `print("Error occurred:", e)`
- Risk: Shows DB errors, paths, etc.
- Fix: Log details, show generic message to user.

### 2.5 No Input Validation

- No checks on username/email/password/search length.
- Risk: Bad inputs, injection, DoS.
- Fix: Validate format and length.

### 2.6 Passwords Shown in Search

- Search prints password field.
- Risk: Any user can see all passwords.
- Fix: Don’t select or print passwords.

### 2.7 No Logging

- No audit trail.
- Fix: Log key events to `security.log`.

## 3. Security Fixes in Secure Version

- Parameterized SQL queries.
- Salted password hashing.
- Input validation (username, email, password, search).
- Safe error handling + logging.
- No password in output.

## 4. Testing

`test_secure_app.py` checks:

- Add/search works.
- Passwords not plain text.
- Invalid inputs rejected.
- Simple SQL injection blocked.

Run: `python -m unittest test_secure_app.py`

## 5. Conclusion

Insecure version shows common mistakes.  
Secure version fixes them while keeping same features.