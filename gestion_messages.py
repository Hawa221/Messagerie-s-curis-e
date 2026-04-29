from datetime import datetime, timedelta
from database import get_connection
from chiffrement import chiffrer_message, dechiffrer_message
from gestion_utilisateurs import get_cle_publique, get_user_id


def envoyer_message(sender: str, receiver: str, message_clair: str, ephemere: bool = False) -> tuple[bool, str]:
    cle_pub_destinataire = get_cle_publique(receiver)
    cle_pub_expediteur = get_cle_publique(sender)

    if not cle_pub_destinataire:
        return False, f"Utilisateur '{receiver}' introuvable."

    sender_id = get_user_id(sender)
    receiver_id = get_user_id(receiver)

    # On chiffre deux fois : une copie pour le destinataire, une pour l'expéditeur
    chiffre_pour_destinataire = chiffrer_message(message_clair, cle_pub_destinataire)
    chiffre_pour_expediteur = chiffrer_message(message_clair, cle_pub_expediteur)

    now = datetime.utcnow()
    expiration = (now + timedelta(minutes=5)).isoformat() if ephemere else None

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO messages
           (sender_id, receiver_id, encrypted_for_receiver, encrypted_for_sender, is_ephemere, timestamp, expiration_timestamp)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (sender_id, receiver_id, chiffre_pour_destinataire, chiffre_pour_expediteur,
         1 if ephemere else 0, now.isoformat(), expiration)
    )
    conn.commit()
    conn.close()
    return True, ""


def recevoir_messages(username: str, interlocuteur: str) -> list[dict]:
    user_id = get_user_id(username)
    inter_id = get_user_id(interlocuteur)

    if not user_id or not inter_id:
        return []

    conn = get_connection()
    cur = conn.cursor()

    
    now = datetime.utcnow().isoformat()
    cur.execute(
        "DELETE FROM messages WHERE expiration_timestamp IS NOT NULL AND expiration_timestamp < ?",
        (now,)
    )

    cur.execute("""
        SELECT id, sender_id, receiver_id, encrypted_for_receiver, encrypted_for_sender, is_ephemere, timestamp
        FROM messages
        WHERE (sender_id = ? AND receiver_id = ?)
           OR (sender_id = ? AND receiver_id = ?)
        ORDER BY timestamp ASC
    """, (user_id, inter_id, inter_id, user_id))

    rows = cur.fetchall()
    conn.commit()
    conn.close()

    messages = []
    for row in rows:
        msg_id, sender_id, receiver_id, chiffre_receiver, chiffre_sender, is_ephemere, timestamp = row

        est_expediteur = (sender_id == user_id)

        try:
            if est_expediteur:
                
                contenu = dechiffrer_message(chiffre_sender, username)
            else:
                
                contenu = dechiffrer_message(chiffre_receiver, username)
        except Exception:
            contenu = "[Message illisible]"

        messages.append({
            "id": msg_id,
            "expediteur": username if est_expediteur else interlocuteur,
            "contenu": contenu,
            "is_ephemere": bool(is_ephemere),
            "timestamp": timestamp
        })

    return messages