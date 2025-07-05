# Outputs pour Azure AI Foundry
# Exposent les informations nécessaires pour l'intégration avec l'application

output "ai_hub_id" {
  description = "ID de l'Azure AI Hub"
  value       = azurerm_cognitive_account.ai_hub.id
}

output "ai_hub_endpoint" {
  description = "Endpoint de l'Azure AI Hub"
  value       = azurerm_cognitive_account.ai_hub.endpoint
  sensitive   = true
}

output "ai_hub_name" {
  description = "Nom de l'Azure AI Hub"
  value       = azurerm_cognitive_account.ai_hub.name
}

output "openai_id" {
  description = "ID du service Azure OpenAI"
  value       = azurerm_cognitive_account.openai.id
}

output "openai_endpoint" {
  description = "Endpoint du service Azure OpenAI"
  value       = azurerm_cognitive_account.openai.endpoint
  sensitive   = true
}

output "openai_name" {
  description = "Nom du service Azure OpenAI"
  value       = azurerm_cognitive_account.openai.name
}

output "deployed_models" {
  description = "Liste des modèles déployés"
  value = {
    for deployment in azurerm_cognitive_deployment.models :
    deployment.name => {
      id              = deployment.id
      name            = deployment.name
      model_name      = deployment.model[0].name
      model_version   = deployment.model[0].version
      endpoint        = azurerm_cognitive_account.openai.endpoint
    }
  }
  sensitive = true
}

output "ai_hub_principal_id" {
  description = "Principal ID de l'identité managée AI Hub"
  value       = azurerm_cognitive_account.ai_hub.identity[0].principal_id
}

output "openai_principal_id" {
  description = "Principal ID de l'identité managée OpenAI"
  value       = azurerm_cognitive_account.openai.identity[0].principal_id
}
