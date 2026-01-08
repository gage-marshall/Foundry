# Styling Guide

This guide explains how to customize the appearance of your Foundry Engine site, how the YAML-based content system works, and how to format content with Markdown.

## Table of Contents

- [Custom CSS](#custom-css)
- [YAML Content System](#yaml-content-system)
- [Section Types](#section-types)
- [Markdown Formatting](#markdown-formatting)

---

## Custom CSS

### Overview

Foundry Engine uses a two-tier CSS system:

1. **Base Styles** (`foundry-base.css`) - Core engine styles with CSS variables
2. **Custom Theme** (`sites/your_site/theme/custom.css`) - Your site-specific overrides

### CSS Variables (Design Tokens)

The base CSS defines comprehensive design tokens that you can override in `custom.css`:

#### Colors

```css
:root {
    /* Primary Colors */
    --color-primary: #6366f1;
    --color-primary-dark: #4f46e5;
    --color-primary-light: #818cf8;
    --color-secondary: #8b5cf6;
    --color-accent: #ec4899;

    /* Status Colors */
    --color-success: #10b981;
    --color-warning: #f59e0b;
    --color-danger: #ef4444;
    --color-info: #3b82f6;

    /* Text & Backgrounds */
    --color-text: #1f2937;
    --color-text-light: #6b7280;
    --color-text-lighter: #9ca3af;
    --color-bg: #ffffff;
    --color-bg-alt: #f9fafb;
    --color-bg-dark: #111827;
    --color-border: #e5e7eb;
}
```

#### Typography

```css
:root {
    /* Font Families */
    --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    --font-serif: Georgia, Cambria, "Times New Roman", Times, serif;
    --font-mono: "SF Mono", Monaco, "Cascadia Code", monospace;

    /* Font Sizes */
    --text-xs: 0.75rem;
    --text-sm: 0.875rem;
    --text-base: 1rem;
    --text-lg: 1.125rem;
    --text-xl: 1.25rem;
    --text-2xl: 1.5rem;
    --text-3xl: 1.875rem;
    --text-4xl: 2.25rem;
    --text-5xl: 3rem;
    --text-6xl: 3.75rem;
}
```

#### Spacing

```css
:root {
    --spacing-xs: 0.25rem;    /* 4px */
    --spacing-sm: 0.5rem;     /* 8px */
    --spacing-md: 1rem;       /* 16px */
    --spacing-lg: 1.5rem;     /* 24px */
    --spacing-xl: 2rem;       /* 32px */
    --spacing-2xl: 3rem;      /* 48px */
    --spacing-3xl: 4rem;      /* 64px */
    --spacing-4xl: 6rem;      /* 96px */
}
```

#### Border Radius

```css
:root {
    --radius-sm: 0.25rem;
    --radius-md: 0.375rem;
    --radius-lg: 0.5rem;
    --radius-xl: 0.75rem;
    --radius-2xl: 1rem;
    --radius-full: 9999px;
}
```

#### Shadows

```css
:root {
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    --shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}
```

#### Transitions

```css
:root {
    --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
    --transition-base: 300ms cubic-bezier(0.4, 0, 0.2, 1);
    --transition-slow: 500ms cubic-bezier(0.4, 0, 0.2, 1);
    --transition-spring: 500ms cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

### Overridable Components

You can customize specific components by targeting their classes in `custom.css`:

#### Navigation

```css
.nav-top-ribbon {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
}

.nav-link {
    color: var(--color-text);
}

.nav-link:hover {
    color: var(--color-primary);
}
```

#### Hero Section

```css
.section-hero {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.hero-text h1 {
    font-size: 3rem;
    color: white;
}
```

#### Feature Cards

```css
.feature-card {
    transition: transform 0.3s ease;
}

.feature-card:hover {
    transform: translateY(-5px);
}

.feature-icon {
    font-size: 3rem;
    color: var(--color-primary);
}
```

#### Buttons

```css
.btn {
    padding: 1rem 2rem;
    border-radius: var(--radius-lg);
}

.btn-primary {
    background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-xl);
}
```

#### Footer

```css
.section-footer {
    background-color: #1f2937;
    color: #9ca3af;
}

.footer-links a:hover {
    color: white;
}
```

### Example: Creating a Custom Theme

Here's a complete example of a custom theme in `sites/your_site/theme/custom.css`:

```css
/* Custom Brand Colors */
:root {
    --color-primary: #ff6b6b;
    --color-secondary: #4ecdc4;
    --color-accent: #ffe66d;
    --font-heading: 'Playfair Display', serif;
    --font-body: 'Inter', sans-serif;
}

/* Custom Typography */
h1, h2, h3, h4, h5, h6 {
    font-family: var(--font-heading);
}

h1 {
    background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Custom Navigation */
.nav-top-ribbon {
    background: white;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

/* Custom Hero */
.section-hero {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

---

## YAML Content System

### Overview

Foundry Engine uses YAML files to define page structure and content. Each page is defined in `sites/your_site/content/pages/`.

### Page Structure

A typical YAML page file looks like this:

```yaml
page:
  slug: "about"
  title: "About Us"
  meta_description: "Learn about our company"

sections:
  - type: "hero"
    content: "sections/hero-about.md"
    config:
      background_image: "/static/images/hero.jpg"
      height: "60vh"

  - type: "text"
    content: "sections/about-content.md"
    config:
      max_width: "800px"
      text_align: "left"
```

### Page Metadata

```yaml
page:
  slug: "about"                    # URL path (e.g., /about)
  title: "About Us"                # Page title (used in <title> tag)
  meta_description: "..."          # SEO meta description
```

### Section Structure

Each section has three components:

```yaml
- type: "hero"                     # Section type (see below)
  content: "sections/hero.md"      # Path to markdown content (optional)
  config:                          # Section-specific configuration
    option1: "value"
    option2: 123
```

---

## Section Types

### Hero

Large banner section with background image/video and call-to-action.

```yaml
- type: "hero"
  content: "sections/hero-home.md"
  config:
    background_image: "https://example.com/hero.jpg"
    background_video: "/static/video/hero.mp4"  # Optional video background
    height: "100vh"                              # Section height
    overlay_opacity: 0.5                         # Dark overlay (0-1)
    text_align: "center"                         # left, center, right
    parallax: true                               # Enable parallax effect
    cta_button:                                  # Call-to-action button
      text: "Get Started"
      url: "/contact"
      style: "primary"                           # primary, secondary, outline
```

**Features:**
- Background image or video
- Parallax scrolling effect
- Animated scroll indicator
- Customizable overlay
- CTA button with hover effects
- Floating decorative elements

---

### Text

Simple text/markdown content section.

```yaml
- type: "text"
  content: "sections/about-content.md"
  config:
    max_width: "800px"              # Content max width
    text_align: "left"              # left, center, right
    background_color: "#f9fafb"     # Optional background color
    padding: "4rem 2rem"            # Section padding
```

**Features:**
- Markdown content rendering
- Configurable width and alignment
- Clean typography
- Background decoration pattern
- AOS fade-up animation

---

### Features

Grid layout for showcasing features, services, or benefits.

```yaml
- type: "features"
  content: "sections/features-intro.md"  # Optional intro text
  config:
    columns: 3                      # Number of columns (1-4)
    icon_style: "outlined"          # outlined, filled, none
    card_style: "elevated"          # flat, elevated, outlined
    features:
      - title: "Fast Performance"
        description: "Blazing fast load times"
        icon: "🚀"                  # Emoji or HTML/SVG
        link:                       # Optional link
          text: "Learn more"
          url: "/features/performance"
      - title: "Secure"
        description: "Built-in security"
        icon: "🔒"
      - title: "Modern"
        description: "Latest technologies"
        icon: "✨"
```

**Features:**
- Responsive grid layout
- Animated hover effects
- Icon backgrounds with gradients
- Optional links
- Staggered AOS animations
- Decorative background grid

---

### Gallery

Image gallery with lightbox functionality.

```yaml
- type: "gallery"
  content: "sections/gallery-intro.md"
  config:
    columns: 3                      # Number of columns
    gap: "1rem"                     # Gap between images
    images:
      - src: "/static/images/gallery/1.jpg"
        alt: "Project showcase"
        caption: "Modern office design"
      - src: "/static/images/gallery/2.jpg"
        alt: "Interior view"
        caption: "Collaborative workspace"
```

**Features:**
- Responsive grid
- Lightbox/modal view
- Image captions
- Hover zoom effect
- Lazy loading
- Keyboard navigation in lightbox

---

### Testimonials

Customer testimonials or reviews section.

```yaml
- type: "testimonials"
  content: "sections/testimonials-intro.md"
  config:
    layout: "grid"                  # grid or carousel
    testimonials:
      - quote: "Amazing product! Highly recommended."
        author: "Sarah Chen"
        role: "Lead Developer"
        company: "TechCorp"
        photo: "/static/images/sarah.jpg"  # Optional
      - quote: "Best service we've ever used."
        author: "John Smith"
        role: "CEO"
        company: "StartupCo"
```

**Features:**
- Grid or carousel layout
- Author photos or avatar initials
- Company/role metadata
- Quote icon
- Hover effects with shadow
- Responsive design

---

### Contact

Contact form with validation and email integration.

```yaml
- type: "contact"
  content: "sections/contact-intro.md"
  config:
    form_fields:
      - name: "name"
        type: "text"
        label: "Your Name"
        required: true
      - name: "email"
        type: "email"
        label: "Email Address"
        required: true
      - name: "message"
        type: "textarea"
        label: "Message"
        required: true
    submit_button:
      text: "Send Message"
      style: "primary"
    success_message: "Thank you! We'll be in touch soon."
```

**Features:**
- Customizable form fields
- Client-side validation
- CSRF protection
- Rate limiting
- Email integration (Brevo, Mailgun, SMTP)
- Animated focus states
- Success/error messages

---

### CTA (Call to Action)

Prominent call-to-action section.

```yaml
- type: "cta"
  content: "sections/cta-home.md"
  config:
    background_color: "#4f46e5"
    text_color: "#ffffff"
    button:
      text: "Get Started Today"
      url: "/signup"
      style: "outline"              # primary, outline, secondary
```

**Features:**
- Full-width design
- Custom colors
- Large prominent button
- Simple and effective

---

### Footer

Site footer with links and copyright.

```yaml
- type: "footer"
  config:
    columns:
      - title: "Product"
        links:
          - text: "Features"
            url: "/features"
          - text: "Pricing"
            url: "/pricing"
      - title: "Company"
        links:
          - text: "About"
            url: "/about"
          - text: "Contact"
            url: "/contact"
      - title: "Resources"
        links:
          - text: "Documentation"
            url: "/docs"
          - text: "Blog"
            url: "/blog"
    copyright: "&copy; 2026 Your Company. All rights reserved."
```

**Features:**
- Multi-column layout
- Link groups
- Social media icons
- Copyright text
- Dark theme
- Responsive design

---

### Parallax

Parallax scrolling section with image and text overlay.

```yaml
- type: "parallax"
  content: "sections/parallax-text.md"
  config:
    background_image: "/static/images/parallax.jpg"
    height: "500px"
    overlay_opacity: 0.6
    text_align: "center"
    text_color: "#ffffff"
```

**Features:**
- Smooth parallax effect
- Fixed background
- Text overlay
- Configurable height and opacity

---

## Markdown Formatting

### Overview

Foundry Engine uses Python-Markdown to render content. All markdown files are stored in `sites/your_site/content/sections/`.

### Basic Syntax

#### Headings

```markdown
# Heading 1
## Heading 2
### Heading 3
#### Heading 4
##### Heading 5
###### Heading 6
```

#### Emphasis

```markdown
*italic text* or _italic text_
**bold text** or __bold text__
***bold and italic*** or ___bold and italic___
```

#### Links

```markdown
[Link text](https://example.com)
[Link with title](https://example.com "Title on hover")
```

#### Images

```markdown
![Alt text](/static/images/photo.jpg)
![Alt text](/static/images/photo.jpg "Optional title")
```

#### Lists

**Unordered:**
```markdown
- Item 1
- Item 2
  - Nested item 2.1
  - Nested item 2.2
- Item 3
```

**Ordered:**
```markdown
1. First item
2. Second item
3. Third item
```

#### Blockquotes

```markdown
> This is a blockquote.
> It can span multiple lines.
>
> And multiple paragraphs.
```

#### Code

**Inline code:**
```markdown
Use `code` in your text.
```

**Code blocks:**
````markdown
```python
def hello():
    print("Hello, world!")
```
````

#### Horizontal Rules

```markdown
---
or
***
or
___
```

### Extended Syntax

#### Tables

```markdown
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Row 1    | Data     | Data     |
| Row 2    | Data     | Data     |
```

#### Task Lists

```markdown
- [x] Completed task
- [ ] Incomplete task
- [ ] Another task
```

#### Footnotes

```markdown
Here's a sentence with a footnote.[^1]

[^1]: This is the footnote content.
```

### Best Practices

1. **Use semantic headings** - Start with H1 and maintain hierarchy
2. **Keep paragraphs short** - Easier to read on all devices
3. **Use lists liberally** - Break up dense information
4. **Add alt text to images** - Improves accessibility and SEO
5. **Link descriptively** - Use meaningful link text instead of "click here"
6. **Preview your content** - Always check how it renders before deploying

### Example Markdown File

```markdown
# Welcome to Foundry Engine

A modern, secure, and blazingly fast static site engine built with FastAPI.

## Key Features

Build beautiful sites with:

- **YAML** for structure
- **Markdown** for content
- **CSS** for styling

### Getting Started

Getting started is easy:

1. Clone the repository
2. Configure your site in YAML
3. Write content in Markdown
4. Deploy anywhere

> "Foundry Engine gave us perfect Lighthouse scores out of the box!"
> — Happy Developer

[Get Started Now](/docs/quickstart)
```

---

## Tips & Tricks

### Performance Optimization

- Use WebP format for images
- Optimize image sizes before upload
- Minimize custom CSS
- Leverage CSS variables for theming

### Accessibility

- Use semantic HTML headings
- Always include alt text for images
- Ensure sufficient color contrast
- Test with keyboard navigation

### SEO

- Write descriptive meta descriptions
- Use heading hierarchy properly
- Include relevant keywords naturally
- Create descriptive URLs (slugs)

### Development Workflow

1. Edit YAML to structure pages
2. Write content in Markdown files
3. Customize appearance in custom.css
4. Preview locally at `http://localhost:8000`
5. Deploy to production

---

## Additional Resources

- [Quick Start Guide](../QUICKSTART.md)
- [Development Guide](../DEVELOPMENT.md)
- [Deployment Guide](../DEPLOYMENT.md)
- [Example Site](../sites/example_site/)

---

**Need Help?**

Check the example site at `sites/example_site/` to see these concepts in action!
