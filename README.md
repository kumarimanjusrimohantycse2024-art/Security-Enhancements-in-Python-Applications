# Week 5 – Security Enhancements in Python Applications

**Author:** Manjusri Mohanty  
**Date:** 2026-08-16  

## Files

- `insecure_user_manager.py` – Vulnerable version.
- `secure_user_manager.py` – Secure version.
- `test_secure_app.py` – Tests.
- `security_audit_report.md` – Audit report.
- `README.md` – This file.

## Run

Insecure (only for learning):

```bash
python insecure_user_manager.py
```

Secure:

```bash
python secure_user_manager.py
```

Tests:

```bash
python -m unittest test_secure_app.py
```

## Security Measures

- Parameterized queries.
- Salted password hashing.
- Input validation.
- Safe errors + logging.
- No password exposure.