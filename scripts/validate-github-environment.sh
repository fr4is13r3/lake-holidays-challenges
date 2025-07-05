#!/bin/bash

# Script de validation de l'environnement GitHub Enterprise
# Ce script vérifie que toutes les variables et secrets nécessaires sont configurés

set -e

ENVIRONMENT=${1:-"prod"}
echo "🔍 Validation de l'environnement: $ENVIRONMENT"

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonction pour afficher les résultats
check_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
        return 1
    fi
}

warn_result() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

echo ""
echo "📋 Vérification des prérequis Azure..."

# Vérifier Azure CLI
if command -v az &> /dev/null; then
    check_result 0 "Azure CLI installé"
    
    # Vérifier la connexion Azure
    if az account show &> /dev/null; then
        check_result 0 "Connecté à Azure"
        SUBSCRIPTION_ID=$(az account show --query id -o tsv)
        echo "   📌 Subscription: $SUBSCRIPTION_ID"
    else
        check_result 1 "Non connecté à Azure"
        echo "   💡 Exécutez: az login"
    fi
else
    check_result 1 "Azure CLI non installé"
fi

echo ""
echo "🔧 Vérification des ressources Azure..."

# Variables basées sur l'environnement
if [ "$ENVIRONMENT" == "prod" ]; then
    RESOURCE_GROUP="lake-holidays-prod-rg"
    AKS_CLUSTER="lake-holidays-prod-aks"
    ACR_NAME="lakeprodacr2h7yde"
    KEY_VAULT="lake-prod-kv-1xnf"
    STORAGE_ACCOUNT="lakeholidaysprodstorage"
else
    warn_result "Configuration pour l'environnement '$ENVIRONMENT' non définie dans ce script"
    exit 1
fi

# Vérifier le groupe de ressources
if az group show --name "$RESOURCE_GROUP" &> /dev/null; then
    check_result 0 "Groupe de ressources: $RESOURCE_GROUP"
else
    check_result 1 "Groupe de ressources non trouvé: $RESOURCE_GROUP"
fi

# Vérifier le cluster AKS
if az aks show --name "$AKS_CLUSTER" --resource-group "$RESOURCE_GROUP" &> /dev/null; then
    check_result 0 "Cluster AKS: $AKS_CLUSTER"
    
    # Vérifier la connectivité kubectl
    if az aks get-credentials --name "$AKS_CLUSTER" --resource-group "$RESOURCE_GROUP" --overwrite-existing &> /dev/null; then
        if command -v kubectl &> /dev/null; then
            if kubectl cluster-info &> /dev/null; then
                check_result 0 "Connectivité kubectl vers AKS"
            else
                check_result 1 "Échec de connexion kubectl"
            fi
        else
            warn_result "kubectl non installé - impossible de vérifier la connectivité"
        fi
    fi
else
    check_result 1 "Cluster AKS non trouvé: $AKS_CLUSTER"
fi

# Vérifier Azure Container Registry
if az acr show --name "$ACR_NAME" &> /dev/null; then
    check_result 0 "Azure Container Registry: $ACR_NAME"
else
    check_result 1 "ACR non trouvé: $ACR_NAME"
fi

# Vérifier Key Vault
if az keyvault show --name "$KEY_VAULT" &> /dev/null; then
    check_result 0 "Azure Key Vault: $KEY_VAULT"
else
    check_result 1 "Key Vault non trouvé: $KEY_VAULT"
fi

# Vérifier Storage Account
if az storage account show --name "$STORAGE_ACCOUNT" --resource-group "$RESOURCE_GROUP" &> /dev/null; then
    check_result 0 "Storage Account: $STORAGE_ACCOUNT"
else
    check_result 1 "Storage Account non trouvé: $STORAGE_ACCOUNT"
fi

echo ""
echo "🌐 Vérification des domaines..."

FRONTEND_DOMAIN="frontend-${ENVIRONMENT}.francecentral.cloudapp.azure.com"
BACKEND_DOMAIN="api-${ENVIRONMENT}.francecentral.cloudapp.azure.com"

# Test de résolution DNS (optionnel)
if command -v nslookup &> /dev/null; then
    if nslookup "$FRONTEND_DOMAIN" &> /dev/null; then
        check_result 0 "Résolution DNS: $FRONTEND_DOMAIN"
    else
        warn_result "Résolution DNS échouée: $FRONTEND_DOMAIN (normal si pas encore déployé)"
    fi
    
    if nslookup "$BACKEND_DOMAIN" &> /dev/null; then
        check_result 0 "Résolution DNS: $BACKEND_DOMAIN"
    else
        warn_result "Résolution DNS échouée: $BACKEND_DOMAIN (normal si pas encore déployé)"
    fi
else
    warn_result "nslookup non disponible - impossible de vérifier les domaines"
fi

echo ""
echo "📁 Vérification des fichiers de configuration..."

# Vérifier les manifests Kubernetes
K8S_DIR="k8s"
if [ -d "$K8S_DIR" ]; then
    check_result 0 "Répertoire k8s trouvé"
    
    REQUIRED_MANIFESTS=(
        "00-namespace-config.yaml"
        "01-backend-deployment.yaml"
        "02-storage.yaml"
        "03-frontend-deployment.yaml"
        "04-ingress.yaml"
    )
    
    for manifest in "${REQUIRED_MANIFESTS[@]}"; do
        if [ -f "$K8S_DIR/$manifest" ]; then
            check_result 0 "Manifest K8s: $manifest"
        else
            check_result 1 "Manifest K8s manquant: $manifest"
        fi
    done
else
    check_result 1 "Répertoire k8s non trouvé"
fi

# Vérifier le workflow GitHub
if [ -f ".github/workflows/ci-cd-aks.yml" ]; then
    check_result 0 "Workflow GitHub Actions trouvé"
else
    check_result 1 "Workflow GitHub Actions manquant"
fi

echo ""
echo "📊 Résumé de la validation"
echo "Environment: $ENVIRONMENT"
echo "Resource Group: $RESOURCE_GROUP"
echo "AKS Cluster: $AKS_CLUSTER"
echo "Frontend URL: https://$FRONTEND_DOMAIN"
echo "Backend URL: https://$BACKEND_DOMAIN"

echo ""
echo "💡 Prochaines étapes:"
echo "1. Configurez l'environnement '$ENVIRONMENT' dans GitHub Enterprise"
echo "2. Ajoutez les variables d'environnement dans GitHub"
echo "3. Vérifiez les secrets Azure dans GitHub"
echo "4. Déployez via un push sur la branche main"

echo ""
echo "✅ Validation terminée!"
