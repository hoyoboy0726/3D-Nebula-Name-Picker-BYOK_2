import os

def update_skill():
    target_dir = r"C:\Users\GU605_PR_MZ\.gemini\skills\github-pages-deployer"
    file_path = os.path.join(target_dir, "SKILL.md")
    
    content = """---
name: github-pages-deployer
description: Automates deployment to GitHub Pages using GitHub Actions. Handles Git initialization, remote creation, Vite configuration (base path), and workflow setup.
---

# GitHub Pages Deployer

Automates deployment to GitHub Pages using GitHub Actions.

## Prerequisites
1. **Git & GitHub CLI**: Ensure `git` and `gh` are installed and authenticated (`gh auth status`).
2. **Lock File Policy**:
   - If `package-lock.json` (npm) or `yarn.lock` (yarn) is missing, DO NOT ask the user to run `npm install` locally.
   - Proceed with the workflow; the CI template will handle dependency installation using `npm install --legacy-peer-deps`.

## Workflow

### 1. Project Configuration
- **Vite Projects**:
  - Read `vite.config.ts`.
  - Add `base: '/<REPO_NAME>/'` to the configuration object.

### 2. Git Initialization (Windows Safe)
- **⚠️ IMPORTANT**: Do NOT use `&&` to chain commands. Execute each command individually.
- Commands: `git init`, `git add .`, `git commit`, `gh repo create`.

### 3. Create Deployment Workflow
Create file: `.github/workflows/deploy.yml`
**Use this verified template:**

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
        run: npm install --legacy-peer-deps
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
1. Push changes to the remote.
2. **Enable via API**:
   - `gh api -X POST /repos/:owner/:repo/pages -F build_type=workflow`
   - If 409 (Conflict), it means Pages is already enabled.
   - If 403 (Forbidden), check if the `gh` user matches the repo owner and has admin rights.

### 5. Proactive Monitoring (MANDATORY)
- **DO NOT ask the user to monitor progress.**
- The agent MUST proactively run `gh run watch` or repeatedly poll `gh run view <RUN_ID>` until the deployment reaches a terminal state (`success` or `failure`).
- If failure occurs, analyze logs (`gh run view --log-failed`) and attempt automatic fixes.

## Post-Mortem & Lessons Learned
| Issue | Root Cause | Fix |
| :--- | :--- | :--- |
| **Missing Lock File** | Cache failure in CI | Use `--legacy-peer-deps` and skip local npm install requirement. |
| **User Monitoring** | Passive agent behavior | Mandate proactive polling using `gh run watch`. |
| **Auth Mismatch** | `gh` user != repo owner | Verify auth status and owner matching before API calls. |
"""
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        
    with open(file_path, "w", encoding="utf-8", newline='
') as f:
        f.write(content.strip() + '
')
    
    print(f"Successfully updated {file_path}")

if __name__ == "__main__":
    update_skill()
