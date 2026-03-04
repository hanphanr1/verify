import sqlite3
from config import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        status TEXT DEFAULT 'started',
        full_name TEXT,
        birth_date TEXT,
        email TEXT,
        branch TEXT,
        discharge_date TEXT,
        verified INTEGER DEFAULT 0,
        verification_id TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    conn.commit()
    conn.close()

def save_user(user_id, username, first_name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT OR REPLACE INTO users (user_id, username, first_name)
                 VALUES (?, ?, ?)''', (user_id, username, first_name))
    conn.commit()
    conn.close()

def update_user_status(user_id, status):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET status = ? WHERE user_id = ?", (status, user_id))
    conn.commit()
    conn.close()

def save_verification_data(user_id, data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''UPDATE users SET
                 full_name = ?,
                 birth_date = ?,
                 email = ?,
                 branch = ?,
                 discharge_date = ?,
                 verification_id = ?,
                 status = ?
                 WHERE user_id = ?''',
              (data.get('full_name'), data.get('birth_date'), data.get('email'),
               data.get('branch'), data.get('discharge_date'), data.get('verification_id'),
               data.get('status'), user_id))
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result

def mark_verified(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET verified = 1, status = 'verified' WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
