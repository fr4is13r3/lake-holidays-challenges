# 📱 Vacances Gamifiées

Bienvenue dans le dépôt de l'application **Vacances Gamifiées**, une application web mobile développée pour transformer les vacances en famille en une expérience ludique et interactive.

---

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

## 🧪 Prochaines étapes

- [ ] Définir l’architecture technique finale
- [ ] Importer les User Stories dans GitHub Projects
- [ ] Générer les premières pages UI statiques
- [ ] Intégrer la logique de scoring
- [ ] Connecter le LLM pour la génération dynamique

---

## 📄 Licence

Projet privé à usage personnel (famille).