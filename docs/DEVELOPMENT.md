# Foundry Engine - Development Guide

Guide for extending and customizing Foundry Engine.

## Architecture Overview

### Core Principles

1. **Separation of Concerns**: Engine code is completely separate from site content
2. **Configuration-Driven**: YAML for structure, Markdown for content, CSS for styling
3. **Modular Design**: Easy to add new section types, navigation styles, etc.
4. **Type Safety**: Full Pydantic validation throughout

### Directory Structure

```
foundry_engine/          # Core engine (version controlled)
├── app.py              # FastAPI app factory
├── config.py           # Pydantic configuration models
├── security/           # Security utilities (JWT, CSRF, rate limiting, headers)
├── mail/               # Email provider implementations
├── navigation/         # Navigation type renderers
├── sections/           # Section type renderers
├── templates/          # Jinja2 templates
├── routers/            # FastAPI routers
└── utils/              # Utilities (markdown, yaml)

sites/                   # Site-specific content (separate from engine)
└── yoursite/
    ├── config.yaml     # Site configuration
    ├── content/        # Page definitions and section content
    ├── theme/          # Custom CSS
    └── assets/         # Images, files
```

## Adding New Section Types

### Step 1: Create Section Class

Create a new file in `foundry_engine/sections/`:

```python
# foundry_engine/sections/pricing.py
from typing import Any
from foundry_engine.sections.base import BaseSection

class PricingSection(BaseSection):
    """Pricing table section."""

    section_type = "pricing"
    template_name = "sections/pricing.html"

    def get_context(self) -> dict[str, Any]:
        """Get context for pricing section."""
        return {
            "content": self.get_rendered_content(),
            "plans": self.config.get("plans", []),
            "currency": self.config.get("currency", "$"),
            "billing_period": self.config.get("billing_period", "month"),
        }
```

### Step 2: Create Template

Create template in `foundry_engine/templates/sections/`:

```html
<!-- foundry_engine/templates/sections/pricing.html -->
<section class="section-pricing">
    <div class="pricing-container">
        {% if content %}
            <div class="pricing-intro">{{ content|safe }}</div>
        {% endif %}

        <div class="pricing-grid">
            {% for plan in plans %}
                <div class="pricing-card">
                    <h3>{{ plan.name }}</h3>
                    <div class="price">
                        {{ currency }}{{ plan.price }}
                        <span class="period">/{{ billing_period }}</span>
                    </div>
                    <ul class="features">
                        {% for feature in plan.features %}
                            <li>{{ feature }}</li>
                        {% endfor %}
                    </ul>
                    <a href="{{ plan.cta_url }}" class="btn btn-primary">
                        {{ plan.cta_text or 'Get Started' }}
                    </a>
                </div>
            {% endfor %}
        </div>
    </div>
</section>
```

### Step 3: Register Section Type

Add to `foundry_engine/sections/registry.py`:

```python
from foundry_engine.sections.pricing import PricingSection

SECTION_REGISTRY: dict[str, Type[BaseSection]] = {
    # ... existing sections
    "pricing": PricingSection,
}
```

### Step 4: Use in Site

Now you can use it in your page YAML:

```yaml
sections:
  - type: "pricing"
    content: "sections/pricing-intro.md"
    config:
      currency: "$"
      billing_period: "month"
      plans:
        - name: "Basic"
          price: 9
          features:
            - "Feature 1"
            - "Feature 2"
          cta_url: "/signup?plan=basic"
        - name: "Pro"
          price: 29
          features:
            - "All Basic features"
            - "Feature 3"
            - "Feature 4"
          cta_url: "/signup?plan=pro"
```

## Adding New Navigation Types

### Step 1: Create Navigation Class

