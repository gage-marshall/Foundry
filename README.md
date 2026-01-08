# Foundry Engine

A modern, secure, and blazingly fast static site engine built with FastAPI. Designed for rapid deployment of 1-5 page sites with a focus on security, reliability, and speed.

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

## Quick Start

Foundry Engine can be used in two ways:

### Option A: Monorepo (Development/Testing)

1. **Clone and setup**
   ```bash
   git clone <repository-url>
   cd foundry
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run**
   ```bash
   python main.py
   ```

Visit `http://localhost:8000` to see your site!

### Option B: As Dependency (Recommended for Production)

**Perfect for separating engine from site content in production.**

1. **Install from GitHub** (in your site repo)
   ```bash
   pip install git+ssh://git@github.com/yourorg/foundry-engine.git@main
   ```

2. **Create site entry point**
   ```python
   # main.py
   from pathlib import Path
   from foundry_engine import create_app

   app = create_app(site_path=Path(__file__).parent)
   ```

3. **Run your site**
   ```bash
   python main.py
   ```

📚 See [INTEGRATION.md](docs/INTEGRATION.md) for complete setup guide.

## Project Structure

### Monorepo Structure (Development)
```
foundry/
├── foundry_engine/          # Core engine (Python package)
│   ├── __init__.py         # Exports create_app()
│   ├── app.py              # FastAPI application factory
│   ├── config.py           # Configuration models
│   ├── security/           # Security modules
│   ├── mail/               # Email providers
│   ├── navigation/         # Navigation types
│   ├── sections/           # Section types
│   ├── templates/          # Jinja2 templates
│   ├── routers/            # API routes
│   └── utils/              # Utilities
│
├── sites/                  # Site-specific content
│   └── example_site/       # Ready to move to separate repo
│       ├── main.py         # Standalone entry point
│       ├── pyproject.toml  # Defines engine dependency
│       ├── config.yaml     # Site configuration
│       ├── content/
│       │   ├── pages/      # Page definitions (YAML)
│       │   └── sections/   # Section content (Markdown)
│       ├── theme/
│       │   └── custom.css  # Site theme
│       └── assets/         # Images, etc.
│
├── docs/
│   ├── INTEGRATION.md      # Using as dependency guide
│   ├── STYLING.md          # Styling and content guide
│   └── ...
├── main.py                 # Example entry point
├── pyproject.toml          # Engine package definition
└── requirements.txt        # Engine dependencies
```

### Separate Repo Structure (Production)
```
[foundry-engine]            ← Engine repository
└── foundry_engine/         (Imported as dependency)

[my-website]                ← Site repository
├── main.py                 (Imports foundry-engine)
├── pyproject.toml          (References engine from GitHub)
├── config.yaml
├── content/
├── theme/
└── assets/
```

## Creating a New Site

1. **Create site directory structure**
```bash
mkdir -p sites/mysite/{content/pages,content/sections,theme,assets/images}
```

2. **Create config.yaml**
```yaml
site:
  name: "My Site"
  domain: "mysite.com"
  description: "My awesome site"

security:
  allowed_hosts:
    - "mysite.com"
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
  from_email: "noreply@mysite.com"
  contact_recipient: "hello@mysite.com"

pages:
  - home
  - about
```

3. **Create page definitions** (e.g., `content/pages/home.yaml`)
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

4. **Write content** (e.g., `content/sections/hero.md`)
```markdown
# Welcome to My Site

## Making the web beautiful, one site at a time
```

5. **Customize theme** (`theme/custom.css`)
```css
:root {
  --color-primary: #your-color;
}
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

## Deployment

### Production Deployment to Render

Foundry uses **Gunicorn** with **Uvicorn workers** for production deployment, providing:
- ✅ Multiple worker processes for reliability
- ✅ Automatic worker restart on failure
- ✅ Graceful shutdown handling
- ✅ Zero-downtime deployments
- ✅ Optimized for async workloads

1. **Push to Git**
```bash
git init
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Connect to Render**
- Create a new Web Service on Render
- Connect your repository
- Render will detect `render.yaml` automatically
- Automatically uses Gunicorn configuration

3. **Configure environment variables**
Set these in the Render dashboard:
- `SECRET_KEY` (auto-generated or set manually)
- `BREVO_API_KEY` (or your chosen email provider)
- `GUNICORN_WORKERS` (optional, auto-calculated by default)
- Any other sensitive configuration

4. **Deploy**
Render will automatically build and deploy your site with Gunicorn!

### Manual Production Deployment

For VPS or other hosting:

```bash
# Linux/Mac
./start.sh

# Windows
.\start.ps1

# Or directly with gunicorn
gunicorn main:app -c gunicorn.conf.py
```

### Gunicorn Configuration

The `gunicorn.conf.py` file provides optimized settings:
- **Workers**: Auto-calculated (2-4 per CPU core, max 8)
- **Worker Class**: `uvicorn.workers.UvicornWorker` (ASGI support)
- **Timeout**: 30 seconds
- **Max Requests**: 1000 per worker (prevents memory leaks)
- **Graceful Timeout**: 30 seconds
- **Preload App**: Enabled (faster startup, memory sharing)

Override workers with environment variable:
```bash
export GUNICORN_WORKERS=4
gunicorn main:app -c gunicorn.conf.py
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
Configure in `sites/yoursite/config.yaml`:
```yaml
security:
  allowed_hosts:
    - "yourdomain.com"
    - "www.yourdomain.com"
    - "*.onrender.com"
```

## Development

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

## Using Foundry as a Dependency

### For New Sites

See [INTEGRATION.md](docs/INTEGRATION.md) for complete guide on:
- Setting up a site repository that imports Foundry Engine
- Installing from private GitHub repositories
- Deployment with SSH keys and deploy keys
- Version pinning strategies
- Troubleshooting

### Example Implementation

Check out `sites/example_site/` which demonstrates:
- Standalone entry point (`main.py`)
- Dependency configuration (`pyproject.toml`, `requirements.txt`)
- Site-specific environment setup (`.env.example`)
- Complete documentation (`README.md`)

This directory is ready to be moved to its own repository!

## Documentation

- [Integration Guide](docs/INTEGRATION.md) - Using as dependency
- [Styling Guide](docs/STYLING.md) - Customization and content
- [Quick Start](QUICKSTART.md) - Get started fast
- [Development Guide](DEVELOPMENT.md) - Contributing
- [Deployment Guide](DEPLOYMENT.md) - Production deployment

## License

Proprietary source-available - see LICENSE file for details

---

Built with ❤️ using FastAPI, Jinja2, and modern Python
