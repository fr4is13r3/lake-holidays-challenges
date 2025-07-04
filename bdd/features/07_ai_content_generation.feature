Feature: Génération de contenu par Intelligence Artificielle
  En tant que système de gamification
  Je veux générer automatiquement du contenu personnalisé via l'IA
  Afin de créer des expériences uniques et adaptées au contexte des vacances

  Background:
    Given le service Azure OpenAI est configuré et accessible
    And la famille est en vacances à "La Réunion"
    And les profils utilisateurs contiennent leurs préférences

  @ai @quiz_generation
  Scenario: Génération de quiz contextuels
    Given nous sommes le "15/07/2025" à "Saint-Denis, La Réunion"
    And l'activité prévue est "Visite du Jardin de l'État"
    When le système génère un quiz
    Then le quiz doit contenir des questions sur :
      | Sujet                        | Exemple de question                                |
      | Flore locale                 | "Quel arbre endémique trouve-t-on dans ce jardin ?" |
      | Histoire de Saint-Denis      | "En quelle année ce jardin a-t-il été créé ?"      |
      | Biodiversité réunionnaise    | "Combien d'espèces d'oiseaux vivent à La Réunion ?" |
    And les questions doivent être adaptées aux âges 15-45 ans

  @ai @photo_challenges
  Scenario: Génération de défis photo créatifs
    Given notre localisation GPS est "Cirque de Mafate"
    And l'heure est "14:30" (après-midi ensoleillé)
    When l'IA génère des défis photo
    Then je dois recevoir des défis comme :
      | Type de défi           | Description                                    |
      | Faune endémique        | "Photographiez un paille-en-queue en vol"     |
      | Paysage panoramique    | "Capturez la vue depuis le Piton des Neiges"  |
      | Détail géologique      | "Trouvez une formation volcanique unique"     |
      | Composition artistique | "Créez un cadrage original avec les remparts" |

  @ai @difficulty_adaptation
  Scenario Outline: Adaptation de la difficulté selon l'utilisateur
    Given l'utilisateur "<utilisateur>" avec l'âge "<age>" et les préférences "<preferences>"
    When l'IA génère du contenu
    Then la difficulté doit être "<niveau_difficulte>"
    And le vocabulaire doit être adapté

    Examples:
      | utilisateur | age | preferences      | niveau_difficulte |
      | Ado2       | 15  | Sport, Gaming    | Moyen            |
      | Ado1       | 18  | Photo, Culture   | Difficile        |
      | Papa       | 45  | Histoire, Nature | Expert           |
      | Maman      | 45  | Cuisine, Art     | Expert           |

  @ai @weather_adaptation
  Scenario: Adaptation au contexte météorologique
    Given la météo actuelle est "Orage tropical"
    And l'activité extérieure prévue était "Plage de l'Ermitage"
    When l'IA génère des alternatives
    Then elle doit proposer des activités d'intérieur :
      | Activité alternative    | Défi associé                              |
      | Musée Léon Dierx       | "Quiz sur l'art contemporain réunionnais" |
      | Marché couvert         | "Trouvez 5 épices créoles différentes"   |
      | Cuisine familiale      | "Préparez un carry maison"               |

  @ai @cultural_context
  Scenario: Intégration du contexte culturel local
    Given nous visitons "Hell-Bourg" dans le cirque de Salazie
    When l'IA génère du contenu éducatif
    Then elle doit inclure des éléments culturels spécifiques :
      | Aspect culturel        | Contenu généré                              |
      | Architecture créole    | "Identifiez les éléments d'une case créole" |
      | Traditions locales     | "Qu'est-ce que le maloya ?"                |
      | Artisanat local        | "Trouvez un objet en vacoa"                |
      | Gastronomie            | "Goûtez un bonbon piment"                  |

  @ai @real_time_adaptation
  Scenario: Adaptation en temps réel aux conditions
    Given nous sommes à "La Plaine des Palmistes" à "16:00"
    And la visibilité est réduite par les nuages
    When je demande un nouveau défi
    Then l'IA doit s'adapter aux conditions actuelles
    And proposer un défi faisable : "Écoutez et identifiez 3 sons de la forêt"
    Instead of un défi visuel impossible

  @ai @multilingual_support
  Scenario: Support multilingue adaptatif
    Given la famille inclut des membres parlant français et anglais
    When l'IA génère du contenu
    Then elle peut proposer des défis bilingues :
      | Langue    | Exemple de contenu                        |
      | Français  | "Trouvez le nom créole de cette plante"  |
      | Anglais   | "Find the English name of this bird"     |
      | Bilingue  | "What is 'tangue' in English?"          |

  @ai @learning_progression
  Scenario: Adaptation basée sur l'historique d'apprentissage
    Given Papa a réussi 10 quiz sur l'histoire géologique
    And il a raté 3 quiz sur la faune
    When l'IA génère de nouveaux défis
    Then elle doit équilibrer le contenu :
      | Type de contenu | Proportion | Raison                           |
      | Géologie        | 30%        | Renforcer les connaissances      |
      | Faune           | 50%        | Combler les lacunes              |
      | Autres sujets   | 20%        | Maintenir la variété             |

  @ai @creativity_enhancement
  Scenario: Encouragement de la créativité
    Given l'utilisateur Ado1 aime la photographie
    When l'IA génère des défis photo
    Then elle doit proposer des défis progressivement plus créatifs :
      | Niveau     | Type de défi                              |
      | Débutant   | "Prenez une photo du coucher de soleil"   |
      | Intermédiaire | "Créez un reflet artistique dans l'eau" |
      | Avancé     | "Utilisez les ombres pour raconter une histoire" |

  @ai @error_handling
  Scenario: Gestion des erreurs de génération IA
    Given le service Azure OpenAI est temporairement indisponible
    When je demande un nouveau défi
    Then le système doit utiliser des défis pré-générés en fallback
    And m'informer : "Défis du cache - nouveaux défis bientôt disponibles"
    When le service redevient disponible
    Then la génération automatique doit reprendre

  @ai @content_quality
  Scenario: Contrôle qualité du contenu généré
    Given l'IA génère un quiz sur "Les volcans de La Réunion"
    When le contenu est validé
    Then il doit respecter les critères :
      | Critère           | Validation                              |
      | Exactitude        | Les faits doivent être vérifiables      |
      | Pertinence        | En rapport avec la localisation         |
      | Difficulté        | Adaptée au profil utilisateur          |
      | Langue            | Français correct et clair               |
      | Sécurité          | Aucun contenu inapproprié              |

  @ai @personalization_learning
  Scenario: Apprentissage des préférences utilisateur
    Given j'ai complété 20 défis avec des patterns de réussite
    When l'IA analyse mes performances
    Then elle doit identifier mes préférences :
      | Observation                    | Adaptation future                    |
      | Réussit mieux les quiz visuels | Plus de questions avec images        |
      | Préfère les défis du matin     | Génération prioritaire matinale      |
      | Excelle en géographie locale   | Défis plus poussés sur ce sujet     |
    And adapter les futurs contenus en conséquence
