# Messagerie sécurisée

Application de messagerie instantanée avec chiffrement de bout en bout, développée en Python dans le cadre du BTS SIO option SLAM.

---

## Présentation

Ce projet permet à des utilisateurs d'échanger des messages de manière sécurisée, en garantissant la **confidentialité**, l'**intégrité** et l'**authenticité** des échanges grâce à un chiffrement asymétrique RSA et une gestion rigoureuse de l'authentification.

---

## Fonctionnalités

### Chiffrement de bout en bout

L'application utilise un chiffrement asymétrique basé sur une paire de clés RSA (bibliothèque Python `cryptography`) :

- Chaque utilisateur possède une **clé publique** (partagée, stockée en base de données) et une **clé privée** (conservée uniquement sur sa machine)
- L'expéditeur chiffre le message avec la clé publique du destinataire
- Le message est transmis et stocké chiffré en base de données
- Le destinataire déchiffre le message localement avec sa clé privée
- **Le serveur n'a jamais accès au contenu en clair**

Pour simuler plusieurs clients sur une même machine, chaque utilisateur dispose d'un dossier dédié contenant sa clé privée.

### Authentification des utilisateurs

- Création de compte et connexion sécurisée
- Mots de passe **hachés** et **salés** avant stockage
- À la connexion, le mot de passe saisi est haché puis comparé au hash stocké en base de données
- Aucun mot de passe en clair en base de données

### Interface utilisateur

- Interface graphique développée avec **Tkinter**
- Liste des conversations, zone de saisie et affichage des messages

### Fonctionnalité supplémentaire : messages éphémères

- L'utilisateur peut envoyer un message qui disparaît automatiquement après lecture ou après un délai défini
- Le message reste chiffré en base de données jusqu'à son expiration
- Une fois expiré, il est supprimé côté client et côté serveur
- Cette fonctionnalité limite l'exposition des données sensibles en cas de compromission d'un appareil

### Programmation orientée objet

Le projet est structuré en POO avec notamment les classes suivantes : `Utilisateur`, `Message`, `Conversation`, `GestionnaireClés`, `GestionnaireStockage`.

---

## Architecture technique

| Composant       | Technologie                  |
|-----------------|------------------------------|
| Langage         | Python                       |
| Interface       | Tkinter                      |
| Cryptographie   | `cryptography` (RSA)         |
| Base de données | SQLite                       |
| Organisation    | Programmation orientée objet |

---

## Base de données

Le projet utilise **SQLite**, via le module `sqlite3` intégré à Python (aucune installation supplémentaire requise).

SQLite a été choisi pour les raisons suivantes :

- Aucun serveur à installer ou configurer
- Toute la base de données est contenue dans un seul fichier local
- Nativement supporté par Python
- Suffisant pour les besoins du projet

---

## Installation

### 1. Cloner le dépôt

```bash
git clone <url-du-repo>
cd messagerie-securisee
```

### 2. Créer et activer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Lancer l'application

```bash
python main.py
```

La base de données SQLite est créée automatiquement au premier lancement.

---

## Étapes du projet

### 1. Recherche et conception

- Étude des concepts cryptographiques et des algorithmes de chiffrement
- Conception de l'architecture de l'application et des flux de données
- Comparaison des bibliothèques Python disponibles
- Choix de la base de données : SQLite
- Mise en place d'un planning Kanban (découpage des tâches, assignation, estimation, antécédents)

### 2. Développement

- Implémentation du chiffrement et du déchiffrement
- Mise en place de l'authentification et de la gestion des clés
- Développement de l'interface utilisateur
- Intégration des messages éphémères

### 3. Tests

- Vérification du chiffrement et du déchiffrement
- Tests de l'authentification et de la gestion des clés
- Tests fonctionnels de l'interface
- Tests de la suppression automatique des messages éphémères

### 4. Documentation

- Documentation du code et des choix de conception
- Explication des mécanismes de sécurité mis en place
- Documentation des tests réalisés
- Préparation de la présentation orale

---

## Choix techniques

> Cette section doit être complétée au fil du projet pour documenter les décisions prises par l'équipe.

| Sujet | Choix | Raison |
|-------|-------|--------|
| Base de données | SQLite | Aucune configuration, module natif Python, suffisant pour le projet |
| Cryptographie | RSA (`cryptography`) | Chiffrement asymétrique adapté à l'échange de clés |
| Interface | Tkinter | Intégré à Python, simple à mettre en place |

---

## Tests

> Cette section doit décrire les tests réalisés pour valider le bon fonctionnement de l'application.

---

## Rendu attendu

- Planning complet et détaillé
- Dépôt GitHub avec le code à jour sur la branche principale et une documentation complète en Markdown
- Présentation orale le **29 avril**

---

## Organisation du travail

- Groupe de 3 ou 4 étudiants
- Répartition claire des tâches et suivi via un tableau Kanban
- Communication régulière pour éviter les doublons
- Mises à jour régulières sur le dépôt Git
- Documentation des décisions techniques au fil du développement

---

## Équipe

Projet réalisé en groupe dans le cadre du **BTS SIO SLAM**.  
Chaque membre contribue au développement, aux tests, à la documentation et à la présentation orale.