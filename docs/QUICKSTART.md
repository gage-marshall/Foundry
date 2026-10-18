# Foundry Engine - Quick Start Guide

Get your first site running in 10 minutes using Foundry Engine as a package!

## Prerequisites

- Python 3.11+
- Git
- SSH access to the Foundry Engine repository (or use HTTPS)

## Step 1: Create Your Site Repository

```bash
# Create new directory for your site
mkdir my-website
cd my-website

# Initialize git
git init

# Create directory structure
mkdir -p content/pages content/sections theme assets/images
```

## Step 2: Install Foundry Engine

### Option A: Using pyproject.toml (Recommended)

Create `pyproject.toml`:
```toml
[project]
name = "my-website"
version = "0.1.0"
requires-python = ">=3.11"

dependencies = [
    "foundry-engine @ git+https://github.com/gage-marshall/Foundry.git@master",
]

[build-system]
requires = ["setuptools>=68.0.0", "wheel"]
build-backend = "setuptools.build_meta"
```

Then install:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
```

### Option B: Direct Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install git+https://github.com/gage-marshall/Foundry.git@master
```

## Step 3: Create Entry Point

Create `main.py`:
```python
from pathlib import Path
from foundry_engine import create_app

# Site path is current directory
app = create_app(site_path=Path(__file__).parent)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

## Step 4: Configure Your Site

Create `config.yaml`:
```yaml
site:
  name: "My Website"
  domain: "mywebsite.com"
  description: "My awesome website"

security:
  allowed_hosts:
    - "mywebsite.com"
    - "localhost"
    - "127.0.0.1"
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

## Step 5: Create Environment File

Create `.env`:
```env
# Application
FOUNDRY_ENV=development

# Security (generate with: openssl rand -hex 32)
SECRET_KEY=your-secret-key-here-generate-with-openssl-rand-hex-32

# Email Provider
MAIL_PROVIDER=brevo
BREVO_API_KEY=your-brevo-api-key

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=10
```

## Step 6: Create Your First Page

Create `content/pages/home.yaml`:
```yaml
page:
  slug: "home"
  title: "Welcome to My Website"
  meta_description: "Welcome to my awesome website"

sections:
  - type: "hero"
    content: "sections/hero.md"
    config:
      height: "100vh"
      text_align: "center"
      background_color: "#1a1a2e"
      cta_button:
        text: "Learn More"
        url: "/about"

  - type: "features"
    content: "sections/features.md"
    config:
      columns: 3
      features:
        - icon: "⚡"
          title: "Fast"
          description: "Lightning-fast performance"
        - icon: "🔒"
          title: "Secure"
          description: "Built-in security features"
        - icon: "🎨"
          title: "Beautiful"
          description: "Modern, clean design"
```

## Step 7: Write Content

Create `content/sections/hero.md`:
```markdown
# Welcome to My Website

## Building something amazing
```

Create `content/sections/features.md`:
```markdown
## Our Features

Check out what makes us special
```

## Step 8: Customize Theme

Create `theme/custom.css`:
```css
:root {
  /* Colors */
  --color-primary: #6366f1;
  --color-secondary: #8b5cf6;
  --color-accent: #ec4899;

  /* Fonts */
  --font-primary: 'Inter', sans-serif;
  --font-heading: 'Montserrat', sans-serif;
}

/* Add your custom styles here */
```

## Step 9: Run Your Site

```bash
python main.py
```

Visit: http://localhost:8000

## Next Steps

### Add More Pages

1. Create page YAML: `content/pages/about.yaml`
2. Add sections markdown
3. Already listed in `config.yaml` pages array!

### Customize Styling

Edit `theme/custom.css` to match your brand

### Add Contact Form

Create `content/pages/contact.yaml`:
```yaml
page:
  slug: "contact"
  title: "Contact Us"

sections:
  - type: "contact"
    content: "sections/contact-intro.md"
    config:
      fields:
        - name: "name"
          type: "text"
          label: "Your Name"
          required: true
        - name: "email"
          type: "email"
          label: "Your Email"
          required: true
        - name: "message"
          type: "textarea"
          label: "Message"
          required: true
      submit_text: "Send Message"
```

### Deploy to Production

See [Deployment Guide](DEPLOYMENT.md) for production deployment options.

## Common Issues

### Module Not Found

```bash
# Make sure virtual environment is activated
source .venv/bin/activate

# Reinstall engine
pip install --force-reinstall git+https://github.com/gage-marshall/Foundry.git@master
```

### Config Not Found

Make sure you're running from the correct directory:
```bash
cd my-website  # Directory containing config.yaml
python main.py
```

### Email Not Working

1. Get API key from your email provider (Brevo, Mailgun, etc.)
2. Add to `.env` file
3. Restart server

## Available Section Types

- `hero` - Hero sections with CTAs
- `text` - Rich markdown content
- `features` - Feature grids
- `gallery` - Photo galleries
- `contact` - Contact forms
- `cta` - Call-to-action
- `parallax` - Parallax scrolling
- `testimonials` - Customer testimonials
- `footer` - Page footers

## Need Help?

- Check [Integration Guide](INTEGRATION.md) for detailed documentation
- Review [Styling Guide](STYLING.md) for customization options
- See [Development Guide](DEVELOPMENT.md) for extending the engine

Happy building! 🚀
