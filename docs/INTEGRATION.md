# Integration Guide: Using Foundry Engine as a Dependency

This guide explains how to use Foundry Engine as an imported dependency from a private GitHub repository, enabling clean separation between engine and site code.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Setup Guide](#setup-guide)
- [Repository Structure](#repository-structure)
- [Installation Methods](#installation-methods)
- [Deployment](#deployment)
- [Updating the Engine](#updating-the-engine)
- [Troubleshooting](#troubleshooting)

---

## Overview

### Why Use Foundry as a Dependency?

**Benefits:**
- ✅ **Clean separation** - Engine updates don't affect site code
- ✅ **Multiple sites** - Run many sites with one engine version
- ✅ **Version control** - Pin sites to specific engine versions
- ✅ **Easy updates** - Update engine across all sites at once
- ✅ **Standard workflow** - Use pip like any other dependency

### Repository Setup

```
[foundry-engine]          ← Engine repository (installed as package)
└── foundry_engine/

[my-website]              ← Your site repository
├── main.py              (imports foundry_engine)
├── pyproject.toml       (defines engine dependency)
├── config.yaml
├── content/
└── theme/
```

---

## Architecture

### How It Works

1. **Engine Repository**: Contains `foundry_engine/` package (this repo)
2. **Your Site Repository**: Imports engine via `pip install git+https://...` or pyproject.toml
3. **Site Entry Point**: Calls `create_app(site_path=Path(__file__).parent)`
4. **Deployment**: Deployment platform installs engine automatically from GitHub

### Directory Structure

**Engine Repo (foundry-engine)**
```
foundry-engine/
├── foundry_engine/           # Python package
│   ├── __init__.py          # Exports create_app()
│   ├── app.py               # Application factory
│   ├── config.py            # Configuration models
│   ├── templates/           # Jinja2 templates
│   ├── static/              # Base CSS/JS
│   └── ...
├── pyproject.toml           # Package metadata
└── README.md
```

**Site Repo (my-website)**
```
my-website/
├── main.py                  # Entry point (imports engine)
├── pyproject.toml          # Defines engine dependency
├── requirements.txt        # Alternative dependency file
├── .env                    # Environment variables
├── config.yaml             # Site configuration
├── content/
│   ├── pages/             # Page YAML files
│   └── sections/          # Markdown content
├── theme/
│   └── custom.css         # Site-specific styles
└── assets/                # Images, fonts, etc.
```

---

## Setup Guide

### Step 1: Prepare Engine Repository

Your engine repository should already be ready if you're reading this. Ensure:

1. Engine is committed and pushed to GitHub
2. Repository is either public or you have SSH access
3. `foundry_engine/__init__.py` exports `create_app`

### Step 2: Create Site Repository

```bash
# Create new site directory
mkdir my-website
cd my-website

# Initialize git
git init
git branch -M master
```

### Step 3: Create Site Structure

```bash
# Create directory structure
mkdir -p content/pages content/sections theme assets/images

# Create entry point
touch main.py

# Create configuration files
touch config.yaml
touch .env
touch .gitignore
```

### Step 4: Create Entry Point

**File: `main.py`**
```python
"""
My Website - Entry Point
"""

import uvicorn
from pathlib import Path
from foundry_engine import create_app

# Site directory is current directory
SITE_PATH = Path(__file__).parent

# Create app with explicit site path
app = create_app(site_path=SITE_PATH)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
```

### Step 5: Define Engine Dependency

Choose **either** `pyproject.toml` **or** `requirements.txt`:

**Option A: pyproject.toml** (recommended)
```toml
[project]
name = "my-website"
version = "0.1.0"
requires-python = ">=3.11"

dependencies = [
    # SSH authentication (recommended for private repos)
    "foundry-engine @ git+https://github.com/gage-marshall/Foundry.git@master",
]

[build-system]
requires = ["setuptools>=68.0.0", "wheel"]
build-backend = "setuptools.build_meta"
```

**Option B: requirements.txt**
```txt
# Install engine from private GitHub repo
git+https://github.com/gage-marshall/Foundry.git@master
```

### Step 6: Create Site Configuration

**File: `config.yaml`**
```yaml
site:
  name: "My Website"
  domain: "mywebsite.com"
  description: "My awesome website"

security:
  allowed_hosts:
    - "mywebsite.com"
    - "*.onrender.com"
  jwt_enabled: false
  csrf_enabled: true

navigation:
  type: "top_ribbon"
  sticky: true
  items:
    - text: "Home"
      url: "/"
    - text: "About"
      url: "/about"
    - text: "Contact"
      url: "/contact"

mail:
  provider: "brevo"
  from_email: "noreply@mywebsite.com"
  from_name: "My Website"
  contact_recipient: "hello@mywebsite.com"

pages:
  - home
  - about
  - contact

theme_css: "theme/custom.css"
```

### Step 7: Create Environment File

**File: `.env`**
```ini
# Application
FOUNDRY_ENV=development

# Security
SECRET_KEY=your-secret-key-generate-with-openssl-rand-hex-32
ALLOWED_HOSTS=localhost,127.0.0.1,mywebsite.com

# Email (example with Brevo)
MAIL_PROVIDER=brevo
BREVO_API_KEY=your-brevo-api-key
MAIL_FROM_EMAIL=noreply@mywebsite.com

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=10
```

### Step 8: Create .gitignore

```gitignore
# Environment
.env
.venv/
venv/
__pycache__/
*.pyc

# IDE
.idea/
.vscode/
*.swp

# OS
.DS_Store
Thumbs.db
```

---

## Installation Methods

### Local Development

#### Using pyproject.toml

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install in editable mode (includes engine from GitHub)
pip install -e .

# Run
python main.py
```

#### Using requirements.txt

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run
python main.py
```

### SSH Authentication Setup

For private repositories, you need SSH authentication:

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add to SSH agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Copy public key
cat ~/.ssh/id_ed25519.pub

# Add to GitHub:
# Settings > SSH and GPG keys > New SSH key
```

Test connection:
```bash
ssh -T git@github.com
# Should respond: "Hi username! You've successfully authenticated..."
```

### HTTPS Authentication (Alternative)

Using Personal Access Token (PAT):

```bash
# Create token: GitHub Settings > Developer settings > Personal access tokens
# Select scopes: repo (all)

# Install with token in URL (not recommended - use SSH instead)
pip install git+https://<USERNAME>:<TOKEN>@github.com/gage-marshall/Foundry.git@master
```

---

## Deployment

### Render

**Setup Steps:**

1. **Create New Web Service** on Render
2. **Connect Repository**: Link your site repository
3. **Add SSH Private Key**:
   - Go to Environment variables
   - Add `SSH_PRIVATE_KEY` with your private key content
   - Render will use this to access the engine repo

4. **Set Environment Variables**:
   ```
   SECRET_KEY=<generated>
   BREVO_API_KEY=<your-key>
   FOUNDRY_ENV=production
   ```

5. **Build Command** (auto-detected from render.yaml or set manually):
   ```bash
   pip install -r requirements.txt
   ```

6. **Start Command**:
   ```bash
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

**Using Deploy Keys (Alternative)**:

1. Generate deploy key on your machine:
   ```bash
   ssh-keygen -t ed25519 -f deploy_key -N ""
   ```

2. Add **public key** to engine repo:
   - GitHub > Engine Repo > Settings > Deploy keys
   - Paste `deploy_key.pub` content
   - ✅ Allow read access

3. Add **private key** to Render:
   - Environment variable: `SSH_PRIVATE_KEY`
   - Value: content of `deploy_key` file

### Railway / Fly.io / Other Platforms

Similar process:
1. Add SSH private key as secret
2. Set environment variables
3. Platform auto-detects Python app
4. Installs dependencies (including engine from GitHub)
5. Runs with gunicorn or uvicorn

### VPS / Manual Deployment

```bash
# On server
git clone git@github.com:yourorg/my-website.git
cd my-website

python -m venv .venv
source .venv/bin/activate

# Install dependencies (will fetch engine from GitHub)
pip install -r requirements.txt

# Create .env with production values
nano .env

# Run with gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

---

## Updating the Engine

### Update to Latest Master Branch

```bash
# Local development
pip install --upgrade --force-reinstall git+https://github.com/gage-marshall/Foundry.git@master

# Or if using pyproject.toml
pip install --upgrade --force-reinstall -e .
```

### Pin to Specific Version

**Edit pyproject.toml or requirements.txt:**

```toml
# Pin to version tag
"foundry-engine @ git+https://github.com/gage-marshall/Foundry.git@v0.1.0"

# Pin to specific commit (maximum stability)
"foundry-engine @ git+https://github.com/gage-marshall/Foundry.git@abc123def456"
```

Then reinstall:
```bash
pip install --upgrade --force-reinstall git+https://github.com/gage-marshall/Foundry.git@v0.1.0
```

### Version Pinning Strategy

**Development**: Track `master` branch
```toml
git+https://github.com/gage-marshall/Foundry.git@master
```

**Staging**: Use version tags
```toml
git+https://github.com/gage-marshall/Foundry.git@v0.2.0
```

**Production**: Pin to specific commit
```toml
git+https://github.com/gage-marshall/Foundry.git@abc123def456789
```

### Testing Engine Updates

```bash
# Create test branch
git checkout -b test-engine-v0.2.0

# Update dependency
# Edit pyproject.toml or requirements.txt

# Reinstall
pip install --upgrade --force-reinstall -e .

# Test thoroughly
python main.py

# If good, merge to master
git checkout master
git merge test-engine-v0.2.0
```

---

## Troubleshooting

### Problem: SSH Authentication Fails

**Symptoms:**
```
fatal: Could not read from remote repository
Permission denied (publickey)
```

**Solutions:**

1. Verify SSH key is added to GitHub:
   ```bash
   ssh -T git@github.com
   ```

2. Check SSH agent:
   ```bash
   eval "$(ssh-agent -s)"
   ssh-add ~/.ssh/id_ed25519
   ssh-add -l  # List loaded keys
   ```

3. Use deploy keys instead of personal SSH keys (for deployment platforms)

### Problem: Module Not Found

**Symptoms:**
```
ModuleNotFoundError: No module named 'foundry_engine'
```

**Solutions:**

1. Reinstall dependencies:
   ```bash
   pip install --force-reinstall -r requirements.txt
   ```

2. Verify installation:
   ```bash
   pip list | grep foundry
   ```

3. Check virtual environment is activated:
   ```bash
   which python  # Should show .venv path
   ```

### Problem: Site Path Not Found

**Symptoms:**
```
FileNotFoundError: Site path does not exist
```

**Solutions:**

1. Verify you're using programmatic site path:
   ```python
   # In main.py
   SITE_PATH = Path(__file__).parent
   app = create_app(site_path=SITE_PATH)
   ```

2. Check directory structure:
   ```bash
   ls -la  # Should see config.yaml, content/, theme/
   ```

3. Run from correct directory:
   ```bash
   cd path/to/your-site
   python main.py
   ```

### Problem: Deployment Platform Can't Access Engine Repo

**Symptoms:**
```
ERROR: Repository not found
```

**Solutions:**

1. **For Render/Railway**: Add SSH private key as environment variable

2. **Use Deploy Keys** (recommended):
   - Generate dedicated key: `ssh-keygen -f deploy_key -N ""`
   - Add public key to engine repo (Settings > Deploy keys)
   - Add private key to deployment platform as secret

3. **Check firewall**: Ensure platform can access github.com

### Problem: Wrong Engine Version Installed

**Symptoms:**
```
AttributeError: 'FoundryEngine' has no attribute 'new_feature'
```

**Solutions:**

1. Check installed version:
   ```bash
   pip show foundry-engine
   ```

2. Force reinstall specific version:
   ```bash
   pip install --force-reinstall git+https://github.com/gage-marshall/Foundry.git@v0.2.0
   ```

3. Clear pip cache:
   ```bash
   pip cache purge
   pip install --no-cache-dir -r requirements.txt
   ```

---

## Best Practices

### Version Control

1. **Never commit `.env`** - Use `.env.example` as template
2. **Pin production versions** - Use commit hashes for stability
3. **Tag engine releases** - Use semantic versioning (v1.0.0, v1.1.0, etc.)

### Security

1. **Use SSH keys** - More secure than HTTPS tokens
2. **Use deploy keys** - Limit access to specific repositories
3. **Rotate keys regularly** - Especially after team member changes
4. **Keep secrets in environment** - Never hardcode in code

### Development Workflow

1. **Test engine updates locally first**
2. **Use branches** - Test updates in separate branches
3. **Document changes** - Note which engine version each site uses
4. **Automated tests** - Create tests before updating engine

### Multi-Site Management

If managing multiple sites:

```bash
# Site 1 - Production (stable)
git+https://github.com/gage-marshall/Foundry.git@v1.0.0

# Site 2 - Staging (latest features)
git+https://github.com/gage-marshall/Foundry.git@master

# Site 3 - Beta (testing new engine)
git+https://github.com/gage-marshall/Foundry.git@v2.0.0-beta
```

---

## Additional Resources

- [Foundry Engine README](../README.md) - Main documentation
- [Quick Start Guide](QUICKSTART.md) - Get started fast
- [Styling Guide](STYLING.md) - Content and customization
- [Development Guide](DEVELOPMENT.md) - Contributing to the engine
- [Deployment Guide](DEPLOYMENT.md) - Production deployment

---

## Need Help?

- Open an issue in the engine repository
- Review this guide's troubleshooting section
- Check the Quick Start guide for basic setup

**Happy building!** 🚀
