# Outputs du module AKS

output "cluster_id" {
  description = "ID du cluster AKS"
  value       = azurerm_kubernetes_cluster.main.id
}

output "cluster_name" {
  description = "Nom du cluster AKS"
  value       = azurerm_kubernetes_cluster.main.name
}

output "cluster_fqdn" {
  description = "FQDN du cluster AKS"
  value       = azurerm_kubernetes_cluster.main.fqdn
}

output "kube_config" {
  description = "Configuration kubectl pour le cluster"
  value       = azurerm_kubernetes_cluster.main.kube_config
  sensitive   = true
}

output "kube_config_raw" {
  description = "Configuration kubectl brute"
  value       = azurerm_kubernetes_cluster.main.kube_config_raw
  sensitive   = true
}

output "kubelet_identity" {
  description = "Identité du kubelet"
  value       = azurerm_kubernetes_cluster.main.kubelet_identity
}

output "cluster_identity" {
  description = "Identité du cluster"
  value       = azurerm_kubernetes_cluster.main.identity
}

output "application_gateway_ingress_controller_enabled" {
  description = "Statut de l'Application Gateway Ingress Controller"
  value       = azurerm_kubernetes_cluster.main.ingress_application_gateway
}

output "virtual_network_id" {
  description = "ID du virtual network"
  value       = azurerm_virtual_network.aks.id
}

output "subnet_id" {
  description = "ID du subnet AKS"
  value       = azurerm_subnet.aks.id
}

output "node_resource_group" {
  description = "Resource group des nœuds AKS"
  value       = azurerm_kubernetes_cluster.main.node_resource_group
}
