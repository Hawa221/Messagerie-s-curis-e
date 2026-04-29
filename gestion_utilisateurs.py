from datetime import datetime
from database import get_connection, create_tables
from securite_mot_de_passe import generer_salt, hasher_mot_de_passe, verifier_mot_de_passe
from chiffrement import generer_paire_cles

def inscrire_utilisateur(username: str, mot_de_passe: str) -> tuple[bool, str]:
    """Inscrit un nouvel utilisateur avec hachage et génération de clés RSA."""
    create_tables()
    conn = get_connection()
    cur = conn.cursor()

    try:
      
        cur.execute("SELECT id FROM users WHERE username = ?", (username,))
        if cur.fetchone():
            return False, "Ce nom d'utilisateur est déjà pris."

       
        salt = generer_salt()
        hash_mdp = hasher_mot_de_passe(mot_de_passe, salt)

        
        cle_publique_pem = generer_paire_cles(username)

      
        cur.execute(
            "INSERT INTO users (username, password_hash, password_salt, public_key, created_at) VALUES (?, ?, ?, ?, ?)",
            (username, hash_mdp, salt, cle_publique_pem, datetime.utcnow().isoformat())
        )
        conn.commit()
        return True, ""
    except Exception as e:
        return False, f"Erreur lors de l'inscription : {str(e)}"
    finally:
        conn.close()

def connecter_utilisateur(username: str, mot_de_passe: str) -> tuple[bool, str]:
    conn = get_connection()
    cur = conn.cursor()

   
    cur.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return False, "Nom d'utilisateur introuvable."

    hash_stocke = row[0] 

    
    if verifier_mot_de_passe(mot_de_passe, hash_stocke):
        return True, ""
    
    return False, "Mot de passe incorrect."

def get_cle_publique(username: str) -> str | None:
    """Récupère la clé publique d'un destinataire pour chiffrer un message."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT public_key FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

def get_user_id(username: str) -> int | None:
    """Récupère l'ID numérique (nécessaire pour la table messages)."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None