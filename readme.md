#  Messagerie Sécurisée

Application de messagerie instantanée chiffrée de bout en bout, développée en Python dans le cadre d'un projet scolaire.

##  Équipe

| Membre        | Rôle                                                  |
|---------------|-------------------------------------------------------|
| Hawa Doucouré | Interface utilisateur (Tkinter), tests, documentation |
| Rassoulou Sow | Chiffrement RSA, authentification, base de données    |

---

##  Fonctionnalités

- **Chiffrement de bout en bout** — chaque message est chiffré avec RSA 2048 bits avant d'être stocké en base de données
- **Authentification sécurisée** — mots de passe hachés avec bcrypt (salage intégré)
- **Messages éphémères** — option pour envoyer des messages qui disparaissent automatiquement après 5 minutes des deux côtés
- **Interface graphique** — application bureau développée avec Tkinter

---

##  Architecture

```
Messagerie-sécurisée/
├── interface.py              # Point d'entrée, interface graphique (Tkinter)
├── gestion_utilisateurs.py   # Inscription, connexion, gestion des clés
├── gestion_messages.py       # Envoi, réception, messages éphémères
├── chiffrement.py            # Génération RSA, chiffrement, déchiffrement
├── securite_mot_de_passe.py  # Hachage bcrypt
├── database.py               # Connexion SQLite, création des tables
├── messagerie.db             # Base de données (ignorée par git)
└── keys/                     # Clés privées locales (ignorées par git)
    └── <username>/
        └── private_key.pem
```

---

##  Sécurité — Choix de conception

### Chiffrement RSA (bout en bout)

À l'inscription, chaque utilisateur reçoit une **paire de clés RSA 2048 bits** :
- La **clé publique** est stockée en base de données — elle sert à chiffrer les messages destinés à cet utilisateur
- La **clé privée** est stockée localement dans `keys/<username>/private_key.pem` — elle ne quitte jamais la machine

Quand Hawa envoie un message à Rassoulou :
1. Le message est chiffré avec la **clé publique de Rassoulou** (seul Rassoulou pourra le lire)
2. Une seconde copie est chiffrée avec la **clé publique de Hawa** (pour que Hawa puisse relire ses messages envoyés)
3. Les deux copies chiffrées sont stockées en base de données
4. Le serveur ne voit jamais le message en clair

L'algorithme de padding utilisé est **OAEP avec SHA-256**, qui est plus sûr que le padding PKCS1v15 classique.

### Hachage des mots de passe (bcrypt)

Les mots de passe ne sont jamais stockés en clair. On utilise **bcrypt** qui :
- Intègre automatiquement un **sel aléatoire** à chaque hachage (deux hachages du même mot de passe donnent des résultats différents)
- Est intentionnellement lent, ce qui rend les attaques par dictionnaire très coûteuses
- Est résistant aux attaques GPU contrairement à SHA1 ou MD5

### Messages éphémères

Chaque message éphémère reçoit un `expiration_timestamp` en base de données (heure d'envoi + 5 minutes). À chaque rafraîchissement (toutes les secondes), les messages expirés sont supprimés de la base de données des **deux côtés** avant affichage.

### Ce qui est protégé en cas de compromission de la base de données

- Les messages sont illisibles sans les clés privées (stockées localement)
- Les mots de passe sont illisibles sans les hacher à nouveau (bcrypt non réversible)

---

##   Base de données — SQLite

**Choix de SQLite** : base de données légère, sans serveur à configurer, idéale pour une application desktop. Le fichier `messagerie.db` est créé automatiquement au premier lancement.

### Schéma

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash BLOB NOT NULL,
    password_salt BLOB NOT NULL,
    public_key TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE messages (
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
);
```

---

##   Installation

### Prérequis

- Python 3.10+
- pip

### Dépendances

```bash
pip install bcrypt cryptography
```

### Lancement

```bash
python interface.py
```

---

##  Tests

Voir le fichier `tests.py` pour les tests automatisés. Les tests couvrent :
- Inscription et connexion (cas valides et invalides)
- Chiffrement et déchiffrement RSA
- Envoi et réception de messages
- Expiration des messages éphémères

```bash
python tests.py
```

---

##      Trello

| Tâche                                     | Assigné   |Statut      |
|------------------------------------------------------ |------------|
| Génération de la paire de clés RSA        | Rassoulou | ✅ Terminé |
| Stockage de l'utilisateur en base         | Rassoulou | ✅ Terminé |
| Hash + sel du mot de passe                | Rassoulou | ✅ Terminé |
| Création de la base + Connexion BDD       | Rassoulou | ✅ Terminé |
| Scripts SQL + données de test             | Rassoulou | ✅ Terminé |
| Écran Inscription (Tkinter)               | Hawa      |✅ Terminé  |
| Écran Connexion (Tkinter)                 | Hawa      |✅ Terminé  |
| Écran Liste des conversations             | Hawa      | ✅ Terminé |
| Écran Chat (affichage + envoi)            | Hawa      | ✅ Terminé |
| Rafraîchissement automatique des messages | Hawa      | ✅ Terminé |
| Vérification fluidité & lisibilité        | Hawa      | ✅ Terminé |
| Tests inscription + tests connexion       | Hawa      | ✅ Terminé |
| README + schéma architecture              | Hawa      | ✅ Terminé |
| Présentation + nettoyage GitHub           | Hawa      | ✅ Terminé |