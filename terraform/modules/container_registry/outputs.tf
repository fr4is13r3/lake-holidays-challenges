# Outputs du module Container Registry

output "container_registry_id" {
  description = "ID du Container Registry"
  value       = azurerm_container_registry.main.id
}

output "container_registry_name" {
  description = "Nom du Container Registry"
  value       = azurerm_container_registry.main.name
}

output "login_server" {
  description = "Serveur de login du Container Registry"
  value       = azurerm_container_registry.main.login_server
}

output "admin_username" {
  description = "Nom d'utilisateur admin du Container Registry"
  value       = azurerm_container_registry.main.admin_username
  sensitive   = true
}

output "admin_password" {
  description = "Mot de passe admin du Container Registry"
  value       = azurerm_container_registry.main.admin_password
  sensitive   = true
}

output "admin_password_secret_name" {
  description = "Nom du secret Key Vault pour le mot de passe admin"
  value       = azurerm_key_vault_secret.acr_admin_password.name
}

output "admin_username_secret_name" {
  description = "Nom du secret Key Vault pour le nom d'utilisateur admin"
  value       = azurerm_key_vault_secret.acr_admin_username.name
}

output "webhook_url" {
  description = "URL du webhook de déploiement (si activé)"
  value       = var.enable_deployment_webhook ? azurerm_container_registry_webhook.deployment_webhook[0].service_uri : null
}