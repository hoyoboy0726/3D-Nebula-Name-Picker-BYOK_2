import os
target_dir = r"C:\Users\GU605_PR_MZ\.gemini\skills\github-pages-deployer"
file_path = os.path.join(target_dir, "SKILL.md")
content = r"""---
name: github-pages-deployer
description: Automates deployment to GitHub Pages using GitHub Actions. Handles Git initialization, remote creation, Vite configuration (base path), and workflow setup.
---

# GitHub Pages Deployer

Automates deployment to GitHub Pages using GitHub Actions.

## Prerequisites
1. **Git & GitHub CLI**: Ensure `git` and `gh` are installed and authenticated (`gh auth status`).
2. **Lock File**: Ensure `package-lock.json` (npm) or `yarn.lock` (yarn) exists.
   - *Reason*: `actions/setup-node` caching relies on this. If missing, run `npm install` locally before starting, or remove `cache: 'npm'` from the workflow.

## Workflow

### 1. Project Configuration
- **Vite Projects**:
  - Read `vite.config.ts`.
  - Add `base: '/<REPO_NAME>/'` to the configuration object.
  - *Example*: `base: '/3d-nebula-name-picker/',`

### 2. Git Initialization (Windows Safe)
- **⚠️ IMPORTANT**: Do NOT use `&&` to chain commands in Windows CMD/PowerShell. Execute each command individually.
- Commands:
  1. `git init`
  2. `git add .`
  3. `git commit -m "initial commit"`
  4. `gh repo create <REPO_NAME> --public --source=. --push --remote=origin`

### 3. Create Deployment Workflow
Create file: `.github/workflows/deploy.yml`
**Use this verified template (fixes `${{ steps.deployment }}` dot notation and Node setup):**

```yaml
name: Deploy static content to Pages

on:
  push:
    branches: ["master", "main"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Set up Node
        uses: actions/setup-node@v4
        with:
          node-version: 20
      - name: Install dependencies
        run: npm install
      - name: Build
        run: npm run build
      - name: Setup Pages
        uses: actions/configure-pages@v4
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: './dist'
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

### 4. Push and Enable Pages
1. `git add .`
2. `git commit -m "Configure GitHub Pages deployment"`
3. `git push origin master` (or main)
4. **Enable via API**:
   - First, try to create: `gh api -X POST /repos/:owner/:repo/pages -F build_type=workflow`
   - If it exists, update: `gh api -X PATCH /repos/:owner/:repo/pages -F build_type=workflow`

### 5. Monitor Deployment
- Run `gh run watch` to track the progress.

## Post-Mortem & Lessons Learned
| Issue | Root Cause | Skill Gap Fixed |
| :--- | :--- | :--- |
| **Command Chaining** | Windows CMD doesn't support `&&` | Added explicit warning against `&&` for Windows users. |
| **Workflow Syntax** | Used `steps:deployment` (colon) instead of `steps.deployment` (dot) | Provided a verified template in the skill. |
| **CI Cache Failure** | `setup-node` failed without `package-lock.json` | Added prerequisite check for lock files. |
| **Pages API 404** | `PATCH` failed because Pages wasn't initialized | Updated API flow to use `POST` for initialization. |
"""
if not os.path.exists(target_dir): os.makedirs(target_dir)
with open(file_path, "wb") as f:
    f.write(content.strip().encode("utf-8").replace(b"
", b"
") + b"
")
"""
print(f"Successfully updated {file_path}")
"""
