Feature: Défis quotidiens et quiz
  En tant qu'utilisateur participant à une saison
  Je veux recevoir des défis quotidiens personnalisés
  Afin de gagner des points et enrichir mon expérience de vacances

  Background:
    Given je participe à la saison active "Vacances Réunion 2025"
    And nous sommes dans la période de la saison
    And l'IA de génération de contenu est disponible

  @challenges @daily_generation
  Scenario: Génération automatique des défis quotidiens
    Given nous sommes le "05/07/2025" à "08:00"
    And notre localisation GPS est "Saint-Denis, La Réunion"
    And notre activité prévue est "Visite du marché de Saint-Denis"
    When le système génère les défis du jour
    Then je dois recevoir 3 défis différents
    And les défis doivent être adaptés à la localisation
    And les défis doivent être en rapport avec l'activité prévue
    And je dois voir une notification "Nouveaux défis disponibles !"

  @challenges @quiz
  Scenario: Répondre à un quiz généré par IA
    Given un quiz sur "La culture créole réunionnaise" est disponible
    When je clique sur le défi quiz
    Then je dois voir une question "Quel est l'épice emblématique de la cuisine créole ?"
    And je dois voir 4 options de réponse
    When je sélectionne "Curcuma"
    And je valide ma réponse au quiz
    Then je dois voir "Bonne réponse ! +10 points"
    And mes points doivent être mis à jour automatiquement

  @challenges @photo
  Scenario: Défi photo avec validation
    Given un défi photo "Trouvez un caméléon endémique" est disponible
    When je clique sur le défi photo
    Then je dois voir l'énoncé du défi
    And je dois voir un bouton "Prendre une photo"
    When je clique sur "Prendre une photo"
    And je prends une photo avec l'appareil
    And je clique sur "Soumettre la photo"
    Then la photo doit être envoyée pour validation
    And je dois voir "Photo soumise, en attente de validation"

  @challenges @sport
  Scenario: Défi sportif avec tracking GPS
    Given un défi sportif "Randonnée de 5km au Piton de la Fournaise" est disponible
    When je clique sur "Commencer le défi"
    Then le tracking GPS doit s'activer
    And je dois voir ma position actuelle sur une carte
    When je parcours 5 kilomètres
    And je termine la randonnée
    Then le défi doit être automatiquement validé
    And je dois gagner les points correspondants "+25 points"

  @challenges @difficulty
  Scenario Outline: Adaptation de la difficulté selon l'âge
    Given un utilisateur de "<age>" ans participe aux défis
    When les défis sont générés
    Then les questions doivent avoir un niveau de difficulté "<niveau>"
    And le vocabulaire utilisé doit être adapté à l'âge

    Examples:
      | age | niveau     |
      | 15  | Moyen      |
      | 18  | Difficile  |
      | 45  | Expert     |

  @challenges @timeout
  Scenario: Gestion du temps limite pour les quiz
    Given un quiz avec une limite de temps de 30 secondes
    When je commence à répondre au quiz
    Then un chronomètre de 30 secondes doit s'afficher
    When le temps expire sans réponse
    Then la question doit se fermer automatiquement
    And je dois voir "Temps écoulé ! Aucun point attribué"

  @challenges @hint
  Scenario: Utilisation d'indices pour les quiz difficiles
    Given un quiz difficile sur "L'histoire géologique de La Réunion"
    When je ne connais pas la réponse
    And je clique sur "Utiliser un indice"
    Then un indice doit s'afficher
    And les points potentiels doivent être réduits de moitié
    When je réponds correctement avec l'indice
    Then je dois gagner 50% des points normaux

  @challenges @multiplayer
  Scenario: Défis multijoueurs en temps réel
    Given un défi multijoueur "Quiz rapide famille" est lancé
    And tous les membres de la famille sont connectés
    When je rejoins le défi
    Then je dois voir les autres participants
    And nous devons tous voir la même question simultanément
    When je réponds en premier avec la bonne réponse
    Then je dois gagner des points bonus pour la rapidité

  @challenges @contextual
  Scenario: Génération contextuelle basée sur la météo
    Given la météo actuelle à La Réunion est "Pluvieuse"
    And notre activité prévue était "Plage"
    When les défis sont générés
    Then le système doit proposer des défis d'intérieur
    And je dois voir des suggestions adaptées "Quiz sur l'artisanat local"
    And aucun défi extérieur ne doit être proposé

  @challenges @validation_manual
  Scenario: Validation manuelle des défis photo
    Given j'ai soumis une photo pour le défi "Trouvez un tangue"
    And Papa Organisateur est validateur
    When Papa Organisateur consulte les soumissions
    Then il doit voir ma photo avec les détails du défi
    When il clique sur "Valider" avec le commentaire "Parfait !"
    Then je dois recevoir une notification de validation
    And mes points doivent être crédités
    And je dois voir le commentaire du validateur
