# Variables pour l'infrastructure Lake Holidays Challenge

# =============================================================================
# VARIABLES GÉNÉRALES
# =============================================================================

variable "app_name" {
  description = "Nom de l'application"
  type        = string
  default     = "lake-holidays"
  
  validation {
    condition     = length(var.app_name) <= 20 && can(regex("^[a-z][a-z0-9-]*[a-z0-9]$", var.app_name))
    error_message = "Le nom de l'application doit contenir uniquement des lettres minuscules, des chiffres et des tirets, et ne pas dépasser 20 caractères."
  }
}

variable "environment" {
  description = "Environnement de déploiement"
  type        = string
  
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "L'environnement doit être dev, staging ou prod."
  }
}

variable "location" {
  description = "Région Azure pour les ressources"
  type        = string
  default     = "France Central"
}

variable "tags" {
  description = "Tags supplémentaires à appliquer aux ressources"
  type        = map(string)
  default     = {}
}

variable "domain_name" {
  description = "Nom de domaine personnalisé (optionnel)"
  type        = string
  default     = ""
}

# =============================================================================
# VARIABLES DATABASE
# =============================================================================

variable "postgresql_version" {
  description = "Version PostgreSQL"
  type        = string
  default     = "15"
}

variable "database_sku_name" {
  description = "SKU de la base de données PostgreSQL"
  type        = string
  default     = "GP_Standard_D2s_v3"  # 2 vCores, 8GB RAM pour production
  
  validation {
    condition = contains([
      "B_Standard_B1ms",  # Burstable - dev/test
      "B_Standard_B2s",   # Burstable - dev/test  
      "GP_Standard_D2s_v3", # General Purpose - prod
      "GP_Standard_D4s_v3", # General Purpose - prod
      "MO_Standard_E4s_v3"  # Memory Optimized - prod
    ], var.database_sku_name)
    error_message = "SKU de base de données non supporté."
  }
}

variable "database_storage_mb" {
  description = "Stockage de la base de données en MB"
  type        = number
  default     = 32768  # 32GB
  
  validation {
    condition     = var.database_storage_mb >= 32768 && var.database_storage_mb <= 16777216
    error_message = "Le stockage doit être entre 32GB et 16TB."
  }
}

variable "database_backup_retention_days" {
  description = "Rétention des sauvegardes en jours"
  type        = number
  default     = 7
  
  validation {
    condition     = var.database_backup_retention_days >= 7 && var.database_backup_retention_days <= 35
    error_message = "La rétention doit être entre 7 et 35 jours."
  }
}

# =============================================================================
# VARIABLES REDIS
# =============================================================================

variable "redis_capacity" {
  description = "Capacité du cache Redis"
  type        = number
  default     = 1
}

variable "redis_family" {
  description = "Famille Redis (C = Basic/Standard, P = Premium)"
  type        = string
  default     = "C"
  
  validation {
    condition     = contains(["C", "P"], var.redis_family)
    error_message = "La famille Redis doit être C ou P."
  }
}

variable "redis_sku_name" {
  description = "SKU Redis"
  type        = string
  default     = "Standard"
  
  validation {
    condition     = contains(["Basic", "Standard", "Premium"], var.redis_sku_name)
    error_message = "Le SKU Redis doit être Basic, Standard ou Premium."
  }
}

variable "redis_version" {
  description = "Version Redis"
  type        = string
  default     = "6"
}

# =============================================================================
# VARIABLES STORAGE
# =============================================================================

variable "storage_account_tier" {
  description = "Tier du compte de stockage"
  type        = string
  default     = "Standard"
  
  validation {
    condition     = contains(["Standard", "Premium"], var.storage_account_tier)
    error_message = "Le tier de stockage doit être Standard ou Premium."
  }
}

variable "storage_replication_type" {
  description = "Type de réplication du stockage"
  type        = string
  default     = "LRS"
  
  validation {
    condition     = contains(["LRS", "GRS", "RAGRS", "ZRS", "GZRS", "RAGZRS"], var.storage_replication_type)
    error_message = "Type de réplication non supporté."
  }
}

# =============================================================================
# VARIABLES AZURE AI FOUNDRY (remplace Azure OpenAI classique)
# =============================================================================

variable "enable_azure_openai" {
  description = "Activer Azure AI Foundry (anciennement Azure OpenAI)"
  type        = bool
  default     = true
}

variable "openai_location" {
  description = "Région spécifique pour Azure AI Foundry (si différente de location principale)"
  type        = string
  default     = ""
  
  validation {
    condition = var.openai_location == "" || can(regex("^(East US|East US 2|West US|West US 2|North Central US|South Central US|West Europe|North Europe|UK South|Sweden Central)$", var.openai_location))
    error_message = "La région doit supporter Azure AI Foundry. Utilisez: East US, East US 2, West US, West US 2, North Central US, South Central US, West Europe, North Europe, UK South, ou Sweden Central."
  }
}

