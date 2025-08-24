#!/bin/bash

# Railway Deployment Script for Django OAuth Hub
# This script sets up the Django application for Railway deployment

echo "🚀 Starting Django OAuth Hub deployment setup..."

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Generate Django secret key if not provided
if [ -z "$DJANGO_SECRET_KEY" ]; then
    echo "🔐 Generating Django secret key..."
    export DJANGO_SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
fi

# Generate encryption key if not provided
if [ -z "$ENCRYPTION_KEY" ]; then
    echo "🔐 Generating encryption key..."
    export ENCRYPTION_KEY=$(python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())')
fi

# Run database migrations
echo "🗄️ Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Collect static files
echo "📄 Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if credentials are provided
if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_EMAIL" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "👤 Creating superuser..."
    python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL
fi

echo "✅ Deployment setup complete!"
echo "🌐 Starting web server..."

# Start the application
if [ "$PORT" ]; then
    gunicorn oauth_hub.wsgi:application --bind 0.0.0.0:$PORT --workers 2
else
    gunicorn oauth_hub.wsgi:application --bind 0.0.0.0:8000 --workers 2
fi