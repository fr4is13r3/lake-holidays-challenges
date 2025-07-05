# Outputs de l'infrastructure Lake Holidays Challenge - AKS

# =============================================================================
# OUTPUTS GÉNÉRAUX
# =============================================================================

output "resource_group_name" {
  description = "Nom du groupe de ressources"
  value       = azurerm_resource_group.main.name
}

output "location" {
  description = "Région Azure utilisée"
  value       = azurerm_resource_group.main.location
}

# =============================================================================
# OUTPUTS AKS (Azure Kubernetes Service)
# =============================================================================

output "aks_cluster_id" {
  description = "ID du cluster AKS"
  value       = module.aks.cluster_id
}

output "aks_cluster_name" {
  description = "Nom du cluster AKS"
  value       = module.aks.cluster_name
}

output "aks_cluster_fqdn" {
  description = "FQDN du cluster AKS"
  value       = module.aks.cluster_fqdn
}

output "aks_kube_config" {
  description = "Configuration kubectl pour AKS"
  value       = module.aks.kube_config_raw
  sensitive   = true
}

output "aks_node_resource_group" {
  description = "Resource group des nœuds AKS"
  value       = module.aks.node_resource_group
}

output "aks_virtual_network_id" {
  description = "ID du virtual network AKS"
  value       = module.aks.virtual_network_id
}

# =============================================================================
# OUTPUTS CONTAINER REGISTRY
# =============================================================================

output "container_registry_login_server" {
  description = "Serveur de connexion du Container Registry"
  value       = module.container_registry.login_server
}

output "container_registry_admin_username" {
  description = "Nom d'utilisateur admin du Container Registry"
  value       = module.container_registry.admin_username
  sensitive   = true
}

output "container_registry_id" {
  description = "ID du Container Registry"
  value       = module.container_registry.container_registry_id
}

# =============================================================================
# OUTPUTS STORAGE
# =============================================================================

output "storage_account_name" {
  description = "Nom du compte de stockage"
  value       = module.storage.storage_account_name
}

output "storage_account_primary_endpoint" {
  description = "Endpoint principal du stockage blob"
  value       = module.storage.storage_account_primary_endpoint
}

output "storage_containers" {
  description = "Conteneurs de stockage créés"
  value       = module.storage.storage_containers
}

output "storage_urls" {
  description = "URLs des containers de stockage"
  value       = module.storage.storage_urls
}

# =============================================================================
# OUTPUTS AZURE AI FOUNDRY
# =============================================================================

output "ai_foundry_hub_endpoint" {
  description = "Endpoint Azure AI Hub (si activé)"
  value       = var.enable_azure_openai ? module.ai_foundry[0].ai_hub_endpoint : null
  sensitive   = true
}

output "ai_foundry_openai_endpoint" {
  description = "Endpoint Azure OpenAI (si activé)"
  value       = var.enable_azure_openai ? module.ai_foundry[0].openai_endpoint : null
  sensitive   = true
}

output "ai_foundry_deployed_models" {
  description = "Modèles déployés sur Azure AI Foundry (si activé)"
  value       = var.enable_azure_openai ? module.ai_foundry[0].deployed_models : null
  sensitive   = true
}

output "ai_foundry_hub_name" {
  description = "Nom de l'Azure AI Hub"
  value       = var.enable_azure_openai ? module.ai_foundry[0].ai_hub_name : null
}

output "ai_foundry_openai_name" {
  description = "Nom du service Azure OpenAI"
  value       = var.enable_azure_openai ? module.ai_foundry[0].openai_name : null
}

# =============================================================================
# OUTPUTS KEY VAULT
# =============================================================================

output "key_vault_name" {
  description = "Nom du Key Vault"
  value       = module.key_vault.key_vault_name
}

output "key_vault_uri" {
  description = "URI du Key Vault"
  value       = module.key_vault.key_vault_uri
}

output "key_vault_id" {
  description = "ID du Key Vault"
  value       = module.key_vault.key_vault_id
}

# =============================================================================
# OUTPUTS MONITORING
# =============================================================================

