# Outputs du module Database

output "server_id" {
  description = "ID du serveur PostgreSQL"
  value       = azurerm_postgresql_flexible_server.main.id
}

output "server_name" {
  description = "Nom du serveur PostgreSQL"
  value       = azurerm_postgresql_flexible_server.main.name
}

output "server_fqdn" {
  description = "FQDN du serveur PostgreSQL"
  value       = azurerm_postgresql_flexible_server.main.fqdn
}

output "database_name" {
  description = "Nom de la base de données principale"
  value       = azurerm_postgresql_flexible_server_database.main.name
}

output "test_database_name" {
  description = "Nom de la base de données de test"
  value       = azurerm_postgresql_flexible_server_database.test.name
}

output "admin_username" {
  description = "Nom d'utilisateur administrateur"
  value       = azurerm_postgresql_flexible_server.main.administrator_login
}

output "connection_string_secret_name" {
  description = "Nom du secret Key Vault pour la chaîne de connexion"
  value       = azurerm_key_vault_secret.connection_string.name
}

output "admin_password_secret_name" {
  description = "Nom du secret Key Vault pour le mot de passe admin"
  value       = azurerm_key_vault_secret.admin_password.name
}

output "connection_details" {
  description = "Détails de connexion (pour référence)"
  value = {
    server   = azurerm_postgresql_flexible_server.main.fqdn
    port     = 5432
    database = azurerm_postgresql_flexible_server_database.main.name
    username = azurerm_postgresql_flexible_server.main.administrator_login
    ssl_mode = "require"
  }
}
