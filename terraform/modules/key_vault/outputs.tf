# Outputs du module Key Vault

output "key_vault_id" {
  description = "ID du Key Vault"
  value       = azurerm_key_vault.main.id
}

output "key_vault_name" {
  description = "Nom du Key Vault"
  value       = azurerm_key_vault.main.name
}

output "key_vault_uri" {
  description = "URI du Key Vault"
  value       = azurerm_key_vault.main.vault_uri
}

output "jwt_secret_name" {
  description = "Nom du secret JWT dans Key Vault"
  value       = azurerm_key_vault_secret.jwt_secret.name
}

output "container_apps_identity_id" {
  description = "ID de l'identité managée pour Container Apps"
  value       = azurerm_user_assigned_identity.container_apps.id
}

output "container_apps_identity_principal_id" {
  description = "Principal ID de l'identité managée pour Container Apps"
  value       = azurerm_user_assigned_identity.container_apps.principal_id
}

output "container_apps_identity_client_id" {
  description = "Client ID de l'identité managée pour Container Apps"
  value       = azurerm_user_assigned_identity.container_apps.client_id
}

output "secret_names" {
  description = "Noms des secrets créés dans Key Vault"
  value = {
    jwt_secret             = azurerm_key_vault_secret.jwt_secret.name
    google_client_secret   = var.google_client_secret != "" ? azurerm_key_vault_secret.google_client_secret[0].name : null
    microsoft_client_secret = var.microsoft_client_secret != "" ? azurerm_key_vault_secret.microsoft_client_secret[0].name : null
    openai_api_key         = var.openai_api_key != "" ? azurerm_key_vault_secret.openai_api_key[0].name : null
  }
}