variable "openai_sku_name" {
  description = "SKU Azure AI Foundry (S0 = Standard, F0 = Gratuit avec limitations)"
  type        = string
  default     = "S0"
  
  validation {
    condition     = contains(["F0", "S0"], var.openai_sku_name)
    error_message = "Le SKU doit être F0 (gratuit, limité) ou S0 (standard, recommandé)."
  }
}

variable "openai_model_deployments" {
  description = "Modèles IA à déployer sur Azure AI Foundry"
  type = list(object({
    name           = string
    model_name     = string
    model_version  = string
    scale_type     = string
    capacity       = number
  }))
  default = [
    {
      name          = "gpt-4o-mini"
      model_name    = "gpt-4o-mini"
      model_version = "2024-07-18"
      scale_type    = "Standard"
      capacity      = 30
    }
  ]
  
  validation {
    condition     = length(var.openai_model_deployments) > 0
    error_message = "Au moins un modèle doit être configuré."
  }
}

# =============================================================================
# VARIABLES CONTAINER APPS - BACKEND
# =============================================================================

variable "backend_cpu_requests" {
  description = "Ressources CPU pour le backend (en millicores)"
  type        = string
  default     = "0.5"
}

variable "backend_memory_requests" {
  description = "Ressources mémoire pour le backend"
  type        = string
  default     = "1Gi"
}

variable "backend_min_replicas" {
  description = "Nombre minimum de réplicas backend"
  type        = number
  default     = 1
}

variable "backend_max_replicas" {
  description = "Nombre maximum de réplicas backend"
  type        = number
  default     = 10
}

# =============================================================================
# VARIABLES CONTAINER APPS - FRONTEND
# =============================================================================

variable "frontend_cpu_requests" {
  description = "Ressources CPU pour le frontend (en millicores)"
  type        = string
  default     = "0.25"
}

variable "frontend_memory_requests" {
  description = "Ressources mémoire pour le frontend"
  type        = string
  default     = "0.5Gi"
}

variable "frontend_min_replicas" {
  description = "Nombre minimum de réplicas frontend"
  type        = number
  default     = 1
}

variable "frontend_max_replicas" {
  description = "Nombre maximum de réplicas frontend"
  type        = number
  default     = 10
}

# =============================================================================
# VARIABLES APPLICATION GATEWAY
# =============================================================================

variable "enable_application_gateway" {
  description = "Activer Application Gateway (Load Balancer + WAF)"
  type        = bool
  default     = false  # Désactivé par défaut pour économiser les coûts
}

variable "enable_ssl" {
  description = "Activer SSL/HTTPS"
  type        = bool
  default     = true
}

variable "ssl_certificate_data" {
  description = "Données du certificat SSL (format base64)"
  type        = string
  default     = ""
  sensitive   = true
}

variable "ssl_certificate_password" {
  description = "Mot de passe du certificat SSL"
  type        = string
  default     = ""
  sensitive   = true
}

# =============================================================================
# VARIABLES MONITORING
# =============================================================================

variable "notification_email" {
  description = "Email pour les notifications d'alertes"
  type        = string
  default     = ""
}

# =============================================================================
# VARIABLES D'ENVIRONNEMENT
# =============================================================================

# Secrets qui seront stockés dans Key Vault
variable "jwt_secret_key" {
  description = "Clé secrète pour JWT"
  type        = string
  sensitive   = true
  default     = ""
}

variable "google_client_id" {
  description = "Google OAuth Client ID"
  type        = string
  default     = ""
}

variable "google_client_secret" {
  description = "Google OAuth Client Secret"
  type        = string
  sensitive   = true
  default     = ""
}

variable "microsoft_client_id" {
  description = "Microsoft OAuth Client ID"
  type        = string
  default     = ""
}

variable "microsoft_client_secret" {
  description = "Microsoft OAuth Client Secret"
  type        = string
  sensitive   = true
  default     = ""
}

variable "openai_api_key" {
  description = "OpenAI API Key (si Azure OpenAI n'est pas utilisé)"
  type        = string
  sensitive   = true
  default     = ""
}

# =============================================================================
# VARIABLES AKS (Azure Kubernetes Service)
# =============================================================================

variable "kubernetes_version" {
  description = "Version de Kubernetes pour AKS"
  type        = string
  default     = "1.27"
}

variable "aks_node_count" {
  description = "Nombre de nœuds par défaut dans AKS"
  type        = number
  default     = 2
}

variable "aks_vm_size" {
  description = "Taille des VMs pour les nœuds AKS"
  type        = string
  default     = "Standard_D2s_v3"
}

variable "aks_enable_auto_scaling" {
  description = "Activer l'auto-scaling sur AKS"
  type        = bool
  default     = true
}

variable "aks_min_count" {
  description = "Nombre minimum de nœuds pour l'auto-scaling"
  type        = number
  default     = 1
}

variable "aks_max_count" {
  description = "Nombre maximum de nœuds pour l'auto-scaling"
  type        = number
  default     = 5
}
