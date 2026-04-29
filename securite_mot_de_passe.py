import bcrypt


def generer_salt():
    return bcrypt.gensalt()


def hasher_mot_de_passe(mot_de_passe: str, salt: bytes) -> bytes:
    return bcrypt.hashpw(mot_de_passe.encode(), salt)


def verifier_mot_de_passe(mot_de_passe: str, hash_stocke: bytes) -> bool:
    return bcrypt.checkpw(mot_de_passe.encode(), hash_stocke)


def test_hash():
    salt = generer_salt()
    hash1 = hasher_mot_de_passe("motdepasse123", salt)

   
    print("Vérification mot de passe correct :", verifier_mot_de_passe("motdepasse123", hash1))
    print("Vérification mauvais mot de passe :", verifier_mot_de_passe("fauxmotdepasse", hash1))


if __name__ == "__main__":
    test_hash()