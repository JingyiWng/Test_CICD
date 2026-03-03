# CICD Learning Project
**Purpose:**
The purpose of this project is to get hands-on with CI/CD. 

**Overview:**
Automated Python Web API Deployment to Azure

A simple Python Flask/FastAPI REST API that gets automatically deployed to Azure App Service using GitHub Actions, with proper release tagging and infrastructure managed by Terraform.

**Project Flow:**
1. Dev<br>
Development will be done in the feature branches. Once done, these changes will be merged to the "develop" branch. 
No tags are created at this stage.
CI/CD pipeline is automatically triggered by the push to the "develop" branch, and deployment will happen in the dev environment. 
2. Test<br>
Once the results look good in dev, "develop" branch will be merged to the "realease/x.x.x" branch (e.g., realease/1.4.0). 
We can create the tag "v1.4.0-rc" once the code is ready for release.
CI/CD pipeline is automatically triggered by the push to the "realease/x.x.x" branch, and deployment will happen in the test environment. 
3. Prod<br>
Once the results look good in test, "realease/x.x.x" branch will be merged to the "main" branch. 
We can create the tag "v1.4.0" to indicate the release version.
CI/CD pipeline is automatically triggered by the push to the "main" branch.
Upon approval (configured in Github Environments), deployment will happen in the prod environment. 

## Project Breakdown: How I structured the project week by week:
#### **Phase 1: Foundation (Week 1)**<br>
- Step 1: Local Python API Setup (the app folder). Deliverable: Working API on localhost:8000
- Step 2: Git Repository & Initial Tagging. Deliverable: Repo with branches and first tag<br>
#### **Phase 2: Infrastructure (Week 2)**
- Step 3: Terraform Multi-Environment Setup (3 Resource Groups: rg-todo-dev, rg-todo-test, rg-todo-prod, and 3 App Services with app_settings)<br>
#### **Phase 3: CI/CD Pipeline (Week 3)**
- Step 4: Manual Deployment Workflow in Dev. Deliverable: Manual deployment workflow ready (manual trigger workflow_dispatch in file .github/workflows/deploy.yml)
- Step 5: Automated Deployment in Dev. Deliverable: Automated deployment workflow ready (trigger based on push to branch)<br>
#### **Phase 4: Version Management (Week 4)**
- Step 6: Multi-Version Workflow. E.g. dev is v1.5.0, test and prod are v1.4.0.<br>

Below, I will cover some important areas/topics around my CI/CD implementation. <br>
Note that there are multiple ways to implement tagging / branching workflows (e.g. gitflow, trunk-based workflows).  <br>
The solution I used below is one of the many possible ways. Happy to hear any feedback or comments.

## Topic 1: Which branch -> which environment
dev environment (develop branch)→ auto-deploy, no approval<br>
test environment (release/1.4.0 branch) → auto-deploy, optional approval<br>
prod environment (main branch) → auto-deploy, requires approval<br>

Plus a deployment-history.md file in repo tracking all deployments.<br>


### **Common Workflow**

**Pattern 1: GitFlow (with release branches)**
```
develop → release/1.4.0 → main
   ↓            ↓           ↓
  DEV         TEST        PROD
```
**Pattern 2: Trunk-based (no release branches)**
```
develop → staging → main
   ↓         ↓       ↓
  DEV      TEST    PROD
```


---


## Topic 2: Tags
Tag and What It Contains<br>
v1.0.0 Python app + tests empty folder (Phase 1)<br>
v1.1.0 Python app + tests empty folder + Terraform (Phase 2) NO Python code deployed ❌<br>
v1.2.0 Python app + tests empty folder + Terraform + GitHub Actions (Phase 3)<br>

> **Note:** Tags point to a **commit**, not a branch — they don't care which branch we're on.

Commit History Example

```
A --- B --- C --- D --- E   (develop branch)
      |           |
    v1.0.0      v1.1.0      ← Tags point to specific commits
```


### Where Tags Are Created

```
develop branch:
  └─ (optional) dev-v1.3.0       ← Development milestone

release/1.2.0 branch:
  └─ v1.2.0-rc                   ← When merged to test

main branch:
  └─ v1.2.0                      ← Official release tag ✅
```


### Tagging Workflow

**1. Develop in `develop` (no tag yet)**
```bash
git checkout develop
# ... work on v1.2.0 ...
```

