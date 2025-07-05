# Module Azure AI Foundry - Configuration moderne pour IA
# Remplace Azure OpenAI classique pour plus de fonctionnalités

# Configuration locale
locals {
  ai_hub_name = "${var.app_name}-${var.environment}-ai-hub"
  ai_project_name = "${var.app_name}-${var.environment}-ai-project"
  openai_account_name = "${var.app_name}-${var.environment}-openai"
}

# Azure AI Hub (centre de gestion IA)
resource "azurerm_cognitive_account" "ai_hub" {
  name                = local.ai_hub_name
  resource_group_name = var.resource_group_name
  location            = var.location
  kind                = "CognitiveServices"  # AI Services multi-model
  sku_name            = var.sku_name
  
  # Configuration de sécurité renforcée
  public_network_access_enabled = true
  
  # Intégration avec l'identité managée
  identity {
    type = "SystemAssigned"
  }
  
  tags = merge(var.tags, {
    Service = "AI-Foundry"
    Purpose = "AI-Hub"
  })
}

# Azure OpenAI Service (pour les modèles OpenAI spécifiques)
resource "azurerm_cognitive_account" "openai" {
  name                = local.openai_account_name
  resource_group_name = var.resource_group_name
  location            = var.location
  kind                = "OpenAI"
  sku_name            = var.sku_name
  
  # Configuration de sécurité
  public_network_access_enabled = true
  
  # Intégration avec l'identité managée
  identity {
    type = "SystemAssigned"
  }
  
  tags = merge(var.tags, {
    Service = "AI-Foundry"
    Purpose = "OpenAI-Models"
  })
}

# Déploiements des modèles OpenAI
resource "azurerm_cognitive_deployment" "models" {
  count                = length(var.model_deployments)
  name                 = var.model_deployments[count.index].name
  cognitive_account_id = azurerm_cognitive_account.openai.id
  
  model {
    format  = "OpenAI"
    name    = var.model_deployments[count.index].model_name
    version = var.model_deployments[count.index].model_version
  }
  
  scale {
    type     = var.model_deployments[count.index].scale_type
    capacity = var.model_deployments[count.index].capacity
  }
}

# Attribution des rôles pour l'identité managée AKS
resource "azurerm_role_assignment" "aks_ai_hub_access" {
  scope                = azurerm_cognitive_account.ai_hub.id
  role_definition_name = "Cognitive Services User"
  principal_id         = var.managed_identity_principal_id
}

resource "azurerm_role_assignment" "aks_openai_access" {
  scope                = azurerm_cognitive_account.openai.id
  role_definition_name = "Cognitive Services OpenAI User"
  principal_id         = var.managed_identity_principal_id
}

# Stockage des configurations dans Key Vault
resource "azurerm_key_vault_secret" "ai_hub_endpoint" {
  name         = "azure-ai-hub-endpoint"
  value        = azurerm_cognitive_account.ai_hub.endpoint
  key_vault_id = var.key_vault_id
  
  tags = var.tags
}

resource "azurerm_key_vault_secret" "openai_endpoint" {
  name         = "azure-openai-endpoint"
  value        = azurerm_cognitive_account.openai.endpoint
  key_vault_id = var.key_vault_id
  
  tags = var.tags
}

resource "azurerm_key_vault_secret" "ai_hub_api_key" {
  name         = "azure-ai-hub-api-key"
  value        = azurerm_cognitive_account.ai_hub.primary_access_key
  key_vault_id = var.key_vault_id
  
  tags = var.tags
}

resource "azurerm_key_vault_secret" "openai_api_key" {
  name         = "azure-openai-api-key"
  value        = azurerm_cognitive_account.openai.primary_access_key
  key_vault_id = var.key_vault_id
  
  tags = var.tags
}

# Configuration des modèles déployés pour l'application
resource "azurerm_key_vault_secret" "ai_models_config" {
  name         = "azure-ai-models-config"
  value = jsonencode({
    ai_hub = {
      endpoint = azurerm_cognitive_account.ai_hub.endpoint
      resource_id = azurerm_cognitive_account.ai_hub.id
    }
    openai = {
      endpoint = azurerm_cognitive_account.openai.endpoint
      resource_id = azurerm_cognitive_account.openai.id
      models = {
        for deployment in azurerm_cognitive_deployment.models :
        deployment.name => {
          deployment_name = deployment.name
          model_name      = deployment.model[0].name
          model_version   = deployment.model[0].version
        }
      }
    }
  })
  key_vault_id = var.key_vault_id
  
  tags = var.tags
}
