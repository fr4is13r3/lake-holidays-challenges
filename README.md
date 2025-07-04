# 📱 Vacances Gamifiées

Bienvenue dans le dépôt de l'application **Vacances ## 🧪 Tests BDD

## 🎯 Objectif

Créer une application web mobile responsive permettant à une famille de 4 membres (2 adultes, 2 adolescents) de :
- Participer à des défis quotidiens lors d'activités touristiques et sportives
- Gagner des points pour chaque défi accompli
- Consulter un classement quotidien et global
- Générer automatiquement des contenus ludiques contextuels grâce à un LLM (GPT via Azure)

---

## 🧱 Architecture prévue

- **Front-end** : Next.js (UI responsive mobile-first)
- **Back-end** : Python / FastAPI avec déploiement sur Azure (App Service ou AKS)
- **Stockage** : Azure Blob Storage (photos, médias)
- **Base de données** : Azure PostgreSQL
- **Génération de contenu** : Azure OpenAI API (GPT)

---

## ⚙️ Fonctionnalités principales

- Gestion des profils utilisateurs simplifiés en utilisant des comptes Google 
- Attribution automatique de points
- Génération de défis quotidiens (questions / photos) basés sur :
  - la localisation
  - l’activité en cours
  - la date
- Tableau de classement en temps réel
- Soumission de réponses et validation

---

## 🚀 Stack technique recommandée

- Front : `Next.js` + `Tailwind CSS`
- Backend : `FastAPI` (REST API)
- LLM : `Azure OpenAI GPT-4 ou 4o-mini`
- CI/CD : GitHub Actions + Azure Container Registry
- Hébergement : Azure Kubernetes Service (AKS) ou App Service

---

## 🗂️ Structure du dépôt

```
📁 /frontend        → Code UI (Next.js ou React Native Web)
📁 /backend         → API REST + logique serveur
📁 /docs            → Documentation fonctionnelle et technique
📁 /scripts         → Outils d'import/export, init de données
📝 README.md        → Présent fichier
```

---

## Methodologie

L'application est entièrement couverte par des tests BDD (Behavior Driven Development) avec **67 scenarios** :

```bash
# Installation et tests rapides
make install
make test-smoke

# Tests par fonctionnalité
make test-auth        # Authentification
make test-challenges  # Défis quotidiens
make test-ai         # Génération IA

# Rapports détaillés
make reports
```

**📋 Fonctionnalités testées :**
- ✅ Authentification (Google/Microsoft/Local)
- ✅ Gestion des profils et préférences
- ✅ Saisons de vacances avec invitations
- ✅ Défis quotidiens (Quiz, Photo, Sport, IA)
- ✅ Système de scoring et classements
- ✅ Interface mobile responsive
- ✅ Génération de contenu contextuel par IA

**📊 Documentation :**
- [`bdd/README.md`](bdd/README.md) - Guide complet des tests
- [`docs/UserStories.md`](docs/UserStories.md) - 23 User Stories pour GitHub Projects
- [`docs/BDD_Summary.md`](docs/BDD_Summary.md) - Résumé complet

## 🚀 Prochaines étapes

- [x] ✅ **Tests BDD complets** - 67 scenarios couvrant toutes les fonctionnalités
- [x] ✅ **User Stories détaillées** - 23 US prêtes pour GitHub Projects
- [x] ✅ **CI/CD automatisé** - Pipeline GitHub Actions
- [ ] 🔧 **Définir l’architecture**  technique finale
- [ ] 🔧 **Importer les User Stories**  dans GitHub Projects
- [ ] 🔧 **Implémentation frontend** - React mobile-first
- [ ] 🔧 **API Backend** - FastAPI avec Azure OpenAI
- [ ] 🔧 **Déploiement Azure** - Conteneurs + App Servicees**, une application web mobile développée pour transformer les vacances en famille en une expérience ludique et interactive.

---

## 🛠️ Lancer le projet en local

```bash
# Exemple pour frontend
cd frontend
npm install
npm run dev

# Exemple pour backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## 📄 Licence

Projet privé à usage personnel (famille).