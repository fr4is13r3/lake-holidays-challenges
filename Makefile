# Makefile pour l'application Vacances Gamifiées - Tests BDD
# Usage: make [target]

.PHONY: help install test test-smoke test-auth test-ui test-api test-staging test-parallel clean reports

# Variables par défaut
PYTHON := python3
PIP := pip3
BDD_DIR := bdd
REPORTS_DIR := reports

# Couleurs pour l'affichage
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[1;33m
RED := \033[0;31m
NC := \033[0m

# Aide par défaut
help: ## Afficher cette aide
	@echo -e "$(BLUE)🧪 Tests BDD - Application Vacances Gamifiées$(NC)"
	@echo ""
	@echo "Targets disponibles:"
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ { printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2 }' $(MAKEFILE_LIST)
	@echo ""
	@echo "Exemples:"
	@echo "  make install     # Installer les dépendances"
	@echo "  make test-smoke  # Tests critiques rapides"
	@echo "  make test-ui     # Tests d'interface uniquement"
	@echo "  make reports     # Générer tous les rapports"

# Installation
install: ## Installer les dépendances BDD
	@echo -e "$(BLUE)📦 Installation des dépendances BDD...$(NC)"
	cd $(BDD_DIR) && $(PIP) install -r requirements.txt
	@echo -e "$(GREEN)✅ Installation terminée$(NC)"

install-dev: ## Installer les dépendances de développement
	@echo -e "$(BLUE)📦 Installation complète (dev + BDD)...$(NC)"
	$(PIP) install -r requirements-dev.txt || echo "requirements-dev.txt non trouvé"
	cd $(BDD_DIR) && $(PIP) install -r requirements.txt
	@echo -e "$(GREEN)✅ Installation développement terminée$(NC)"

# Tests rapides
test-smoke: ## Exécuter les tests de smoke (critiques uniquement)
	@echo -e "$(BLUE)🚀 Tests de smoke...$(NC)"
	cd $(BDD_DIR) && ./run_bdd_tests.sh --tags @smoke

test-quick: ## Tests rapides sans interface graphique
	@echo -e "$(BLUE)⚡ Tests rapides...$(NC)"
	cd $(BDD_DIR) && ./run_bdd_tests.sh --tags @smoke,@api --headless true

# Tests par fonctionnalité
test-auth: ## Tests d'authentification
	@echo -e "$(BLUE)🔐 Tests d'authentification...$(NC)"
	cd $(BDD_DIR) && ./run_bdd_tests.sh --tags @authentication

test-profile: ## Tests de gestion des profils
	@echo -e "$(BLUE)👤 Tests de profils...$(NC)"
	cd $(BDD_DIR) && ./run_bdd_tests.sh --tags @profile

test-season: ## Tests de gestion des saisons
	@echo -e "$(BLUE)📅 Tests de saisons...$(NC)"
	cd $(BDD_DIR) && ./run_bdd_tests.sh --tags @season

test-challenges: ## Tests des défis quotidiens
	@echo -e "$(BLUE)🎯 Tests de défis...$(NC)"
	cd $(BDD_DIR) && ./run_bdd_tests.sh --tags @challenges

test-scoring: ## Tests du système de scoring
	@echo -e "$(BLUE)🏆 Tests de scoring...$(NC)"
	cd $(BDD_DIR) && ./run_bdd_tests.sh --tags @scoring

test-ui: ## Tests d'interface utilisateur
	@echo -e "$(BLUE)📱 Tests d'interface...$(NC)"
	cd $(BDD_DIR) && ./run_bdd_tests.sh --tags @ui --headless false

test-ai: ## Tests de génération de contenu IA
	@echo -e "$(BLUE)🤖 Tests IA...$(NC)"
	cd $(BDD_DIR) && ./run_bdd_tests.sh --tags @ai

# Tests par environnement
test: ## Exécuter tous les tests (environnement dev)
	@echo -e "$(BLUE)🧪 Tests complets - Environnement dev...$(NC)"
	cd $(BDD_DIR) && ./run_bdd_tests.sh --env dev

test-dev: ## Tests sur environnement de développement
	@echo -e "$(BLUE)🔧 Tests développement...$(NC)"
	cd $(BDD_DIR) && ./run_bdd_tests.sh --env dev --headless false

test-staging: ## Tests sur environnement de staging
	@echo -e "$(BLUE)🎭 Tests staging...$(NC)"
	cd $(BDD_DIR) && ./run_bdd_tests.sh --env staging --tags @smoke,@api

test-prod: ## Tests en lecture seule sur production
	@echo -e "$(BLUE)🏭 Tests production (lecture seule)...$(NC)"
	cd $(BDD_DIR) && ./run_bdd_tests.sh --env prod --tags @prod_safe

# Tests parallèles et performance
test-parallel: ## Exécuter les tests en parallèle
	@echo -e "$(BLUE)🚀 Tests parallèles...$(NC)"
	cd $(BDD_DIR) && ./run_bdd_tests.sh --parallel --tags @smoke,@api

test-performance: ## Tests de performance
	@echo -e "$(BLUE)⚡ Tests de performance...$(NC)"
	cd $(BDD_DIR) && ./run_bdd_tests.sh --tags @performance --parallel

# Rapports
reports: ## Générer tous les rapports de tests
	@echo -e "$(BLUE)📊 Génération des rapports...$(NC)"
	mkdir -p $(REPORTS_DIR)
	cd $(BDD_DIR) && ./run_bdd_tests.sh --format html --tags @smoke
	@echo -e "$(GREEN)📄 Rapport HTML: $(REPORTS_DIR)/behave_report.html$(NC)"

reports-full: ## Générer des rapports complets avec tous les tests
	@echo -e "$(BLUE)📈 Rapports complets...$(NC)"
	mkdir -p $(REPORTS_DIR)
	cd $(BDD_DIR) && ./run_bdd_tests.sh --format html
	@echo -e "$(GREEN)📄 Rapport complet: $(REPORTS_DIR)/behave_report.html$(NC)"

reports-allure: ## Générer des rapports Allure (avancés)
	@echo -e "$(BLUE)📋 Rapports Allure...$(NC)"
	mkdir -p $(REPORTS_DIR)/allure-results
	cd $(BDD_DIR) && behave -f allure_behave.formatter:AllureFormatter -o ../$(REPORTS_DIR)/allure-results
	allure serve $(REPORTS_DIR)/allure-results

# Nettoyage
clean: ## Nettoyer les fichiers de test et rapports
	@echo -e "$(BLUE)🧹 Nettoyage...$(NC)"
	rm -rf $(REPORTS_DIR)/*
	rm -rf $(BDD_DIR)/__pycache__
	rm -rf $(BDD_DIR)/.pytest_cache
	find $(BDD_DIR) -name "*.pyc" -delete
	find $(BDD_DIR) -name "*.pyo" -delete
	@echo -e "$(GREEN)✅ Nettoyage terminé$(NC)"

clean-screenshots: ## Supprimer les captures d'écran
	@echo -e "$(BLUE)🗑️  Suppression des captures d'écran...$(NC)"
	rm -rf $(REPORTS_DIR)/screenshots/*
	@echo -e "$(GREEN)✅ Captures supprimées$(NC)"

# Debug et développement
debug: ## Lancer les tests en mode debug (verbose, sans headless)
	@echo -e "$(BLUE)🔍 Mode debug...$(NC)"
	cd $(BDD_DIR) && behave --verbose --no-capture --headless false features/01_authentication.feature

debug-single: ## Debug d'un seul test (spécifier FEATURE=nom_du_fichier)
	@echo -e "$(BLUE)🎯 Debug test unique: $(FEATURE)$(NC)"
	cd $(BDD_DIR) && behave --verbose --no-capture --headless false features/$(FEATURE)

lint: ## Vérifier la qualité du code des tests
	@echo -e "$(BLUE)🔍 Vérification du code...$(NC)"
	cd $(BDD_DIR) && flake8 steps/ --max-line-length=120
	cd $(BDD_DIR) && black --check steps/
	@echo -e "$(GREEN)✅ Code vérifié$(NC)"

format: ## Formater le code des tests
	@echo -e "$(BLUE)🎨 Formatage du code...$(NC)"
	cd $(BDD_DIR) && black steps/
	cd $(BDD_DIR) && isort steps/
	@echo -e "$(GREEN)✅ Code formaté$(NC)"

# Validation et qualité
validate: ## Valider tous les fichiers features
	@echo -e "$(BLUE)✅ Validation des features...$(NC)"
	cd $(BDD_DIR) && behave --dry-run
	@echo -e "$(GREEN)✅ Features valides$(NC)"

# CI/CD
ci-smoke: ## Tests de smoke pour CI/CD
	@echo -e "$(BLUE)🔄 Tests CI - Smoke$(NC)"
	cd $(BDD_DIR) && ./run_bdd_tests.sh --tags @smoke --format json --headless true

ci-full: ## Tests complets pour CI/CD
	@echo -e "$(BLUE)🔄 Tests CI - Complets$(NC)"
	cd $(BDD_DIR) && ./run_bdd_tests.sh --format json --headless true --parallel

# Utilitaires
setup: install ## Alias pour installation
dev-setup: install-dev ## Configuration complète développement

status: ## Afficher le statut de l'environnement de test
	@echo -e "$(BLUE)📊 Statut de l'environnement de test$(NC)"
	@echo "Python: $(shell $(PYTHON) --version 2>&1)"
	@echo "Pip: $(shell $(PIP) --version 2>&1)"
	@if command -v behave >/dev/null 2>&1; then \
		echo "Behave: $(shell behave --version 2>&1)"; \
	else \
		echo -e "$(RED)Behave: Non installé$(NC)"; \
	fi
	@if command -v chromedriver >/dev/null 2>&1; then \
		echo "ChromeDriver: Disponible"; \
	else \
		echo -e "$(YELLOW)ChromeDriver: Non trouvé (géré automatiquement)$(NC)"; \
	fi
	@echo "Répertoire BDD: $(shell ls -la $(BDD_DIR) 2>/dev/null | wc -l) fichiers"
	@echo "Rapports: $(shell ls -la $(REPORTS_DIR) 2>/dev/null | wc -l) fichiers"

# Target par défaut
.DEFAULT_GOAL := help
