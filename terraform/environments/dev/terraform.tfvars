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
aks_node_count           = 1
aks_vm_size             = "Standard_B4as_v2"  # 2 vCPU, 8GB RAM
aks_enable_auto_scaling = false
aks_min_count           = 1
aks_max_count           = 1

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
    name           = "gpt-4o-mini"
    model_name     = "gpt-4o-mini"
    model_version  = "2024-07-18"
    scale_type     = "Standard"
    capacity       = 30
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
  AutoShutdown   = "true"
  BackupPolicy    = "Daily"
  MonitoringLevel = "Full"
  Project         = "lake-holidays-challenge"
  Terraform       = "true"
  Architecture    = "AKS"
  DataStorage     = "Integrated"  # PostgreSQL/Redis intégrés
}

# =============================================================================
# CONFIGURATION AVANCÉE (optionnelle)
# =============================================================================

# Domaine personnalisé (optionnel en dev)
domain_name = ""  # Laissé vide, utilisera les domaines Azure par défaut
