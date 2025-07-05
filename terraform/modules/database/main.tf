# Module Database PostgreSQL pour Lake Holidays Challenge
# Base de données managée Azure Database for PostgreSQL

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

# Génération du mot de passe administrateur
resource "random_password" "admin_password" {
  length  = 32
  special = true
}

# Serveur PostgreSQL flexible
resource "azurerm_postgresql_flexible_server" "main" {
  name                   = "${var.app_name}-${var.environment}-psql-server"
  resource_group_name    = var.resource_group_name
  location               = var.location
  version                = var.postgresql_version
  
  # Configuration de l'administrateur
  administrator_login    = var.admin_username
  administrator_password = random_password.admin_password.result
  
  # Configuration du SKU
  sku_name   = var.sku_name
  storage_mb = var.storage_mb
  
  # Configuration de sauvegarde
  backup_retention_days        = var.backup_retention_days
  geo_redundant_backup_enabled = var.environment == "prod" ? true : false
  
  # Configuration de haute disponibilité (prod uniquement)
  dynamic "high_availability" {
    for_each = var.environment == "prod" && var.enable_high_availability ? [1] : []
    content {
      mode = "ZoneRedundant"
    }
  }
  
  # Configuration de maintenance
  dynamic "maintenance_window" {
    for_each = var.maintenance_window != null ? [var.maintenance_window] : []
    content {
      day_of_week  = maintenance_window.value.day_of_week
      start_hour   = maintenance_window.value.start_hour
      start_minute = maintenance_window.value.start_minute
    }
  }
  
  tags = var.tags
}

# Base de données principale
resource "azurerm_postgresql_flexible_server_database" "main" {
  name      = var.database_name
  server_id = azurerm_postgresql_flexible_server.main.id
  collation = "en_US.utf8"
  charset   = "utf8"
}

# Base de données de test
resource "azurerm_postgresql_flexible_server_database" "test" {
  name      = "${var.database_name}_test"
  server_id = azurerm_postgresql_flexible_server.main.id
  collation = "en_US.utf8"
  charset   = "utf8"
}

# Configuration de la règle de pare-feu pour Azure services
resource "azurerm_postgresql_flexible_server_firewall_rule" "azure_services" {
  name             = "AllowAzureServices"
  server_id        = azurerm_postgresql_flexible_server.main.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "0.0.0.0"
}

# Règles de pare-feu personnalisées
resource "azurerm_postgresql_flexible_server_firewall_rule" "custom_rules" {
  for_each = var.firewall_rules
  
  name             = each.key
  server_id        = azurerm_postgresql_flexible_server.main.id
  start_ip_address = each.value.start_ip
  end_ip_address   = each.value.end_ip
}

# Configuration SSL/TLS
resource "azurerm_postgresql_flexible_server_configuration" "ssl_enforcement" {
  name      = "ssl"
  server_id = azurerm_postgresql_flexible_server.main.id
  value     = var.ssl_enforcement_enabled ? "on" : "off"
}

# Configuration des extensions PostgreSQL
resource "azurerm_postgresql_flexible_server_configuration" "shared_preload_libraries" {
  name      = "shared_preload_libraries"
  server_id = azurerm_postgresql_flexible_server.main.id
  value     = "pg_stat_statements,pg_cron"
}

# Extension uuid-ossp pour UUIDs
resource "azurerm_postgresql_flexible_server_configuration" "uuid_extension" {
  name      = "azure.extensions"
  server_id = azurerm_postgresql_flexible_server.main.id
  value     = "UUID-OSSP,PG_TRGM,POSTGIS"
}

# Stockage du mot de passe admin dans Key Vault
resource "azurerm_key_vault_secret" "admin_password" {
  name         = "postgresql-admin-password"
  value        = random_password.admin_password.result
  key_vault_id = var.key_vault_id
  
  content_type = "PostgreSQL Admin Password"
  
  tags = merge(var.tags, {
    SecretType = "Database"
  })
}

