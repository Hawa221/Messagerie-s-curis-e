import sqlite3


def get_connection():
    return sqlite3.connect("messagerie.db")


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash BLOB NOT NULL,
            password_salt BLOB NOT NULL,
            public_key TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER NOT NULL,
            receiver_id INTEGER NOT NULL,
            encrypted_for_receiver TEXT NOT NULL,
            encrypted_for_sender TEXT NOT NULL,
            is_ephemere INTEGER NOT NULL DEFAULT 0,
            timestamp TEXT NOT NULL,
            expiration_timestamp TEXT,
            FOREIGN KEY(sender_id) REFERENCES users(id),
            FOREIGN KEY(receiver_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()