# Directives de Prompt pour GitHub Copilot - Génération d'Application Mobile-First

## Contexte et Objectif
Génère une application complète mobile-first basée sur la description fonctionnelle fournie, en respectant les spécifications techniques suivantes :

## Spécifications Techniques Obligatoires

### Architecture Générale
- **Frontend** : React avec design responsive mobile-first
- **Backend** : Services Python (FastAPI/Flask)
- **Déploiement** : Conteneurs Docker sur Microsoft Azure
- **Méthodologie** : Principes CI/CD (Continuous Integration/Continuous Deployment)

### Frontend React Mobile-First
```
Exigences frontend :
- Interface optimisée pour écrans mobiles (320px-768px priority)
- Responsive design avec breakpoints : mobile (320px), tablet (768px), desktop (1024px+)
- Composants React fonctionnels avec hooks
- Gestion d'état avec Context API ou Redux Toolkit
- Navigation tactile intuitive
- Performance optimisée (lazy loading, code splitting)
- PWA capabilities (offline, notifications push)
- Accessibilité WCAG 2.1 AA
```

### Backend Python
```
Exigences backend :
- FastAPI ou Flask avec architecture REST API
- Modèles de données avec Pydantic/SQLAlchemy
- Authentification JWT
- Validation des données entrantes
- Gestion des erreurs robuste
- Documentation API automatique (Swagger/OpenAPI)
- Tests unitaires avec pytest
- Logging structuré
```

### Conteneurisation Docker
```
Exigences Docker :
- Dockerfile multi-stage pour optimisation
- docker-compose.yml pour développement local
- Images légères basées sur Alpine Linux
- Variables d'environnement pour configuration
- Health checks pour monitoring
- Séparation des préoccupations (frontend/backend/db)
```

### CI/CD Azure DevOps
```
Exigences CI/CD :
- Pipeline Azure DevOps YAML
- Étapes : build, test, security scan, deploy
- Déploiement sur Azure Container Instances ou App Service
- Environnements : dev, staging, production
- Rollback automatique en cas d'échec
- Monitoring et alertes
```

## Instructions de Génération

### 1. Structure du Projet
Crée la structure suivante :
```
project-name/
├── frontend/                 # React mobile-first
│   ├── src/
│   ├── public/
│   ├── Dockerfile
│   └── package.json
├── backend/                  # Python services
│   ├── app/
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
├── infrastructure/           # Azure & Docker
│   ├── docker-compose.yml
│   └── azure-pipelines.yml
└── README.md
```

### 2. Composants à Générer

#### Frontend React Mobile-First
- [ ] Composants UI responsive avec CSS modules/Styled Components
- [ ] Hooks personnalisés pour logique métier
- [ ] Service workers pour PWA
- [ ] Formulaires avec validation côté client
- [ ] Navigation mobile (bottom tabs, drawer)
- [ ] Animations fluides et micro-interactions
- [ ] Optimisation des images (WebP, lazy loading)

#### Backend Python
- [ ] Modèles de données avec relations
- [ ] Endpoints REST avec documentation
- [ ] Middleware d'authentification
- [ ] Services métier découplés
- [ ] Tests automatisés (unitaires et intégration)
- [ ] Configuration par environnement

#### Infrastructure
- [ ] Dockerfiles optimisés
- [ ] Pipeline CI/CD complet
- [ ] Configuration Azure (App Service, Container Registry)
- [ ] Scripts de déploiement
- [ ] Monitoring et logging

### 3. Bonnes Pratiques à Respecter

#### Mobile-First
- Commencer par le design mobile puis adapter aux écrans plus grands
- Touch-friendly (boutons min 44px, zones tactiles généreuses)
- Navigation intuitive avec pouces
- Temps de chargement optimisés pour réseaux mobiles

#### Code Quality
- Nommage explicite et cohérent
- Commentaires pour logique complexe
- Séparation des responsabilités
- Gestion d'erreurs exhaustive
- Tests avec couverture > 80%

#### Sécurité
- Validation stricte des inputs
- Protection CSRF/XSS
- Secrets via variables d'environnement
- HTTPS obligatoire
- Rate limiting sur API

## Format de Réponse Attendu

Pour chaque composant généré, fournis :
1. **Code source complet** avec commentaires
2. **Instructions d'installation** et de configuration
3. **Commandes de déploiement** Azure
4. **Tests de validation** fonctionnels
5. **Documentation technique** concise