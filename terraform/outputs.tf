output "resource_group_name" {
  description = "Name of the resource group"
  value       = azurerm_resource_group.rg.name
}

output "app_service_name" {
  description = "Name of the App Service"
  value       = azurerm_linux_web_app.webapp.name
}

output "app_service_default_hostname" {
  description = "Default hostname of the App Service"
  value       = azurerm_linux_web_app.webapp.default_hostname
}

output "app_service_url" {
  description = "Full URL of the deployed application"
  value       = "https://${azurerm_linux_web_app.webapp.default_hostname}"
}