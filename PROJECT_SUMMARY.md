# Foundry Engine - Project Summary

## Overview

Foundry is a production-ready FastAPI-based web engine for serving static sites (1-5 pages typical, any number supported). It emphasizes **security**, **reliability**, and **speed** while maintaining a clean separation between the reusable engine and site-specific content.

## Key Design Decisions

### 1. Separation of Concerns
- **Engine Code** (`foundry_engine/`): Version controlled, reusable, updates don't affect sites
- **Site Content** (`sites/`): YAML configs, Markdown content, CSS themes
- Updates to engine don't require changes to existing sites

### 2. Configuration-Driven Architecture
- **YAML**: Page structure, section configuration, site settings
- **Markdown**: Rich text content with full markdown support
- **CSS**: Theme customization with CSS variables

### 3. Security First
- **JWT Authentication**: Optional per-site, configurable
- **CSRF Protection**: Built-in token validation for all forms
- **Rate Limiting**: Configurable per-endpoint using slowapi
- **Security Headers**: CSP, HSTS, X-Frame-Options, etc.
- **Input Validation**: Pydantic models throughout
- **Allowed Hosts**: Host header validation

### 4. Performance
- **Async/Await**: Full async throughout the stack
- **FastAPI**: Modern, fast framework
- **Minimal Dependencies**: Lean dependency tree
- **Static Asset Optimization**: Efficient serving

### 5. Developer Experience
- **Type Safety**: Full type hints with Pydantic
- **Clear Errors**: Comprehensive logging and validation
- **Hot Reload**: Development mode with auto-reload
- **Intuitive YAML**: Easy-to-understand configuration format

## Project Structure

```
foundry/
├── foundry_engine/              # Core engine (reusable)
│   ├── app.py                  # FastAPI application factory
│   ├── config.py               # Pydantic configuration models
│   │
│   ├── security/               # Security layer
│   │   ├── jwt.py             # JWT authentication
│   │   ├── csrf.py            # CSRF protection
│   │   ├── rate_limit.py      # Rate limiting
│   │   └── headers.py         # Security headers middleware
│   │
│   ├── mail/                   # Email providers
│   │   ├── base.py            # Abstract base class
│   │   ├── brevo.py           # Brevo (Sendinblue) integration
│   │   ├── mailgun.py         # Mailgun integration
│   │   └── smtp.py            # Generic SMTP
│   │
│   ├── navigation/             # Navigation renderers
│   │   ├── base.py            # Base navigation class
│   │   ├── registry.py        # Navigation type registry
│   │   ├── top_ribbon.py      # Top bar navigation
│   │   ├── hamburger.py       # Hamburger menu
│   │   └── sidebar.py         # Sidebar navigation
│   │
│   ├── sections/               # Section renderers
│   │   ├── base.py            # Base section class
│   │   ├── registry.py        # Section type registry
│   │   ├── hero.py            # Hero sections
│   │   ├── parallax.py        # Parallax sections
│   │   ├── gallery.py         # Photo galleries
│   │   ├── text.py            # Text/markdown sections
│   │   ├── contact.py         # Contact forms
│   │   ├── cta.py             # Call-to-action sections
│   │   ├── features.py        # Feature grids
│   │   ├── testimonials.py    # Testimonials
│   │   └── footer.py          # Footer sections
│   │
│   ├── templates/              # Jinja2 templates
│   │   ├── base.html          # Base page layout
│   │   ├── page.html          # Page template
│   │   ├── navigation/        # Navigation templates
│   │   └── sections/          # Section templates
│   │
│   ├── static/                 # Core static assets
│   │   ├── css/
│   │   │   └── foundry-base.css
│   │   └── js/
│   │       └── foundry.js
│   │
│   ├── routers/                # API routes
│   │   ├── pages.py           # Page rendering
│   │   └── contact.py         # Contact form handling
│   │
│   └── utils/                  # Utilities
│       ├── markdown.py        # Markdown processor
│       └── yaml_loader.py     # YAML loading & validation
│
├── sites/                      # Site-specific content
│   └── example_site/
│       ├── config.yaml        # Site configuration
│       ├── content/
│       │   ├── pages/         # Page definitions (YAML)
│       │   └── sections/      # Section content (MD)
│       ├── theme/
│       │   └── custom.css     # Custom theme
│       └── assets/            # Images, files
│
├── main.py                     # Application entry point
├── requirements.txt            # Python dependencies
├── pyproject.toml             # Project metadata
├── render.yaml                # Render deployment config
├── .env                       # Environment variables
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
│
└── Documentation
    ├── README.md              # Main documentation
    ├── QUICKSTART.md          # Quick start guide
    ├── DEVELOPMENT.md         # Development guide
    └── PROJECT_SUMMARY.md     # This file
```

## Built-in Features

### Section Types (9 total)
1. **Hero**: Full-screen hero sections with backgrounds, CTAs
2. **Parallax**: Parallax scrolling effects
3. **Gallery**: Photo galleries (grid, masonry, carousel)
4. **Text**: Rich markdown content
5. **Contact**: Full-featured contact forms
6. **CTA**: Call-to-action sections
7. **Features**: Feature grids with icons
8. **Testimonials**: Customer testimonials
9. **Footer**: Flexible footer layouts

