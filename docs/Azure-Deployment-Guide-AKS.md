# Guide de Déploiement Azure - Lake Holidays Challenge (AKS)

Ce guide détaille le déploiement automatisé de l'application Lake Holidays Challenge sur Azure Kubernetes Service (AKS) avec Terraform et GitHub Actions.

## 🏗️ Architecture

### Infrastructure Azure
- **Azure Kubernetes Service (AKS)** : Cluster Kubernetes managé
- **Azure Container Registry (ACR)** : Registry privé pour les images Docker
- **Azure Key Vault** : Gestion sécurisée des secrets
- **Azure Storage Account** : Stockage des fichiers uploadés
- **Azure Monitor + Log Analytics** : Surveillance et logs
- **Azure OpenAI** (optionnel) : Services IA pour génération de contenu

### Applications
- **Backend** : FastAPI avec PostgreSQL et Redis intégrés
- **Frontend** : React + Vite avec Nginx
- **Base de données** : PostgreSQL (intégré au backend)
- **Cache** : Redis (intégré au backend)

## 🚀 Déploiement

### 1. Prérequis

```bash
# Outils requis
- Azure CLI 2.50+
- Terraform 1.5+
- kubectl 1.27+
- Docker 20.10+
- Git 2.30+

# Installation des outils
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
wget https://releases.hashicorp.com/terraform/1.5.7/terraform_1.5.7_linux_amd64.zip
unzip terraform_1.5.7_linux_amd64.zip && sudo mv terraform /usr/local/bin/
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl && sudo mv kubectl /usr/local/bin/
```

### 2. Configuration Azure

```bash
# Connexion à Azure
az login

# Créer un Service Principal pour Terraform et GitHub Actions
az ad sp create-for-rbac --name "lake-holidays-sp" \
  --role="Contributor" \
  --scopes="/subscriptions/YOUR_SUBSCRIPTION_ID" \
  --sdk-auth

# Résultat à ajouter dans GitHub Secrets (AZURE_CREDENTIALS)
```
Ou
```bash
# Créer une User Managed Identity

## Créer le groupe de ressources si nécessaire
az group create --name "lake-holidays-identity-rg" --location "France Central"

## Créer la User Managed Identity : lake-holidays-umi-gha
az identity create \
    --name "lake-holidays-umi-gha" \
    --resource-group "lake-holidays-identity-rg" \
    --location "France Central"

## Récupérer les informations importantes
az identity show \
    --name "lake-holidays-umi-gha" \
    --resource-group "lake-holidays-identity-rg" \
    --query '{clientId: clientId, principalId: principalId, id: id}'

## Assigner les permissions nécessaires
### Récupérer l'ID de l'abonnement
SUBSCRIPTION_ID=$(az account show --query id -o tsv)

### Récupérer le Principal ID de la Managed Identity
PRINCIPAL_ID=$(az identity show --name "lake-holidays-umi-gha" --resource-group "lake-holidays-identity-rg" --query principalId -o tsv)

### Assigner le rôle Contributor au niveau de l'abonnement 
az role assignment create \
    --assignee $PRINCIPAL_ID \
    --role "Contributor" \
    --scope "/subscriptions/$SUBSCRIPTION_ID"

## Configurer la Federated Identity pour GitHub - Cette étape permet à GitHub Actions d'utiliser la Managed Identity sans secret 
### Récupérer les informations de la Managed Identity
CLIENT_ID=$(az identity show --name "lake-holidays-umi-gha" --resource-group "lake-holidays-identity-rg" --query clientId -o tsv)
IDENTITY_ID=$(az identity show --name "lake-holidays-umi-gha" --resource-group "lake-holidays-identity-rg" --query id -o tsv)

### Créer la federated credential avec Azure CLI
az identity federated-credential create \
    --name "github-actions-credential" \
    --identity-name "lake-holidays-umi-gha" \
    --resource-group "lake-holidays-identity-rg" \
    --issuer "https://token.actions.githubusercontent.com" \
    --subject "repo:fr4is13r3/lake-holidays-challenges:ref:refs/heads/main" \
    --audience "api://AzureADTokenExchange"

# Pour autoriser toutes les branches (optionnel)
az identity federated-credential create \
    --name "github-actions-credential-all" \
    --identity-name "lake-holidays-umi-gha" \
    --resource-group "lake-holidays-identity-rg" \
    --issuer "https://token.actions.githubusercontent.com" \
    --subject "repo:fr4is13r3/lake-holidays-challenges:*" \
    --audience "api://AzureADTokenExchange"

```

### 3. Configuration des Variables

