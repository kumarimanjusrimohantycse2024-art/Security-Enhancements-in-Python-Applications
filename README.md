# Security Enhancements in Python Applications

This repository demonstrates how to evolve a vulnerable Python CLI app into a more secure implementation while preserving core functionality.

## Value proposition

- Practical side-by-side learning: insecure vs secure implementation.
- Concrete mitigations for common application security flaws.
- Runnable tests that verify security-focused behavior.

## Features

- User add/search workflow backed by SQLite.
- Input validation for usernames, emails, passwords, and search terms.
- Parameterized SQL queries to reduce SQL injection risk.
- Salted SHA-256 password hashing (educational baseline).
- Safer error handling and security event logging.

## Tech stack

- [Python 3](https://www.python.org/)
- [sqlite3](https://docs.python.org/3/library/sqlite3.html) (standard library)
- [unittest](https://docs.python.org/3/library/unittest.html) (standard library)

## Project structure

- [`secure_user_manager.py`](./secure_user_manager.py) - hardened CLI implementation.
- [`insecure_user_manager.py`](./insecure_user_manager.py) - intentionally vulnerable baseline for comparison.
- [`test_secure_app.py`](./test_secure_app.py) - unit/security behavior tests.
- [`security_audit_report.md`](./security_audit_report.md) - audit findings and mitigations.
- [`security.log`](./security.log) - runtime log output file (created/updated during runs).

## Prerequisites

- Python 3.9+ available on `PATH`.

## Installation

```bash
git clone https://github.com/kumarimanjusrimohantycse2024-art/Security-Enhancements-in-Python-Applications.git
cd Security-Enhancements-in-Python-Applications
```

No third-party dependencies are required.

## Configuration

By default, the secure app writes to:

- SQLite DB: `users_secure.db`
- Log file: `security.log`

These defaults are defined in [`secure_user_manager.py`](./secure_user_manager.py).

## Usage

Run the secure application:

```bash
python secure_user_manager.py
```

Run the insecure learning baseline:

```bash
python insecure_user_manager.py
```

## Testing

Run tests:

```bash
python -m unittest -v test_secure_app.py
```

## Troubleshooting

- **`python: command not found`**: use `python3` instead of `python`.
- **Permission issues writing DB/log files**: run in a writable directory.
- **Duplicate user/email errors**: usernames and emails must be unique.

## CI

This repository includes a GitHub Actions workflow:

- [`python-ci.yml`](./.github/workflows/python-ci.yml) - runs unit tests on pushes and pull requests.

## Contributing

1. Fork the repository.
2. Create a branch for your change.
3. Run tests locally.
4. Open a pull request with a clear summary.

## License and project status

- **License:** No license file is currently present in this repository.
- **Status:** Active educational project focused on secure coding practices in Python CLI applications.
