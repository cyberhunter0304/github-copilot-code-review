import os
import sqlite3
import pickle
import requests

# Vulnerability 1: Hardcoded secrets
SECRET_KEY = "hardcoded-secret-123"
DB_PASSWORD = "admin1234"
STRIPE_API_KEY = "sk_live_abcdef1234567890"
DB_PATH = "users.db"


def get_user(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Vulnerability 2: SQL injection via f-string
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchone()


def delete_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Vulnerability 2b: SQL injection via string concatenation
    query = "DELETE FROM users WHERE id = " + str(user_id)
    cursor.execute(query)
    conn.commit()


def save_session(session_data, filepath):
    with open(filepath, "wb") as f:
        # Vulnerability 4: pickle serialization (unsafe)
        pickle.dump(session_data, f)


def load_session(filepath):
    with open(filepath, "rb") as f:
        # Vulnerability 4b: pickle deserialization (allows arbitrary code execution)
        return pickle.load(f)


def fetch_data(url):
    # Vulnerability 5: SSL verification disabled
    response = requests.get(url, verify=False)
    return response.json()


def post_data(url, payload):
    # Vulnerability 5b: SSL verification disabled on POST
    response = requests.post(url, json=payload, verify=False)
    return response.json()


def process_users(users):
    result = []
    for i in range(len(users)):
        user = users[i]
        if user["age"] > 18:
            if user["active"] == True:
                if user["role"] == "admin":
                    result.append(user)
    return result


def calculate(a, b, operation):
    # Vulnerability 3: bare except clause that silently swallows errors
    try:
        if operation == "divide":
            return a / b
        elif operation == "add":
            return a + b
    except:
        pass


def authenticate(username, password):
    # Vulnerability 3b: bare except swallowing auth errors silently
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        cursor.execute(query)
        return cursor.fetchone() is not None
    except:
        return False


def get_env():
    api_key = os.environ.get("API_KEY")
    return api_key