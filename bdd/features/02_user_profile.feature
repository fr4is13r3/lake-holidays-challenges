Feature: Gestion des profils utilisateur
  En tant qu'utilisateur de l'application
  Je veux pouvoir créer et personnaliser mon profil
  Afin d'avoir une identité unique dans les défis familiaux

  Background:
    Given je suis connecté à l'application
    And je suis sur la page de gestion de profil

  @profile @creation
  Scenario: Création d'un profil complet
    Given je suis un nouvel utilisateur connecté
    When je saisis mon pseudo "Papa Aventurier"
    And je choisis un avatar depuis la galerie prédéfinie
    And je sélectionne mon âge "45 ans"
    And je définis mes préférences de défis "Sport et Culture"
    And je clique sur "Enregistrer le profil"
    Then mon profil doit être créé avec succès
    And je dois voir une confirmation "Profil créé avec succès"
    And mes informations doivent être sauvegardées

  @profile @modification
  Scenario: Modification des informations de profil
    Given j'ai un profil existant avec le pseudo "Papa"
    When je modifie mon pseudo en "Papa Aventurier"
    And je change mon avatar
    And je clique sur "Mettre à jour"
    Then mes modifications doivent être sauvegardées
    And je dois voir "Profil mis à jour avec succès"
    And les autres membres de la famille doivent voir mon nouveau pseudo

  @profile @avatar
  Scenario Outline: Sélection d'avatars prédéfinis
    Given je suis en train de configurer mon profil
    When je clique sur "Choisir un avatar"
    Then je dois voir une galerie d'avatars
    And je peux sélectionner un avatar "<type_avatar>"
    And l'avatar sélectionné doit s'afficher dans mon profil

    Examples:
      | type_avatar    |
      | Aventurier     |
      | Sportif        |
      | Photographe    |
      | Explorateur    |
      | Gourmand      |

  @profile @preferences
  Scenario: Configuration des préférences de défis
    Given je configure mon profil
    When je sélectionne mes préférences de défis
    And je choisis "Sport" comme préférence principale
    And je choisis "Photographie" comme préférence secondaire
    And je désélectionne "Quiz difficiles"
    And je sauvegarde mes préférences
    Then le système doit adapter les défis générés selon mes préférences
    And je dois recevoir plus de défis sportifs et photo

  @profile @validation
  Scenario: Validation des données de profil
    Given je crée un nouveau profil
    When je laisse le champ pseudo vide
    And je clique sur "Enregistrer"
    Then je dois voir une erreur "Le pseudo est obligatoire"
    And le profil ne doit pas être créé

  @profile @family_visibility
  Scenario: Visibilité du profil pour la famille
    Given j'ai complété mon profil "Papa Aventurier"
    And ma famille est dans la même saison "Réunion 2025"
    When un membre de ma famille consulte la liste des participants
    Then il doit voir mon profil avec mon pseudo et avatar
    And il doit voir mes statistiques publiques
    But il ne doit pas voir mes informations privées
