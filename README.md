Week 5 – Security Enhancements in Python Applications

Author: Manjusri Mohanty  
Date: 2026-08-16  

Overview

This project demonstrates how to identify and fix common security vulnerabilities in a Python CLI application. It includes both an insecure baseline (for learning) and a hardened secure version, along with tests and a detailed security audit.

Project Structure

- `insecure_user_manager.py` – Vulnerable version with intentional flaws (for audit reference)  
- `secure_user_manager.py` – Hardened version with security fixes applied  
- `test_secure_app.py` – Unit tests and security-oriented validations  
- `security_audit_report.md` – Comprehensive audit: vulnerabilities, exploit scenarios, and mitigations  
- `README.md` – This file  

 How to Run

 Insecure Version (Learning Only – Do Not Use with Real Data)

```bash
python insecure_user_manager.py
```

Secure Version

```bash
python secure_user_manager.py
```

 Run Tests

```bash
python -m unittest test_secure_app.py
```

 Security Measures Implemented

- Parameterized SQL Queries: Prevents SQL injection by separating data from query logic.  
- Salted Password Hashing: Stores salted SHA-256 hashes instead of plain-text passwords.  
- Input Validation: Enforces rules on username format, email structure, password length, and search term size.  
- Safe Error Handling: Shows generic messages to users; logs detailed errors securely for debugging.  
- No Password Exposure: Passwords are never displayed in search results or logs.  
- Security Logging: Tracks key events (user additions, invalid inputs, errors) to `security.log` for monitoring.  



- The insecure version is provided solely to illustrate typical beginner mistakes and support the audit narrative.  
- For production use, replace SHA-256 with a dedicated password hasher (e.g., `bcrypt` or `argon2`), add authentication with rate limiting, and harden deployment (file permissions, log rotation, dependency scanning).  
