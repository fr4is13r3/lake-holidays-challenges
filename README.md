# 🏖️ Lake Holidays Challenge - Application Vacances Gamifiées

Une application web mobile responsive qui transforme vos vacances en famille en une expérience ludique et interactive avec des défis quotidiens, du scoring en temps réel et du contenu généré par IA.

## 🎯 Objectif

Permettre à une famille de **gamifier chaque journée de vacances** avec :
- 🎮 Défis quotidiens adaptés (Quiz, Photo, Sport)
- 🏆 Système de points et classements en temps réel
- 🤖 Contenu généré automatiquement par IA selon localisation/activité
- 📱 Interface mobile-first optimisée

---

## 🏗️ Architecture

### Stack Technique
- **Frontend**: React + Vite (mobile-first responsive)
- **Backend**: Python FastAPI + PostgreSQL + Redis
- **AI**: Azure OpenAI / OpenAI API
- **Storage**: Azure Blob Storage
- **Deploy**: Docker + Azure Container Instances
- **Tests**: Behave BDD + pytest

### Structure du Projet
```
lake-holidays-challenge/
├── 🎨 frontend/           # React + Vite (interface mobile)
├── 🐍 backend/            # FastAPI + SQLAlchemy (API REST)
├── 🧪 bdd/               # Tests BDD Behave (67 scenarios)
├── 📖 docs/              # Documentation technique
├── 🛠️ tools/             # Scripts utilitaires
├── 🐳 docker-compose.yml # Stack de développement
└── 📋 Makefile           # Commandes simplifiées
```

---

## 🚀 Démarrage Rapide

### Prérequis
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose

### 1. Configuration complète
```bash
# Clone et setup complet
git clone <repo-url>
cd lake-holidays-challenge
make setup  # Configure backend, frontend et tests BDD
```

### 2. Développement backend
```bash
# Démarrer le backend avec base de données
make backend-dev  # API disponible sur http://localhost:8000
```

### 3. Développement frontend
```bash
# Dans un nouveau terminal
make frontend-dev  # Interface disponible sur http://localhost:5173
```

### 4. Tests BDD
```bash
# Tests critiques rapides
make test-smoke

# Tests par fonctionnalité
make test-auth        # Authentification
make test-challenges  # Défis quotidiens
make test-ai         # Génération IA

# Rapports détaillés
make reports
```

---

## 🧪 Tests BDD - 67 Scenarios

L'application est entièrement couverte par des tests BDD comportementaux :

### ✅ Fonctionnalités Testées
- **Authentification** (6 scenarios) - Local, OAuth Google/Microsoft, sessions
- **Profils Utilisateur** (6 scenarios) - Création, modification, préférences
- **Saisons de Vacances** (8 scenarios) - Création, invitations, activation auto
- **Défis Quotidiens** (10 scenarios) - Quiz IA, photo, sport, validation
- **Système de Scoring** (10 scenarios) - Points, bonus, classements, badges
- **Interface Mobile** (15 scenarios) - Responsive, offline, notifications
- **Génération IA** (12 scenarios) - Contenu contextuel, adaptation, qualité

### 📊 Métriques
- **67 scenarios** au total
- **100% de couverture** fonctionnelle
- **25+ tags** pour organisation
- **CI/CD automatisé** avec GitHub Actions

---

## 🎮 Fonctionnalités Principales

### 👤 Gestion Utilisateurs
- Authentification locale, Google, Microsoft (OAuth)
- Profils personnalisés avec avatars et préférences
- Gestion de sessions sécurisées

### 🏖️ Saisons de Vacances
- Création de saisons avec localisation et dates
- Système d'invitation par code familial
- Activation/désactivation automatique

### 🎯 Défis Quotidiens
- **Quiz contextuels** générés par IA selon localisation
- **Défis photo** créatifs avec validation
- **Défis sportifs** avec tracking GPS
- Adaptation selon âge et préférences

### 🏆 Système de Scoring
- Attribution de points selon difficulté
- Bonus de rapidité et régularité
- Classements quotidiens et globaux
- Système de badges et achievements

### 🤖 Intelligence Artificielle
- Génération automatique de quiz contextuels
- Adaptation selon météo et localisation
- Personnalisation par profil utilisateur
- Contrôle qualité du contenu

---

## 📱 Interface Mobile-First

### Responsive Design
- Optimisée pour écrans 320px-768px priority
- Breakpoints: mobile, tablet, desktop
- Navigation tactile intuitive

### Fonctionnalités Natives
- Intégration caméra pour défis photo
- Géolocalisation pour défis sportifs
- Mode hors ligne avec synchronisation
- Notifications push
- Gestes avancés (pinch, swipe)

---

## 🔧 Développement

### Backend (FastAPI)
```bash
# Installation
cd backend
pip install -r requirements.txt

# Base de données
docker-compose up -d postgres redis
alembic upgrade head

# Développement
uvicorn app.main:app --reload

# Tests
pytest -v
```

### Frontend (React + Vite)
```bash
# Installation
cd frontend
npm install

# Développement
npm run dev

# Build production
npm run build

# Tests
npm test
```

### Tests BDD
```bash
# Installation
cd bdd
pip install -r requirements.txt

# Tests complets
behave

# Tests par tag
behave --tags @smoke
behave --tags @api,@challenges
```

---

## 🐳 Docker

### Développement Local
```bash
# Démarrer tous les services
make docker-up

# Voir les logs
make docker-logs

# Arrêter
make docker-down
```

### Services Disponibles
- **API Backend**: http://localhost:8000
- **Frontend**: http://localhost:5173
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

---

## 📚 Documentation

### Guides Techniques
- [`backend/README.md`](backend/README.md) - Guide backend complet
- [`frontend/README.md`](frontend/README.md) - Guide frontend détaillé
- [`bdd/README.md`](bdd/README.md) - Documentation tests BDD

### Documentation Métier
- [`docs/UserStories.md`](docs/UserStories.md) - 23 User Stories détaillées
- [`docs/BDD_Summary.md`](docs/BDD_Summary.md) - Résumé complet des tests
- [`docs/Context.md`](docs/Context.md) - Contexte et spécifications

### API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🚀 Déploiement

### Azure Container Instances
```bash
# Build et déploiement
docker build -t lake-holidays-api ./backend
az container create --resource-group myRG --name lake-holidays --image lake-holidays-api
```

### Variables d'Environnement
```bash
# Copier et configurer
cp backend/.env.example backend/.env
# Configurer: DATABASE_URL, OPENAI_API_KEY, etc.
```

---

## 🎉 Prochaines Étapes

- [x] ✅ **Framework BDD complet** - 67 scenarios
- [x] ✅ **Backend FastAPI** - API REST avec auth et IA
- [x] ✅ **Docker configuration** - Stack de développement
- [ ] 🔄 **Frontend React** - Interface mobile-first
- [ ] 🔄 **Intégration IA** - Azure OpenAI
- [ ] 🔄 **Déploiement Azure** - Production ready

---

## 🤝 Contribution

```bash
# Setup développement
make setup
make backend-dev  # Terminal 1
make frontend-dev # Terminal 2

# Tests avant commit
make test-smoke
make backend-test
make frontend-test
```

---

## 📄 Licence

Projet privé à usage familial - Tous droits réservés.
