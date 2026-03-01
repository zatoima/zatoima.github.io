---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "GitHub .gitignore and git-secrets Configuration"
subtitle: ""
summary: " "
tags: ["Github"]
categories: ["Github"]
url: github-gitignore-git-secrets-setting
date: 2022-12-28
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: ""
  focal_point: ""
  preview_only: fals
---

### Overview

Notes on configuring `.gitignore` and `git-secrets` to prevent accidentally committing sensitive information like AWS access keys to GitHub.

### git-secrets Setup

`git-secrets` is a tool that scans commits and prevents you from accidentally committing secrets.

#### Installation

```sh
brew install git-secrets
```

#### Configure AWS Patterns

Register AWS credential patterns:

```sh
git secrets --register-aws --global
```

This adds patterns to detect:
- AWS access key IDs (`AKIA...`)
- AWS secret access keys
- AWS account IDs in ARNs

#### Install Hooks for a Repository

```sh
cd /path/to/your/repo
git secrets --install
```

This installs the following hooks:
- `commit-msg`
- `pre-commit`
- `prepare-commit-msg`

#### Install Hooks Globally (for all repositories)

```sh
git secrets --install ~/.git-templates/git-secrets
git config --global init.templateDir ~/.git-templates/git-secrets
```

All newly created or cloned repositories will automatically have the hooks installed.

#### Testing

Try to commit a file containing a fake AWS key:

```sh
echo "AKIAIOSFODNN7EXAMPLE" > test.txt
git add test.txt
git commit -m "test"
# Should be blocked with an error message
```

### .gitignore Configuration

A typical `.gitignore` for projects that work with AWS and Python:

```gitignore
# AWS credentials
.aws/
credentials
*.pem
*.key

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.env
venv/
env/
.venv/

# Jupyter Notebooks
.ipynb_checkpoints

# macOS
.DS_Store

# IDE
.idea/
.vscode/
*.swp
*.swo

# Sensitive config files
config.ini
secrets.yaml
*.secret
```

### Reference

- [awslabs/git-secrets: Prevents you from committing secrets and credentials into git repositories](https://github.com/awslabs/git-secrets)