**2. Create release branch (optional tag)**
```bash
git checkout -b release/1.2.0
git tag v1.2.0-rc
git push origin release/1.2.0 --tags
```

**3. After testing passes, deploy to PROD**
```bash
git checkout main
git merge release/1.2.0
git tag v1.2.0          # ← Official tag on main
git push origin main --tags
```


### Scenario: Bug Found in TEST

```
develop:        v1.5.0 features (ahead)
release/1.4.0:  v1.4.0 (in TEST, has bug) ← fix here
If I find a bug in 1.4.0 while testing, what do I do?
```

**1. Fix bug in release branch**
```bash
git checkout release/1.4.0
# ... fix the bug ...
git commit -m "Fix critical bug in v1.4.0"
git push origin release/1.4.0
# → Auto-deploys to TEST (re-test the fix)
```

**2. Update tag (optional)**
```bash
git tag -f v1.4.0-rc2           # New release candidate
git push origin v1.4.0-rc2 --force
```

**3. Re-test in TEST environment**

**4. After testing passes, merge to main**
```bash
git checkout main
git merge release/1.4.0
git tag v1.4.0
git push origin main --tags
# → Deploys to PROD
```

**5. IMPORTANT: Merge fix back to `develop`**
```bash
git checkout develop
git merge release/1.4.0         # Bring the bug fix to develop
# Or cherry-pick specific commits:
git cherry-pick <commit-hash-of-bug-fix>
git push origin develop
```

---


## Topic 3: Terraform

### Using separate state per environment:

TEST
```bash
# Create and select workspace
terraform workspace new test
terraform workspace select test

# Deploy
terraform apply \
  -var="environment=test" \
  -var="app_version=1.0.0"
```

PROD
```bash
terraform workspace new prod
terraform workspace select prod

terraform apply \
  -var="environment=prod" \
  -var="app_version=1.0.0"
```


### Verification & Testing

```bash
# List workspaces
terraform workspace list

# Check current workspace
terraform workspace show

# See what's deployed
terraform show
```

**Check in Azure CLI:**
```bash
# List all resource groups
az group list --query "[?contains(name, 'todo-api')]" --output table

# List app services
az webapp list --query "[?contains(name, 'todo-api')]" --output table
```

---



## Topic 4: GitHub Runner (Ubuntu VM) vs Azure

> Everything in the workflow runs on the **GitHub Runner** — EXCEPT the final deployed app.

```
┌─────────────────────────────────────────────────────────┐
│              GitHub Runner (Ubuntu VM)                  │
├─────────────────────────────────────────────────────────┤
│  ✅ Checkout code                                       │
│  ✅ Install Python & dependencies                       │
│  ✅ Run tests                                           │
│  ✅ Login to Azure (authenticate)                       │
│  ✅ Install Terraform                                   │
│  ✅ Run terraform init / plan / apply                   │
│     └─> Makes API calls to Azure to create resources    │
│  ✅ Deploy code to Azure                                │
│     └─> Uploads code to Azure App Service               │
└──────────────────────────┬──────────────────────────────┘
                           │  API calls & file uploads
                           ▼
┌─────────────────────────────────────────────────────────┐
│                     Azure Cloud                         │
├─────────────────────────────────────────────────────────┤
│  ✅ Resource Group      (created by Terraform)          │
│  ✅ App Service Plan    (created by Terraform)          │
│  ✅ App Service         (created by Terraform)          │
│  ✅ My Python app     (uploaded by GitHub Actions)      │
│     └─> RUNS HERE 24/7                                  │
└─────────────────────────────────────────────────────────┘
```


**Analogy:**
- GitHub runner = My laptop
- Terraform = A program on my laptop
- Azure = A remote server
- Terraform on my laptop *tells* Azure to create things

---

**On Azure (Permanent, running my app):**

**My Python app runs here:**
```
Azure App Service
├─ Receives my code from GitHub Actions
├─ Detects it's a Python app
├─ Runs: uvicorn app.main:app --host 0.0.0.0 --port 8000
└─ Serves requests at https://app-todo-api-test.azurewebsites.net
```
> This is **permanent** — runs 24/7 (or until we stop it), accessible via public URL. 


### **Flow Diagram:**

```
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
                                                  │   (My app runs here)  │
User requests:                                    │   ├─ app/               │
https://app-todo-api-test.azurewebsites.net ─────>│   ├─ main.py            │
                                                  │   └─ Running 24/7       │
                                                  └─────────────────────────┘

```
