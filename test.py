import os
import shutil
import sqlite3
from datetime import datetime, timedelta


if os.path.exists("test.db"):
    os.remove("test.db")
if os.path.exists("keys_test"):
    shutil.rmtree("keys_test")

import database
database.get_connection = lambda: sqlite3.connect("test.db")

import chiffrement
chiffrement.KEYS_DIR = "keys_test"

from database import create_tables
from gestion_utilisateurs import inscrire_utilisateur, connecter_utilisateur
from chiffrement import chiffrer_message, dechiffrer_message, generer_paire_cles
from gestion_messages import envoyer_message, recevoir_messages

create_tables()

# --- Test 1 : Inscription ---
ok, err = inscrire_utilisateur("alice", "motdepasse123")
print("Test inscription :", "OK" if ok else "ECHEC")

# --- Test 2 : Doublon ---
ok, err = inscrire_utilisateur("alice", "motdepasse123")
print("Test doublon refusé :", "OK" if not ok else "ECHEC")

# --- Test 3 : Connexion correcte ---
ok, err = connecter_utilisateur("alice", "motdepasse123")
print("Test connexion correcte :", "OK" if ok else "ECHEC")

# --- Test 4 : Mauvais mot de passe ---
ok, err = connecter_utilisateur("alice", "mauvaismdp")
print("Test mauvais mot de passe :", "OK" if not ok else "ECHEC")

# --- Test 5 : Chiffrement RSA ---
inscrire_utilisateur("bob", "supersecret99")
from gestion_utilisateurs import get_cle_publique
cle_pub_bob = get_cle_publique("bob")
msg_chiffre = chiffrer_message("Bonjour Bob", cle_pub_bob)
msg_dechiffre = dechiffrer_message(msg_chiffre, "bob")
print("Test chiffrement RSA :", "OK" if msg_dechiffre == "Bonjour Bob" else "ECHEC")

# --- Test 6 : Alice ne peut pas lire le message de Bob ---
try:
    dechiffrer_message(msg_chiffre, "alice")
    print("Test isolation clés : ECHEC")
except Exception:
    print("Test isolation clés : OK")

# --- Test 7 : Envoi et réception ---
envoyer_message("alice", "bob", "Salut Bob !")
msgs = recevoir_messages("bob", "alice")
print("Test réception message :", "OK" if msgs[0]["contenu"] == "Salut Bob !" else "ECHEC")

# --- Test 8 : Message éphémère ---#
envoyer_message("alice", "bob", "Message secret", ephemere=True)
msgs_avant = recevoir_messages("bob", "alice")
ephemeres = [m for m in msgs_avant if m["is_ephemere"]]
print("Test message éphémère visible :", "OK" if len(ephemeres) == 1 else "ECHEC")


conn = sqlite3.connect("test.db")
conn.execute("UPDATE messages SET expiration_timestamp = ? WHERE is_ephemere = 1",
             ((datetime.utcnow() - timedelta(seconds=1)).isoformat(),))
conn.commit()
conn.close()

msgs_apres = recevoir_messages("bob", "alice")
ephemeres_apres = [m for m in msgs_apres if m["is_ephemere"]]
print("Test message éphémère supprimé :", "OK" if len(ephemeres_apres) == 0 else "ECHEC")


if os.path.exists("test.db"):
    os.remove("test.db")
if os.path.exists("keys_test"):
    shutil.rmtree("keys_test")