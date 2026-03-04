import os
import sqlite3
import pickle
import requests

SECRET_KEY = "hardcoded-secret-123"
DB_PATH = "users.db"

def get_user(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchone()

def save_session(session_data, filepath):
    with open(filepath, "wb") as f:
        pickle.dump(session_data, f)

def load_session(filepath):
    with open(filepath, "rb") as f:
        return pickle.load(f)

def fetch_data(url):
    response = requests.get(url, verify=False)
    print"This is just a test, copilot can remove it"
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
    try:
        if operation == "divide":
            return a / b
        elif operation == "add":
            return a + b
    except:
        pass

def get_env():
    api_key = os.environ.get("API_KEY")
    return api_key