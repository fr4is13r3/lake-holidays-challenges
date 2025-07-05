#!/bin/bash

# =============================================================================
# Script de configuration et déploiement automatisé
# Lake Holidays Challenge - Infrastructure Azure
# =============================================================================

set -euo pipefail

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variables par défaut
ENVIRONMENT=${1:-"dev"}
ACTION=${2:-"plan"}
FORCE=${3:-"false"}

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TERRAFORM_DIR="$PROJECT_ROOT/terraform"

# Fonctions utilitaires
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_prerequisites() {
    log_info "Vérification des prérequis..."
    
    # Vérifier les outils nécessaires
    local tools=("az" "terraform" "jq" "curl")
    for tool in "${tools[@]}"; do
        if ! command -v "$tool" &> /dev/null; then
            log_error "$tool n'est pas installé"
            exit 1
        fi
    done
    
    # Vérifier la connexion Azure
    if ! az account show &> /dev/null; then
        log_error "Vous n'êtes pas connecté à Azure. Exécutez 'az login'"
        exit 1
    fi
    
    log_success "Tous les prérequis sont satisfaits"
}

setup_terraform_backend() {
    log_info "Configuration du backend Terraform..."
    
    local subscription_id=$(az account show --query id -o tsv)
    local resource_group="rg-lake-apps-prd-tfstate"
    local storage_account="stalakeholidaysprd" #$(date +%s | tail -c 6)"
    local container_name="tfstate"
    
    # Créer le groupe de ressources pour le state
    if ! az group show --name "$resource_group" &> /dev/null; then
        log_info "Création du groupe de ressources $resource_group..."
        az group create --name "$resource_group" --location "France Central"
    fi
    
    # Créer le compte de stockage pour le state
    if ! az storage account show --name "$storage_account" --resource-group "$resource_group" &> /dev/null; then
        log_info "Création du compte de stockage $storage_account..."
        az storage account create \
            --resource-group "$resource_group" \
            --name "$storage_account" \
            --sku Standard_LRS \
            --encryption-services blob
    fi
    
    # Créer le conteneur pour le state
    local storage_key=$(az storage account keys list \
        --resource-group "$resource_group" \
        --account-name "$storage_account" \
        --query '[0].value' -o tsv)
    
    if ! az storage container show \
        --name "$container_name" \
        --account-name "$storage_account" \
        --account-key "$storage_key" &> /dev/null; then
        log_info "Création du conteneur $container_name..."
        az storage container create \
            --name "$container_name" \
            --account-name "$storage_account" \
            --account-key "$storage_key"
    fi
    
    # Sauvegarder la configuration
    cat > "$PROJECT_ROOT/.terraform-backend.conf" << EOF
storage_account_name = "$storage_account"
container_name = "$container_name"
resource_group_name = "$resource_group"
key = "lake-holidays-$ENVIRONMENT.tfstate"
EOF
    
    log_success "Backend Terraform configuré"
}

generate_secrets() {
    log_info "Génération des secrets..."
    
    local secrets_file="$PROJECT_ROOT/.env.terraform"
    
    if [[ ! -f "$secrets_file" ]] || [[ "$FORCE" == "true" ]]; then
        log_info "Création du fichier de secrets..."
        
        # Générer une clé JWT secrète
        local jwt_secret=$(openssl rand -base64 64 | tr -d '\n')
        
        cat > "$secrets_file" << EOF
# Secrets générés pour Terraform
# NE PAS COMMITTER CE FICHIER

# JWT Secret Key
export TF_VAR_jwt_secret_key="$jwt_secret"

# Azure Service Principal (à configurer)
export ARM_CLIENT_ID=""
export ARM_CLIENT_SECRET=""
export ARM_SUBSCRIPTION_ID="$(az account show --query id -o tsv)"
export ARM_TENANT_ID="$(az account show --query tenantId -o tsv)"

# OAuth Secrets (optionnels)
export TF_VAR_google_client_secret=""
export TF_VAR_microsoft_client_secret=""

# OpenAI API Key (optionnel)
export TF_VAR_openai_api_key=""

# Email pour notifications
export TF_VAR_notification_email=""

# Backend Terraform
export TF_BACKEND_CONFIG_FILE="$PROJECT_ROOT/.terraform-backend.conf"
EOF
        
        log_warning "Fichier de secrets créé: $secrets_file"
        log_warning "Veuillez configurer les variables manquantes avant de continuer"
    fi
    
    # Charger les secrets
    if [[ -f "$secrets_file" ]]; then
        source "$secrets_file"
    fi
}

validate_environment() {
    log_info "Validation de l'environnement $ENVIRONMENT..."
    
    case "$ENVIRONMENT" in
        dev|staging|prod)
            log_success "Environnement $ENVIRONMENT valide"
            ;;
        *)
            log_error "Environnement $ENVIRONMENT non supporté. Utilisez: dev, staging, prod"
            exit 1
            ;;
    esac
    
    # Vérifier que le fichier de variables existe
    local tfvars_file="$TERRAFORM_DIR/environments/$ENVIRONMENT/terraform.tfvars"
    if [[ ! -f "$tfvars_file" ]]; then
        log_error "Fichier de variables non trouvé: $tfvars_file"
        exit 1
    fi
}

