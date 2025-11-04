# 🚀 ADV IHM - Plateforme d'Intelligence Artificielle

## 📋 Table des matières
- [Présentation du projet](#-présentation-du-projet)
- [🏗️ Architecture](#%EF%B8%8F-architecture)
- [⚙️ Prérequis](#%EF%B8%8F-prérequis)
- [🚀 Installation](#-installation)
- [🔧 Configuration](#-configuration)
- [🏃 Exécution](#-exécution)
- [🧪 Tests](#-tests)
- [🤝 Contribution](#-contribution)
- [📄 Licence](#-licence)

## 🌟 Présentation du projet

Le projet **ADV IHM** est une plateforme avancée d'Intelligence Artificielle conçue pour fournir des réponses intelligentes et contextuelles dans le domaine du support utilisateur. Cette refonte en architecture microservices permet une meilleure scalabilité, maintenabilité et séparation des responsabilités.

## 🏗️ Architecture

L'architecture du projet est basée sur plusieurs microservices spécialisés :

### 1. `mcp-server-python` 🐍
- **Langage** : Python
- **Responsabilités** :
  - Traitement du langage naturel (NLP)
  - Gestion des modèles d'IA
  - Raisonnement et inférence
  - Manipulation des contextes conversationnels

### 2. `mcp-server-java` ☕
- **Langage** : Java
- **Responsabilités** :
  - Gestion des opérations CRUD
  - Persistance des données
  - Logique métier
  - Sécurité et authentification

### 3. `mcp-client` 🔄
- **Rôle** : Orchestrateur
- **Fonctionnalités** :
  - Routage des requêtes entre les services
  - Gestion des erreurs
  - Load balancing
  - Cache distribué

### 4. `ai-assistant` 🤖
- **Technologies** : Few-Shot Learning, NLP
- **Capacités** :
  - Compréhension du langage naturel
  - Réponses contextuelles
  - Apprentissage continu
  - Intégration IHM

## ⚙️ Prérequis

- Java 17+
- Python 3.9+
- Node.js 16+
- Maven 3.8+
- PostgreSQL 13+
- Redis 6+

## 🚀 Installation

1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/votre-org/mcp-agent.git
   cd mcp-agent
   ```

2. **Installer les dépendances** :
   ```bash
   # Backend Java
   cd mcp-server-java
   mvn clean install
   
   # Backend Python
   cd ../mcp-server-python
   pip install -r requirements.txt
   
   # Frontend
   cd ../frontend
   npm install
   ```

## 🔧 Configuration

1. **Variables d'environnement** :
   - Créer un fichier `.env` à la racine du projet
   - Configurer les variables nécessaires (voir `.env.example`)

2. **Base de données** :
   - Configurer PostgreSQL
   - Exécuter les migrations

## 🏃 Exécution

```bash
# Démarrer les services
./start-services.sh

# Ou démarrer manuellement chaque service
# Java Server
cd mcp-server-java && mvn spring-boot:run

# Python Server
cd ../mcp-server-python && python app.py

# Client
cd mcp-client && npm start

# Frontend
cd frontend && npm start
```

## 🧪 Tests

```bash
# Tests unitaires Java
cd mcp-server-java
mvn test

# Tests Python
cd ../mcp-server-python
pytest

# Tests frontend
cd ../frontend
npm test
```

## 🤝 Contribution

1. Forkez le projet
2. Créez votre branche (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Poussez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## ✉️ Contact

Équipe ADV IHM - Sofrecom 

---

<div align="center">
  <sub>Construit avec ❤️ par l'équipe ADV IHM</sub>
</div>
