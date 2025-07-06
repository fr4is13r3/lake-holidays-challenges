# Module AKS - Azure Kubernetes Service
# Configuration complète du cluster Kubernetes pour Lake Holidays Challenge

# Variables du module AKS
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

variable "kubernetes_version" {
  description = "Version de Kubernetes"
  type        = string
  default     = "1.27"
}

variable "node_count" {
  description = "Nombre de nœuds par défaut"
  type        = number
  default     = 2
}

variable "vm_size" {
  description = "Taille des VMs pour les nœuds"
  type        = string
  default     = "Standard_D2s_v3"
}

variable "enable_auto_scaling" {
  description = "Activer l'auto-scaling"
  type        = bool
  default     = true
}

variable "min_count" {
  description = "Nombre minimum de nœuds"
  type        = number
  default     = 1
}

variable "max_count" {
  description = "Nombre maximum de nœuds"
  type        = number
  default     = 5
}

variable "container_registry_id" {
  description = "ID du Container Registry"
  type        = string
}

variable "log_analytics_workspace_id" {
  description = "ID du workspace Log Analytics"
  type        = string
}

variable "key_vault_id" {
  description = "ID du Key Vault"
  type        = string
}

# Configuration locale
locals {
  cluster_name = "${var.app_name}-${var.environment}-aks"
  dns_prefix   = "${var.app_name}-${var.environment}"
}

# Cluster AKS principal
resource "azurerm_kubernetes_cluster" "main" {
  name                = local.cluster_name
  location            = var.location
  resource_group_name = var.resource_group_name
  dns_prefix          = local.dns_prefix
  kubernetes_version  = var.kubernetes_version

  # AJOUT: Nom personnalisé pour le resource group des nœuds
  node_resource_group = "${var.resource_group_name}_aks"

  # Configuration du node pool par défaut
  default_node_pool {
    name                = "default"
    node_count          = var.node_count
    vm_size             = var.vm_size
    enable_auto_scaling = var.enable_auto_scaling
    min_count           = var.enable_auto_scaling ? var.min_count : null
    max_count           = var.enable_auto_scaling ? var.max_count : null
    os_disk_size_gb     = 30
    type                = "VirtualMachineScaleSets"
    
    # Configuration réseau
    vnet_subnet_id = azurerm_subnet.aks.id
    
    # Labels pour le node pool
    node_labels = {
      "nodepool" = "default"
      "environment" = var.environment
    }
    
    tags = var.tags
  }

  # Configuration de l'identité (System Assigned)
  identity {
    type = "SystemAssigned"
  }

  # Configuration réseau
  network_profile {
    network_plugin    = "azure"
    network_policy    = "azure"
    dns_service_ip    = "10.0.0.10"
    service_cidr      = "10.0.0.0/16"
  }

  # Configuration de la surveillance
  oms_agent {
    log_analytics_workspace_id = var.log_analytics_workspace_id
  }

  # Configuration des add-ons
  ingress_application_gateway {
    gateway_name = "${local.cluster_name}-agw"
    subnet_cidr  = "10.225.0.0/16"
  }

  # Key Vault Secrets Provider
  key_vault_secrets_provider {
    secret_rotation_enabled  = true
    secret_rotation_interval = "2m"
  }

  tags = var.tags

  lifecycle {
    ignore_changes = [
      default_node_pool[0].node_count
    ]
  }
}

# Virtual Network pour AKS
resource "azurerm_virtual_network" "aks" {
  name                = "${local.cluster_name}-vnet"
  address_space       = ["10.224.0.0/12"]
  location            = var.location
  resource_group_name = var.resource_group_name
  tags                = var.tags
}

# Subnet pour les nœuds AKS
resource "azurerm_subnet" "aks" {
  name                 = "${local.cluster_name}-subnet"
  resource_group_name  = var.resource_group_name
  virtual_network_name = azurerm_virtual_network.aks.name
  address_prefixes     = ["10.224.0.0/16"]
}

# Node Pool pour les charges de travail applicatives
resource "azurerm_kubernetes_cluster_node_pool" "apps" {
  name                  = "apps"
  kubernetes_cluster_id = azurerm_kubernetes_cluster.main.id
  vm_size               = var.vm_size
  node_count            = var.node_count
  enable_auto_scaling   = var.enable_auto_scaling
  min_count             = var.enable_auto_scaling ? var.min_count : null
  max_count             = var.enable_auto_scaling ? var.max_count : null
  
  # Configuration du stockage
  os_disk_size_gb = 50
  os_type         = "Linux"
  
  # Configuration réseau
  vnet_subnet_id = azurerm_subnet.aks.id
  
  # Labels et taints pour la séparation des charges
  node_labels = {
    "nodepool" = "apps"
    "workload" = "application"
    "environment" = var.environment
  }
  
  node_taints = [
    "workload=application:NoSchedule"
  ]
  
  tags = var.tags
}

# Permissions pour accéder au Container Registry
resource "azurerm_role_assignment" "aks_acr_pull" {
  scope                = var.container_registry_id
  role_definition_name = "AcrPull"
  principal_id         = azurerm_kubernetes_cluster.main.kubelet_identity[0].object_id
}

# Permissions pour accéder au Key Vault
resource "azurerm_role_assignment" "aks_keyvault_reader" {
  scope                = var.key_vault_id
  role_definition_name = "Key Vault Reader"
  principal_id         = azurerm_kubernetes_cluster.main.kubelet_identity[0].object_id
}

# Permissions supplémentaires pour le CSI driver du Key Vault
resource "azurerm_role_assignment" "aks_keyvault_secrets_user" {
  scope                = var.key_vault_id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = azurerm_kubernetes_cluster.main.key_vault_secrets_provider[0].secret_identity[0].object_id
}
