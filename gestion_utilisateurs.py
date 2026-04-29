import sqlite3
from datetime import datetime

def get_connection():
    return sqlite3.connect("messagerie.db")

def creer_table_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            hash BLOB NOT NULL,
            sel BLOB NOT NULL,
            public_key TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def user_exists(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username = ?", (username,))
    result = cur.fetchone()
    conn.close()
    return result is not None

def save_user(username, hash_mdp, sel, cle_publique):
    if user_exists(username):
        return False

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (username, hash, sel, public_key, created_at) VALUES (?, ?, ?, ?, ?)",
        (username, hash_mdp, sel, cle_publique, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()
    return True

def test_insertion():
    creer_table_users()
    ok = save_user("testuser", b"hash123", b"sel123", "cle_publique_test")
    print(ok)
    print(user_exists("testuser"))
