# Code Review Instructions

You are performing a code review. When reviewing, check for:

1. **Security** — SQL injection, hardcoded secrets, unsafe deserialization, 
   disabled SSL verification
2. **Error handling** — bare except clauses, silent failures, unhandled edge cases
3. **Readability** — nested conditionals deeper than 2 levels, non-Pythonic patterns
4. **Standards** — no string formatting in SQL queries, no hardcoded credentials

For each issue found, provide:
- The line number
- What the problem is
- A corrected code snippet