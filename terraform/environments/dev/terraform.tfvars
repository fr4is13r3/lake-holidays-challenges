# Configuration Terraform pour l'environnement de développement - AKS
# Lake Holidays Challenge - Architecture Kubernetes

# =============================================================================
# CONFIGURATION GÉNÉRALE
# =============================================================================
app_name    = "lake-holidays"
environment = "dev"
location    = "France Central"

# =============================================================================
# CONFIGURATION AKS (Azure Kubernetes Service)
# =============================================================================
kubernetes_version       = "1.28"
aks_node_count           = 2
aks_vm_size             = "Standard_D2s_v3"  # 2 vCPU, 8GB RAM
aks_enable_auto_scaling = true
aks_min_count           = 1
aks_max_count           = 3

# =============================================================================
# CONFIGURATION STORAGE (fichiers uploadés)
# =============================================================================
storage_account_tier     = "Standard"
storage_replication_type = "LRS"  # Local Redundant Storage pour dev

# =============================================================================
# CONFIGURATION AZURE OPENAI (désactivé en dev pour économiser)
# =============================================================================
enable_azure_openai = false
openai_location     = "East US"  # Région avec OpenAI disponible
openai_sku_name     = "S0"

# Modèles de base pour dev (si activé)
openai_model_deployments = [
  {
    name           = "gpt-35-turbo"
    model_name     = "gpt-35-turbo"
    model_version  = "0613"
    scale_type     = "Standard"
    scale_capacity = 10
  }
]

# =============================================================================
# MONITORING ET ALERTES
# =============================================================================
notification_email = ""  # Optionnel en dev

# =============================================================================
# SECRETS D'APPLICATION (à configurer via variables d'environnement ou CI/CD)
# =============================================================================
# Ces valeurs doivent être définies via:
# - Variables d'environnement TF_VAR_*
# - GitHub Secrets
# - Azure Key Vault
# - Fichier terraform.tfvars.local (non versionné)

# jwt_secret_key         = "votre-jwt-secret-dev"
# google_client_secret   = "votre-google-oauth-secret-dev"
# microsoft_client_secret = "votre-microsoft-oauth-secret-dev"
# openai_api_key        = "votre-openai-api-key-dev"

# =============================================================================
# TAGS SPÉCIFIQUES À L'ENVIRONNEMENT DE DÉVELOPPEMENT
# =============================================================================
tags = {
  Environment     = "Development"
  CostCenter      = "Development"
  Owner          = "DevTeam"
  AutoShutdown   = "true"
  Project        = "lake-holidays-challenge"
  Terraform      = "true"
  Architecture   = "AKS"
  DataStorage    = "Integrated"  # PostgreSQL/Redis intégrés
}

# =============================================================================
# CONFIGURATION AVANCÉE (optionnelle)
# =============================================================================

# Domaine personnalisé (optionnel en dev)
domain_name = ""  # Laissé vide, utilisera les domaines Azure par défaut
