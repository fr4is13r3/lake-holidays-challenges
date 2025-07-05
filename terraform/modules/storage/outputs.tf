# Outputs du module Storage

output "storage_account_id" {
  description = "ID du compte de stockage"
  value       = azurerm_storage_account.main.id
}

output "storage_account_name" {
  description = "Nom du compte de stockage"
  value       = azurerm_storage_account.main.name
}

output "storage_account_primary_endpoint" {
  description = "Endpoint principal du compte de stockage"
  value       = azurerm_storage_account.main.primary_blob_endpoint
}

output "storage_account_secondary_endpoint" {
  description = "Endpoint secondaire du compte de stockage"
  value       = azurerm_storage_account.main.secondary_blob_endpoint
}

output "storage_containers" {
  description = "Liste des containers créés"
  value = {
    audio     = azurerm_storage_container.audio.name
    documents = azurerm_storage_container.documents.name
    images    = azurerm_storage_container.images.name
    videos    = azurerm_storage_container.videos.name
    backups   = azurerm_storage_container.backups.name
  }
}

output "storage_urls" {
  description = "URLs des containers de stockage"
  value = {
    audio     = "${azurerm_storage_account.main.primary_blob_endpoint}${azurerm_storage_container.audio.name}/"
    documents = "${azurerm_storage_account.main.primary_blob_endpoint}${azurerm_storage_container.documents.name}/"
    images    = "${azurerm_storage_account.main.primary_blob_endpoint}${azurerm_storage_container.images.name}/"
    videos    = "${azurerm_storage_account.main.primary_blob_endpoint}${azurerm_storage_container.videos.name}/"
  }
}
