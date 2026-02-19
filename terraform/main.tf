terraform {
  required_version = ">= 1.0"
  
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}

# Resource Group
resource "azurerm_resource_group" "rg" {
  name     = "rg-${var.app_name}-${var.environment}"
  location = var.location

  tags = {
    Environment = var.environment
    Application = var.app_name
    ManagedBy   = "Terraform"
  }
}

# App Service Plan
resource "azurerm_service_plan" "asp" {
  name                = "asp-${var.app_name}-${var.environment}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  os_type             = "Linux"
  
  # Free tier for dev/test/prod
  sku_name = "F1"

  tags = {
    Environment = var.environment
    Application = var.app_name
  }
}

# App Service (Web App)
resource "azurerm_linux_web_app" "webapp" {
  name                = "appservice-${var.app_name}-${var.environment}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  service_plan_id     = azurerm_service_plan.asp.id

  site_config {
    # Free tier doesn't support always_on
    always_on = false
    
    application_stack {
      python_version = "3.11"
    }

    # Startup command. Azure defaults to looking for Flask apps (app.py), not FastAPI. 
    # We set this up, so that Azure knows HOW to start your FastAPI app
    # uvicorn app.main:app starts FastAPI with uvicorn server. --host 0.0.0.0 allows external connections. --port 8000 matches Azure's expected port
    app_command_line = "python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"

    # Health check endpoint
    health_check_path = "/health"
  }

  app_settings = {
    "ENVIRONMENT"                    = var.environment
    "APP_VERSION"                    = var.app_version
    "SCM_DO_BUILD_DURING_DEPLOYMENT" = "true"
    "WEBSITES_PORT"                  = "8000"
  }

  tags = {
    Environment     = var.environment
    Application     = var.app_name
    DeployedVersion = var.app_version
  }
}