Feature: Interface mobile et expérience utilisateur
  En tant qu'utilisateur sur mobile
  Je veux une interface optimisée et intuitive
  Afin d'utiliser facilement l'application pendant mes vacances

  Background:
    Given je suis connecté à l'application
    And j'utilise un iPhone 12 avec Safari
    And l'application est en mode responsive mobile

  @ui @responsive
  Scenario: Affichage adaptatif selon la taille d'écran
    Given l'application est ouverte
    When je fais tourner mon téléphone en mode paysage
    Then l'interface doit s'adapter automatiquement
    And tous les éléments doivent rester accessibles
    When je remets en mode portrait
    Then l'interface doit revenir à la disposition mobile optimale

  @ui @navigation
  Scenario: Navigation tactile intuitive
    Given je suis sur la page d'accueil
    When je swipe vers la gauche
    Then je dois naviguer vers la page suivante
    When je swipe vers la droite
    Then je dois revenir à la page précédente
    And la navigation doit être fluide sans latence

  @ui @touch_targets
  Scenario: Zones tactiles optimisées
    Given l'interface affiche des boutons d'action
    Then tous les boutons doivent avoir une taille minimum de 44px
    And l'espacement entre les boutons doit être suffisant
    When je tape sur un bouton
    Then l'action doit s'exécuter sans erreur de ciblage

  @ui @loading_states
  Scenario: États de chargement pendant la génération de défis
    Given je demande la génération de nouveaux défis
    When le système fait appel à l'IA
    Then je dois voir un indicateur de chargement
    And un message "Génération de défis personnalisés..."
    When la génération est terminée
    Then l'indicateur doit disparaître
    And les défis doivent s'afficher

  @ui @offline_mode
  Scenario: Mode hors ligne avec synchronisation
    Given je suis dans une zone sans réseau
    When je complète un défi hors ligne
    Then mes actions doivent être sauvegardées localement
    And je dois voir une indication "Mode hors ligne"
    When la connexion revient
    Then mes données doivent se synchroniser automatiquement

  @ui @notifications
  Scenario: Notifications push contextuelles
    Given les notifications sont activées
    When de nouveaux défis sont générés à 9h00
    Then je dois recevoir une notification "Nouveaux défis disponibles !"
    When je tape sur la notification
    Then l'application doit s'ouvrir sur la page des défis

  @ui @camera_integration
  Scenario: Intégration caméra native
    Given un défi photo est actif
    When je clique sur "Prendre une photo"
    Then l'appareil photo natif doit s'ouvrir
    When je prends une photo
    Then la photo doit être automatiquement redimensionnée
    And un aperçu doit s'afficher avec les options "Garder" ou "Reprendre"

  @ui @gestures
  Scenario: Gestes tactiles avancés
    Given je consulte une photo soumise par un autre joueur
    When je fais un pinch sur la photo
    Then je dois pouvoir zoomer
    When je double-tape sur la photo
    Then le zoom doit se réinitialiser

  @ui @dark_mode
  Scenario: Mode sombre automatique
    Given l'heure locale est 20:00 (coucher du soleil)
    When j'ouvre l'application
    Then l'interface doit passer en mode sombre automatiquement
    And la lisibilité doit être maintenue
    When l'heure locale est 6:00 (lever du soleil)
    Then l'interface doit repasser en mode clair

  @ui @accessibility
  Scenario: Accessibilité et lisibilité
    Given un utilisateur avec des difficultés visuelles
    When il active le mode haute lisibilité
    Then les contrastes doivent être renforcés
    And la taille des textes doit augmenter
    And les éléments interactifs doivent être plus visibles

  @ui @performance
  Scenario: Performance et fluidité
    Given l'application est ouverte depuis 30 minutes
    And j'ai navigué entre plusieurs pages
    When je lance un nouveau défi
    Then la réponse doit être instantanée (< 300ms)
    And aucun ralentissement ne doit être perceptible

  @ui @battery_optimization
  Scenario: Optimisation de la batterie
    Given j'utilise l'application pour un défi GPS
    When le tracking est actif pendant 2 heures
    Then la consommation de batterie doit être optimisée
    And je dois voir l'impact estimé sur l'autonomie

  @ui @error_handling
  Scenario: Gestion des erreurs utilisateur
    Given je soumets un défi sans connexion internet
    When l'envoi échoue
    Then je dois voir un message clair "Impossible d'envoyer - pas de connexion"
    And un bouton "Réessayer plus tard" doit être disponible
    And ma soumission doit être conservée localement

  @ui @orientation_lock
  Scenario: Verrouillage d'orientation pour certaines activités
    Given je prends une photo pour un défi
    When l'appareil photo s'ouvre
    Then l'orientation doit être verrouillée en mode optimal
    When je ferme l'appareil photo
    Then la rotation libre doit être rétablie

  @ui @haptic_feedback
  Scenario: Retour haptique pour les interactions
    Given je réponds à un quiz
    When je sélectionne une réponse correcte
    Then je dois sentir une vibration de validation
    When je sélectionne une réponse incorrecte
    Then je dois sentir une vibration d'erreur différente
