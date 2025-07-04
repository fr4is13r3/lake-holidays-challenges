# Guide BDD avec Behave - Application Vacances Gamifiées

## Vue d'ensemble

Ce dossier contient tous les tests BDD (Behavior Driven Development) pour l'application de gamification des vacances familiales. Les tests sont écrits en utilisant le framework **Behave** avec la syntaxe Gherkin.

## Structure des tests

```
bdd/
├── features/                          # Fichiers .feature (cas d'usage)
│   ├── 01_authentication.feature      # Tests d'authentification
│   ├── 02_user_profile.feature        # Gestion des profils
│   ├── 03_season_management.feature   # Gestion des saisons
│   ├── 04_daily_challenges.feature    # Défis quotidiens
│   ├── 05_scoring_leaderboard.feature # Scoring et classements
│   ├── 06_mobile_ui_ux.feature        # Interface mobile
│   └── 07_ai_content_generation.feature # Génération de contenu IA
├── steps/                             # Implémentations des steps
│   ├── authentication_steps.py
│   ├── profile_steps.py
│   ├── season_steps.py
│   ├── challenge_steps.py
│   ├── scoring_steps.py
│   ├── ui_steps.py
│   └── ai_steps.py
├── environment.py                     # Configuration Behave
├── behave.ini                         # Configuration
├── requirements.txt                   # Dépendances
└── README.md                          # Ce fichier
```

## Installation

1. **Installer les dépendances :**
```bash
cd bdd
pip install -r requirements.txt
```

2. **Installer ChromeDriver (pour Selenium) :**
```bash
# Automatique avec webdriver-manager (inclus dans requirements.txt)
# Ou manuellement selon votre OS
```

## Exécution des tests

### Tous les tests
```bash
behave
```

### Tests par feature
```bash
behave features/01_authentication.feature
```

### Tests par tag
```bash
# Tests de smoke uniquement
behave --tags=smoke

# Tests d'authentification
behave --tags=authentication

# Tests mobiles
behave --tags=mobile

# Exclure les tests lents
behave --tags=-slow
```

### Tests avec environnement spécifique
```bash
# Tests en local
TEST_ENV=dev behave

# Tests sur staging
TEST_ENV=staging behave

# Tests en mode headless (sans interface graphique)
behave -D headless=true
```

## Tags organisationnels

### Par fonctionnalité
- `@authentication` - Tests d'authentification
- `@profile` - Gestion des profils
- `@season` - Gestion des saisons
- `@challenges` - Défis et quiz
- `@scoring` - Système de points
- `@ui` - Interface utilisateur
- `@ai` - Génération de contenu IA

### Par type de test
- `@smoke` - Tests critiques rapides
- `@web` - Tests avec navigateur
- `@api` - Tests d'API
- `@mobile` - Tests spécifiques mobile
- `@slow` - Tests longs (exclus par défaut)

### Par environnement
- `@dev_only` - Tests pour développement uniquement
- `@staging_only` - Tests pour staging
- `@prod_safe` - Tests sûrs pour production

## Configuration des environnements

Les tests peuvent s'exécuter contre différents environnements :

### Development (local)
```bash
export TEST_ENV=dev
export BASE_URL=http://localhost:3000
```

### Staging
```bash
export TEST_ENV=staging  
export BASE_URL=https://staging-vacances.azurewebsites.net
```

### Production (lecture seule)
```bash
export TEST_ENV=prod
export BASE_URL=https://vacances.azurewebsites.net
```

## Données de test

### Utilisateurs prédéfinis
- `papa_test` - Papa Aventurier (45 ans, préférences: Sport, Histoire)
- `maman_test` - Maman Photographe (45 ans, préférences: Photo, Culture)  
- `ado1_test` - Ado1 Sportif (18 ans, préférences: Sport, Gaming)
- `ado2_test` - Ado2 Créatif (15 ans, préférences: Art, Photo)

### Saisons de test
- `reunion_2025` - Vacances Réunion 2025 (01/07 - 30/07/2025)

## Rapports de tests

### Rapport HTML
```bash
behave -f html -o reports/behave_report.html
```

### Rapport Allure (avancé)
```bash
behave -f allure_behave.formatter:AllureFormatter -o reports/allure-results
allure serve reports/allure-results
```

### Captures d'écran
En cas d'échec des tests UI, des captures d'écran sont automatiquement sauvegardées dans `reports/screenshots/`.

## Développement de nouveaux tests

### 1. Créer une nouvelle feature
```gherkin
Feature: Nouvelle fonctionnalité
  En tant qu'utilisateur
  Je veux pouvoir faire quelque chose
  Afin d'atteindre un objectif

  @nouveauté @smoke
  Scenario: Cas d'usage principal
    Given un contexte initial
    When j'effectue une action
    Then je vois le résultat attendu
```

### 2. Implémenter les steps
```python
@given('un contexte initial')
def step_context_initial(context):
    # Implémentation
    pass

@when('j\'effectue une action')  
def step_perform_action(context):
    # Implémentation
    pass

@then('je vois le résultat attendu')
def step_verify_result(context):
    # Implémentation avec assertions
    assert condition, "Message d'erreur"
```

### 3. Bonnes pratiques

#### Features (Gherkin)
- Utiliser un langage métier clair
- Éviter les détails techniques
- Un scenario = un comportement
- Utiliser des exemples concrets
- Organiser avec des Background

#### Steps (Python)
- Steps réutilisables
- Assertions claires avec messages
- Gestion des timeouts
- Nettoyage approprié
- Logs structurés

## Intégration CI/CD

### GitHub Actions
```yaml
name: BDD Tests
on: [push, pull_request]

jobs:
  bdd-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: |
          cd bdd
          pip install -r requirements.txt
          behave --tags=smoke
```

### Azure DevOps
```yaml
- task: PythonScript@0
  inputs:
    scriptSource: 'inline'
    script: |
      cd bdd
      pip install -r requirements.txt
      behave --tags=smoke --junit --junit-directory=test-results
```

## Debugging

### Mode verbose
```bash
behave --verbose
```

### Arrêt au premier échec
```bash
behave --stop
```

### Tests en mode interactif
```bash
behave --no-capture
```

### Logs détaillés
```bash
behave --logging-level=DEBUG
```

## Performance

### Tests en parallèle
```bash
behave-parallel --processes 4
```

### Profiling mémoire
```bash
behave --define memory_profile=true
```

## Contribution

1. Créer une branche feature
2. Ajouter/modifier les tests BDD
3. Vérifier que tous les tests passent
4. Créer une pull request
5. Review par l'équipe

## Ressources

- [Documentation Behave](https://behave.readthedocs.io/)
- [Gherkin Reference](https://cucumber.io/docs/gherkin/)
- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [BDD Best Practices](https://cucumber.io/docs/bdd/)

## Support

Pour toute question sur les tests BDD :
1. Consulter cette documentation
2. Vérifier les exemples existants
3. Consulter les logs de test
4. Créer une issue GitHub si nécessaire
