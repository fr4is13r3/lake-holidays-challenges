# Module Redis Cache pour Lake Holidays Challenge

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.80"
    }
  }
}

# Azure Cache for Redis
resource "azurerm_redis_cache" "main" {
  name                = "${var.app_name}-${var.environment}-redis"
  location            = var.location
  resource_group_name = var.resource_group_name
  capacity            = var.capacity
  family              = var.family
  sku_name            = var.sku_name
  enable_non_ssl_port = false
  minimum_tls_version = "1.2"
  redis_version       = var.redis_version

  # Configuration selon le SKU
  dynamic "redis_configuration" {
    for_each = var.sku_name == "Premium" ? [1] : []
    content {
      enable_authentication           = true
      maxmemory_reserved              = 10
      maxmemory_delta                 = 2
      maxmemory_policy               = "allkeys-lru"
      rdb_backup_enabled             = true
      rdb_backup_frequency           = 60
      rdb_backup_max_snapshot_count  = 1
      rdb_storage_connection_string  = var.backup_storage_connection_string
    }
  }

  # Patch schedule pour les mises à jour (Premium uniquement)
  dynamic "patch_schedule" {
    for_each = var.sku_name == "Premium" ? [1] : []
    content {
      day_of_week    = "Sunday"
      start_hour_utc = 2
    }
  }

  tags = var.tags
}

# Firewall rules pour Redis
resource "azurerm_redis_firewall_rule" "azure_services" {
  name               = "AllowAzureServices"
  redis_cache_name   = azurerm_redis_cache.main.name
  resource_group_name = var.resource_group_name
  start_ip           = "0.0.0.0"
  end_ip             = "0.0.0.0"
}

# Règles de pare-feu personnalisées
resource "azurerm_redis_firewall_rule" "custom_rules" {
  for_each = var.firewall_rules

  name               = each.key
  redis_cache_name   = azurerm_redis_cache.main.name
  resource_group_name = var.resource_group_name
  start_ip           = each.value.start_ip
  end_ip             = each.value.end_ip
}

# Chaîne de connexion Redis
locals {
  redis_connection_string = "redis://:${azurerm_redis_cache.main.primary_access_key}@${azurerm_redis_cache.main.hostname}:${azurerm_redis_cache.main.ssl_port}/0?ssl_cert_reqs=required"
}

# Stockage de la chaîne de connexion dans Key Vault
resource "azurerm_key_vault_secret" "connection_string" {
  name         = "redis-connection-string"
  value        = local.redis_connection_string
  key_vault_id = var.key_vault_id

  content_type = "Redis Connection String"

  tags = merge(var.tags, {
    SecretType = "Cache"
  })
}

# Stockage de la clé primaire dans Key Vault
resource "azurerm_key_vault_secret" "primary_access_key" {
  name         = "redis-primary-access-key"
  value        = azurerm_redis_cache.main.primary_access_key
  key_vault_id = var.key_vault_id

  content_type = "Redis Primary Access Key"

  tags = merge(var.tags, {
    SecretType = "Cache"
  })
}

# Configuration de monitoring
resource "azurerm_monitor_diagnostic_setting" "redis_audit" {
  count = var.enable_redis_audit ? 1 : 0

  name                       = "${var.app_name}-${var.environment}-redis-audit"
  target_resource_id         = azurerm_redis_cache.main.id
  log_analytics_workspace_id = var.log_analytics_workspace_id

  metric {
    category = "AllMetrics"
    enabled  = true
  }
}

# Alertes de monitoring
resource "azurerm_monitor_metric_alert" "redis_cpu" {
  count = var.enable_alerts ? 1 : 0

  name                = "${var.app_name}-${var.environment}-redis-cpu-alert"
  resource_group_name = var.resource_group_name
  scopes              = [azurerm_redis_cache.main.id]
  description         = "Alert when Redis CPU usage is high"
  severity            = 2
  frequency           = "PT5M"
  window_size         = "PT15M"

  criteria {
    metric_namespace = "Microsoft.Cache/Redis"
    metric_name      = "percentProcessorTime"
    aggregation      = "Average"
    operator         = "GreaterThan"
    threshold        = 80
  }

  action {
    action_group_id = var.action_group_id
  }

  tags = var.tags
}

resource "azurerm_monitor_metric_alert" "redis_memory" {
  count = var.enable_alerts ? 1 : 0

  name                = "${var.app_name}-${var.environment}-redis-memory-alert"
  resource_group_name = var.resource_group_name
  scopes              = [azurerm_redis_cache.main.id]
  description         = "Alert when Redis memory usage is high"
  severity            = 2
  frequency           = "PT5M"
  window_size         = "PT15M"

  criteria {
    metric_namespace = "Microsoft.Cache/Redis"
    metric_name      = "usedmemorypercentage"
    aggregation      = "Average"
    operator         = "GreaterThan"
    threshold        = 85
  }

  action {
    action_group_id = var.action_group_id
  }

  tags = var.tags
}

resource "azurerm_monitor_metric_alert" "redis_connections" {
  count = var.enable_alerts ? 1 : 0

  name                = "${var.app_name}-${var.environment}-redis-connections-alert"
  resource_group_name = var.resource_group_name
  scopes              = [azurerm_redis_cache.main.id]
  description         = "Alert when Redis connection count is high"
  severity            = 3
  frequency           = "PT5M"
  window_size         = "PT15M"

  criteria {
    metric_namespace = "Microsoft.Cache/Redis"
    metric_name      = "connectedclients"
    aggregation      = "Average"
    operator         = "GreaterThan"
    threshold        = 100
  }

  action {
    action_group_id = var.action_group_id
  }

  tags = var.tags
}
