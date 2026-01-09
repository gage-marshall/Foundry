# Foundry Engine - Development Guide

Guide for contributing to and extending Foundry Engine.

## Architecture Overview

### Core Principles

1. **Package-First Design**: Engine is a standalone Python package
2. **Configuration-Driven**: YAML for structure, Markdown for content, CSS for styling
3. **Modular Components**: Easy to add new section types, navigation styles, etc.
4. **Type Safety**: Full Pydantic validation throughout
5. **Separation of Concerns**: Engine code separate from consumer site content

### Directory Structure

```
foundry-engine/             # Engine repository (this repo)
├── foundry_engine/         # Core package
│   ├── __init__.py        # Exports create_app()
│   ├── app.py             # FastAPI application factory
│   ├── config.py          # Pydantic configuration models
│   ├── security/          # Security utilities (JWT, CSRF, rate limiting, headers)
│   ├── mail/              # Email provider implementations
│   ├── navigation/        # Navigation type renderers
│   ├── sections/          # Section type renderers
│   ├── templates/         # Jinja2 templates
│   ├── routers/           # FastAPI routers
│   └── utils/             # Utilities (markdown, yaml)
├── docs/                  # Engine documentation
├── pyproject.toml         # Package definition
├── LICENSE
└── README.md
```

## Development Setup

### Clone and Install

```bash
# Clone the engine repository
git clone <engine-repo-url>
cd foundry-engine

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

### Development Dependencies

Automatically installed with `[dev]`:
- `pytest` - Testing framework
- `pytest-asyncio` - Async test support
- `black` - Code formatter
- `ruff` - Fast linter
- `mypy` - Type checker

## Testing the Engine

### Create a Test Site

To test the engine during development, create a simple test site:

```bash
# In the engine repository root
mkdir test-site
cd test-site
mkdir -p content/pages content/sections theme assets
```

Create minimal `config.yaml`, `content/`, and `main.py` that imports the engine.

### Run Test Site

```bash
# From test-site directory
python main.py
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

### Step 4: Test in Consumer Site

Now consumers can use it in their page YAML:

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
          features: ["Feature 1", "Feature 2"]
          cta_url: "/signup?plan=basic"
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

### Run All Tests

```bash
pytest
```

### Test Specific Module

```bash
pytest foundry_engine/tests/test_sections.py
```

### Test with Coverage

```bash
pytest --cov=foundry_engine --cov-report=html
open htmlcov/index.html
```

### Write Tests

```python
# foundry_engine/tests/test_pricing.py
import pytest
from foundry_engine.sections.pricing import PricingSection

def test_pricing_section_context():
    section = PricingSection(
        content_path=None,
        config={"currency": "€", "plans": [{"name": "Basic", "price": 10}]},
        site_path=Path("/fake"),
        markdown_processor=None
    )
    context = section.get_context()
    assert context["currency"] == "€"
    assert len(context["plans"]) == 1
```

## Code Style

### Format Code

```bash
# Format all Python code
black foundry_engine/

# Check formatting
black --check foundry_engine/
```

### Lint Code

```bash
# Run linter
ruff check foundry_engine/

# Auto-fix issues
ruff check --fix foundry_engine/
```

### Type Checking

```bash
# Check types
mypy foundry_engine/

# Check specific file
mypy foundry_engine/sections/pricing.py
```

## Best Practices

### Section Classes

1. Always extend `BaseSection`
2. Implement `get_context()` method
3. Use `get_rendered_content()` for markdown content
4. Validate config in `validate_config()` if needed
5. Add type hints for all parameters

### Templates

1. Use semantic HTML5 elements
2. Add proper ARIA labels for accessibility
3. Use CSS classes that can be overridden by consumers
4. Keep templates simple and focused
5. Document expected context variables

### Configuration

1. Use Pydantic models for all config validation
2. Provide sensible defaults
3. Document config options in docstrings
4. Use enums for fixed choices
5. Validate early, fail fast

### Security

1. Always validate user input with Pydantic
2. Use CSRF tokens for all forms
3. Apply rate limiting to sensitive endpoints
4. Sanitize HTML output when rendering user content
5. Never trust environment variables without validation

## Debugging

### Enable Debug Logging

```env
LOG_LEVEL=DEBUG
```

### Access Request State

In routes and sections:
- `request.app.state.settings` - Environment settings
- `request.app.state.site_config` - Site configuration
- `request.app.state.templates` - Jinja2 templates
- `request.app.state.markdown` - Markdown processor

### Common Issues

**Templates not found**:
- Check that template path matches `template_name`
- Verify template exists in `foundry_engine/templates/`

**Section not rendering**:
- Verify section is registered in `sections/registry.py`
- Check for typos in section type name

**Config validation fails**:
- Review Pydantic models in `config.py`
- Check error messages for required fields

## Release Process

### Version Numbering

Use semantic versioning: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

### Creating a Release

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Run tests: `pytest`
4. Format code: `black foundry_engine/`
5. Check types: `mypy foundry_engine/`
6. Commit changes
7. Tag release: `git tag v0.2.0`
8. Push: `git push origin main --tags`

### Release Notes

Document in CHANGELOG.md:
- New features
- Bug fixes
- Breaking changes
- Migration guide (if needed)

## Contributing

### Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Add tests for new functionality
5. Run code quality checks
6. Commit with clear messages
7. Push and create pull request
8. Address review feedback

### Commit Messages

Use conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation only
- `style:` Code style (formatting, etc.)
- `refactor:` Code restructuring
- `test:` Adding tests
- `chore:` Maintenance tasks

Example: `feat: add pricing section type`

## Questions?

- Review existing code for examples
- Check type hints for parameter types
- Look at Pydantic models for configuration
- Open an issue for clarification

## Architecture Decisions

### Why Package-First?

- **Separation**: Engine updates don't affect site content
- **Versioning**: Sites can pin to specific engine versions
- **Maintainability**: Single codebase for engine improvements
- **Distribution**: Easy to share across multiple sites

### Why Pydantic?

- **Validation**: Automatic input validation
- **Type Safety**: Full IDE autocomplete support
- **Documentation**: Self-documenting config structure
- **Performance**: Fast validation with Rust backend

### Why Jinja2?

- **Familiar**: Standard Python templating
- **Powerful**: Rich template inheritance
- **Safe**: Auto-escaping prevents XSS
- **Extensible**: Easy to add custom filters

Happy developing! 🛠️
