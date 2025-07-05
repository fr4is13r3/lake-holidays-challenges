# Outputs du module Monitoring

output "log_analytics_workspace_id" {
  description = "ID du workspace Log Analytics"
  value       = azurerm_log_analytics_workspace.main.id
}

output "log_analytics_workspace_key" {
  description = "Clé primaire du workspace Log Analytics"
  value       = azurerm_log_analytics_workspace.main.primary_shared_key
  sensitive   = true
}

output "application_insights_id" {
  description = "ID d'Application Insights"
  value       = azurerm_application_insights.main.id
}

output "application_insights_instrumentation_key" {
  description = "Clé d'instrumentation Application Insights"
  value       = azurerm_application_insights.main.instrumentation_key
  sensitive   = true
}

output "application_insights_connection_string" {
  description = "Chaîne de connexion Application Insights"
  value       = azurerm_application_insights.main.connection_string
  sensitive   = true
}

output "dashboard_id" {
  description = "ID du dashboard de monitoring"
  value       = azurerm_portal_dashboard.main.id
}
