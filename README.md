# Foundry Engine

A modern, secure, and blazingly fast static site engine built with FastAPI. Designed as a **Python package** for rapid deployment of 1-5 page sites with a focus on security, reliability, and speed.

## Features

### Security First
- **JWT Authentication**: Optional per-site JWT protection
- **CSRF Protection**: Built-in CSRF token validation for forms
- **Rate Limiting**: Configurable rate limiting per endpoint
- **Security Headers**: Comprehensive security headers (CSP, HSTS, X-Frame-Options, etc.)
- **Input Validation**: Pydantic-based validation for all inputs

### Performance
- **Async/Await**: Fully async throughout the stack
- **Fast Response**: Optimized template rendering and caching
- **Minimal Dependencies**: Lean dependency tree for fast deployments
- **Static Asset Optimization**: Efficient static file serving

### Developer Experience
- **Configuration-Driven**: YAML for structure, Markdown for content
- **Hot Reload**: Development mode with auto-reload
- **Type Safety**: Full type hints with Pydantic models
- **Clear Separation**: Engine updates don't affect site content

## Installation

Foundry Engine is designed to be installed as a **Python package** in your site repository.

### Install from GitHub

```bash
# SSH (recommended for private repos)
pip install git+ssh://git@github.com/yourorg/foundry-engine.git@main

# HTTPS
pip install git+https://github.com/yourorg/foundry-engine.git@main
```

### Or via pyproject.toml

```toml
[project]
dependencies = [
    "foundry-engine @ git+ssh://git@github.com/yourorg/foundry-engine.git@main",
]
```

## Quick Start

### 1. Create Your Site Repository

```bash
mkdir my-website
cd my-website
mkdir -p content/pages content/sections theme assets/images
```

### 2. Create Entry Point

**File: `main.py`**
```python
from pathlib import Path
from foundry_engine import create_app

# Your site directory contains: config.yaml, content/, theme/, assets/
app = create_app(site_path=Path(__file__).parent)
```

### 3. Create Site Configuration

**File: `config.yaml`**
```yaml
site:
  name: "My Website"
  domain: "mywebsite.com"
  description: "My awesome site"

security:
  allowed_hosts:
    - "mywebsite.com"
    - "*.onrender.com"

navigation:
  type: "top_ribbon"
  items:
    - text: "Home"
      url: "/"
    - text: "About"
      url: "/about"

mail:
  provider: "brevo"
  from_email: "noreply@mywebsite.com"
  contact_recipient: "hello@mywebsite.com"

pages:
  - home
  - about
```

### 4. Create Page Definition

**File: `content/pages/home.yaml`**
```yaml
page:
  slug: "home"
  title: "Welcome"
  meta_description: "Welcome to my site"

sections:
  - type: "hero"
    content: "sections/hero.md"
    config:
      height: "100vh"
      text_align: "center"
      cta_button:
        text: "Learn More"
        url: "/about"
```

### 5. Write Content

**File: `content/sections/hero.md`**
```markdown
# Welcome to My Site

## Making the web beautiful, one site at a time
```

### 6. Customize Theme

**File: `theme/custom.css`**
```css
:root {
  --color-primary: #your-color;
}
```

### 7. Run Development Server

```bash
python main.py
```

Visit `http://localhost:8000`

## Project Structure

### Your Site Repository

```
my-website/                 ← Your site repository
├── main.py                 (Imports foundry-engine)
├── pyproject.toml          (Defines engine dependency)
├── .env                    (Environment variables)
├── config.yaml             (Site configuration)
├── content/
│   ├── pages/             (Page definitions - YAML)
│   └── sections/          (Section content - Markdown)
├── theme/
│   └── custom.css         (Site-specific styles)
└── assets/
    └── images/            (Images, fonts, etc.)
```

### Engine Package (Imported)

