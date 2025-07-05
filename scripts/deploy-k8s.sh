#!/bin/bash

# Script de déploiement Kubernetes pour Lake Holidays Challenge
# Ce script déploie l'application sur AKS en utilisant les manifests Kubernetes

set -e

# =============================================================================
# CONFIGURATION
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
K8S_DIR="$PROJECT_ROOT/k8s"
TERRAFORM_DIR="$PROJECT_ROOT/terraform"

# Couleurs pour les logs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# =============================================================================
# FONCTIONS UTILITAIRES
# =============================================================================

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
    
    # Vérifier kubectl
    if ! command -v kubectl &> /dev/null; then
        log_error "kubectl n'est pas installé"
        exit 1
    fi
    
    # Vérifier az CLI
    if ! command -v az &> /dev/null; then
        log_error "Azure CLI n'est pas installé"
        exit 1
    fi
    
    # Vérifier terraform
    if ! command -v terraform &> /dev/null; then
        log_error "Terraform n'est pas installé"
        exit 1
    fi
    
    log_success "Tous les prérequis sont installés"
}

get_terraform_outputs() {
    log_info "Récupération des outputs Terraform..."
    
    # Option 1: Utiliser les variables d'environnement si disponibles (GitHub Actions)
    if [ -n "${AZURE_RESOURCE_GROUP:-}" ] && [ -n "${AKS_CLUSTER_NAME:-}" ]; then
        log_info "Utilisation des variables d'environnement GitHub Actions..."
        export RESOURCE_GROUP="$AZURE_RESOURCE_GROUP"
        export AKS_CLUSTER_NAME="$AKS_CLUSTER_NAME"
        export CONTAINER_REGISTRY="${AZURE_CONTAINER_REGISTRY:-}"
        export KEY_VAULT_NAME="${KEY_VAULT_NAME:-}"
        export STORAGE_ACCOUNT_NAME="${STORAGE_ACCOUNT_NAME:-}"
        export SUBSCRIPTION_ID=$(az account show --query id -o tsv)
        export TENANT_ID=$(az account show --query tenantId -o tsv)
        log_success "Variables d'environnement GitHub Actions utilisées"
        return 0
    fi
    
    # Option 2: Utiliser Terraform outputs depuis le backend remote
    cd "$TERRAFORM_DIR"
    
    # Charger la configuration du backend si elle existe
    if [ -f "$PROJECT_ROOT/.env.terraform" ]; then
        log_info "Chargement de la configuration Terraform..."
        source "$PROJECT_ROOT/.env.terraform"
    fi
    
    # Initialiser Terraform avec le backend remote
    log_info "Initialisation de Terraform avec backend remote..."
    if [ -f "$PROJECT_ROOT/.terraform-backend.conf" ]; then
        terraform init -backend-config="$PROJECT_ROOT/.terraform-backend.conf" -input=false > /dev/null
    else
        terraform init -input=false > /dev/null
    fi
    
    if [ $? -ne 0 ]; then
        log_error "Impossible d'initialiser Terraform. Vérifiez la configuration du backend."
        exit 1
    fi
    
    # Tester si on peut récupérer les outputs (au lieu de vérifier le fichier tfstate local)
    log_info "Vérification de l'état Terraform remote..."
    if ! terraform output resource_group_name &> /dev/null; then
        log_error "Impossible de récupérer les outputs Terraform."
        log_error "Vérifiez que l'infrastructure est déployée et que vous avez accès au backend remote."
        log_info "Exécutez d'abord: ./scripts/deploy-infrastructure.sh $ENVIRONMENT apply"
        log_info "Ou configurez les variables d'environnement directement (voir GitHub Actions secrets)"
        exit 1
    fi
    
    # Récupérer les valeurs depuis Terraform
    export RESOURCE_GROUP=$(terraform output -raw resource_group_name)
    export AKS_CLUSTER_NAME=$(terraform output -raw aks_cluster_name)
    export CONTAINER_REGISTRY=$(terraform output -raw container_registry_login_server)
    export KEY_VAULT_NAME=$(terraform output -raw key_vault_name)
    export STORAGE_ACCOUNT_NAME=$(terraform output -raw storage_account_name)
    
    # Récupérer des informations Azure
    export SUBSCRIPTION_ID=$(az account show --query id -o tsv)
    export TENANT_ID=$(az account show --query tenantId -o tsv)
    
    log_success "Outputs Terraform récupérés depuis le backend remote"
}

configure_kubectl() {
    log_info "Configuration de kubectl pour AKS..."
    
    az aks get-credentials \
        --resource-group "$RESOURCE_GROUP" \
        --name "$AKS_CLUSTER_NAME" \
        --overwrite-existing
    
    # Vérifier la connexion
    if kubectl cluster-info &> /dev/null; then
        log_success "kubectl configuré et connecté à AKS"
    else
        log_error "Impossible de se connecter au cluster AKS"
        exit 1
    fi
}

