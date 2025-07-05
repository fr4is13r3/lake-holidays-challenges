# Configuration Terraform pour l'environnement de production - AKS
# Lake Holidays Challenge - Architecture Kubernetes

# =============================================================================
# CONFIGURATION GÉNÉRALE
# =============================================================================
app_name    = "lake-holidays"
environment = "prod"
location    = "France Central"

# =============================================================================
# CONFIGURATION AKS (Azure Kubernetes Service) - PRODUCTION
# =============================================================================
kubernetes_version       = "1.33"  # Version supportée
aks_node_count           = 1
aks_vm_size             = "Standard_B2s"  # 2 vCPU, 4GB RAM - Économique
aks_enable_auto_scaling = false  # Un seul node fixe
aks_min_count           = 1
aks_max_count           = 1

# =============================================================================
# CONFIGURATION STORAGE (haute disponibilité)
# =============================================================================
storage_account_tier     = "Standard"
storage_replication_type = "LRS"  # Geo-Redundant Storage pour production

# =============================================================================
# CONFIGURATION AZURE AI FOUNDRY (activé en production)
# =============================================================================
enable_azure_openai = true
openai_location     = "East US"  # Région avec AI Foundry/OpenAI disponible
openai_sku_name     = "S0"

# Modèles AI Foundry pour production - GPT-4o-mini optimisé
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
# MONITORING ET ALERTES (complet en production)
# =============================================================================
notification_email = "erwan.lancien@gmail.com"  # À CONFIGURER

# =============================================================================
# SECRETS D'APPLICATION (à configurer via variables d'environnement sécurisées)
# =============================================================================
# IMPORTANT: Ces valeurs NE DOIVENT PAS être mises dans ce fichier en production
# Utilisez plutôt:
# - Variables d'environnement TF_VAR_* dans votre pipeline CI/CD
# - GitHub Secrets pour GitHub Actions
# - Azure Key Vault references
# - Fichier terraform.tfvars.local (non versionné, chiffré au repos)

# jwt_secret_key         = "voir-azure-key-vault-ou-github-secrets"
# google_client_secret   = "voir-azure-key-vault-ou-github-secrets"
# microsoft_client_secret = "voir-azure-key-vault-ou-github-secrets"
# openai_api_key        = "voir-azure-key-vault-ou-github-secrets"

# =============================================================================
# CONFIGURATION AVANCÉE PRODUCTION
# =============================================================================

# Domaine personnalisé pour production (à configurer)
domain_name = ""  # ex: "lakeholidays.com" - nécessite configuration DNS

# =============================================================================
# TAGS SPÉCIFIQUES À L'ENVIRONNEMENT DE PRODUCTION
# =============================================================================
# Reduced to 8 tags to stay under Azure's 15-tag limit (considering common_tags adds 5 more)
tags = {
  Environment      = "Production"
  BackupPolicy    = "Daily"
  MonitoringLevel = "Full"
  Project         = "lake-holidays-challenge"
  Terraform       = "true"
  Architecture    = "AKS"
  DataStorage     = "Integrated"  # PostgreSQL/Redis intégrés
  AIService       = "AI-Foundry"  # Azure AI Foundry activé
}