# Chaîne de connexion pour l'application
locals {
  connection_string = "postgresql://${var.admin_username}:${random_password.admin_password.result}@${azurerm_postgresql_flexible_server.main.fqdn}:5432/${azurerm_postgresql_flexible_server_database.main.name}?sslmode=require"
  connection_string_async = "postgresql+asyncpg://${var.admin_username}:${random_password.admin_password.result}@${azurerm_postgresql_flexible_server.main.fqdn}:5432/${azurerm_postgresql_flexible_server_database.main.name}?sslmode=require"
}

# Stockage de la chaîne de connexion dans Key Vault
resource "azurerm_key_vault_secret" "connection_string" {
  name         = "postgresql-connection-string"
  value        = local.connection_string_async
  key_vault_id = var.key_vault_id
  
  content_type = "PostgreSQL Connection String (AsyncPG)"
  
  tags = merge(var.tags, {
    SecretType = "Database"
  })
}

# Configuration de monitoring
resource "azurerm_monitor_diagnostic_setting" "postgresql_audit" {
  count = var.enable_database_audit ? 1 : 0
  
  name                       = "${var.app_name}-${var.environment}-psql-audit"
  target_resource_id         = azurerm_postgresql_flexible_server.main.id
  log_analytics_workspace_id = var.log_analytics_workspace_id
  
  enabled_log {
    category = "PostgreSQLLogs"
  }
  
  metric {
    category = "AllMetrics"
    enabled  = true
  }
}

# Alerte sur l'utilisation CPU
resource "azurerm_monitor_metric_alert" "cpu_usage" {
  count = var.enable_alerts ? 1 : 0
  
  name                = "${var.app_name}-${var.environment}-psql-cpu-alert"
  resource_group_name = var.resource_group_name
  scopes              = [azurerm_postgresql_flexible_server.main.id]
  description         = "Alert when PostgreSQL CPU usage is high"
  severity            = 2
  frequency           = "PT5M"
  window_size         = "PT15M"
  
  criteria {
    metric_namespace = "Microsoft.DBforPostgreSQL/flexibleServers"
    metric_name      = "cpu_percent"
    aggregation      = "Average"
    operator         = "GreaterThan"
    threshold        = 80
  }
  
  action {
    action_group_id = var.action_group_id
  }
  
  tags = var.tags
}

# Alerte sur l'utilisation de la mémoire
resource "azurerm_monitor_metric_alert" "memory_usage" {
  count = var.enable_alerts ? 1 : 0
  
  name                = "${var.app_name}-${var.environment}-psql-memory-alert"
  resource_group_name = var.resource_group_name
  scopes              = [azurerm_postgresql_flexible_server.main.id]
  description         = "Alert when PostgreSQL memory usage is high"
  severity            = 2
  frequency           = "PT5M"
  window_size         = "PT15M"
  
  criteria {
    metric_namespace = "Microsoft.DBforPostgreSQL/flexibleServers"
    metric_name      = "memory_percent"
    aggregation      = "Average"
    operator         = "GreaterThan"
    threshold        = 85
  }
  
  action {
    action_group_id = var.action_group_id
  }
  
  tags = var.tags
}

# Alerte sur l'utilisation du stockage
resource "azurerm_monitor_metric_alert" "storage_usage" {
  count = var.enable_alerts ? 1 : 0
  
  name                = "${var.app_name}-${var.environment}-psql-storage-alert"
  resource_group_name = var.resource_group_name
  scopes              = [azurerm_postgresql_flexible_server.main.id]
  description         = "Alert when PostgreSQL storage usage is high"
  severity            = 1
  frequency           = "PT5M"
  window_size         = "PT15M"
  
  criteria {
    metric_namespace = "Microsoft.DBforPostgreSQL/flexibleServers"
    metric_name      = "storage_percent"
    aggregation      = "Average"
    operator         = "GreaterThan"
    threshold        = 90
  }
  
  action {
    action_group_id = var.action_group_id
  }
  
  tags = var.tags
}
