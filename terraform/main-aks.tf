# Lake Holidays Challenge - Infrastructure Terraform Azure avec AKS
# Configuration principale pour déploiement Kubernetes

terraform {
  required_version = ">= 1.5"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.80"
    }
    azuread = {
      source  = "hashicorp/azuread"
      version = "~> 2.45"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.23"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.11"
    }
  }

  backend "azurerm" {
    resource_group_name  = "rg-lake-apps-prd-tfstate"
    storage_account_name = "stalakeholidaysprd"
    container_name       = "tfstate"
    key                  = "lake-holidays-prd.terraform.tfstate"
  }
}

# Configuration du provider Azure
provider "azurerm" {
  features {
    key_vault {
      purge_soft_delete_on_destroy    = true
      recover_soft_deleted_key_vaults = true
    }
    resource_group {
      prevent_deletion_if_contains_resources = false
    }
  }
}

provider "azuread" {}

# Configuration des providers Kubernetes et Helm
provider "kubernetes" {
  host                   = module.aks.kube_config.0.host
  client_certificate     = base64decode(module.aks.kube_config.0.client_certificate)
  client_key             = base64decode(module.aks.kube_config.0.client_key)
  cluster_ca_certificate = base64decode(module.aks.kube_config.0.cluster_ca_certificate)
}

provider "helm" {
  kubernetes {
    host                   = module.aks.kube_config.0.host
    client_certificate     = base64decode(module.aks.kube_config.0.client_certificate)
    client_key             = base64decode(module.aks.kube_config.0.client_key)
    cluster_ca_certificate = base64decode(module.aks.kube_config.0.cluster_ca_certificate)
  }
}

# Variables locales pour la configuration
locals {
  # Nom de l'application
  app_name = var.app_name
  
  # Environment (dev, staging, prod)
  environment = var.environment
  
  # Région Azure
  location = var.location
  
  # Tags communs pour toutes les ressources
  common_tags = merge(var.tags, {
    Application = local.app_name
    Environment = local.environment
    ManagedBy   = "Terraform"
    CreatedBy   = "GitHub-Actions"
    Project     = "lake-holidays-challenge"
  })
  
  # Noms des ressources avec convention de nommage
  resource_group_name = "${local.app_name}-${local.environment}-rg"
  
  # Configuration des domaines et DNS
  domain_name = var.domain_name != "" ? var.domain_name : "${local.app_name}-${local.environment}.azure.com"
}

# Resource Group principal
resource "azurerm_resource_group" "main" {
  name     = local.resource_group_name
  location = local.location
  tags     = local.common_tags
}

# Module Monitoring (créé en premier pour le workspace Log Analytics)
module "monitoring" {
  source = "./modules/monitoring"
  
  resource_group_name = azurerm_resource_group.main.name
  location           = azurerm_resource_group.main.location
  app_name           = local.app_name
  environment        = local.environment
  tags               = local.common_tags
  
  # Configuration des alertes
  notification_email = var.notification_email
}

# Module Key Vault pour la gestion des secrets
module "key_vault" {
  source = "./modules/key_vault"
  
  resource_group_name = azurerm_resource_group.main.name
  location           = azurerm_resource_group.main.location
  app_name           = local.app_name
  environment        = local.environment
  tags               = local.common_tags
  
  # Permissions pour les services
  tenant_id = data.azurerm_client_config.current.tenant_id
  object_id = data.azurerm_client_config.current.object_id
  
  # Secrets d'application
  google_client_secret    = var.google_client_secret
  microsoft_client_secret = var.microsoft_client_secret
  openai_api_key         = var.openai_api_key
  
  # Audit et monitoring
  enable_key_vault_audit     = var.environment == "prod"
  log_analytics_workspace_id = module.monitoring.log_analytics_workspace_id
}

# Module Container Registry
module "container_registry" {
  source = "./modules/container_registry"
  
  resource_group_name = azurerm_resource_group.main.name
  location           = azurerm_resource_group.main.location
  app_name           = local.app_name
  environment        = local.environment
  tags               = local.common_tags
  
  # Configuration du SKU selon l'environnement
  sku = var.environment == "prod" ? "Premium" : "Standard"
  
  # Intégration avec Key Vault
  key_vault_id = module.key_vault.key_vault_id
}

# Module Storage Account pour les fichiers
module "storage" {
  source = "./modules/storage"
  
  resource_group_name = azurerm_resource_group.main.name
  location           = azurerm_resource_group.main.location
  app_name           = local.app_name
  environment        = local.environment
  tags               = local.common_tags
  
  # Configuration du stockage
  account_tier             = var.storage_account_tier
  account_replication_type = var.storage_replication_type
  
  key_vault_id = module.key_vault.key_vault_id
}

# Module Azure AI Foundry (remplace Azure OpenAI classique)
module "ai_foundry" {
  count  = var.enable_azure_openai ? 1 : 0
  source = "./modules/ai_foundry"
  
  resource_group_name = azurerm_resource_group.main.name
  location           = var.openai_location != "" ? var.openai_location : local.location
  app_name           = local.app_name
  environment        = local.environment
  tags               = local.common_tags
  
  # Configuration AI Foundry et OpenAI
  sku_name                       = var.openai_sku_name
  model_deployments             = var.openai_model_deployments
  
  # Intégration sécurisée
  key_vault_id                  = module.key_vault.key_vault_id
  managed_identity_principal_id = module.aks.kubelet_identity[0].object_id
  
  # Configuration avancée
  enable_monitoring             = var.environment == "prod"
  public_network_access_enabled = true
  local_auth_enabled           = var.environment != "prod"
  
  depends_on = [module.aks, module.key_vault]
}

# Module AKS (Azure Kubernetes Service)
module "aks" {
  source = "./modules/aks"
  
  resource_group_name = azurerm_resource_group.main.name
  location           = azurerm_resource_group.main.location
  app_name           = local.app_name
  environment        = local.environment
  tags               = local.common_tags
  
  # Configuration du cluster
  kubernetes_version         = var.kubernetes_version
  node_count                = var.aks_node_count
  vm_size                   = var.aks_vm_size
  enable_auto_scaling       = var.aks_enable_auto_scaling
  min_count                 = var.aks_min_count
  max_count                 = var.aks_max_count
  
  # Intégration avec les autres services
  container_registry_id      = module.container_registry.container_registry_id
  log_analytics_workspace_id = module.monitoring.log_analytics_workspace_id
  key_vault_id              = module.key_vault.key_vault_id
}

# Configuration des permissions Key Vault pour AKS (après création du cluster)
resource "azurerm_key_vault_access_policy" "aks_kubelet_keyvault_access" {
  key_vault_id = module.key_vault.key_vault_id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = module.aks.kubelet_identity[0].object_id
  
  # Permissions minimales pour le CSI Secret Store Driver
  secret_permissions = [
    "Get",
    "List"
  ]
  
  depends_on = [module.aks, module.key_vault]
}

# Données de configuration Azure
data "azurerm_client_config" "current" {}
