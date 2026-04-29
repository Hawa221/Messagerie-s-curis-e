import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

def generer_paire_cles(username):
    """Génère des clés RSA : privée stockée localement, publique retournée pour la BDD."""
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    if not os.path.exists('cles'):
        os.makedirs('cles')


    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open(f"cles/{username}_privee.pem", "wb") as f:
        f.write(private_pem)

  
    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return public_pem.decode('utf-8')

def chiffrer_message(message_clair, cle_publique_pem):
    """Chiffre un texte avec la clé publique du destinataire."""
    public_key = serialization.load_pem_public_key(cle_publique_pem.encode())
    
    message_chiffre = public_key.encrypt(
        message_clair.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return message_chiffre 

def dechiffrer_message(message_chiffre, username):
    """Déchiffre un message avec la clé privée locale de l'utilisateur."""
    
    with open(f"cles/{username}_privee.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )

    message_clair = private_key.decrypt(
        message_chiffre,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return message_clair.decode('utf-8')