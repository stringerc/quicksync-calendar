#!/bin/bash

# Django OAuth Hub - Quick Setup Script
# This script helps set up the development environment quickly

echo "🔗 Django OAuth Hub - Quick Setup"
echo "=================================="
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.8+ and try again."
    exit 1
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is required but not installed."
    echo "Please install pip3 and try again."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo "✅ pip3 found: $(pip3 --version)"
echo

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Copy environment file
if [ ! -f ".env" ]; then
    echo "⚙️ Creating environment configuration..."
    cp .env.example .env
    echo "✅ Created .env file from template"
    echo "🔧 Please edit .env file with your OAuth credentials"
else
    echo "✅ .env file already exists"
fi

# Generate encryption key if needed
echo "🔐 Generating secure keys..."
python generate_keys.py > keys.txt
echo "✅ Generated secure keys (saved to keys.txt)"
echo "🔧 Please add these keys to your .env file"

# Run migrations
echo "🗄️ Setting up database..."
python manage.py makemigrations
python manage.py migrate

echo
echo "🎉 Setup Complete!"
echo
echo "Next steps:"
echo "1. Edit .env file with your OAuth platform credentials"
echo "2. Add the generated keys from keys.txt to your .env file"
echo "3. Create a superuser: python manage.py createsuperuser"
echo "4. Run the development server: python manage.py runserver"
echo
echo "📖 For detailed instructions, see README.md"
echo "🚀 For deployment instructions, see DEPLOYMENT.md"
