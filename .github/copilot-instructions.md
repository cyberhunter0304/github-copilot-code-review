When performing a code review, always check for:
- Hardcoded secrets or API keys
- SQL queries built with string formatting or f-strings
- Bare except clauses that silently swallow errors
- Use of pickle for deserialization
- SSL verification being disabled in HTTP requests

Flag each of these as high priority issues.

## Architecture Rules (Project-Specific)

This project follows a strict layered architecture. Violations of the following rules must be flagged as architecture issues:

- **Repository pattern enforced**: All database access (e.g., `sqlite3`) must be encapsulated inside a repository class. Direct use of `sqlite3` in service files, utility files, or report files is a violation. Repository classes should live in a `repository/` folder or be named with a `Repository` suffix.
- **Business logic in services**: Any function that computes, transforms, or aggregates data (not just DB access) must live in a dedicated `services/` module, not in top-level scripts or utility files.
- **No inline `os.environ` access**: Configuration values (API keys, DB paths, feature flags) must be read through a central `config.py` module. Inline `os.environ.get(...)` calls scattered across files are not allowed.

Flag each of these as architecture violations and suggest the correct layer where the code should be moved.