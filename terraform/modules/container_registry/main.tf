# Module Container Registry pour Lake Holidays Challenge
# Registry privé pour les images Docker de l'application

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

# Génération d'un nom unique pour le Container Registry
resource "random_string" "acr_suffix" {
  length  = 6
  special = false
  upper   = false
}

# Azure Container Registry
resource "azurerm_container_registry" "main" {
  name                = "lake${var.environment}acr${random_string.acr_suffix.result}"
  resource_group_name = var.resource_group_name
  location            = var.location
  sku                 = var.sku
  
  # Configuration admin (nécessaire pour Container Apps)
  admin_enabled = true
  
  # Configuration réseau
  public_network_access_enabled = true
  
  # Politique de rétention des images (Premium uniquement)
  dynamic "retention_policy" {
    for_each = var.sku == "Premium" ? [1] : []
    content {
      days    = var.retention_days
      enabled = true
    }
  }
  
  tags = var.tags
}

# Stockage du mot de passe admin dans Key Vault
resource "azurerm_key_vault_secret" "acr_admin_password" {
  name         = "container-registry-admin-password"
  value        = azurerm_container_registry.main.admin_password
  key_vault_id = var.key_vault_id
  
  content_type = "Container Registry Admin Password"
  
  tags = merge(var.tags, {
    SecretType = "Registry"
    Usage      = "Container-Deployment"
  })
}

# Stockage du nom d'utilisateur admin dans Key Vault
resource "azurerm_key_vault_secret" "acr_admin_username" {
  name         = "container-registry-admin-username"
  value        = azurerm_container_registry.main.admin_username
  key_vault_id = var.key_vault_id
  
  content_type = "Container Registry Admin Username"
  
  tags = merge(var.tags, {
    SecretType = "Registry"
    Usage      = "Container-Deployment"
  })
}

# Webhook pour déclencher les déploiements (optionnel)
resource "azurerm_container_registry_webhook" "deployment_webhook" {
  count = var.enable_deployment_webhook ? 1 : 0
  
  name                = "${var.app_name}-${var.environment}-deploy-webhook"
  resource_group_name = var.resource_group_name
  registry_name       = azurerm_container_registry.main.name
  location            = var.location
  
  service_uri = var.webhook_service_uri
  status      = "enabled"
  scope       = "${var.app_name}-*:*"
  actions     = ["push"]
  
  custom_headers = {
    "Content-Type" = "application/json"
    "X-Source"     = "Azure-Container-Registry"
  }
  
  tags = var.tags
}

# Configuration de Log Analytics pour audit du registry
resource "azurerm_monitor_diagnostic_setting" "acr_audit" {
  count = var.enable_acr_audit ? 1 : 0
  
  name                       = "${var.app_name}-${var.environment}-acr-audit"
  target_resource_id         = azurerm_container_registry.main.id
  log_analytics_workspace_id = var.log_analytics_workspace_id
  
  enabled_log {
    category = "ContainerRegistryRepositoryEvents"
  }
  
  enabled_log {
    category = "ContainerRegistryLoginEvents"
  }
  
  metric {
    category = "AllMetrics"
    enabled  = true
  }
}
