# Module Storage - Stockage pour les fichiers uploadés
# Configuration pour audio, documents, images, vidéos

variable "resource_group_name" {
  description = "Nom du resource group"
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
  description = "Tags pour les ressources"
  type        = map(string)
  default     = {}
}

variable "account_tier" {
  description = "Tier du compte de stockage"
  type        = string
  default     = "Standard"
}

variable "account_replication_type" {
  description = "Type de réplication"
  type        = string
  default     = "LRS"
}

variable "key_vault_id" {
  description = "ID du Key Vault pour stocker les clés"
  type        = string
}

# Configuration locale
locals {
  storage_account_name = "${var.app_name}${var.environment}storage"
  # Supprimer les caractères non autorisés et limiter à 24 caractères
  sanitized_name = substr(replace(local.storage_account_name, "/[^a-z0-9]/", ""), 0, 24)
}

# Storage Account principal
resource "azurerm_storage_account" "main" {
  name                     = local.sanitized_name
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = var.account_tier
  account_replication_type = var.account_replication_type
  account_kind             = "StorageV2"
  
  # Configuration de sécurité
  https_traffic_only_enabled = true
  min_tls_version          = "TLS1_2"
  
  # Configuration des blobs
  blob_properties {
    cors_rule {
      allowed_headers    = ["*"]
      allowed_methods    = ["DELETE", "GET", "HEAD", "MERGE", "POST", "OPTIONS", "PUT", "PATCH"]
      allowed_origins    = ["*"]
      exposed_headers    = ["*"]
      max_age_in_seconds = 3600
    }
    
    delete_retention_policy {
      days = var.environment == "prod" ? 30 : 7
    }
    
    versioning_enabled = var.environment == "prod"
  }

  tags = var.tags
}

# Container pour les fichiers audio
resource "azurerm_storage_container" "audio" {
  name                  = "audio"
  storage_account_name  = azurerm_storage_account.main.name
  container_access_type = "blob"
}

# Container pour les documents
resource "azurerm_storage_container" "documents" {
  name                  = "documents"
  storage_account_name  = azurerm_storage_account.main.name
  container_access_type = "blob"
}

# Container pour les images
resource "azurerm_storage_container" "images" {
  name                  = "images"
  storage_account_name  = azurerm_storage_account.main.name
  container_access_type = "blob"
}

# Container pour les vidéos
resource "azurerm_storage_container" "videos" {
  name                  = "videos"
  storage_account_name  = azurerm_storage_account.main.name
  container_access_type = "blob"
}

# Container privé pour les backups
resource "azurerm_storage_container" "backups" {
  name                  = "backups"
  storage_account_name  = azurerm_storage_account.main.name
  container_access_type = "private"
}

# Stockage des clés de storage dans Key Vault
resource "azurerm_key_vault_secret" "storage_connection_string" {
  name         = "storage-connection-string"
  value        = azurerm_storage_account.main.primary_connection_string
  key_vault_id = var.key_vault_id
  
  tags = var.tags
}

resource "azurerm_key_vault_secret" "storage_account_key" {
  name         = "storage-account-key"
  value        = azurerm_storage_account.main.primary_access_key
  key_vault_id = var.key_vault_id
  
  tags = var.tags
}

# Politique de gestion du cycle de vie pour optimiser les coûts
resource "azurerm_storage_management_policy" "main" {
  storage_account_id = azurerm_storage_account.main.id

  rule {
    name    = "lifecycle-rule"
    enabled = true
    
    filters {
      prefix_match = ["audio/", "documents/", "images/", "videos/"]
      blob_types   = ["blockBlob"]
    }
    
    actions {
      base_blob {
        # Passer au tier Cool après 30 jours
        tier_to_cool_after_days_since_modification_greater_than = 30
        # Passer au tier Archive après 90 jours (seulement en prod)
        tier_to_archive_after_days_since_modification_greater_than = var.environment == "prod" ? 90 : null
        # Supprimer après 365 jours (seulement en dev/staging)
        delete_after_days_since_modification_greater_than = var.environment != "prod" ? 365 : null
      }
    }
  }
}
