# Production startup script for Foundry Engine (Windows)

Write-Host "🚀 Starting Foundry Engine..." -ForegroundColor Green

# Activate virtual environment if it exists
if (Test-Path ".venv") {
    Write-Host "📦 Activating virtual environment..." -ForegroundColor Yellow
    .\.venv\Scripts\Activate.ps1
}

# Set environment to production if not set
if (-not $env:FOUNDRY_ENV) {
    $env:FOUNDRY_ENV = "production"
}

# Check if required environment variables are set
if (-not $env:SECRET_KEY) {
    Write-Host "⚠️  WARNING: SECRET_KEY not set. Using development key (NOT FOR PRODUCTION!)" -ForegroundColor Yellow
    $env:SECRET_KEY = "dev-secret-key-please-set-in-production-min-32-chars"
}

# Start gunicorn with config
Write-Host "🔧 Starting Gunicorn with workers..." -ForegroundColor Cyan
gunicorn main:app -c gunicorn.conf.py
