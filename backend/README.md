# Lake Holidays Challenge - Backend API

## 🎯 Vue d'ensemble

Backend FastAPI pour l'application de gamification des vacances familiales. Ce backend fournit une API REST complète pour gérer l'authentification, les profils, les saisons, les défis quotidiens et le système de scoring.

## 🏗️ Architecture

### Structure du projet
```
backend/
├── app/                          # Code principal de l'application
│   ├── __init__.py
│   ├── main.py                   # Point d'entrée FastAPI
│   ├── config.py                 # Configuration de l'application
│   ├── database.py               # Configuration base de données
│   ├── auth/                     # Authentification et sécurité
│   ├── models/                   # Modèles SQLAlchemy
│   ├── schemas/                  # Schémas Pydantic (validation)
│   ├── routers/                  # Endpoints API par domaine
│   ├── services/                 # Logique métier
│   ├── utils/                    # Utilitaires et helpers
│   └── ai/                       # Intégration IA/LLM
├── tests/                        # Tests unitaires et d'intégration
├── alembic/                      # Migrations de base de données
├── docker/                       # Configuration Docker
├── requirements.txt              # Dépendances Python
├── Dockerfile                    # Image Docker
├── docker-compose.yml           # Stack de développement
└── README.md                     # Cette documentation
```

### Technologies utilisées

- **FastAPI 0.104.1** - Framework web moderne et performant
- **SQLAlchemy 2.0** - ORM avec support async
- **PostgreSQL** - Base de données principale
- **Redis** - Cache et sessions
- **OpenAI API** - Génération de contenu par IA
- **Azure Services** - Stockage et services cloud
- **Docker** - Conteneurisation

## 🚀 Installation et démarrage

### Prérequis
- Python 3.11+
- Docker et Docker Compose
- PostgreSQL (si développement local)

### Installation des dépendances
```bash
# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### Configuration
1. Copier `.env.example` vers `.env`
2. Configurer les variables d'environnement :
   ```env
   # Database
   DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/lake_holidays
   
   # Security
   SECRET_KEY=your-secret-key-here
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   
   # OAuth
   GOOGLE_CLIENT_ID=your-google-client-id
   GOOGLE_CLIENT_SECRET=your-google-client-secret
   MICROSOFT_CLIENT_ID=your-microsoft-client-id
   MICROSOFT_CLIENT_SECRET=your-microsoft-client-secret
   
   # AI Services
   OPENAI_API_KEY=your-openai-key
   AZURE_OPENAI_ENDPOINT=your-azure-endpoint
   
   # Azure Storage
   AZURE_STORAGE_CONNECTION_STRING=your-azure-storage
   
   # Environment
   ENVIRONMENT=development
   ```

### Démarrage avec Docker
```bash
# Démarrer la stack complète
docker-compose up -d

# Voir les logs
docker-compose logs -f api

# Arrêter
docker-compose down
```

### Démarrage en développement local
```bash
# Démarrer PostgreSQL et Redis
docker-compose up -d postgres redis

# Appliquer les migrations
alembic upgrade head

# Démarrer l'API
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📡 API Documentation

### Accès à la documentation
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc
- **OpenAPI JSON** : http://localhost:8000/openapi.json

### Endpoints principaux

#### Authentification (`/auth`)
- `POST /auth/register` - Création de compte local
- `POST /auth/login` - Connexion avec compte local
- `POST /auth/oauth/google` - Connexion via Google OAuth
- `POST /auth/oauth/microsoft` - Connexion via Microsoft OAuth
- `POST /auth/logout` - Déconnexion
- `GET /auth/me` - Informations utilisateur actuel

#### Profils utilisateur (`/profiles`)
- `POST /profiles` - Création de profil
- `GET /profiles/me` - Récupération du profil actuel
- `PUT /profiles/me` - Modification du profil
- `GET /profiles/{user_id}` - Profil d'un autre utilisateur

#### Saisons (`/seasons`)
- `POST /seasons` - Création d'une nouvelle saison
- `GET /seasons` - Liste des saisons de l'utilisateur
- `GET /seasons/{season_id}` - Détails d'une saison
- `POST /seasons/{season_id}/join` - Rejoindre avec code d'invitation
- `PUT /seasons/{season_id}` - Modification d'une saison

#### Défis (`/challenges`)
- `GET /challenges/daily` - Défis du jour
- `POST /challenges/{challenge_id}/submit` - Soumettre une réponse
- `GET /challenges/{challenge_id}/submissions` - Soumissions d'un défi
- `POST /challenges/{submission_id}/validate` - Valider une soumission

#### Scoring (`/scoring`)
- `GET /scoring/leaderboard/daily` - Classement quotidien
- `GET /scoring/leaderboard/global` - Classement global
- `GET /scoring/user/{user_id}/points` - Points d'un utilisateur
- `GET /scoring/badges` - Badges disponibles

#### IA et contenu (`/ai`)
- `POST /ai/generate/quiz` - Générer un quiz contextuel
- `POST /ai/generate/photo-challenge` - Générer un défi photo
- `POST /ai/generate/sport-challenge` - Générer un défi sportif

## 🧪 Tests

### Exécution des tests
```bash
# Tous les tests
pytest

# Tests avec couverture
pytest --cov=app --cov-report=html

# Tests d'un module spécifique
pytest tests/test_auth.py

# Tests avec détails
pytest -v
```

### Types de tests
- **Tests unitaires** - Logic métier et utilitaires
- **Tests d'intégration** - API endpoints et database
- **Tests E2E** - Scénarios complets utilisateur

## 🔧 Développement

### Formatage et linting
```bash
# Formatage du code
black app/ tests/

# Tri des imports
isort app/ tests/

# Vérification du style
flake8 app/ tests/

# Vérification des types
mypy app/
```

### Migrations de base de données
```bash
# Créer une nouvelle migration
alembic revision --autogenerate -m "Description of changes"

# Appliquer les migrations
alembic upgrade head

# Revenir à une migration précédente
alembic downgrade -1
```

### Ajout de nouvelles fonctionnalités
1. Créer les modèles dans `app/models/`
2. Définir les schémas Pydantic dans `app/schemas/`
3. Implémenter la logique dans `app/services/`
4. Créer les endpoints dans `app/routers/`
5. Ajouter les tests dans `tests/`
6. Mettre à jour la documentation

## 🔐 Sécurité

### Authentification
- **JWT tokens** avec expiration
- **Refresh tokens** pour sessions longues
- **OAuth 2.0** pour Google et Microsoft
- **Hashage bcrypt** pour mots de passe locaux

### Protection des données
- **Validation stricte** avec Pydantic
- **CORS configuré** pour le frontend
- **Rate limiting** sur les endpoints sensibles
- **Chiffrement** des données sensibles

### Variables d'environnement
- Jamais de secrets dans le code
- Configuration par environnement
- Validation des variables au démarrage

## 📊 Monitoring et logs

### Logs structurés
- **Structlog** pour des logs JSON
- **Niveaux appropriés** (DEBUG, INFO, ERROR)
- **Corrélation** des requêtes avec trace_id

### Métriques
- **Prometheus** pour métriques applicatives
- **Health checks** sur `/health`
- **Monitoring** des performances

## 🚀 Déploiement

### Docker en production
```bash
# Build de l'image
docker build -t lake-holidays-api .

# Run avec variables d'environnement
docker run -p 8000:8000 --env-file .env lake-holidays-api
```

### Azure Container Instances
Configuration dans `.github/workflows/deploy-api.yml`

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Committer les changes (`git commit -am 'Ajout nouvelle fonctionnalité'`)
4. Pusher la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créer une Pull Request

## 📜 License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
