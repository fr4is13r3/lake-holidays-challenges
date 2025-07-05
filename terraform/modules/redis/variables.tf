# Variables du module Redis

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

variable "key_vault_id" {
  description = "ID du Key Vault pour stocker les secrets"
  type        = string
}

# Configuration Redis
variable "capacity" {
  description = "Capacité du cache Redis"
  type        = number
  default     = 1
}

variable "family" {
  description = "Famille Redis (C = Basic/Standard, P = Premium)"
  type        = string
  default     = "C"
  
  validation {
    condition     = contains(["C", "P"], var.family)
    error_message = "La famille Redis doit être C ou P."
  }
}

variable "sku_name" {
  description = "SKU Redis"
  type        = string
  default     = "Standard"
  
  validation {
    condition     = contains(["Basic", "Standard", "Premium"], var.sku_name)
    error_message = "Le SKU Redis doit être Basic, Standard ou Premium."
  }
}

variable "redis_version" {
  description = "Version Redis"
  type        = string
  default     = "6"
}

# Configuration Premium
variable "backup_storage_connection_string" {
  description = "Chaîne de connexion du stockage pour les sauvegardes (Premium uniquement)"
  type        = string
  default     = ""
}

# Règles de pare-feu
variable "firewall_rules" {
  description = "Règles de pare-feu personnalisées"
  type = map(object({
    start_ip = string
    end_ip   = string
  }))
  default = {}
}

# Monitoring et alertes
variable "enable_redis_audit" {
  description = "Activer l'audit Redis"
  type        = bool
  default     = false
}

variable "log_analytics_workspace_id" {
  description = "ID du workspace Log Analytics"
  type        = string
  default     = ""
}

variable "enable_alerts" {
  description = "Activer les alertes de monitoring"
  type        = bool
  default     = false
}

variable "action_group_id" {
  description = "ID du groupe d'action pour les alertes"
  type        = string
  default     = ""
}