terraform_plan() {
    log_info "Exécution du plan Terraform pour $ENVIRONMENT..."
    
    cd "$TERRAFORM_DIR"
    
    # Initialisation
    terraform init \
        -backend-config="$TF_BACKEND_CONFIG_FILE" \
        -reconfigure
    
    # Validation
    terraform validate
    
    # Plan
    terraform plan \
        -var-file="environments/$ENVIRONMENT/terraform.tfvars" \
        -out="terraform-$ENVIRONMENT.tfplan" \
        -detailed-exitcode
    
    local exit_code=$?
    
    case $exit_code in
        0)
            log_success "Aucun changement détecté"
            ;;
        2)
            log_warning "Changements détectés - review the plan above"
            ;;
        *)
            log_error "Erreur lors du plan"
            exit $exit_code
            ;;
    esac
}

terraform_apply() {
    log_info "Application du plan Terraform pour $ENVIRONMENT..."
    
    cd "$TERRAFORM_DIR"
    
    if [[ ! -f "terraform-$ENVIRONMENT.tfplan" ]]; then
        log_error "Aucun plan trouvé. Exécutez d'abord 'plan'"
        exit 1
    fi
    
    if [[ "$ENVIRONMENT" == "prod" ]] && [[ "$FORCE" != "true" ]]; then
        log_warning "Déploiement en production détecté!"
        read -p "Êtes-vous sûr de vouloir continuer? (yes/no): " confirm
        if [[ "$confirm" != "yes" ]]; then
            log_info "Déploiement annulé"
            exit 0
        fi
    fi
    
    terraform apply "terraform-$ENVIRONMENT.tfplan"
    
    log_success "Infrastructure déployée avec succès!"
    
    # Afficher les outputs importants
    log_info "Informations de déploiement:"
    terraform output -json | jq -r '
        .deployment_info.value | 
        "Resource Group: \(.resource_group)",
        "Container Registry: \(.container_registry)",
        "Backend App: \(.backend_app_name)",
        "Frontend App: \(.frontend_app_name)"
    '
}

terraform_destroy() {
    log_warning "DESTRUCTION de l'infrastructure $ENVIRONMENT!"
    
    if [[ "$FORCE" != "true" ]]; then
        log_warning "Cette action est IRRÉVERSIBLE!"
        read -p "Tapez 'DELETE' pour confirmer: " confirm
        if [[ "$confirm" != "DELETE" ]]; then
            log_info "Destruction annulée"
            exit 0
        fi
    fi
    
    cd "$TERRAFORM_DIR"
    
    terraform destroy \
        -var-file="environments/$ENVIRONMENT/terraform.tfvars" \
        -auto-approve
    
    log_success "Infrastructure détruite"
}

display_help() {
    cat << EOF
🏖️ Lake Holidays Challenge - Déploiement Infrastructure

Usage: $0 [ENVIRONMENT] [ACTION] [FORCE]

ENVIRONMENT:
    dev     - Environnement de développement (par défaut)
    staging - Environnement de staging  
    prod    - Environnement de production

ACTION:
    plan    - Planifier les changements (par défaut)
    apply   - Appliquer les changements
    destroy - Détruire l'infrastructure
    setup   - Configuration initiale du backend

OPTIONS:
    force   - Forcer l'action sans confirmation

Exemples:
    $0                          # Plan pour dev
    $0 prod plan                # Plan pour production
    $0 dev apply force          # Appliquer dev sans confirmation
    $0 setup                    # Configuration initiale

Configuration requise:
    1. Connexion Azure (az login)
    2. Variables dans .env.terraform
    3. Service Principal Azure avec permissions
EOF
}

main() {
    echo -e "${BLUE}"
    echo "🏖️  Lake Holidays Challenge - Infrastructure Deployment"
    echo "=================================================="
    echo -e "${NC}"
    
    case "$ACTION" in
        help|--help|-h)
            display_help
            exit 0
            ;;
        setup)
            check_prerequisites
            setup_terraform_backend
            generate_secrets
            log_success "Configuration initiale terminée"
            log_info "Prochaines étapes:"
            log_info "1. Configurez les secrets dans .env.terraform"
            log_info "2. Exécutez: $0 $ENVIRONMENT plan"
            exit 0
            ;;
        plan)
            check_prerequisites
            validate_environment
            generate_secrets
            terraform_plan
            ;;
        apply)
            check_prerequisites
            validate_environment
            generate_secrets
            terraform_apply
            ;;
        destroy)
            check_prerequisites
            validate_environment
            generate_secrets
            terraform_destroy
            ;;
        *)
            log_error "Action non reconnue: $ACTION"
            display_help
            exit 1
            ;;
    esac
}

# Point d'entrée
main "$@"
