# Variables pour le module Azure AI Foundry
# Configuration centralisée pour les services IA

variable "resource_group_name" {
  description = "Nom du resource group où déployer les services IA"
  type        = string
}

variable "location" {
  description = "Région Azure (doit supporter Azure AI Foundry et OpenAI)"
  type        = string
  
  validation {
    condition = can(regex("^(eastus|eastus2|westus|westus2|northcentralus|southcentralus|westeurope|northeurope|uksouth|swedencentral)$", lower(replace(var.location, " ", ""))))
    error_message = "La région doit supporter Azure AI Foundry et OpenAI. Utilisez: East US, East US 2, West US, West US 2, North Central US, South Central US, West Europe, North Europe, UK South, ou Sweden Central."
  }
}

variable "app_name" {
  description = "Nom de l'application (utilisé pour nommer les ressources)"
  type        = string
  
  validation {
    condition     = length(var.app_name) >= 2 && length(var.app_name) <= 20
    error_message = "Le nom de l'application doit contenir entre 2 et 20 caractères."
  }
}

variable "environment" {
  description = "Environnement de déploiement"
  type        = string
  
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "L'environnement doit être: dev, staging, ou prod."
  }
}

variable "tags" {
  description = "Tags à appliquer à toutes les ressources"
  type        = map(string)
  default     = {}
}

variable "sku_name" {
  description = "SKU pour les services Azure AI (S0 = Standard)"
  type        = string
  default     = "S0"
  
  validation {
    condition     = contains(["F0", "S0"], var.sku_name)
    error_message = "Le SKU doit être F0 (gratuit, limité) ou S0 (standard, recommandé)."
  }
}

variable "model_deployments" {
  description = "Configuration des modèles IA à déployer"
  type = list(object({
    name         = string
    model_name   = string
    model_version = string
    scale_type   = string
    capacity     = number
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
    condition     = length(var.model_deployments) > 0
    error_message = "Au moins un modèle doit être configuré."
  }
}

variable "key_vault_id" {
  description = "ID du Key Vault pour stocker les clés et endpoints"
  type        = string
}

variable "managed_identity_principal_id" {
  description = "Principal ID de l'identité managée AKS pour accès aux services IA"
  type        = string
}

variable "enable_monitoring" {
  description = "Activer le monitoring avancé des services IA"
  type        = bool
  default     = true
}

variable "public_network_access_enabled" {
  description = "Autoriser l'accès depuis l'internet public"
  type        = bool
  default     = true
}

variable "local_auth_enabled" {
  description = "Autoriser l'authentification par clé API (recommandé: false pour production)"
  type        = bool
  default     = true
}
