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
    
    # Récupérer l'identity client ID pour Workload Identity (kubelet identity)
    AKS_KUBELET_IDENTITY_CLIENT_ID=$(az aks show --resource-group "$RESOURCE_GROUP" --name "$AKS_CLUSTER_NAME" --query identityProfile.kubeletidentity.clientId -o tsv)
    
    # Log pour debug
    log_info "AKS Kubelet Identity Client ID: $AKS_KUBELET_IDENTITY_CLIENT_ID"
    
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
        -e "s/{{AKS_KUBELET_IDENTITY_CLIENT_ID}}/$AKS_KUBELET_IDENTITY_CLIENT_ID/g" \
        "$file" > "$temp_file"
}

deploy_manifests() {
    log_info "Déploiement des manifests Kubernetes dans l'ordre correct..."
    
    local temp_dir=$(mktemp -d)
    local namespace="lake-holidays-${ENVIRONMENT}"
    
    # Créer le namespace s'il n'existe pas
    kubectl create namespace "$namespace" --dry-run=client -o yaml | kubectl apply -f -
    
    # Fonction helper pour appliquer un manifest
    apply_manifest() {
        local manifest_name="$1"
        local manifest_file="$K8S_DIR/$manifest_name"
        
        if [ ! -f "$manifest_file" ]; then
            log_warning "Manifest $manifest_name non trouvé, ignoré"
            return 0
        fi
        
        local temp_file="$temp_dir/$manifest_name"
        log_info "📦 Déploiement de $manifest_name..."
        
        substitute_variables "$manifest_file" "$temp_file"
        
        if kubectl apply -f "$temp_file"; then
            log_success "✓ $manifest_name appliqué"
        else
            log_error "✗ Échec de l'application de $manifest_name"
            exit 1
        fi
    }
    
    # 1. Configuration et namespace
    log_info "🔧 Étape 1: Configuration et namespace"
    apply_manifest "00-namespace-config.yaml"
    
    # 2. Storage
    log_info "💾 Étape 2: Storage (PVC)"
    apply_manifest "02-storage.yaml"
    
    # 3. Key Vault secrets
    log_info "🔐 Étape 3: Key Vault secrets"
    apply_manifest "06-key-vault-secrets.yaml"
    
    # 4. Services de base de données (PostgreSQL et Redis)
    log_info "🗄️ Étape 4: Services de base de données"
    apply_manifest "07-postgres-deployment.yaml"
    apply_manifest "08-redis-deployment.yaml"
    
    # Attendre que les bases de données soient prêtes
    log_info "⏳ Attente que les services de base de données soient prêts..."
    kubectl wait --for=condition=available deployment/postgres -n "$namespace" --timeout=300s || {
        log_error "PostgreSQL n'est pas devenu disponible"
        kubectl get pods -n "$namespace" -l component=postgres
        kubectl logs -l component=postgres -n "$namespace" --tail=20
        exit 1
    }
    
    kubectl wait --for=condition=available deployment/redis -n "$namespace" --timeout=300s || {
        log_error "Redis n'est pas devenu disponible"
        kubectl get pods -n "$namespace" -l component=redis
        kubectl logs -l component=redis -n "$namespace" --tail=20
        exit 1
    }
    
    log_success "✓ Services de base de données prêts"
    
    # 5. Migrations de base de données
    log_info "🔄 Étape 5: Migrations de base de données"
    apply_manifest "09-alembic-migrations.yaml"
    
    # Attendre que les migrations se terminent
    log_info "⏳ Attente de la fin des migrations..."
    kubectl wait --for=condition=complete job/alembic-migrations-$VERSION -n "$namespace" --timeout=300s || {
        log_error "Les migrations n'ont pas réussi"
        kubectl describe job/alembic-migrations-$VERSION -n "$namespace"
        kubectl logs job/alembic-migrations-$VERSION -n "$namespace" --tail=50
        exit 1
    }
    
    log_success "✓ Migrations terminées"
    
    # 6. Application backend
    log_info "🚀 Étape 6: Application backend"
    apply_manifest "01-backend-deployment.yaml"
    
    # 7. Application frontend
    log_info "🎨 Étape 7: Application frontend"
    apply_manifest "03-frontend-deployment.yaml"
    
    # 8. Ingress et networking
    log_info "🌐 Étape 8: Ingress et networking"
    apply_manifest "04-ingress.yaml"
    
    # 9. Autoscaling
    log_info "📈 Étape 9: Autoscaling"
    apply_manifest "05-autoscaling.yaml"
    
    # Nettoyer les fichiers temporaires
    rm -rf "$temp_dir"
    
    log_success "Tous les manifests ont été appliqués dans l'ordre correct"
}

