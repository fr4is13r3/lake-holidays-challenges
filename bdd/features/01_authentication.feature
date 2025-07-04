Feature: Authentification des utilisateurs
  En tant qu'utilisateur de l'application de vacances gamifiées
  Je veux pouvoir me connecter avec différents moyens d'authentification
  Afin d'accéder à mes données personnalisées et participer aux défis familiaux

  Background:
    Given l'application est accessible via un navigateur mobile
    And l'interface d'authentification est affichée

  @authentication @smoke
  Scenario: Connexion avec un compte local
    Given je suis un nouvel utilisateur
    When je clique sur "Créer un compte local"
    And je saisis un nom d'utilisateur valide "papa_vacances"
    And je saisis un mot de passe sécurisé "MonMotDePasse123!"
    And je confirme mon mot de passe
    And je clique sur "Créer le compte"
    Then je dois être connecté automatiquement
    And je dois voir la page d'accueil de l'application
    And mon profil doit être créé avec le nom "papa_vacances"

  @authentication @google
  Scenario: Connexion avec un compte Google
    Given je suis sur la page de connexion
    When je clique sur "Se connecter avec Google"
    And je suis redirigé vers Google OAuth
    And je m'authentifie avec mes identifiants Google valides
    And j'autorise l'application à accéder à mes informations
    Then je dois être redirigé vers l'application
    And je dois être connecté automatiquement
    And mon profil doit être créé avec les informations Google

  @authentication @microsoft
  Scenario: Connexion avec un compte Microsoft
    Given je suis sur la page de connexion
    When je clique sur "Se connecter avec Microsoft"
    And je suis redirigé vers Microsoft OAuth
    And je m'authentifie avec mes identifiants Microsoft valides
    And j'autorise l'application à accéder à mes informations
    Then je dois être redirigé vers l'application
    And je dois être connecté automatiquement
    And mon profil doit être créé avec les informations Microsoft

  @authentication @error
  Scenario: Échec de connexion avec des identifiants invalides
    Given je suis sur la page de connexion
    When je saisis un nom d'utilisateur "utilisateur_inexistant"
    And je saisis un mot de passe "mauvais_mot_de_passe"
    And je clique sur "Se connecter"
    Then je dois voir un message d'erreur "Identifiants incorrects"
    And je dois rester sur la page de connexion

  @authentication @logout
  Scenario: Déconnexion de l'application
    Given je suis connecté avec le compte "papa_vacances"
    And je suis sur la page d'accueil
    When je clique sur le menu profil
    And je clique sur "Se déconnecter"
    Then je dois être déconnecté
    And je dois être redirigé vers la page de connexion
    And mes données de session doivent être effacées

  @authentication @session
  Scenario: Maintien de la session utilisateur
    Given je suis connecté avec le compte "papa_vacances"
    When je ferme mon navigateur
    And je rouvre l'application dans les 24 heures
    Then je dois être toujours connecté
    And je dois voir la page d'accueil directement