substitute_variables() {
    local file="$1"
    local temp_file="$2"
    
    # Variables par défaut
    ENVIRONMENT="${ENVIRONMENT:-dev}"
    VERSION="${VERSION:-latest}"
    
    # Domaines (à adapter selon votre configuration DNS)
    FRONTEND_DOMAIN="${FRONTEND_DOMAIN:-frontend-${ENVIRONMENT}.${AKS_CLUSTER_NAME}.azure.com}"
    BACKEND_DOMAIN="${BACKEND_DOMAIN:-api-${ENVIRONMENT}.${AKS_CLUSTER_NAME}.azure.com}"
    
    # OpenAI endpoint (optionnel)
    cd "$TERRAFORM_DIR"
    if terraform output openai_endpoint &> /dev/null; then
        OPENAI_ENDPOINT=$(terraform output -raw openai_endpoint)
    else
        OPENAI_ENDPOINT=""
        log_warning "OpenAI endpoint non configuré dans Terraform"
    fi
    
    # Récupérer l'identity client ID pour Workload Identity
    AKS_CLIENT_ID=$(az aks show --resource-group "$RESOURCE_GROUP" --name "$AKS_CLUSTER_NAME" --query identityProfile.kubeletidentity.clientId -o tsv)
    
    # Remplacements dans le fichier
    sed \
        -e "s/{{ENVIRONMENT}}/$ENVIRONMENT/g" \
        -e "s/{{VERSION}}/$VERSION/g" \
        -e "s/{{CONTAINER_REGISTRY}}/$CONTAINER_REGISTRY/g" \
        -e "s/{{KEY_VAULT_NAME}}/$KEY_VAULT_NAME/g" \
        -e "s/{{STORAGE_ACCOUNT_NAME}}/$STORAGE_ACCOUNT_NAME/g" \
        -e "s/{{FRONTEND_DOMAIN}}/$FRONTEND_DOMAIN/g" \
        -e "s/{{BACKEND_DOMAIN}}/$BACKEND_DOMAIN/g" \
        -e "s/{{OPENAI_ENDPOINT}}/$OPENAI_ENDPOINT/g" \
        -e "s/{{SUBSCRIPTION_ID}}/$SUBSCRIPTION_ID/g" \
        -e "s/{{RESOURCE_GROUP}}/$RESOURCE_GROUP/g" \
        -e "s/{{TENANT_ID}}/$TENANT_ID/g" \
        -e "s/{{AKS_CLIENT_ID}}/$AKS_CLIENT_ID/g" \
        "$file" > "$temp_file"
}

deploy_manifests() {
    log_info "Déploiement des manifests Kubernetes..."
    
    local temp_dir=$(mktemp -d)
    
    # Traiter chaque fichier manifest
    for manifest in "$K8S_DIR"/*.yaml; do
        if [ -f "$manifest" ]; then
            local filename=$(basename "$manifest")
            local temp_file="$temp_dir/$filename"
            
            log_info "Traitement de $filename..."
            substitute_variables "$manifest" "$temp_file"
            
            # Appliquer le manifest
            if kubectl apply -f "$temp_file"; then
                log_success "✓ $filename appliqué"
            else
                log_error "✗ Échec de l'application de $filename"
                exit 1
            fi
        fi
    done
    
    # Nettoyer les fichiers temporaires
    rm -rf "$temp_dir"
    
    log_success "Tous les manifests ont été appliqués"
}

wait_for_deployment() {
    log_info "Attente du démarrage des déploiements..."
    
    local namespace="lake-holidays-${ENVIRONMENT}"
    
    # Attendre que les déploiements soient prêts
    kubectl wait --for=condition=available \
        --timeout=300s \
        deployment/backend \
        deployment/frontend \
        -n "$namespace"
    
    log_success "Tous les déploiements sont prêts"
}

show_status() {
    log_info "État du déploiement:"
    
    local namespace="lake-holidays-${ENVIRONMENT}"
    
    echo ""
    echo "=== PODS ==="
    kubectl get pods -n "$namespace" -o wide
    
    echo ""
    echo "=== SERVICES ==="
    kubectl get services -n "$namespace"
    
    echo ""
    echo "=== INGRESS ==="
    kubectl get ingress -n "$namespace"
    
    echo ""
    echo "=== HPA ==="
    kubectl get hpa -n "$namespace"
    
    echo ""
    log_info "Pour voir les logs du backend:"
    echo "  kubectl logs -l component=backend -n $namespace -f"
    
    log_info "Pour voir les logs du frontend:"
    echo "  kubectl logs -l component=frontend -n $namespace -f"
    
    log_info "Pour accéder à l'application:"
    echo "  Frontend: https://$FRONTEND_DOMAIN"
    echo "  Backend API: https://$BACKEND_DOMAIN"
}

# =============================================================================
# FONCTION PRINCIPALE
# =============================================================================

main() {
    log_info "🚀 Démarrage du déploiement Lake Holidays Challenge sur AKS"
    
    # Variables d'environnement (peuvent être surchargées)
    ENVIRONMENT="${1:-dev}"
    VERSION="${2:-latest}"
    
    log_info "Environnement: $ENVIRONMENT"
    log_info "Version: $VERSION"
    
    # Étapes de déploiement
    check_prerequisites
    get_terraform_outputs
    configure_kubectl
    deploy_manifests
    wait_for_deployment
    show_status
    
    log_success "🎉 Déploiement terminé avec succès!"
}

# =============================================================================
# GESTION DES ERREURS
# =============================================================================

cleanup() {
    if [ $? -ne 0 ]; then
        log_error "Le déploiement a échoué"
        log_info "Vérifiez les logs ci-dessus pour plus de détails"
    fi
}

trap cleanup EXIT

# =============================================================================
# EXÉCUTION
# =============================================================================

# Afficher l'aide si demandé
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    echo "Usage: $0 [ENVIRONMENT] [VERSION]"
    echo ""
    echo "ENVIRONMENT: dev, staging, prod (défaut: dev)"
    echo "VERSION: version des images Docker (défaut: latest)"
    echo ""
    echo "Exemples:"
    echo "  $0                    # Déploie en dev avec latest"
    echo "  $0 staging v1.2.3     # Déploie en staging avec la version v1.2.3"
    echo "  $0 prod v1.0.0        # Déploie en prod avec la version v1.0.0"
    exit 0
fi

# Exécuter le script principal
main "$@"