wait_for_deployment() {
    log_info "Attente du démarrage final de tous les déploiements..."
    
    local namespace="lake-holidays-${ENVIRONMENT}"
    
    # Attendre que tous les déploiements soient prêts
    log_info "⏳ Attente finale du backend..."
    kubectl wait --for=condition=available \
        --timeout=600s \
        deployment/backend \
        -n "$namespace" || {
        log_error "Backend n'est pas devenu disponible"
        kubectl get pods -n "$namespace" -l component=backend
        kubectl logs -l component=backend -n "$namespace" --tail=50
        exit 1
    }
    
    log_info "⏳ Attente finale du frontend..."
    kubectl wait --for=condition=available \
        --timeout=300s \
        deployment/frontend \
        -n "$namespace" || {
        log_error "Frontend n'est pas devenu disponible"
        kubectl get pods -n "$namespace" -l component=frontend
        kubectl logs -l component=frontend -n "$namespace" --tail=20
        exit 1
    }
    
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
    echo "=== SECRETS ==="
    kubectl get secrets -n "$namespace"
    
    echo ""
    echo "=== JOBS (MIGRATIONS) ==="
    kubectl get jobs -n "$namespace"
    
    echo ""
    echo "=== PVC ==="
    kubectl get pvc -n "$namespace"
    
    echo ""
    log_info "Commandes utiles pour le debug:"
    echo "  kubectl logs -l component=postgres -n $namespace -f"
    echo "  kubectl logs -l component=redis -n $namespace -f"
    echo "  kubectl logs -l component=backend -n $namespace -f"
    echo "  kubectl logs -l component=frontend -n $namespace -f"
    echo "  kubectl logs job/alembic-migrations-$VERSION -n $namespace"
    
    log_info "Pour accéder à l'application:"
    echo "  Frontend: https://$FRONTEND_DOMAIN"
    echo "  Backend API: https://$BACKEND_DOMAIN"
    
    # Vérification rapide de l'état des services
    echo ""
    log_info "🔍 Vérification rapide des services:"
    
    # PostgreSQL
    if kubectl get pod -l component=postgres -n "$namespace" &>/dev/null; then
        postgres_status=$(kubectl get pods -l component=postgres -n "$namespace" -o jsonpath='{.items[0].status.phase}' 2>/dev/null || echo "Unknown")
        if [ "$postgres_status" == "Running" ]; then
            log_success "✓ PostgreSQL: Running"
        else
            log_warning "⚠ PostgreSQL: $postgres_status"
        fi
    else
        log_error "✗ PostgreSQL: Not found"
    fi
    
    # Redis
    if kubectl get pod -l component=redis -n "$namespace" &>/dev/null; then
        redis_status=$(kubectl get pods -l component=redis -n "$namespace" -o jsonpath='{.items[0].status.phase}' 2>/dev/null || echo "Unknown")
        if [ "$redis_status" == "Running" ]; then
            log_success "✓ Redis: Running"
        else
            log_warning "⚠ Redis: $redis_status"
        fi
    else
        log_error "✗ Redis: Not found"
    fi
    
    # Backend
    if kubectl get pod -l component=backend -n "$namespace" &>/dev/null; then
        backend_status=$(kubectl get pods -l component=backend -n "$namespace" -o jsonpath='{.items[0].status.phase}' 2>/dev/null || echo "Unknown")
        backend_ready=$(kubectl get pods -l component=backend -n "$namespace" -o jsonpath='{.items[0].status.conditions[?(@.type=="Ready")].status}' 2>/dev/null || echo "Unknown")
        if [ "$backend_status" == "Running" ] && [ "$backend_ready" == "True" ]; then
            log_success "✓ Backend: Running and Ready"
        else
            log_warning "⚠ Backend: $backend_status (Ready: $backend_ready)"
        fi
    else
        log_error "✗ Backend: Not found"
    fi
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
