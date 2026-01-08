# Foundry Engine - Quick Start Guide

Get your first site running in 5 minutes!

## Step 1: Install Dependencies

```bash
# Create and activate virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Configure Environment

A development `.env` file has been created for you. For production, update these values:

```env
SECRET_KEY=your-secret-key-here
BREVO_API_KEY=your-brevo-api-key
```

## Step 3: Run the Server

```bash
python main.py
```

Visit: http://localhost:8000

## Step 4: Customize Your Site

### Edit Site Configuration
Edit `sites/example_site/config.yaml`:
- Change site name and domain
- Update navigation items
- Configure email recipient

### Edit Page Content
Edit files in `sites/example_site/content/`:
- `pages/*.yaml` - Page structure
- `sections/*.md` - Content

### Customize Theme
Edit `sites/example_site/theme/custom.css`:
- Change colors in `:root` variables
- Add custom styles

## Common Tasks

### Add a New Page

1. Create page config:
```bash
# sites/example_site/content/pages/services.yaml
```

2. Add to site config:
```yaml
pages:
  - home
  - about
  - contact
  - services  # Add this
```

3. Add navigation item:
```yaml
navigation:
  items:
    - text: "Services"
      url: "/services"
```

### Change Navigation Style

Edit `sites/example_site/config.yaml`:
```yaml
navigation:
  type: "hamburger"  # or "top_ribbon", "sidebar"
```

### Configure Email

1. Get API key from [Brevo](https://app.brevo.com/)
2. Update `.env`:
```env
BREVO_API_KEY=your-actual-api-key
```
3. Update `sites/example_site/config.yaml`:
```yaml
mail:
  contact_recipient: "your-email@example.com"
```

## Deploy to Render

1. Push to Git:
```bash
git init
git add .
git commit -m "Initial commit"
git push origin main
```

2. On Render:
   - Create new Web Service
   - Connect your repository
   - Set environment variables
   - Deploy!

## Available Section Types

Use these in your page YAML files:

- `hero` - Hero sections with backgrounds and CTAs
- `text` - Rich markdown content
- `features` - Feature grids with icons
- `gallery` - Photo galleries
- `contact` - Contact forms
- `cta` - Call-to-action sections
- `parallax` - Parallax scrolling
- `testimonials` - Customer testimonials
- `footer` - Page footers

## Need Help?

- Check `README.md` for full documentation
- Review example site in `sites/example_site/`
- See inline comments in YAML files

## What's Next?

1. Replace example content with yours
2. Add your branding and colors
3. Configure email provider
4. Deploy to Render
5. Point your domain to Render

Happy building! 🚀
