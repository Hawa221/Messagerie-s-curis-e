-- ============================
-- RESET DES TABLES
-- ============================

DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS users;

-- ============================
-- TABLE USERS
-- ============================

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    password_salt TEXT NOT NULL,
    public_key TEXT NOT NULL,
    created_at TEXT NOT NULL
);

-- ============================
-- TABLE MESSAGES
-- ============================

CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    encrypted_message TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    expiration_timestamp TEXT,
    FOREIGN KEY(sender_id) REFERENCES users(id),
    FOREIGN KEY(receiver_id) REFERENCES users(id)
);

-- ============================
-- INSERTION DES UTILISATEURS
-- ============================

INSERT INTO users (username, password_hash, password_salt, public_key, created_at)
VALUES
('ablaye', 'hash_ablaye', 'salt_ablaye', 'public_key_ablaye', '2026-04-23'),
('aissatou', 'hash_aissatou', 'salt_aissatou', 'public_key_aissatou', '2026-04-23'),
('rassoulou', 'hash_rassoulou', 'salt_rassoulou', 'public_key_rassoulou', '2026-04-23');

-- ============================
-- INSERTION DES MESSAGES
-- ============================

INSERT INTO messages (sender_id, receiver_id, encrypted_message, timestamp, expiration_timestamp)
VALUES
(1, 2, 'msg_chiffre_de_ablaye_vers_aissatou', '2026-04-23 10:00', NULL),
(2, 1, 'msg_chiffre_de_aissatou_vers_ablaye', '2026-04-23 10:05', NULL),
(3, 1, 'msg_chiffre_de_rassoulou_vers_ablaye', '2026-04-23 11:00', '2026-04-23 11:10'),
(1, 3, 'msg_chiffre_de_ablaye_vers_rassoulou', '2026-04-23 11:15', '2026-04-23 11:25');