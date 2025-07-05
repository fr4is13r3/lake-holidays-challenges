# Module Monitoring - Azure Monitor et Log Analytics
# Configuration complète de la surveillance pour AKS

variable "resource_group_name" {
  description = "Nom du resource group"
  type        = string
}

variable "location" {
  description = "Région Azure"
  type        = string
}

variable "app_name" {
  description = "Nom de l'application"
  type        = string
}

variable "environment" {
  description = "Environnement (dev, staging, prod)"
  type        = string
}

variable "tags" {
  description = "Tags pour les ressources"
  type        = map(string)
  default     = {}
}

variable "notification_email" {
  description = "Email pour les notifications d'alertes"
  type        = string
  default     = ""
}

# Configuration locale
locals {
  workspace_name = "${var.app_name}-${var.environment}-logs"
}

# Log Analytics Workspace
resource "azurerm_log_analytics_workspace" "main" {
  name                = local.workspace_name
  location            = var.location
  resource_group_name = var.resource_group_name
  sku                 = "PerGB2018"
  retention_in_days   = var.environment == "prod" ? 90 : 30
  
  tags = var.tags
}

# Application Insights
resource "azurerm_application_insights" "main" {
  name                = "${var.app_name}-${var.environment}-ai"
  location            = var.location
  resource_group_name = var.resource_group_name
  workspace_id        = azurerm_log_analytics_workspace.main.id
  application_type    = "web"
  
  tags = var.tags
}

# Action Group pour les notifications (si email fourni)
resource "azurerm_monitor_action_group" "main" {
  count               = var.notification_email != "" ? 1 : 0
  name                = "${var.app_name}-${var.environment}-alerts"
  resource_group_name = var.resource_group_name
  short_name          = "alerts"

  email_receiver {
    name          = "admin-email"
    email_address = var.notification_email
  }

  tags = var.tags
}

# # Alerte pour la disponibilité des pods
# resource "azurerm_monitor_metric_alert" "pod_availability" {
#   count               = var.notification_email != "" ? 1 : 0
#   name                = "${var.app_name}-${var.environment}-pod-availability"
#   resource_group_name = var.resource_group_name
#   scopes              = [azurerm_log_analytics_workspace.main.id]
#   description         = "Alerte quand la disponibilité des pods est faible"
#   severity            = 2
#   frequency           = "PT5M"
#   window_size         = "PT15M"

#   criteria {
#     metric_namespace = "insights.container/pods"
#     metric_name      = "podCount"
#     aggregation      = "Average"
#     operator         = "LessThan"
#     threshold        = 1
#   }

#   action {
#     action_group_id = azurerm_monitor_action_group.main[0].id
#   }

#   tags = var.tags
# }

# # Alerte pour l'utilisation CPU élevée
# resource "azurerm_monitor_metric_alert" "high_cpu" {
#   count               = var.notification_email != "" ? 1 : 0
#   name                = "${var.app_name}-${var.environment}-high-cpu"
#   resource_group_name = var.resource_group_name
#   scopes              = [azurerm_log_analytics_workspace.main.id]
#   description         = "Alerte quand l'utilisation CPU est élevée"
#   severity            = 3
#   frequency           = "PT5M"
#   window_size         = "PT15M"

#   criteria {
#     metric_namespace = "insights.container/nodes"
#     metric_name      = "cpuUsagePercentage"
#     aggregation      = "Average"
#     operator         = "GreaterThan"
#     threshold        = 80
#   }

#   action {
#     action_group_id = azurerm_monitor_action_group.main[0].id
#   }

#   tags = var.tags
# }

# Dashboard pour le monitoring
resource "azurerm_portal_dashboard" "main" {
  name                = "${var.app_name}-${var.environment}-dashboard"
  resource_group_name = var.resource_group_name
  location            = var.location
  
  dashboard_properties = jsonencode({
    lenses = {
      "0" = {
        order = 0
        parts = {
          "0" = {
            position = {
              x = 0
              y = 0
              rowSpan = 4
              colSpan = 6
            }
            metadata = {
              inputs = [
                {
                  name = "resourceTypeMode"
                  isOptional = true
                }
              ]
              type = "Extension/Microsoft_Azure_Monitoring/PartType/MetricsChartPart"
            }
          }
        }
      }
    }
    metadata = {
      model = {
        timeRange = {
          value = {
            relative = {
              duration = 24
              timeUnit = 1
            }
          }
          type = "MsPortalFx.Composition.Configuration.ValueTypes.TimeRange"
        }
      }
    }
  })

  tags = var.tags
}
