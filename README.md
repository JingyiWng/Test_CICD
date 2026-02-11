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