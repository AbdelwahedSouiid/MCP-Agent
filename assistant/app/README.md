# Projet FastAPI - AI-FastAPI

Ce projet est une API REST développée avec FastAPI, qui inclut une structure modulaire, des dépendances essentielles, et les bonnes pratiques pour une gestion efficace du dépôt.

## Table des Matières

1. [Pré-requis](#pré-requis)
2. [Installation et Configuration](#installation-et-configuration)
3. [Structure du Projet](#structure-du-projet)
4. [Lancer l'application](#lancer-lapplication)
5. [Gestion des Dépendances](#gestion-des-dépendances)
6. [Bonnes Pratiques pour le Push](#bonnes-pratiques-pour-le-push)

---

## 1. Pré-requis

Avant de commencer, assurez-vous d'avoir les éléments suivants installés :

- **Python 3.11+**
- **Git** (pour le contrôle de version)
- **UV** (gestionnaire de paquets Python moderne)

---

## 2. Installation et Configuration

Suivez les étapes ci-dessous pour configurer le projet FastAPI.

### 1. Cloner le dépôt

```bash
git clone <URL_DU_DEPOT>
cd AI-FastAPI
```

### 2. Installer UV (si pas déjà installé)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# ou
pip install uv
```

### 3. Créer et activer l'environnement virtuel

```bash
uv venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

### 4. Initialiser le projet

```bash
uv init
```

### 5. Installer les dépendances

```bash
uv add fastapi "uvicorn[standard]" pydantic-settings numpy pandas ollama beautifulsoup4 requests-html aiohttp requests ...
```

---

## 3. Structure du Projet

```
AI-FastAPI/
├── ai/
│   ├── data/                    # Données brutes
│   │   └── *.csv
│   ├── preparation/             # Données préparées
│   │   ├── clean/              # Données nettoyées
│   │   ├── formatting/         # Données formatées
│   │   ├── processing/         # Données traitées
│   │   └── *.csv
│   └── models/                 # Modèles AI sauvegardés
├── app/
│   ├── __init__.py
│   ├── main.py                 # Point d'entrée FastAPI
│   ├── routes/                 # Routes de l'API
│   │   ├── __init__.py
│   │   └── v1/                 # Versioning des routes
│   │       ├── __init__.py
│   │       ├── data_routes.py      # Routes préparation données
│   │       ├── chat_routes.py      # Routes chatbot
│   │       └── question_routes.py  # Routes recherche
│   ├── schemas/                # Schémas Pydantic
│   │   ├── __init__.py
│   │   ├── user.py            # Schéma utilisateurs
│   │   └── question.py        # Schéma questions/chatbot
│   ├── core/                   # Configuration
│   │   ├── __init__.py
│   │   └── config.py          # Configuration globale
│   └── services/               # Logique métier
│       ├── __init__.py
│       ├── preparation_service.py  # Service préparation données
│       └── question_service.py     # Service chatbot
├── tests/                      # Tests unitaires
│   ├── __init__.py
│   └── test_main.py
├── .venv/                      # Environnement virtuel (ignoré par Git)
├── pyproject.toml             # Configuration du projet
├── uv.lock                    # Fichier de verrouillage des dépendances
├── Dockerfile                 # Configuration Docker
├── docker-compose.yml         # Configuration Docker Compose
├── .gitignore                 # Fichiers ignorés par Git
└── README.md                  # Documentation
```

---

## 4. Lancer l'application

### En mode développement

```bash
uv run uvicorn app.main:app --reload --port 8000
```

### Ou avec le module Python

```bash
uv run python -m app.main
```

### Avec Docker

```bash
docker-compose up --build
```

L'API sera accessible à l'adresse : `http://localhost:8089`

Documentation automatique : `http://localhost:8089/docs`

---

## 5. Gestion des Dépendances

### Synchroniser les dépendances

```bash
uv sync
```

### Ajouter une nouvelle dépendance

```bash
uv add <nom_du_package>
```

### Ajouter une dépendance de développement

```bash
uv add --dev <nom_du_package>
```

### Mettre à jour les dépendances

```bash
uv lock --upgrade
```

### Exporter les dépendances (pour compatibilité)

```bash
uv export --format requirements-txt --output-file requirements.txt
```

---

## 6. Bonnes Pratiques pour le Push

### Structure de commits

Utilisez des messages de commit clairs et structurés :

```bash
git commit -m "feat: ajout route pour traitement des données"
git commit -m "fix: correction du service de chatbot"
git commit -m "docs: mise à jour README"
```

### Avant chaque push

1. **Vérifier le statut du dépôt**

   ```bash
   git status
   ```

2. **Tester l'application**

   ```bash
   uv run python -m pytest tests/
   ```

3. **Vérifier le formatage du code**

   ```bash
   uv run black app/
   uv run isort app/
   ```

4. **Vérifier la qualité du code**
   ```bash
   uv run flake8 app/
   ```

### Fichiers à ignorer (.gitignore)

```gitignore
# Environnement virtuel
.venv/
venv/
env/

# Fichiers Python
__pycache__/
*.py[cod]
*$py.class
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/

# Données sensibles
.env
.env.local
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# Système
.DS_Store
Thumbs.db
```

### Workflow Git recommandé

```bash
# 1. Créer une branche pour une nouvelle fonctionnalité
git checkout -b feature/nouvelle-fonctionnalité

# 2. Faire les modifications et commits
git add .
git commit -m "feat: description de la fonctionnalité"

# 3. Pousser la branche
git push origin feature/nouvelle-fonctionnalité

# 4. Créer une Pull Request
# 5. Après validation, merger dans main
git checkout main
git pull origin main
git merge feature/nouvelle-fonctionnalité
git push origin main

# 6. Supprimer la branche locale
git branch -d feature/nouvelle-fonctionnalité
```

---

## Variables d'Environnement

Créez un fichier `.env` à la racine du projet :

```env
# Configuration de l'application
APP_NAME=AI-FastAPI
APP_VERSION=1.0.0
DEBUG=True

# Base de données
DATABASE_URL=sqlite:///./ai_fastapi.db

# API Keys
OLLAMA_HOST=http://localhost:11434
```

---

## Contribution

1. Forkez le projet
2. Créez votre branche de fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Commitez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Poussez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

---

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
