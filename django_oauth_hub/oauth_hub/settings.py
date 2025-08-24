import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# Load environment variables
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-fallback-key-change-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'oauth_manager',  # Our OAuth management app
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'oauth_hub.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'oauth_hub.wsgi.application'

# Database
if os.getenv('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# OAuth Platform Configuration
OAUTH_PLATFORMS = {
    'facebook': {
        'client_id': os.getenv('FACEBOOK_CLIENT_ID'),
        'client_secret': os.getenv('FACEBOOK_CLIENT_SECRET'),
        'auth_url': 'https://www.facebook.com/v18.0/dialog/oauth',
        'token_url': 'https://graph.facebook.com/v18.0/oauth/access_token',
        'scope': 'email,public_profile,pages_show_list,pages_read_engagement,pages_manage_posts',
        'user_info_url': 'https://graph.facebook.com/me?fields=id,name,email',
    },
    'instagram': {
        'client_id': os.getenv('INSTAGRAM_CLIENT_ID'),
        'client_secret': os.getenv('INSTAGRAM_CLIENT_SECRET'),
        'auth_url': 'https://api.instagram.com/oauth/authorize',
        'token_url': 'https://api.instagram.com/oauth/access_token',
        'scope': 'user_profile,user_media',
        'user_info_url': 'https://graph.instagram.com/me?fields=id,username',
    },
    'twitter': {
        'client_id': os.getenv('TWITTER_CLIENT_ID'),
        'client_secret': os.getenv('TWITTER_CLIENT_SECRET'),
        'auth_url': 'https://twitter.com/i/oauth2/authorize',
        'token_url': 'https://api.twitter.com/2/oauth2/token',
        'scope': 'tweet.read tweet.write users.read offline.access',
        'user_info_url': 'https://api.twitter.com/2/users/me',
    },
    'linkedin': {
        'client_id': os.getenv('LINKEDIN_CLIENT_ID'),
        'client_secret': os.getenv('LINKEDIN_CLIENT_SECRET'),
        'auth_url': 'https://www.linkedin.com/oauth/v2/authorization',
        'token_url': 'https://www.linkedin.com/oauth/v2/accessToken',
        'scope': 'profile email w_member_social',
        'user_info_url': 'https://api.linkedin.com/v2/userinfo',
    },
    'youtube': {
        'client_id': os.getenv('YOUTUBE_CLIENT_ID'),
        'client_secret': os.getenv('YOUTUBE_CLIENT_SECRET'),
        'auth_url': 'https://accounts.google.com/o/oauth2/v2/auth',
        'token_url': 'https://oauth2.googleapis.com/token',
        'scope': 'https://www.googleapis.com/auth/youtube https://www.googleapis.com/auth/userinfo.profile',
        'user_info_url': 'https://www.googleapis.com/oauth2/v2/userinfo',
    },
    'tiktok': {
        'client_id': os.getenv('TIKTOK_CLIENT_ID'),
        'client_secret': os.getenv('TIKTOK_CLIENT_SECRET'),
        'auth_url': 'https://www.tiktok.com/v2/auth/authorize/',
        'token_url': 'https://open.tiktokapis.com/v2/oauth/token/',
        'scope': 'user.info.basic video.list',
        'user_info_url': 'https://open.tiktokapis.com/v2/user/info/',
    },
    'pinterest': {
        'client_id': os.getenv('PINTEREST_CLIENT_ID'),
        'client_secret': os.getenv('PINTEREST_CLIENT_SECRET'),
        'auth_url': 'https://www.pinterest.com/oauth/',
        'token_url': 'https://api.pinterest.com/v5/oauth/token',
        'scope': 'user_accounts:read boards:read pins:read',
        'user_info_url': 'https://api.pinterest.com/v5/user_account',
    },
}

# Security Settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# CSRF Settings
CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_HTTPONLY = True
CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', '').split(',') if os.getenv('CSRF_TRUSTED_ORIGINS') else []

# Session Security
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 86400  # 24 hours

# CORS Settings
CORS_ALLOW_ALL_ORIGINS = DEBUG
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
] if DEBUG else []

# Encryption Key for Token Storage
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY', 'fallback-key-change-in-production').encode()[:32].ljust(32, b'0')

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'oauth_manager': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
    },
}
