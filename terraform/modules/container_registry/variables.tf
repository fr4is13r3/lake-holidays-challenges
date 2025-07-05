# Variables du module Container Registry

variable "resource_group_name" {
  description = "Nom du groupe de ressources"
  type        = string
}

variable "location" {
  description = "Région Azure"
  type        = string
}

variable "app_name" {
  description = "Nom de l'application"
  type        = string
}

variable "environment" {
  description = "Environnement (dev, staging, prod)"
  type        = string
}

variable "tags" {
  description = "Tags à appliquer aux ressources"
  type        = map(string)
  default     = {}
}

variable "sku" {
  description = "SKU du Container Registry"
  type        = string
  default     = "Basic"
  
  validation {
    condition     = contains(["Basic", "Standard", "Premium"], var.sku)
    error_message = "Le SKU doit être Basic, Standard ou Premium."
  }
}

variable "key_vault_id" {
  description = "ID du Key Vault pour stocker les secrets"
  type        = string
}

# Configuration Premium
variable "retention_days" {
  description = "Nombre de jours de rétention des images (Premium uniquement)"
  type        = number
  default     = 7
}

variable "enable_content_trust" {
  description = "Activer la confiance du contenu (Premium uniquement)"
  type        = bool
  default     = false
}

variable "georeplications" {
  description = "Configuration de géo-réplication (Premium uniquement)"
  type = list(object({
    location                = string
    zone_redundancy_enabled = bool
  }))
  default = []
}

# Webhook configuration
variable "enable_deployment_webhook" {
  description = "Activer le webhook de déploiement"
  type        = bool
  default     = false
}

variable "webhook_service_uri" {
  description = "URI du service pour le webhook"
  type        = string
  default     = ""
}

# Auto-build configuration (Premium)
variable "enable_auto_build" {
  description = "Activer les builds automatiques ACR Tasks (Premium uniquement)"
  type        = bool
  default     = false
}

variable "github_repo" {
  description = "Repository GitHub (format: owner/repo)"
  type        = string
  default     = ""
}

variable "github_token" {
  description = "Token GitHub pour ACR Tasks"
  type        = string
  default     = ""
  sensitive   = true
}

# Intégration avec Container Apps
variable "container_apps_identity_principal_id" {
  description = "Principal ID de l'identité managée des Container Apps"
  type        = string
  default     = ""
}

# Audit configuration
variable "enable_acr_audit" {
  description = "Activer l'audit du Container Registry"
  type        = bool
  default     = false
}

variable "log_analytics_workspace_id" {
  description = "ID du workspace Log Analytics pour l'audit"
  type        = string
  default     = ""
}