output "log_analytics_workspace_id" {
  description = "ID du workspace Log Analytics"
  value       = module.monitoring.log_analytics_workspace_id
}

output "application_insights_instrumentation_key" {
  description = "Clé d'instrumentation Application Insights"
  value       = module.monitoring.application_insights_instrumentation_key
  sensitive   = true
}

output "application_insights_connection_string" {
  description = "Chaîne de connexion Application Insights"
  value       = module.monitoring.application_insights_connection_string
  sensitive   = true
}

# =============================================================================
# OUTPUTS POUR CI/CD et Kubernetes
# =============================================================================

output "deployment_info" {
  description = "Informations de déploiement pour CI/CD"
  value = {
    resource_group       = azurerm_resource_group.main.name
    container_registry   = module.container_registry.login_server
    aks_cluster_name     = module.aks.cluster_name
    aks_resource_group   = azurerm_resource_group.main.name
    key_vault_name       = module.key_vault.key_vault_name
    storage_account_name = module.storage.storage_account_name
    environment         = var.environment
  }
}

# =============================================================================
# OUTPUTS POUR CONFIGURATION KUBERNETES
# =============================================================================

output "kubernetes_config" {
  description = "Configuration pour les manifests Kubernetes"
  value = {
    # Informations du cluster
    cluster_name = module.aks.cluster_name
    namespace    = "${var.app_name}-${var.environment}"
    
    # Images containers
    backend_image  = "${module.container_registry.login_server}/${var.app_name}-backend:latest"
    frontend_image = "${module.container_registry.login_server}/${var.app_name}-frontend:latest"
    
    # Services intégrés dans les containers
    postgres_enabled = true  # Intégré dans le backend
    redis_enabled    = true  # Intégré dans le backend
    
    # Services externes
    storage_account     = module.storage.storage_account_name
    key_vault_name      = module.key_vault.key_vault_name
    app_insights_key    = module.monitoring.application_insights_instrumentation_key
    ai_hub_endpoint     = var.enable_azure_openai ? module.ai_foundry[0].ai_hub_endpoint : null
    openai_endpoint     = var.enable_azure_openai ? module.ai_foundry[0].openai_endpoint : null
  }
  sensitive = true
}

# =============================================================================
# OUTPUTS POUR DÉVELOPPEMENT LOCAL
# =============================================================================

output "local_development_info" {
  description = "Informations pour le développement local"
  value = {
    # Commandes kubectl
    kubectl_config = "az aks get-credentials --resource-group ${azurerm_resource_group.main.name} --name ${module.aks.cluster_name}"
    
    # Configuration Docker
    docker_login = "az acr login --name ${module.container_registry.login_server}"
    
    # URLs des services (seront disponibles après déploiement k8s)
    backend_service  = "http://backend.${var.app_name}-${var.environment}.svc.cluster.local"
    frontend_service = "http://frontend.${var.app_name}-${var.environment}.svc.cluster.local"
    
    # Key Vault pour les secrets
    key_vault_secrets = "az keyvault secret list --vault-name ${module.key_vault.key_vault_name}"
    
    # Accès aux logs
    logs_command = "kubectl logs -l app=backend -n ${var.app_name}-${var.environment}"
  }
}

# =============================================================================
# OUTPUTS DE DEBUG
# =============================================================================

output "debug_info" {
  description = "Informations de debug pour le déploiement"
  value = {
    terraform_version = "~> 1.5"
    azurerm_version  = "~> 3.80"
    deployment_time  = timestamp()
    architecture     = "AKS"
    modules_deployed = [
      "key_vault",
      "container_registry", 
      "storage",
      "monitoring",
      "aks",
      var.enable_azure_openai ? "ai_foundry" : null
    ]
    next_steps = [
      "1. Déployer les manifests Kubernetes dans k8s/",
      "2. Configurer les secrets Kubernetes depuis Key Vault",
      "3. Déployer les applications via GitHub Actions",
      "4. Vérifier la connectivité et les logs"
    ]
  }
}