#### Variables Terraform (terraform.tfvars)
```hcl
# Variables obligatoires
app_name    = "lake-holidays"
environment = "dev"  # ou "staging", "prod"
location    = "France Central"

# Secrets d'application
jwt_secret_key         = "votre-jwt-secret-tres-long-et-securise"
google_client_secret   = "votre-google-oauth-secret"
microsoft_client_secret = "votre-microsoft-oauth-secret"
openai_api_key        = "votre-openai-api-key"

# Configuration AKS
kubernetes_version     = "1.27"
aks_node_count        = 2
aks_vm_size          = "Standard_D2s_v3"
aks_enable_auto_scaling = true
aks_min_count        = 1
aks_max_count        = 5

# Configuration des notifications
notification_email = "admin@votredomaine.com"

# Azure OpenAI (optionnel)
enable_azure_openai = true
openai_location    = "East US"  # Vérifier la disponibilité
```

#### Secrets GitHub
```bash
# Secrets requis dans GitHub Repository Settings > Secrets
#AZURE_CREDENTIALS             # JSON du Service Principal ##TOREMOVE
TENANT_ID                     # Identifiance de tenant Azure
SUBSCRIPTION_ID               # Identifiant de souscription
CLIENT_ID                     # Identifiant client de la managed identity
AZURE_CONTAINER_REGISTRY      # Nom du registry (sans .azurecr.io)
AKS_CLUSTER_NAME              # Nom du cluster AKS
AZURE_RESOURCE_GROUP          # Nom du resource group
KEY_VAULT_NAME                # Nom du Key Vault
STORAGE_ACCOUNT_NAME          # Nom du Storage Account
DOMAIN_SUFFIX                 # Suffixe de domaine (ex: example.com)
```

### 4. Déploiement de l'Infrastructure

```bash
# Cloner le repository
git clone https://github.com/votre-organisation/lake-holidays-challenge.git
cd lake-holidays-challenge

# Initialiser Terraform
cd terraform
terraform init

# Configurer le backend remote (recommandé pour la production)
# Créer un Storage Account Azure pour l'état Terraform
az group create --name "terraform-state-rg" --location "France Central"
az storage account create \
  --name "lakeholidaysterraformstate" \
  --resource-group "terraform-state-rg" \
  --location "France Central" \
  --sku "Standard_LRS"

# Configurer terraform/backend.tf
cat > backend.tf << EOF
terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-state-rg"
    storage_account_name = "lakeholidaysterraformstate"
    container_name       = "tfstate"
    key                  = "lake-holidays.terraform.tfstate"
  }
}
EOF

# Planifier et appliquer
terraform plan -var-file="terraform.tfvars"
terraform apply -var-file="terraform.tfvars"
```

### 5. Configuration Kubernetes

```bash
# Récupérer les credentials AKS
az aks get-credentials \
  --resource-group $(terraform output -raw resource_group_name) \
  --name $(terraform output -raw aks_cluster_name)

# Vérifier la connexion
kubectl cluster-info

# Installer les add-ons requis (si pas déjà installés par Terraform)
# Secret Store CSI Driver
helm repo add secrets-store-csi-driver https://kubernetes-sigs.github.io/secrets-store-csi-driver/charts
helm install csi-secrets-store secrets-store-csi-driver/secrets-store-csi-driver \
  --namespace kube-system \
  --set syncSecret.enabled=true

# Azure Key Vault Provider
kubectl apply -f https://raw.githubusercontent.com/Azure/secrets-store-csi-driver-provider-azure/master/deployment/provider-azure-installer.yaml
```

### 6. Déploiement des Applications

#### Option A: Via GitHub Actions (Recommandé)
```bash
# Pousser le code vers GitHub
git add .
git commit -m "Initial deployment setup"
git push origin main

# Le pipeline GitHub Actions va automatiquement :
# 1. Exécuter les tests
# 2. Construire les images Docker
# 3. Les pousser vers ACR
# 4. Déployer sur AKS
```

#### Option B: Déploiement Manuel
```bash
# Utiliser le script de déploiement
./scripts/deploy-k8s.sh dev latest

# Ou déployer étape par étape
cd k8s
for manifest in *.yaml; do
  envsubst < "$manifest" | kubectl apply -f -
done

# Vérifier le déploiement
kubectl get pods -n lake-holidays-dev
kubectl get services -n lake-holidays-dev
kubectl get ingress -n lake-holidays-dev
```

## 🔧 Configuration Post-Déploiement

### 1. Configuration DNS

```bash
# Récupérer l'IP publique de l'Application Gateway
kubectl get ingress lake-holidays-ingress -n lake-holidays-dev

# Configurer vos enregistrements DNS :
# frontend-dev.votredomaine.com -> IP_PUBLIQUE
# api-dev.votredomaine.com -> IP_PUBLIQUE
```

### 2. Configuration SSL/TLS

```bash
# Option A: Let's Encrypt avec cert-manager
helm repo add jetstack https://charts.jetstack.io
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --set installCRDs=true

# Option B: Certificat personnalisé via Key Vault
kubectl create secret tls lake-holidays-tls \
  --cert=path/to/tls.crt \
  --key=path/to/tls.key \
  -n lake-holidays-dev
```

### 3. Configuration des Secrets

