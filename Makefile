# Makefile pour l'application Vacances Gamifiées - Full Stack
# Usage: make [target]

.PHONY: help install test test-smoke test-auth test-ui test-api test-staging test-parallel clean reports backend-setup backend-dev backend-test frontend-setup frontend-dev terraform-setup terraform-plan terraform-apply terraform-destroy deploy-dev deploy-prod

# Variables par défaut
PYTHON := python3
PIP := pip3
BDD_DIR := bdd
BACKEND_DIR := backend
FRONTEND_DIR := frontend
TERRAFORM_DIR := terraform
REPORTS_DIR := reports

# Couleurs pour l'affichage
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[1;33m
RED := \033[0;31m
NC := \033[0m

# Aide par défaut
help: ## Afficher cette aide
	@echo -e "$(BLUE)🚀 Lake Holidays Challenge - Full Stack Application$(NC)"
	@echo ""
	@echo "Targets disponibles:"
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ { printf "  $(GREEN)%-25s$(NC) %s\n", $$1, $$2 }' $(MAKEFILE_LIST)
	@echo ""
	@echo "Exemples:"
	@echo "  make setup               # Configuration complète (backend + frontend + BDD)"
	@echo "  make backend-dev         # Démarrer le backend en mode développement"
	@echo "  make frontend-dev        # Démarrer le frontend en mode développement"
	@echo "  make test-smoke          # Tests critiques rapides"
	@echo "  make docker-up           # Démarrer tous les services avec Docker"
	@echo ""
	@echo "🏗️  Azure & Terraform:"
	@echo "  make terraform-setup     # Configuration initiale Azure/Terraform"
	@echo "  make deploy-dev          # Déploiement complet développement"
	@echo "  make deploy-prod         # Déploiement complet production"

# =============================================================================
# SETUP ET INSTALLATION
# =============================================================================

setup: backend-setup frontend-setup install ## Configuration complète du projet
	@echo -e "$(GREEN)✅ Configuration complète terminée$(NC)"
	@echo ""
	@echo "Prochaines étapes:"
	@echo "1. Backend:  make backend-dev"
	@echo "2. Frontend: make frontend-dev"
	@echo "3. Tests:    make test-smoke"

# Backend
backend-setup: ## Configuration du backend Python/FastAPI
	@echo -e "$(BLUE)🐍 Configuration du backend...$(NC)"
	cd $(BACKEND_DIR) && chmod +x scripts/setup-dev.sh && ./scripts/setup-dev.sh

backend-install: ## Installer uniquement les dépendances backend
	@echo -e "$(BLUE)📦 Installation backend...$(NC)"
	cd $(BACKEND_DIR) && $(PIP) install -r requirements.txt

backend-dev: ## Démarrer le backend en mode développement
	@echo -e "$(BLUE)🚀 Démarrage backend (http://localhost:8000)...$(NC)"
	cd $(BACKEND_DIR) && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

backend-test: ## Tests unitaires du backend
	@echo -e "$(BLUE)🧪 Tests backend...$(NC)"
	cd $(BACKEND_DIR) && pytest -v

backend-lint: ## Vérification du code backend
	@echo -e "$(BLUE)🔍 Lint backend...$(NC)"
	cd $(BACKEND_DIR) && black . && isort . && flake8 .

# Frontend
frontend-setup: ## Configuration du frontend React/Vite
	@echo -e "$(BLUE)⚛️  Configuration du frontend...$(NC)"
	cd $(FRONTEND_DIR) && npm install

frontend-dev: ## Démarrer le frontend en mode développement
	@echo -e "$(BLUE)🚀 Démarrage frontend (http://localhost:5173)...$(NC)"
	cd $(FRONTEND_DIR) && npm run dev

frontend-build: ## Build du frontend pour production
	@echo -e "$(BLUE)🏗️  Build frontend...$(NC)"
	cd $(FRONTEND_DIR) && npm run build

frontend-test: ## Tests du frontend
	@echo -e "$(BLUE)🧪 Tests frontend...$(NC)"
	cd $(FRONTEND_DIR) && npm test

frontend-lint: ## Vérification du code frontend
	@echo -e "$(BLUE)🔍 Lint frontend...$(NC)"
	cd $(FRONTEND_DIR) && npm run lint

# =============================================================================
# DOCKER
# =============================================================================

docker-up: ## Démarrer tous les services avec Docker
	@echo -e "$(BLUE)🐳 Démarrage des services Docker...$(NC)"
	cd $(BACKEND_DIR) && docker-compose up -d

docker-down: ## Arrêter tous les services Docker
	@echo -e "$(BLUE)🛑 Arrêt des services Docker...$(NC)"
	cd $(BACKEND_DIR) && docker-compose down

docker-logs: ## Voir les logs des services Docker
	@echo -e "$(BLUE)📋 Logs des services...$(NC)"
	cd $(BACKEND_DIR) && docker-compose logs -f

docker-build: ## Rebuild des images Docker
	@echo -e "$(BLUE)🔨 Build des images Docker...$(NC)"
	cd $(BACKEND_DIR) && docker-compose build

# =============================================================================
# BDD TESTS (Tests d'acceptation)
# =============================================================================
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

# =============================================================================
# TERRAFORM & AZURE DEPLOYMENT  
# =============================================================================

terraform-setup: ## Configuration initiale Terraform et Azure
	@echo -e "$(BLUE)🏗️  Configuration initiale Terraform...$(NC)"
	./scripts/deploy-infrastructure.sh $(if $(ENVIRONMENT),$(ENVIRONMENT),dev) setup

terraform-plan: ## Planifier les changements Terraform (dev par défaut)
	@echo -e "$(BLUE)📋 Planification Terraform (dev)...$(NC)"
	./scripts/deploy-infrastructure.sh dev plan

terraform-plan-prod: ## Planifier les changements Terraform (production)
	@echo -e "$(BLUE)📋 Planification Terraform (production)...$(NC)"
	./scripts/deploy-infrastructure.sh prod plan

terraform-apply: ## Appliquer les changements Terraform (dev)
	@echo -e "$(BLUE)🚀 Déploiement Terraform (dev)...$(NC)"
	./scripts/deploy-infrastructure.sh dev apply

terraform-apply-prod: ## Appliquer les changements Terraform (production)
	@echo -e "$(YELLOW)⚠️  Déploiement en PRODUCTION!$(NC)"
	./scripts/deploy-infrastructure.sh prod apply

terraform-destroy: ## Détruire l'infrastructure (dev)
	@echo -e "$(RED)💥 Destruction infrastructure (dev)...$(NC)"
	./scripts/deploy-infrastructure.sh dev destroy

terraform-destroy-prod: ## Détruire l'infrastructure (production)
	@echo -e "$(RED)💥 DESTRUCTION PRODUCTION!$(NC)"
	./scripts/deploy-infrastructure.sh prod destroy

deploy-dev: ## Déploiement complet développement
	@echo -e "$(BLUE)🚀 Déploiement complet développement...$(NC)"
	make terraform-plan
	make terraform-apply
	@echo -e "$(GREEN)✅ Déploiement dev terminé$(NC)"

deploy-prod: ## Déploiement complet production
	@echo -e "$(YELLOW)🚀 Déploiement complet production...$(NC)"
	make terraform-plan-prod
	make terraform-apply-prod
	@echo -e "$(GREEN)✅ Déploiement production terminé$(NC)"

terraform-format: ## Formater les fichiers Terraform
	@echo -e "$(BLUE)🔧 Formatage Terraform...$(NC)"
	cd $(TERRAFORM_DIR) && terraform fmt -recursive

terraform-validate: ## Valider la configuration Terraform
	@echo -e "$(BLUE)✅ Validation Terraform...$(NC)"
	cd $(TERRAFORM_DIR) && terraform init -backend=false && terraform validate

terraform-security: ## Scanner la sécurité Terraform
	@echo -e "$(BLUE)🔒 Scan sécurité Terraform...$(NC)"
	@if command -v tfsec >/dev/null 2>&1; then \
		cd $(TERRAFORM_DIR) && tfsec .; \
	else \
		echo -e "$(YELLOW)tfsec non installé. Installer avec: brew install tfsec$(NC)"; \
	fi

terraform-docs: ## Générer la documentation Terraform
	@echo -e "$(BLUE)📚 Génération documentation Terraform...$(NC)"
	@if command -v terraform-docs >/dev/null 2>&1; then \
		cd $(TERRAFORM_DIR) && terraform-docs markdown table --output-file README.md .; \
	else \
		echo -e "$(YELLOW)terraform-docs non installé.$(NC)"; \
	fi

azure-login: ## Connexion Azure CLI
	@echo -e "$(BLUE)🔐 Connexion Azure...$(NC)"
	az login

azure-info: ## Informations compte Azure
	@echo -e "$(BLUE)ℹ️  Informations Azure...$(NC)"
	@echo "Compte actuel:"
	@az account show --query "{nom: name, id: id, tenant: tenantId}" -o table 2>/dev/null || echo "Non connecté à Azure"
	@echo ""
	@echo "Groupes de ressources Lake Holidays:"
	@az group list --query "[?contains(name, 'lake-holidays')].{nom: name, region: location, status: properties.provisioningState}" -o table 2>/dev/null || echo "Aucun groupe trouvé"

# Target par défaut
.DEFAULT_GOAL := help