```
foundry-engine/            ← Installed as dependency
└── foundry_engine/
    ├── app.py            (FastAPI application factory)
    ├── config.py         (Configuration models)
    ├── security/         (Security modules)
    ├── mail/             (Email providers)
    ├── navigation/       (Navigation types)
    ├── sections/         (Section types)
    ├── templates/        (Jinja2 templates)
    └── routers/          (API routes)
```

## Built-in Section Types

- **hero**: Hero sections with background images/videos and CTAs
- **parallax**: Parallax scrolling sections
- **gallery**: Photo galleries (grid, masonry, carousel)
- **text**: Rich markdown content sections
- **contact**: Contact forms with validation
- **cta**: Call-to-action sections
- **features**: Feature grids with icons
- **testimonials**: Testimonials/reviews
- **footer**: Flexible footer layouts

## Navigation Types

- **top_ribbon**: Classic top navigation bar
- **hamburger**: Mobile-friendly hamburger menu
- **sidebar**: Vertical sidebar navigation

## Email Providers

Configure email in `.env`:

### Brevo (Sendinblue)
```env
MAIL_PROVIDER=brevo
BREVO_API_KEY=your-api-key
```

### Mailgun
```env
MAIL_PROVIDER=mailgun
MAILGUN_API_KEY=your-api-key
MAILGUN_DOMAIN=mg.yourdomain.com
```

### SMTP
```env
MAIL_PROVIDER=smtp
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USERNAME=your-username
SMTP_PASSWORD=your-password
```

## Production Deployment

### Deployment to Render

1. **Create `render.yaml` in your site repo:**
```yaml
services:
  - type: web
    name: my-website
    env: python
    buildCommand: pip install -e .
    startCommand: gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

2. **Set environment variables in Render dashboard:**
   - `SECRET_KEY` (auto-generate or set manually)
   - `BREVO_API_KEY` (or your email provider)
   - Any other sensitive configuration

3. **Deploy!** Render auto-detects and deploys.

### Manual Deployment

```bash
# Install dependencies
pip install -e .

# Run with gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Security Configuration

### Environment Variables
```env
# Required
SECRET_KEY=your-secret-key-here-32-chars-minimum

# Optional - JWT
JWT_SECRET_KEY=your-jwt-secret
JWT_ENABLED=false  # Enable in site config.yaml

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=10
```

### Allowed Hosts
Configure in `config.yaml`:
```yaml
security:
  allowed_hosts:
    - "yourdomain.com"
    - "www.yourdomain.com"
    - "*.onrender.com"
```

## Engine Development

### Clone Engine Repository

```bash
git clone <engine-repo-url>
cd foundry-engine
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Run Tests
```bash
pytest
```

### Format Code
```bash
black foundry_engine/
ruff check foundry_engine/
```

### Type Checking
```bash
mypy foundry_engine/
```

## Documentation

- **[Integration Guide](docs/INTEGRATION.md)** - Complete guide for using as a package
- **[Quick Start](docs/QUICKSTART.md)** - Get started fast
- **[Styling Guide](docs/STYLING.md)** - Customization and content
- **[Development Guide](docs/DEVELOPMENT.md)** - Contributing to the engine
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Production deployment strategies

## Updating the Engine

### Update to Latest

```bash
pip install --upgrade --force-reinstall git+ssh://git@github.com/yourorg/foundry-engine.git@main
```

### Pin to Specific Version

```toml
# Pin to version tag
"foundry-engine @ git+ssh://git@github.com/yourorg/foundry-engine.git@v0.1.0"

# Pin to commit hash (maximum stability)
"foundry-engine @ git+ssh://git@github.com/yourorg/foundry-engine.git@abc123def"
```

## Version Pinning Strategy

- **Development**: Track `main` branch for latest features
- **Staging**: Use version tags (e.g., `v0.2.0`)
- **Production**: Pin to specific commit hashes for stability

## License

Proprietary source-available - see LICENSE file for details

---

Built with ❤️ using FastAPI, Jinja2, and modern Python
