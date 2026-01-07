#!/bin/bash
# Production startup script for Foundry Engine

set -e  # Exit on error

echo "🚀 Starting Foundry Engine..."

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo "📦 Activating virtual environment..."
    source .venv/bin/activate
fi

# Set environment to production if not set
export FOUNDRY_ENV=${FOUNDRY_ENV:-production}

# Check if required environment variables are set
if [ -z "$SECRET_KEY" ]; then
    echo "⚠️  WARNING: SECRET_KEY not set. Using development key (NOT FOR PRODUCTION!)"
    export SECRET_KEY="dev-secret-key-please-set-in-production-min-32-chars"
fi

# Run database migrations if needed (future enhancement)
# python -m alembic upgrade head

# Start gunicorn with config
echo "🔧 Starting Gunicorn with workers..."
exec gunicorn main:app -c gunicorn.conf.py
