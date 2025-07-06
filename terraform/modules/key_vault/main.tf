# Module Key Vault pour Lake Holidays Challenge
# Gestion sécurisée des secrets et certificats

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.80"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
  }
}

# Données Azure actuelles
data "azurerm_client_config" "current" {}

# Génération d'un nom unique pour Key Vault
resource "random_string" "key_vault_suffix" {
  length  = 4
  special = false
  upper   = false
}

# Key Vault principal
resource "azurerm_key_vault" "main" {
  name                = "lake-${var.environment}-kv-${random_string.key_vault_suffix.result}"
  location            = var.location
  resource_group_name = var.resource_group_name
  tenant_id           = var.tenant_id
  enable_rbac_authorization = true
  # Configuration de sécurité
  sku_name                   = "standard"
  soft_delete_retention_days = 7
  purge_protection_enabled   = var.environment == "prod" ? true : false
  
  # Configuration d'accès réseau
  network_acls {
    default_action = "Allow"  # Pour le développement, restrictif en production
    bypass         = "AzureServices"
  }
  
  tags = var.tags
}

# Politique d'accès pour l'utilisateur/service principal actuel
resource "azurerm_key_vault_access_policy" "current_user" {
  key_vault_id = azurerm_key_vault.main.id
  tenant_id    = var.tenant_id
  object_id    = var.object_id
  
  # Permissions sur les secrets
  secret_permissions = [
    "Get",
    "List", 
    "Set",
    "Delete",
    "Recover",
    "Backup",
    "Restore",
    "Purge"
  ]
  
  # Permissions sur les certificats
  certificate_permissions = [
    "Get",
    "List",
    "Create",
    "Import",
    "Update",
    "ManageContacts",
    "GetIssuers",
    "ListIssuers",
    "SetIssuers",
    "DeleteIssuers"
  ]
  
  # Permissions sur les clés
  key_permissions = [
    "Get",
    "List",
    "Create",
    "Delete",
    "Update",
    "Import",
    "Backup",
    "Restore",
    "Recover"
  ]
}

# Génération automatique du secret JWT
resource "random_password" "jwt_secret" {
  length  = 64
  special = true
}

# Secret JWT pour l'authentification
resource "azurerm_key_vault_secret" "jwt_secret" {
  name         = "jwt-secret-key"
  value        = random_password.jwt_secret.result
  key_vault_id = azurerm_key_vault.main.id
  
  content_type = "JWT Secret Key"
  
  depends_on = [azurerm_key_vault_access_policy.current_user]
  
  tags = merge(var.tags, {
    SecretType = "JWT"
    Usage      = "Authentication"
  })
}

# Secret pour les clés d'API externes (Google OAuth)
resource "azurerm_key_vault_secret" "google_client_secret" {
  count = var.google_client_secret != "" ? 1 : 0
  
  name         = "google-client-secret"
  value        = var.google_client_secret
  key_vault_id = azurerm_key_vault.main.id
  
  content_type = "Google OAuth Client Secret"
  
  depends_on = [azurerm_key_vault_access_policy.current_user]
  
  tags = merge(var.tags, {
    SecretType = "OAuth"
    Provider   = "Google"
  })
}

# Secret pour Microsoft OAuth
resource "azurerm_key_vault_secret" "microsoft_client_secret" {
  count = var.microsoft_client_secret != "" ? 1 : 0
  
  name         = "microsoft-client-secret"
  value        = var.microsoft_client_secret
  key_vault_id = azurerm_key_vault.main.id
  
  content_type = "Microsoft OAuth Client Secret"
  
  depends_on = [azurerm_key_vault_access_policy.current_user]
  
  tags = merge(var.tags, {
    SecretType = "OAuth"
    Provider   = "Microsoft"
  })
}

# Secret pour OpenAI API Key (si non Azure OpenAI)
resource "azurerm_key_vault_secret" "openai_api_key" {
  count = var.openai_api_key != "" ? 1 : 0
  
  name         = "openai-api-key"
  value        = var.openai_api_key
  key_vault_id = azurerm_key_vault.main.id
  
  content_type = "OpenAI API Key"
  
  depends_on = [azurerm_key_vault_access_policy.current_user]
  
  tags = merge(var.tags, {
    SecretType = "API"
    Provider   = "OpenAI"
  })
}

# Identité managée pour Container Apps
resource "azurerm_user_assigned_identity" "container_apps" {
  name                = "${var.app_name}-${var.environment}-container-identity"
  location            = var.location
  resource_group_name = var.resource_group_name
  
  tags = var.tags
}

# Politique d'accès pour l'identité managée des Container Apps
resource "azurerm_key_vault_access_policy" "container_apps" {
  key_vault_id = azurerm_key_vault.main.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = azurerm_user_assigned_identity.container_apps.principal_id
  
  # Permissions minimales pour les Container Apps
  secret_permissions = [
    "Get",
    "List"
  ]
  
  depends_on = [azurerm_user_assigned_identity.container_apps]
}

# Configuration de Log Analytics pour audit des accès Key Vault
resource "azurerm_monitor_diagnostic_setting" "key_vault_audit" {
  count = var.enable_key_vault_audit ? 1 : 0
  
  name                       = "${var.app_name}-${var.environment}-kv-audit"
  target_resource_id         = azurerm_key_vault.main.id
  log_analytics_workspace_id = var.log_analytics_workspace_id
  
  enabled_log {
    category = "AuditEvent"
  }
  
  enabled_log {
    category = "AzurePolicyEvaluationDetails"
  }
  
  metric {
    category = "AllMetrics"
    enabled  = true
  }
}
