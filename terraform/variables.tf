variable "environment" {
  description = "Environment name (dev, test, prod)"
  type        = string
  validation {
    condition     = contains(["DEV", "TEST", "PROD"], var.environment)
    error_message = "Environment must be dev, test, or prod."
  }
}

variable "app_version" {
  description = "Application version to deploy"
  type        = string
  default     = "1.0.0"
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "Canada East"
}

variable "app_name" {
  description = "Base application name"
  type        = string
  default     = "todo_app"
}

variable "subscription_id" {
  description = "Azure subscription ID"
  type        = string
}