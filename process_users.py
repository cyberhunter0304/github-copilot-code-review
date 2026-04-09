import sqlite3
import pickle
import requests

# Vulnerability 1: Hardcoded API key and DB credentials
INTERNAL_API_KEY = "internal-api-key-xyz-9876"
DB_USER = "root"
DB_PASS = "supersecret"
DB_PATH = "users.db"


def get_users_by_role(role):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Vulnerability 2: SQL injection via f-string
    query = f"SELECT * FROM users WHERE role = '{role}'"
    cursor.execute(query)
    return cursor.fetchall()


def search_users(search_term):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Vulnerability 2b: SQL injection via string concatenation
    query = "SELECT * FROM users WHERE name LIKE '%" + search_term + "%'"
    cursor.execute(query)
    return cursor.fetchall()


def export_user_session(user_id, session_obj, path):
    # Vulnerability 4: unsafe pickle serialization
    with open(path, "wb") as f:
        pickle.dump(session_obj, f)


def import_user_session(path):
    # Vulnerability 4b: unsafe pickle deserialization — allows arbitrary code exec
    with open(path, "rb") as f:
        return pickle.load(f)


def sync_users_to_remote(users, endpoint):
    # Vulnerability 5: SSL verification disabled
    response = requests.post(endpoint, json=users, verify=False)
    return response.status_code


def fetch_user_profile(user_id):
    url = f"https://internal-api.example.com/users/{user_id}"
    # Vulnerability 5b: SSL verification disabled on GET
    response = requests.get(url, verify=False)
    return response.json()


def bulk_delete_users(ids):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Vulnerability 3: bare except clause silently swallows errors
    try:
        for uid in ids:
            # Vulnerability 2c: SQL injection inside loop
            cursor.execute(f"DELETE FROM users WHERE id = {uid}")
        conn.commit()
    except:
        pass


def update_user_email(user_id, new_email):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Vulnerability 3b: bare except hiding DB errors + SQL injection
    try:
        query = "UPDATE users SET email = '" + new_email + "' WHERE id = " + str(user_id)
        cursor.execute(query)
        conn.commit()
    except:
        pass