### Navigation Types (3 total)
1. **Top Ribbon**: Classic horizontal navigation
2. **Hamburger**: Mobile-friendly hamburger menu
3. **Sidebar**: Vertical sidebar navigation

### Email Providers (3 total)
1. **Brevo** (Sendinblue): API integration
2. **Mailgun**: API integration
3. **SMTP**: Generic SMTP support

## Technology Stack

### Core
- **FastAPI** 0.109+: Modern async web framework
- **Python** 3.11+: Modern Python with type hints
- **Uvicorn**: ASGI server

### Templates & Content
- **Jinja2**: Templating engine
- **Python-Markdown**: Markdown processing
- **PyMdown Extensions**: Enhanced markdown features
- **PyYAML**: YAML parsing

### Security
- **python-jose**: JWT handling
- **passlib**: Password hashing (for future auth)
- **slowapi**: Rate limiting
- **secure.py**: Security headers

### Email & HTTP
- **httpx**: Async HTTP client
- **aiosmtplib**: Async SMTP
- **email-validator**: Email validation

### Configuration
- **Pydantic**: Data validation and settings
- **python-dotenv**: Environment variable loading

### Frontend
- **HTMX**: Dynamic interactions without heavy JS
- **Alpine.js**: Lightweight reactive framework
- **Modern CSS**: CSS Grid, Flexbox, Variables

## Deployment

### Render Configuration
- Automatic deployment via `render.yaml`
- Health check endpoint: `/health`
- Environment-based configuration
- Production-ready settings

### Environment Variables
**Required:**
- `SECRET_KEY`: Application secret (32+ chars)
- Email provider credentials

**Optional:**
- JWT configuration
- Rate limiting settings
- reCAPTCHA keys

## YAML Schema Overview

### Site Config (`config.yaml`)
```yaml
site:           # Site metadata
security:       # Security settings
navigation:     # Navigation configuration
mail:           # Email configuration
pages:          # List of pages
```

### Page Config (`pages/*.yaml`)
```yaml
page:           # Page metadata (title, description, etc.)
sections:       # List of sections with type and config
```

### Section Config (in page YAML)
```yaml
type:           # Section type (hero, text, etc.)
content:        # Path to markdown file (optional)
config:         # Section-specific configuration
```

## Extensibility

### Adding New Section Types
1. Create class extending `BaseSection`
2. Implement `get_context()` method
3. Create Jinja2 template
4. Register in `sections/registry.py`

### Adding New Navigation Types
1. Create class extending `BaseNavigation`
2. Implement `get_context()` method
3. Create Jinja2 template
4. Register in `navigation/registry.py`

### Adding New Email Providers
1. Create class extending `BaseMailProvider`
2. Implement `send()` and `verify_config()` methods
3. Add to config enum
4. Register in contact router

## Security Features

### Request Security
- Host header validation (allowed hosts)
- CORS configuration
- Rate limiting per IP/user
- Input validation with Pydantic

### Response Security
- CSP headers
- HSTS (production only)
- X-Frame-Options: DENY
- X-Content-Type-Options: nosniff
- X-XSS-Protection
- Referrer-Policy
- Permissions-Policy

### Form Security
- CSRF token validation
- reCAPTCHA support
- Rate limiting on submissions
- Email validation

### Authentication (Optional)
- JWT-based authentication
- Per-site enable/disable
- Configurable expiration
- Protected pages support

## Performance Optimizations

### Backend
- Full async/await implementation
- Efficient template caching
- Minimal middleware overhead
- Optimized static file serving

### Frontend
- Lazy loading for images
- Minimal JavaScript footprint
- Modern CSS (no preprocessor needed)
- HTMX for dynamic behavior (no heavy frameworks)

## Use Cases

Foundry is ideal for:
- **Landing Pages**: 1-3 page sites with contact forms
- **Small Business Sites**: 3-5 page brochure sites
- **Portfolio Sites**: Personal or professional portfolios
- **Documentation Sites**: Simple documentation (though consider dedicated docs tools for complex docs)
- **Event Sites**: Single-page event sites with registration

Foundry is NOT ideal for:
- **E-commerce**: No shopping cart, payment processing
- **Complex Web Apps**: Not designed for app-like functionality
- **Blogs**: No built-in blog functionality (could be added)
- **User Management**: No built-in user registration/profiles

## Next Steps

### Immediate Enhancements
1. Add more section types (pricing tables, timeline, etc.)
2. Add blog functionality (posts, categories, RSS)
3. Add image optimization pipeline
4. Add sitemap.xml generation
5. Add robots.txt configuration

### Future Enhancements
1. Admin panel for content editing
2. Multiple language support (i18n)
3. Form builder for custom forms
4. Analytics integration
5. SEO optimization tools
6. A/B testing support

## Contributing

See `DEVELOPMENT.md` for detailed contribution guidelines.

## License

MIT License - Free for commercial and personal use.

---

**Foundry Engine** - Built with ❤️ for developers who value security, performance, and simplicity.