```python
# foundry_engine/navigation/dropdown.py
from typing import Any
from foundry_engine.navigation.base import BaseNavigation

class DropdownNavigation(BaseNavigation):
    """Dropdown navigation with mega menu support."""

    nav_type = "dropdown"
    template_name = "navigation/dropdown.html"

    def get_context(self) -> dict[str, Any]:
        items = []
        for item in self.config.items:
            item_dict = item.model_dump()
            item_dict["is_active"] = self.is_active(item.url)
            items.append(item_dict)

        return {
            "logo": self.config.logo,
            "logo_alt": self.config.logo_alt or "Site Logo",
            "items": items,
        }
```

### Step 2: Create Template

```html
<!-- foundry_engine/templates/navigation/dropdown.html -->
<nav class="nav-dropdown">
    <!-- Your navigation HTML -->
</nav>
```

### Step 3: Update Config Enum

Add to `foundry_engine/config.py`:

```python
class NavigationType(str, Enum):
    TOP_RIBBON = "top_ribbon"
    HAMBURGER = "hamburger"
    SIDEBAR = "sidebar"
    DROPDOWN = "dropdown"  # Add this
```

### Step 4: Register Navigation

Add to `foundry_engine/navigation/registry.py`:

```python
from foundry_engine.navigation.dropdown import DropdownNavigation

NAVIGATION_REGISTRY = {
    # ... existing
    NavigationType.DROPDOWN: DropdownNavigation,
}
```

## Adding Email Providers

### Step 1: Create Provider Class

```python
# foundry_engine/mail/sendgrid.py
import logging
from typing import Any
import httpx
from foundry_engine.mail.base import BaseMailProvider, EmailMessage

logger = logging.getLogger(__name__)

class SendGridMailProvider(BaseMailProvider):
    """SendGrid email provider implementation."""

    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.api_key = config.get("api_key")

    async def send(self, message: EmailMessage) -> bool:
        # Implementation here
        pass

    async def verify_config(self) -> bool:
        # Verify API key
        pass
```

### Step 2: Register Provider

Add to `foundry_engine/config.py`:

```python
class MailProvider(str, Enum):
    BREVO = "brevo"
    MAILGUN = "mailgun"
    SMTP = "smtp"
    SENDGRID = "sendgrid"  # Add this
```

Add to `foundry_engine/routers/contact.py`:

```python
elif provider_type == MailProvider.SENDGRID:
    config = {...}
    return SendGridMailProvider(config)
```

## Testing

### Run Tests

```bash
pytest
```

### Test a Specific Module

```bash
pytest foundry_engine/tests/test_sections.py
```

### Test with Coverage

```bash
pytest --cov=foundry_engine --cov-report=html
```

## Code Style

### Format Code

```bash
black foundry_engine/
```

### Lint Code

```bash
ruff check foundry_engine/
```

### Type Checking

```bash
mypy foundry_engine/
```

## Best Practices

### Section Classes

1. Always extend `BaseSection`
2. Implement `get_context()` method
3. Use `get_rendered_content()` for markdown content
4. Validate config in `validate_config()` if needed

### Templates

1. Use semantic HTML
2. Add proper ARIA labels for accessibility
3. Use CSS classes that can be overridden
4. Keep templates simple and focused

### Configuration

1. Use Pydantic models for validation
2. Provide sensible defaults
3. Document config options in docstrings
4. Use enums for fixed choices

### Security

1. Always validate user input
2. Use CSRF tokens for forms
3. Apply rate limiting to endpoints
4. Sanitize HTML output when needed

## Debugging

### Enable Debug Logging

```env
LOG_LEVEL=DEBUG
```

### Access Request State

In routes, you can access:
- `request.app.state.settings` - Environment settings
- `request.app.state.site_config` - Site configuration
- `request.app.state.templates` - Jinja2 templates
- `request.app.state.markdown` - Markdown processor

### Common Issues

**Templates not found**: Check that template path matches `template_name`

**Section not rendering**: Verify section is registered in `registry.py`

**Config validation fails**: Check Pydantic models in `config.py`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run code style checks
6. Submit a pull request

## Questions?

- Check existing code for examples
- Review type hints for parameter types
- Look at example site for usage patterns
