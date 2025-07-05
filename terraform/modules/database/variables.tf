# Variables du module Database

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

# Configuration PostgreSQL
variable "postgresql_version" {
  description = "Version PostgreSQL"
  type        = string
  default     = "15"
}

variable "admin_username" {
  description = "Nom d'utilisateur administrateur"
  type        = string
  default     = "psqladmin"
}

variable "database_name" {
  description = "Nom de la base de données principale"
  type        = string
  default     = "lake_holidays"
}

variable "sku_name" {
  description = "SKU du serveur PostgreSQL"
  type        = string
  default     = "GP_Standard_D2s_v3"
}

variable "storage_mb" {
  description = "Taille du stockage en MB"
  type        = number
  default     = 32768
}

variable "backup_retention_days" {
  description = "Nombre de jours de rétention des sauvegardes"
  type        = number
  default     = 7
}

variable "ssl_enforcement_enabled" {
  description = "Activer l'application SSL"
  type        = bool
  default     = true
}

# Configuration haute disponibilité
variable "enable_high_availability" {
  description = "Activer la haute disponibilité"
  type        = bool
  default     = false
}

# Fenêtre de maintenance
variable "maintenance_window" {
  description = "Configuration de la fenêtre de maintenance"
  type = object({
    day_of_week  = number
    start_hour   = number
    start_minute = number
  })
  default = null
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
variable "enable_database_audit" {
  description = "Activer l'audit de la base de données"
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
