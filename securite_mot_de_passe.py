import bcrypt

def generer_salt():
    return bcrypt.gensalt()

def hasher_mot_de_passe(mot_de_passe, salt):
    mot_de_passe_bytes = mot_de_passe.encode()
    return bcrypt.hashpw(mot_de_passe_bytes, salt)

def verifier_mot_de_passe(mot_de_passe, hash_stocke):
    mot_de_passe_bytes = mot_de_passe.encode()
    return bcrypt.checkpw(mot_de_passe_bytes, hash_stocke)

def test_hash():
    salt = generer_salt()
    hash1 = hasher_mot_de_passe("motdepasse123", salt)
    hash2 = hasher_mot_de_passe("motdepasse123", salt)

    print(hash1 != hash2)
    print(verifier_mot_de_passe("motdepasse123", hash1))
    print(verifier_mot_de_passe("fauxmotdepasse", hash1))
