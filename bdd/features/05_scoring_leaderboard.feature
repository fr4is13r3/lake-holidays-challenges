Feature: Système de scoring et classements
  En tant qu'utilisateur participant aux défis
  Je veux voir mes points et mon classement en temps réel
  Afin de suivre ma progression et me motiver à participer davantage

  Background:
    Given je participe à la saison "Vacances Réunion 2025"
    And la famille comprend 4 membres : Papa, Maman, Ado1 (18 ans), Ado2 (15 ans)
    And tous ont des profils actifs

  @scoring @points_attribution
  Scenario Outline: Attribution des points selon le type de défi
    Given un défi de type "<type_defi>" est disponible
    When je complète le défi avec succès
    Then je dois recevoir "<points>" points
    And mes points totaux doivent être mis à jour
    And une notification doit confirmer "+<points> points"

    Examples:
      | type_defi    | points |
      | Quiz facile  | 10     |
      | Quiz moyen   | 15     |
      | Quiz difficile| 25     |
      | Photo simple | 15     |
      | Photo créative| 20     |
      | Sport 5km    | 25     |
      | Sport 10km   | 40     |

  @scoring @bonus_speed
  Scenario: Bonus de rapidité pour les quiz
    Given un quiz multijoueur est lancé
    And tous les membres de la famille participent
    When je réponds correctement en premier
    Then je dois recevoir les points de base + 5 points de bonus
    And je dois voir "Première réponse correcte ! +5 points bonus"
    When Maman répond correctement en deuxième
    Then elle doit recevoir les points de base + 3 points bonus

  @scoring @streak_bonus
  Scenario: Bonus de série pour participation quotidienne
    Given j'ai participé à des défis pendant 5 jours consécutifs
    When je complète au moins un défi le 6ème jour
    Then je dois recevoir un bonus de série de 20 points
    And je dois voir "6 jours consécutifs ! Bonus de série : +20 points"
    And un badge "Régularité" doit m'être attribué

  @scoring @daily_leaderboard
  Scenario: Classement quotidien de la famille
    Given nous sommes le 5ème jour de vacances
    And les scores du jour sont :
      | Membre | Points |
      | Papa   | 45     |
      | Maman  | 60     |
      | Ado1   | 35     |
      | Ado2   | 40     |
    When je consulte le classement quotidien
    Then je dois voir Maman en première position
    And Papa en deuxième position
    And Ado2 en troisième position
    And Ado1 en quatrième position

  @scoring @global_leaderboard
  Scenario: Classement global de la saison
    Given nous sommes au 10ème jour de la saison
    And les scores globaux sont :
      | Membre | Points totaux |
      | Papa   | 450           |
      | Maman  | 520           |
      | Ado1   | 380           |
      | Ado2   | 410           |
    When je consulte le classement global
    Then le classement doit refléter les points totaux
    And je dois voir l'évolution par rapport à hier

  @scoring @badges
  Scenario Outline: Attribution de badges selon les achievements
    Given j'ai accompli un exploit spécifique
    When je "<action>"
    Then je dois recevoir le badge "<badge>"
    And le badge doit être visible sur mon profil

    Examples:
      | action                           | badge               |
      | complète 10 défis photo          | Photographe Expert  |
      | réponds à 20 quiz                | Cerveau de la famille|
      | parcours 50km en sport           | Athlète Olympique   |
      | participe 7 jours consécutifs    | Assidu             |
      | termine premier 3 jours de suite | Champion           |

  @scoring @points_details
  Scenario: Détails de l'historique des points
    Given j'ai participé à plusieurs défis aujourd'hui
    When je clique sur "Détails de mes points"
    Then je dois voir l'historique chronologique :
      | Heure | Défi                    | Points | Total |
      | 09:15 | Quiz marché créole      | +15    | 15    |
      | 14:30 | Photo caméléon          | +20    | 35    |
      | 16:45 | Randonnée 5km           | +25    | 60    |
      | 18:00 | Bonus rapidité quiz     | +5     | 65    |

  @scoring @team_challenges
  Scenario: Défis en équipe avec partage de points
    Given un défi d'équipe "Cuisine créole en famille" est lancé
    When notre famille complète le défi ensemble
    Then chaque membre doit recevoir les mêmes points
    And nous devons voir "Défi familial réussi ! +30 points pour tous"
    And le défi doit apparaître comme "Réussi en équipe" dans l'historique

  @scoring @penalty
  Scenario: Pénalités pour tricherie ou mauvaises soumissions
    Given j'ai soumis une photo non pertinente pour un défi
    When le validateur rejette ma soumission avec "Photo non conforme"
    Then aucun point ne doit être attribué
    And je dois voir "Soumission rejetée - aucun point attribué"
    But aucune pénalité ne doit être appliquée pour une première erreur

  @scoring @real_time_updates
  Scenario: Mise à jour en temps réel des scores
    Given je suis sur la page de classement
    And Maman complète un défi sur son téléphone
    When ses points sont attribués
    Then je dois voir son score se mettre à jour automatiquement
    And le classement doit se réorganiser si nécessaire
    Sans que j'aie besoin de rafraîchir la page

  @scoring @end_of_day_summary
  Scenario: Résumé de fin de journée
    Given la journée se termine à 23:59
    When l'horloge passe à 00:00
    Then je dois recevoir un résumé de ma journée :
      | Défis complétés | 4        |
      | Points gagnés   | 75       |
      | Position du jour| 2ème     |
      | Position globale| 1er      |
    And le système doit préparer les défis du lendemain
