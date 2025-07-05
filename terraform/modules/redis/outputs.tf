# Outputs du module Redis

output "cache_id" {
  description = "ID du cache Redis"
  value       = azurerm_redis_cache.main.id
}

output "cache_name" {
  description = "Nom du cache Redis"
  value       = azurerm_redis_cache.main.name
}

output "hostname" {
  description = "Hostname du cache Redis"
  value       = azurerm_redis_cache.main.hostname
}

output "port" {
  description = "Port du cache Redis"
  value       = azurerm_redis_cache.main.port
}

output "ssl_port" {
  description = "Port SSL du cache Redis"
  value       = azurerm_redis_cache.main.ssl_port
}

output "primary_access_key" {
  description = "Clé d'accès primaire Redis"
  value       = azurerm_redis_cache.main.primary_access_key
  sensitive   = true
}

output "secondary_access_key" {
  description = "Clé d'accès secondaire Redis"
  value       = azurerm_redis_cache.main.secondary_access_key
  sensitive   = true
}

output "connection_string_secret_name" {
  description = "Nom du secret Key Vault pour la chaîne de connexion"
  value       = azurerm_key_vault_secret.connection_string.name
}

output "primary_access_key_secret_name" {
  description = "Nom du secret Key Vault pour la clé primaire"
  value       = azurerm_key_vault_secret.primary_access_key.name
}

output "redis_configuration" {
  description = "Configuration Redis"
  value = {
    hostname    = azurerm_redis_cache.main.hostname
    port        = azurerm_redis_cache.main.port
    ssl_port    = azurerm_redis_cache.main.ssl_port
    sku_name    = azurerm_redis_cache.main.sku_name
    family      = azurerm_redis_cache.main.family
    capacity    = azurerm_redis_cache.main.capacity
    version     = azurerm_redis_cache.main.redis_version
  }
}
