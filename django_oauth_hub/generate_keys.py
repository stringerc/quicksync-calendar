#!/usr/bin/env python
"""
Utility script to generate secure keys for Django OAuth Hub.
"""

import secrets
import string
from cryptography.fernet import Fernet
from django.core.management.utils import get_random_secret_key

def generate_django_secret_key():
    """Generate a secure Django secret key."""
    return get_random_secret_key()

def generate_encryption_key():
    """Generate a secure Fernet encryption key."""
    return Fernet.generate_key().decode()

def generate_oauth_state():
    """Generate a secure OAuth state parameter."""
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))

if __name__ == '__main__':
    print("Django OAuth Hub - Key Generator")
    print("=" * 40)
    print()
    print("Django Secret Key:")
    print(generate_django_secret_key())
    print()
    print("Encryption Key (for token storage):")
    print(generate_encryption_key())
    print()
    print("Sample OAuth State:")
    print(generate_oauth_state())
    print()
    print("Add these to your .env file:")
    print(f"DJANGO_SECRET_KEY={generate_django_secret_key()}")
    print(f"ENCRYPTION_KEY={generate_encryption_key()}")
