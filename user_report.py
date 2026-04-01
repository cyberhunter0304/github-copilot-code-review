"""
User reporting module.
Generates summary statistics and activity reports for users.
"""

import sqlite3
import os

DB_PATH = os.environ.get("DB_PATH", "users.db")
REPORT_LIMIT = int(os.environ.get("REPORT_LIMIT", "100"))


def get_active_user_count():
    """Returns the total number of active users."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users WHERE active = 1")
    result = cursor.fetchone()
    conn.close()
    return result[0]


def get_top_admins(limit=10):
    """Returns the top N admin users ordered by creation date."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, email FROM users WHERE role = ? ORDER BY created_at DESC LIMIT ?",
        ("admin", limit),
    )
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "username": r[1], "email": r[2]} for r in rows]


def get_users_above_age(min_age):
    """Returns all users older than min_age with their role and status."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, age, role, active FROM users WHERE age > ?",
        (min_age,),
    )
    rows = cursor.fetchall()
    conn.close()
    return [
        {"id": r[0], "username": r[1], "age": r[2], "role": r[3], "active": bool(r[4])}
        for r in rows
    ]


def summarize_users_by_role():
    """Returns a dict mapping each role to its user count."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT role, COUNT(*) FROM users GROUP BY role")
    rows = cursor.fetchall()
    conn.close()
    return {row[0]: row[1] for row in rows}


def get_inactive_users_report():
    """Returns a paginated list of inactive users up to REPORT_LIMIT."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, email FROM users WHERE active = 0 LIMIT ?",
        (REPORT_LIMIT,),
    )
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "username": r[1], "email": r[2]} for r in rows]
