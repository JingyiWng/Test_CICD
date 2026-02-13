# Test_CICD
Project: Automated Python Web API Deployment to Azure

A simple Python Flask/FastAPI REST API that gets automatically deployed to Azure App Service using GitHub Actions, with proper release tagging and infrastructure managed by Terraform.

Project Breakdown: Todo API with Clean Version Tracking

Clean Version Strategy:

Tags are clean versions: v1.0.0, v1.1.0, v1.2.0 (no suffixes)
Each tag represents a point-in-time snapshot of code
Environments deploy specific tagged versions

Version Tracking:
We'll use GitHub Environments feature (free!) to track which version is deployed where:

DEV environment (develop branch)→ shows "v1.2.0"
TEST environment (test branch) → shows "v1.1.0"
PROD environment (main branch) → shows "v1.0.0"

Plus a deployment-history.md file in repo tracking all deployments.

Instead of merging branches, we deploy specific tags to specific environments.




Running Terraform å
    cd terraform
    terraform init


    **What this does:**
    - Downloads Azure provider plugin
    - Creates `.terraform/` directory
    - Sets up backend


Step 10: Deploy DEV Environment
A) Plan the deployment (see what will be created):
    terraform plan \
    -var="environment=dev" \
    -var="app_version=1.0.0"

B) Apply (create the resources):
    terraform apply \
    -var="environment=dev" \
    -var="app_version=1.0.0"

app_service_default_hostname = "app-todo-app-dev.azurewebsites.net"
app_service_name = "app-todo-app-dev"
app_service_url = "https://app-todo-app-dev.azurewebsites.net"
resource_group_name = "rg-todo-app-dev"

Step 11: Verify Deployment
A) Test the URL (will show default page for now):
curl https://app-todo-app-dev.azurewebsites.net
You'll get a default Azure page since we haven't deployed code yet.


Step 12: Deploy TEST Environment
Using separate state per environment:
Option A: Using workspace (recommended):
bash # Create workspace
terraform workspace new test
terraform workspace select test

bash # Deploy
terraform apply \
  -var="environment=test" \
  -var="app_version=1.0.0"


Step 13: Deploy PROD Environment
bash 
terraform workspace new prod
terraform workspace select prod

terraform apply \
  -var="environment=prod" \
  -var="app_version=1.0.0"



Step 14: Verification & Testing List All Resources
bash # List workspaces
terraform workspace list

bash # Check current workspace
terraform workspace show

bash # See what's deployed
terraform show

Check in Azure CLI:
bash # List all resource groups you created
az group list --query "[?contains(name, 'todo-api')]" --output table
bash # List app services
az webapp list --query "[?contains(name, 'todo-api')]" --output table