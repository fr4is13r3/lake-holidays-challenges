Feature: Gestion des saisons de vacances
  En tant qu'organisateur familial
  Je veux pouvoir créer et gérer des saisons de vacances
  Afin que ma famille puisse participer aux défis pendant notre séjour

  Background:
    Given je suis connecté en tant qu'utilisateur "Papa Organisateur"
    And j'ai accès aux fonctionnalités de gestion des saisons

  @season @creation
  Scenario: Création d'une nouvelle saison
    Given je suis sur la page de gestion des saisons
    When je clique sur "Créer une nouvelle saison"
    And je saisis le titre "Vacances Réunion 2025"
    And je sélectionne la date de début "01/07/2025"
    And je sélectionne la date de fin "30/07/2025"
    And je saisis la localisation "Île de La Réunion, France"
    And je télécharge une photo de couverture "reunion_plage.jpg"
    And je clique sur "Créer la saison"
    Then la saison doit être créée avec succès
    And je dois voir "Saison créée avec succès"
    And la saison doit apparaître dans ma liste des saisons

  @season @join
  Scenario: Rejoindre une saison existante
    Given une saison "Vacances Réunion 2025" existe
    And j'ai reçu un code d'invitation "REUNION2025"
    When je clique sur "Rejoindre une saison"
    And je saisis le code d'invitation "REUNION2025"
    And je clique sur "Rejoindre"
    Then je dois être ajouté à la saison
    And je dois voir "Vous avez rejoint la saison avec succès"
    And la saison doit apparaître dans mes saisons actives

  @season @invitation
  Scenario: Invitation des membres de la famille
    Given j'ai créé la saison "Vacances Réunion 2025"
    When je clique sur "Inviter des membres"
    And je génère un code d'invitation
    Then je dois recevoir un code unique "REUNION2025"
    And je peux partager ce code avec ma famille
    And le code doit être valide jusqu'à la fin de la saison

  @season @activation
  Scenario: Activation automatique de la saison
    Given la saison "Vacances Réunion 2025" commence le "01/07/2025"
    And nous sommes le "01/07/2025" de la saison
    When j'ouvre l'application
    Then la saison doit être automatiquement activée
    And je dois voir "Votre saison Vacances Réunion 2025 a commencé !"
    And les défis quotidiens doivent être disponibles

  @season @end
  Scenario: Fin automatique de la saison
    Given la saison "Vacances Réunion 2025" se termine le "30/07/2025"
    And nous sommes le "31/07/2025" de la saison
    When j'ouvre l'application
    Then la saison doit être automatiquement désactivée
    And je dois voir un résumé final des scores
    And aucun nouveau défi ne doit être généré

  @season @settings
  Scenario: Modification des paramètres de saison
    Given je suis le créateur de la saison "Vacances Réunion 2025"
    When je clique sur "Paramètres de la saison"
    And je modifie la date de fin à "31/07/2025"
    And je change la photo de couverture
    And je sauvegarde les modifications
    Then les changements doivent être appliqués
    And tous les membres doivent voir les modifications

  @season @validation
  Scenario Outline: Validation des données de saison
    Given je crée une nouvelle saison
    When je saisis "<titre>" comme titre
    And je sélectionne "<date_debut>" comme date de début
    And je sélectionne "<date_fin>" comme date de fin
    And je clique sur "Créer"
    Then je dois voir le message "<message_erreur>"

    Examples:
      | titre | date_debut | date_fin   | message_erreur                           |
      |       | 01/07/2025 | 30/07/2025 | Le titre de la saison est obligatoire   |
      | Test  | 30/07/2025 | 01/07/2025 | La date de fin doit être après le début |
      | Test  | 01/01/2020 | 02/01/2020 | La saison ne peut pas être dans le passé|

  @season @multiple
  Scenario: Gestion de plusieurs saisons
    Given j'ai participé à la saison "Vacances Réunion 2024" (terminée)
    And j'ai créé la saison "Vacances Réunion 2025" (active)
    When je consulte mes saisons
    Then je dois voir les deux saisons
    And seule la saison active doit permettre de nouveaux défis
    And je peux consulter l'historique de la saison terminée
