import sqlite3


def get_connection():
    return sqlite3.connect("messagerie.db")


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Table des utilisateurs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            password_salt TEXT NOT NULL,
            public_key TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    # Table des messages
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER NOT NULL,
            receiver_id INTEGER NOT NULL,
            encrypted_message TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            expiration_timestamp TEXT,
            FOREIGN KEY(sender_id) REFERENCES users(id),
            FOREIGN KEY(receiver_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()