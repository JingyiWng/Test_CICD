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

DEV environment (develop branch)→ shows "v1.2.0" (auto-deploy, no approval)
TEST environment (test branch) → shows "v1.1.0" (auto-deploy, optional approval)
PROD environment (main branch) → shows "v1.0.0" (auto-deploy, requires approval)

Plus a deployment-history.md file in repo tracking all deployments.

Instead of merging branches, we deploy specific tags to specific environments.


**Most companies use ONE of these:**

### **Pattern 1: GitFlow (with release branches)**
develop → release/1.4.0 → main
   ↓            ↓           ↓
  DEV         TEST        PROD

### **Pattern 2: Trunk-based (no release branches)**
develop → staging → main
   ↓         ↓       ↓
  DEV      TEST    PROD


Tag and What It Contains
v1.0.0 Python app + tests empty folder (Phase 1)
v1.1.0 Python app + tests empty folder + Terraform (Phase 2) NO Python code deployed ❌
v1.2.0 Python app + tests empty folder + Terraform + GitHub Actions (Phase 3)

Tags don't care which branch you're on - they point to a commit, not a branch.
Commit History:
A --- B --- C --- D --- E  (develop branch)
      |           |
    v1.0.0      v1.1.0  ← Tags point to specific commits


## **Where Tags Are Actually Created:**
develop branch:
  └─ (optional) dev-v1.3.0  ← Development milestone

release/1.2.0 branch:
  └─ v1.2.0-rc  ← When merged to test

main branch:
  └─ v1.2.0  ← Official release tag ✅

Tagging Workflow:
- 1. Develop in develop (no tag yet)
git checkout develop
... work on v1.2.0 ...

- 2. Create release branch (optional tag)
git checkout -b release/1.2.0
git tag v1.2.0-rc
git push origin release/1.2.0 --tags

- 3. After testing passes, deploy to PROD
git checkout main
git merge release/1.2.0
git tag v1.2.0  # ← Official tag on main
git push origin main --tags





## **Scenario: Bug found in TEST**
develop: v1.5.0 features (ahead)
release/1.4.0: v1.4.0 (in TEST, has bug)
You found a bug in v1.4.0 while testing. What do you do?
# 1. Fix bug in release branch
git checkout release/1.4.0
# ... fix the bug ...
git commit -m "Fix critical bug in v1.4.0"
git push origin release/1.4.0
# → Auto-deploys to TEST (re-test the fix)

# 2. Update tag (optional)
git tag -f v1.4.0-rc2  # New release candidate
git push origin v1.4.0-rc2 --force

# 3. Re-test in TEST environment
# ... testing ...

# 4. After testing passes, merge to main
git checkout main
git merge release/1.4.0
git tag v1.4.0
git push origin main --tags
# → Deploys to PROD

# 5. IMPORTANT: Merge fix back to develop
git checkout develop
git merge release/1.4.0  # Bring the bug fix to develop
# Or cherry-pick specific commits:
git cherry-pick <commit-hash-of-bug-fix>
git push origin develop




Running Terraform
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





GitHub Runner (Ubuntu VM) vs Azure
Everything in the workflow runs on GitHub's runner EXCEPT the final deployed app:
┌─────────────────────────────────────────────────────────┐
│           GitHub Runner (Ubuntu VM)                      │
├─────────────────────────────────────────────────────────┤
│ ✅ Checkout code                                         │
│ ✅ Install Python                                        │
│ ✅ Install dependencies                                  │
│ ✅ Run tests                                             │
│ ✅ Login to Azure (authenticate)                         │
│ ✅ Install Terraform                                     │
│ ✅ Run terraform init/plan/apply                         │
│    └─> Makes API calls to Azure to create resources     │
│ ✅ Deploy code to Azure                                  │
│    └─> Uploads code to Azure App Service                │
└─────────────────────────────────────────────────────────┘
                    │
                    │ API calls & file uploads
                    ↓
┌─────────────────────────────────────────────────────────┐
│                    Azure Cloud                           │
├─────────────────────────────────────────────────────────┤
│ ✅ Resource Group (created by Terraform)                 │
│ ✅ App Service Plan (created by Terraform)               │
│ ✅ App Service (created by Terraform)                    │
│ ✅ Your Python app (uploaded by GitHub Actions)          │
│    └─> RUNS HERE 24/7                                   │
└─────────────────────────────────────────────────────────┘
Analogy:

GitHub runner = Your laptop
Terraform = A program on your laptop
Azure = Remote server
Terraform on your laptop tells Azure to create things

**On Azure (Permanent, running your app):**

**Your Python app runs here:**
```
Azure App Service
├─ Receives your code from GitHub Actions
├─ Detects it's a Python app
├─ Runs: uvicorn app.main:app --host 0.0.0.0 --port 8000
└─ Serves requests at https://app-todo-api-test.azurewebsites.net
```

**This is PERMANENT:**
- Runs 24/7 (or until you stop it)
- Accessible via public URL
- Users hit this, not the GitHub runner

## **Flow Diagram:**
GitHub Actions Workflow (on GitHub runner):
┌──────────────────────────────────────────┐
│ 1. Checkout code from repo               │
│ 2. Install Python & dependencies         │
│ 3. Run tests (on runner)                 │
│ 4. Authenticate with Azure               │
│ 5. Run Terraform ────────────────────────┼──> API calls ──> Azure creates resources
│ 6. Deploy code ──────────────────────────┼──> Upload ────> Azure App Service
└──────────────────────────────────────────┘
                                                  
After workflow completes:                         ┌─────────────────────────┐
GitHub runner is DELETED ✓                        │   Azure App Service     │
                                                  │   (Your app runs here)  │
User requests:                                    │   ├─ app/               │
https://app-todo-api-test.azurewebsites.net ─────>│   ├─ main.py            │
                                                  │   └─ Running 24/7       │
                                                  └─────────────────────────┘



