# Variables du module Key Vault

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

variable "tenant_id" {
  description = "ID du tenant Azure AD"
  type        = string
}

variable "object_id" {
  description = "Object ID de l'utilisateur/service principal"
  type        = string
}

# Secrets optionnels
variable "google_client_secret" {
  description = "Google OAuth Client Secret"
  type        = string
  default     = ""
  sensitive   = true
}

variable "microsoft_client_secret" {
  description = "Microsoft OAuth Client Secret"
  type        = string
  default     = ""
  sensitive   = true
}

variable "openai_api_key" {
  description = "OpenAI API Key"
  type        = string
  default     = ""
  sensitive   = true
}

# Configuration audit
variable "enable_key_vault_audit" {
  description = "Activer l'audit du Key Vault"
  type        = bool
  default     = false
}

variable "log_analytics_workspace_id" {
  description = "ID du workspace Log Analytics pour l'audit"
  type        = string
  default     = ""
}
