# Contexte de l'application

Ceci une version réécrite, structurée de l'expression de besoin. Elle est adaptée pour servir :

* de **base de réflexion pour l’architecture technique**,
* de **support à la création de user stories** (importables dans GitHub Projects),
* et de **document de contextualisation initiale** pour GitHub Copilot.


## 📌 Expression de besoin – Application de gamification des vacances 

### 🎯 Objectif du projet

Créer une application mobile web responsive permettant de **gamifier chaque journée de vacances en famille à l'île de La Réunion**. L’objectif est de transformer le séjour en une expérience ludique et interactive où chaque membre de la famille peut accumuler des points au fil des activités journalières, tout en enrichissant sa connaissance du patrimoine local.

### 👨‍👩‍👦‍👦 Contexte utilisateur

* **Utilisateurs** : 4 membres d’une famille (2 adultes de 45 ans, 2 adolescents de 18 et 15 ans)
* **Durée d’utilisation** : pendant la totalité d’un voyage (été 2025)
* **Support utilisé** :

  * iPhone 12, iPhone 12 Pro, iPhone 15 Pro
  * Navigateurs mobiles : Chrome, Opera

### 🧩 Fonctionnalités principales attendues

1. **Système de points & challenges**

   * Chaque jour, les membres peuvent gagner des points selon différentes mécaniques :

     * Répondre à des **quiz générés dynamiquement** en lien avec l'activité, la localisation ou la date.
     * Réaliser des **défis photos** (ex. : "Prendre une photo d’un caméléon", "Selfie au sommet du volcan").
     * Répondre plus vite ou plus pertinemment que les autres.
   * Possibilité de **valider ou attribuer les points** par un membre désigné ou automatiquement via des règles simples.

2. **Génération dynamique de contenu via LLM**

   * Les quiz/questions du jour sont générés automatiquement grâce à un **modèle de langage (LLM)** (ex. GPT-4 via Azure OpenAI), à partir de :

     * la localisation GPS actuelle
     * la date/heure
     * l’activité prévue (pré-enregistrée ou sélectionnée dans un agenda)

3. **Interface simple et responsive**

   * Affichage du programme du jour (activités prévues)
   * Tableau des scores en temps réel
   * Accès aux défis quotidiens et soumission des réponses/photos

4. **Multijoueur local et scoring**

   * Les 4 utilisateurs ont leur profil (pseudo/avatar)
   * Un tableau de classement quotidien et global est visible

### 🧱 Architecture & contraintes techniques

* **Front-end**

  * Doit être utilisable via navigateur mobile (Chrome, Opera) sur iOS
  * Framework recommandé : **Next.js + Tailwind CSS** pour un rendu full web adaptatif
  * Interface légère, orientée mobile-first

* **Back-end**

  * Déployé sur **Azure** dans un environnement conteneurisé (Kubernetes AKS)
  * API REST (ou GraphQL) pour la gestion des utilisateurs, des scores, et des contenus
  * Intégration Azure OpenAI ou API tierce pour génération des questions

* **Stockage & services**

  * Azure Blob Storage pour les photos et fichiers médias
  * Azure Cosmos DB ou PostgreSQL pour la gestion des données utilisateur, défis, scores

* **Sécurité & accès**

  * Authentification simple avec compte Google
  * Pas de gestion de compte complexe nécessaire (usage ponctuel, privé)

### 🧰 Méthodologie de développement

* Durée cible de développement : **1 semaine**
* Équipe de **1 à 2 développeurs maximum**
* Utilisation de GitHub Copilot pour accélérer le développement à partir de **user stories bien documentées**
* Utilisation de **GitHub Projects** pour gérer les tâches agiles et leur avancement
* Génération automatique de code et tests à partir de **descriptions claires en langage naturel**

---

### 📑 Étapes suivantes

1. **Définition de l’architecture technique**

   * Choix des composants (SDK, APIs, infrastructure cloud)
   * Arborescence des composants (front, back, LLM, stockage)

2. **Création des user stories**

   * Structurées en épics : "Gestion des défis", "Interface utilisateur", "Scoring", "Génération de contenu", etc.
   * Formaté pour import GitHub (YAML/CSV)

3. **Initialisation de la documentation du projet**

   * Un README.md général
   * Un dossier `/docs` contenant :

     * Le contexte projet
     * Les cas d’usage principaux
     * Un guide pour contributeurs (architecture, endpoints, conventions)

---

Souhaites-tu que je t’aide à générer :

* ✅ les **user stories** formatées pour GitHub Projects ?
* ✅ un **README.md** initial ?
* ✅ un **schéma d’architecture modulaire** pour Azure ?
* ✅ une **todo technique avec priorisation sur 7 jours** ?

Tu peux me dire sur quoi tu veux commencer, et je te le prépare.