```bash
# Les secrets sont automatiquement synchronisés depuis Key Vault
# Vérifier la synchronisation
kubectl get secrets -n lake-holidays-dev
kubectl describe secretproviderclass lake-holidays-secrets -n lake-holidays-dev
```

## 📊 Surveillance et Monitoring

### 1. Accès aux Logs

```bash
# Logs du backend
kubectl logs -l component=backend -n lake-holidays-dev -f

# Logs du frontend
kubectl logs -l component=frontend -n lake-holidays-dev -f

# Logs de tous les pods
kubectl logs -l app=lake-holidays -n lake-holidays-dev -f
```

### 2. Métriques et Dashboards

```bash
# Azure Portal > Votre Resource Group > AKS Cluster > Insights
# Ou directement : https://portal.azure.com

# Dashboard Kubernetes
kubectl proxy
# Puis : http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/
```

### 3. Health Checks

```bash
# Vérifier la santé des applications
kubectl get pods -n lake-holidays-dev
kubectl describe pod <pod-name> -n lake-holidays-dev

# Tester les endpoints de santé
kubectl port-forward deployment/backend 8000:8000 -n lake-holidays-dev
curl http://localhost:8000/health
```

## 🔧 Maintenance et Mises à Jour

### 1. Mise à Jour de l'Infrastructure

```bash
# Modifier terraform/terraform.tfvars
# Puis appliquer les changements
cd terraform
terraform plan -var-file="terraform.tfvars"
terraform apply -var-file="terraform.tfvars"
```

### 2. Mise à Jour des Applications

```bash
# Via GitHub Actions (automatique sur push vers main/develop)
git push origin main

# Ou manuellement
./scripts/deploy-k8s.sh prod v1.2.3
```

### 3. Scaling

```bash
# Scaling manuel
kubectl scale deployment backend --replicas=5 -n lake-holidays-dev

# L'auto-scaling est configuré via HPA (Horizontal Pod Autoscaler)
kubectl get hpa -n lake-holidays-dev
```

## 🛠️ Dépannage

### 1. Problèmes Courants

```bash
# Pods en état Pending
kubectl describe pod <pod-name> -n lake-holidays-dev
# Vérifier les ressources et les contraintes de placement

# Problèmes de réseau
kubectl exec -it <pod-name> -n lake-holidays-dev -- nslookup kubernetes.default

# Problèmes de secrets
kubectl get secretproviderclass -n lake-holidays-dev
kubectl describe secretproviderclass lake-holidays-secrets -n lake-holidays-dev
```

### 2. Logs de Debug

```bash
# Activer le mode debug
kubectl set env deployment/backend LOG_LEVEL=DEBUG -n lake-holidays-dev

# Redémarrer les pods
kubectl rollout restart deployment/backend -n lake-holidays-dev
```

### 3. Rollback

```bash
# Rollback vers la version précédente
kubectl rollout undo deployment/backend -n lake-holidays-dev
kubectl rollout undo deployment/frontend -n lake-holidays-dev

# Vérifier l'historique
kubectl rollout history deployment/backend -n lake-holidays-dev
```

## 🔒 Sécurité

### 1. Gestion des Secrets
- ✅ Key Vault pour tous les secrets sensibles
- ✅ CSI Secret Store Driver pour la synchronisation
- ✅ Rotation automatique des secrets
- ✅ Chiffrement au repos et en transit

### 2. Network Policies
- ✅ Isolation réseau entre les namespaces
- ✅ Restriction des communications inter-pods
- ✅ Contrôle d'accès basé sur les labels

### 3. RBAC
- ✅ Service Accounts dédiés
- ✅ Permissions minimales requises
- ✅ Azure AD intégration

## 📈 Performance

### 1. Optimisations
- ✅ HPA pour l'auto-scaling
- ✅ Resource requests et limits
- ✅ PDB pour la haute disponibilité
- ✅ Cache Redis intégré

### 2. Monitoring
- ✅ Azure Monitor intégration
- ✅ Prometheus metrics endpoints
- ✅ Application Insights pour le backend
- ✅ Alertes automatiques

## 🌍 Multi-Environnements

```bash
# Déploiement par environnement
./scripts/deploy-k8s.sh dev latest      # Développement
./scripts/deploy-k8s.sh staging v1.2.3  # Staging
./scripts/deploy-k8s.sh prod v1.2.3     # Production

# Chaque environnement a son propre namespace et sa configuration
```

---

## 📞 Support

En cas de problème :
1. Vérifier les logs via `kubectl logs`
2. Consulter Azure Monitor et Application Insights
3. Vérifier la documentation Kubernetes
4. Contacter l'équipe DevOps

## 🔗 Liens Utiles

- [Documentation AKS](https://docs.microsoft.com/en-us/azure/aks/)
- [Terraform Azure Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Azure Container Registry](https://docs.microsoft.com/en-us/azure/container-registry/)
- [Azure Key Vault](https://docs.microsoft.com/en-us/azure/key-vault/)
