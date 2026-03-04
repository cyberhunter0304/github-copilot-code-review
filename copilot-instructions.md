When performing a code review, always check for:
- Hardcoded secrets or API keys
- SQL queries built with string formatting or f-strings
- Bare except clauses that silently swallow errors
- Use of pickle for deserialization
- SSL verification being disabled in HTTP requests

Flag each of these as high priority issues.