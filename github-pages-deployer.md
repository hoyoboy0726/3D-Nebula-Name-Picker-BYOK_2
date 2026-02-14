---
name: github-pages-deployer
description: Automates deployment to GitHub Pages using GitHub Actions. Handles Git initialization, remote creation, Vite configuration (base path), and workflow setup.
---

# GitHub Pages Deployer

Automates deployment to GitHub Pages using GitHub Actions.

## Workflow

1. Verify Git and GH CLI.
2. For Vite projects, set base path in config.
3. Initialize Git and create remote via gh repo create.
4. Create .github/workflows/deploy.yml.
5. Push and enable Pages via API (gh api -X PATCH /repos/:owner/:repo/pages -F build_type=workflow).
6. Monitor with gh run watch.
