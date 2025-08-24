#!/usr/bin/env python
"""
Django OAuth Hub - Development Server Runner

This script helps run the development server with proper configuration.
It also performs basic setup checks and provides helpful information.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_environment():
    """Check if the environment is properly set up."""
    issues = []
    
    # Check if .env file exists
    if not Path('.env').exists():
        issues.append(".env file not found. Copy from .env.example and configure.")
    
    # Check if virtual environment is activated
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        issues.append("Virtual environment not activated. Run 'source venv/bin/activate' first.")
    
    # Check if database exists
    if not Path('db.sqlite3').exists():
        issues.append("Database not found. Run 'python manage.py migrate' first.")
    
    # Check if required packages are installed
    try:
        import django
        import requests
        import cryptography
    except ImportError as e:
        issues.append(f"Required package missing: {e.name}. Run 'pip install -r requirements.txt'.")
    
    return issues

def print_info():
    """Print helpful information about the application."""
    print("🔗 Django OAuth Hub - Development Server")
    print("=" * 45)
    print()
    print("📍 Local URLs:")
    print("   • Main Application: http://localhost:8000/")
    print("   • Admin Interface:  http://localhost:8000/admin/")
    print("   • Demo User Login:  http://localhost:8000/create-demo-user/")
    print()
    print("🔧 Useful Commands:")
    print("   • Create superuser: python manage.py createsuperuser")
    print("   • Run tests:        python manage.py test")
    print("   • Generate keys:    python generate_keys.py")
    print()
    print("📚 Documentation:")
    print("   • Setup Guide:      README.md")
    print("   • Deployment:       DEPLOYMENT.md")
    print("   • Contributing:     CONTRIBUTING.md")
    print()
    print("🚀 OAuth Platform Setup:")
    print("   Remember to configure redirect URIs in your OAuth apps:")
    print("   http://localhost:8000/oauth/callback/<platform>/")
    print()

def main():
    """Main function to run development server with checks."""
    print_info()
    
    # Check environment
    issues = check_environment()
    if issues:
        print("❌ Environment Issues Found:")
        for issue in issues:
            print(f"   • {issue}")
        print()
        print("Please fix these issues and try again.")
        return 1
    
    print("✅ Environment looks good!")
    print("🚀 Starting development server...")
    print()
    
    # Run development server
    try:
        subprocess.run([sys.executable, 'manage.py', 'runserver', '0.0.0.0:8000'], check=True)
    except KeyboardInterrupt:
        print("\n\n👋 Development server stopped.")
        print("Thanks for using Django OAuth Hub!")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Server failed to start: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
