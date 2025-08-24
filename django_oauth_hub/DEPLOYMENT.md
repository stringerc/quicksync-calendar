# Deployment Guide - Django OAuth Hub

This guide provides step-by-step instructions for deploying the Django OAuth Hub to various cloud platforms.

## Pre-Deployment Checklist

Before deploying to any platform, ensure you have:

- [ ] Set up OAuth applications for desired platforms
- [ ] Collected all client IDs and secrets
- [ ] Generated a strong Django secret key
- [ ] Tested the application locally

## Platform-Specific Deployment Instructions

### 1. Heroku Deployment

#### Prerequisites
- Heroku CLI installed
- Git repository initialized

#### Step-by-Step Instructions

1. **Install Heroku CLI** (if not already installed)
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   
   # Windows
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   
   # Ubuntu
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku Application**
   ```bash
   heroku create your-oauth-hub-name
   ```

4. **Add PostgreSQL Database**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

5. **Configure Environment Variables**
   ```bash
   # Required Django settings
   heroku config:set DJANGO_SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS=your-oauth-hub-name.herokuapp.com
   
   # OAuth Platform Credentials
   heroku config:set FACEBOOK_CLIENT_ID=your_facebook_app_id
   heroku config:set FACEBOOK_CLIENT_SECRET=your_facebook_app_secret
   
   heroku config:set INSTAGRAM_CLIENT_ID=your_instagram_app_id
   heroku config:set INSTAGRAM_CLIENT_SECRET=your_instagram_app_secret
   
   heroku config:set TWITTER_CLIENT_ID=your_twitter_client_id
   heroku config:set TWITTER_CLIENT_SECRET=your_twitter_client_secret
   
   heroku config:set LINKEDIN_CLIENT_ID=your_linkedin_client_id
   heroku config:set LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
   
   heroku config:set YOUTUBE_CLIENT_ID=your_youtube_client_id
   heroku config:set YOUTUBE_CLIENT_SECRET=your_youtube_client_secret
   
   heroku config:set TIKTOK_CLIENT_ID=your_tiktok_client_id
   heroku config:set TIKTOK_CLIENT_SECRET=your_tiktok_client_secret
   
   heroku config:set PINTEREST_CLIENT_ID=your_pinterest_client_id
   heroku config:set PINTEREST_CLIENT_SECRET=your_pinterest_client_secret
   
   # Security settings
   heroku config:set ENCRYPTION_KEY=$(python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())')
   heroku config:set CSRF_TRUSTED_ORIGINS=https://your-oauth-hub-name.herokuapp.com
   ```

6. **Deploy to Heroku**
   ```bash
   git add .
   git commit -m "Initial deployment"
   git push heroku main
   ```

7. **Run Database Migrations**
   ```bash
   heroku run python manage.py migrate
   ```

8. **Create Superuser**
   ```bash
   heroku run python manage.py createsuperuser
   ```

9. **Open Application**
   ```bash
   heroku open
   ```

#### Update OAuth Platform Redirect URIs

Update all your OAuth platform applications with the new redirect URIs:
- Facebook: `https://your-oauth-hub-name.herokuapp.com/oauth/callback/facebook/`
- Instagram: `https://your-oauth-hub-name.herokuapp.com/oauth/callback/instagram/`
- Twitter: `https://your-oauth-hub-name.herokuapp.com/oauth/callback/twitter/`
- LinkedIn: `https://your-oauth-hub-name.herokuapp.com/oauth/callback/linkedin/`
- YouTube: `https://your-oauth-hub-name.herokuapp.com/oauth/callback/youtube/`
- TikTok: `https://your-oauth-hub-name.herokuapp.com/oauth/callback/tiktok/`
- Pinterest: `https://your-oauth-hub-name.herokuapp.com/oauth/callback/pinterest/`

### 2. Railway Deployment

#### Prerequisites
- GitHub account with repository
- Railway account

#### Step-by-Step Instructions

1. **Connect to Railway**
   - Go to [Railway](https://railway.app)
   - Sign in with GitHub
   - Click "Start a New Project"
   - Select "Deploy from GitHub repo"
   - Choose your OAuth Hub repository

2. **Add PostgreSQL Database**
   - In Railway dashboard, click "Add"
   - Select "Database" → "PostgreSQL"
   - Railway will automatically set `DATABASE_URL`

3. **Configure Environment Variables**
   - Go to your app in Railway dashboard
   - Click "Variables" tab
   - Add the following variables:

   ```
   DJANGO_SECRET_KEY=your-generated-secret-key
   DEBUG=False
   ALLOWED_HOSTS=your-app-name.up.railway.app
   
   FACEBOOK_CLIENT_ID=your_facebook_app_id
   FACEBOOK_CLIENT_SECRET=your_facebook_app_secret
   
   INSTAGRAM_CLIENT_ID=your_instagram_app_id
   INSTAGRAM_CLIENT_SECRET=your_instagram_app_secret
   
   TWITTER_CLIENT_ID=your_twitter_client_id
   TWITTER_CLIENT_SECRET=your_twitter_client_secret
   
   LINKEDIN_CLIENT_ID=your_linkedin_client_id
   LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
   
   YOUTUBE_CLIENT_ID=your_youtube_client_id
   YOUTUBE_CLIENT_SECRET=your_youtube_client_secret
   
   TIKTOK_CLIENT_ID=your_tiktok_client_id
   TIKTOK_CLIENT_SECRET=your_tiktok_client_secret
   
   PINTEREST_CLIENT_ID=your_pinterest_client_id
   PINTEREST_CLIENT_SECRET=your_pinterest_client_secret
   
   ENCRYPTION_KEY=your-32-character-encryption-key
   CSRF_TRUSTED_ORIGINS=https://your-app-name.up.railway.app
   ```

4. **Deploy**
   - Railway will automatically build and deploy
   - Monitor the deployment logs for any issues

5. **Run Migrations**
   - In Railway dashboard, go to your app
   - Click "Deploy" → "View Logs"
   - Use the terminal to run: `python manage.py migrate`
   - Create superuser: `python manage.py createsuperuser`

6. **Update OAuth Redirect URIs**
   Update all platform redirect URIs to use your Railway domain:
   `https://your-app-name.up.railway.app/oauth/callback/<platform>/`

### 3. DigitalOcean App Platform

#### Prerequisites
- DigitalOcean account
- GitHub repository

#### Step-by-Step Instructions

1. **Create App**
   - Go to [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
   - Click "Create App"
   - Connect your GitHub account
   - Select your OAuth Hub repository
   - Choose the main branch

2. **Configure Build Settings**
   - App Type: Web Service
   - HTTP Port: 8000
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `gunicorn oauth_hub.wsgi --bind 0.0.0.0:8000`

3. **Add Database**
   - Click "Add Component"
   - Select "Database"
   - Choose "PostgreSQL"
   - Select appropriate plan

4. **Configure Environment Variables**
   ```
   DJANGO_SECRET_KEY=your-secret-key
   DEBUG=False
   DATABASE_URL=${db.DATABASE_URL}
   ALLOWED_HOSTS=your-app-name.ondigitalocean.app
   
   # Add all OAuth platform credentials
   FACEBOOK_CLIENT_ID=your_facebook_app_id
   FACEBOOK_CLIENT_SECRET=your_facebook_app_secret
   # ... (add all other platform credentials)
   
   ENCRYPTION_KEY=your-encryption-key
   CSRF_TRUSTED_ORIGINS=https://your-app-name.ondigitalocean.app
   ```

5. **Deploy**
   - Review configuration
   - Click "Create Resources"
   - Wait for deployment to complete

6. **Run Migrations**
   - Use DigitalOcean console to access your app
   - Run: `python manage.py migrate`
   - Run: `python manage.py createsuperuser`

### 4. Local Development Setup

#### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

#### Instructions

1. **Clone Repository**
   ```bash
   git clone <your-repository-url>
   cd django_oauth_hub
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # Activate (Linux/macOS)
   source venv/bin/activate
   
   # Activate (Windows)
   venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your OAuth credentials
   ```

5. **Setup Database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

7. **Configure OAuth Platforms**
   For local development, use these redirect URIs:
   - `http://localhost:8000/oauth/callback/<platform>/`

### 5. Docker Deployment

#### Create Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "oauth_hub.wsgi:application", "--bind", "0.0.0.0:8000"]
```

#### Create docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://oauth_user:oauth_pass@db:5432/oauth_hub_db
    depends_on:
      - db
    env_file:
      - .env

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=oauth_hub_db
      - POSTGRES_USER=oauth_user
      - POSTGRES_PASSWORD=oauth_pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

#### Deploy with Docker
```bash
# Build and run
docker-compose up --build

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

## Post-Deployment Configuration

### 1. OAuth Platform Configuration

After deployment, update all OAuth platforms with your production URLs:

#### Facebook
- Go to Facebook Developers Console
- Update Valid OAuth Redirect URIs
- Add: `https://your-domain.com/oauth/callback/facebook/`

#### Instagram
- Update redirect URI in Facebook app settings
- Add: `https://your-domain.com/oauth/callback/instagram/`

#### Twitter
- Go to Twitter Developer Portal
- Update Callback URL
- Add: `https://your-domain.com/oauth/callback/twitter/`

#### LinkedIn
- Go to LinkedIn Developer Console
- Update Authorized redirect URLs
- Add: `https://your-domain.com/oauth/callback/linkedin/`

#### YouTube (Google)
- Go to Google Cloud Console
- Update Authorized redirect URIs
- Add: `https://your-domain.com/oauth/callback/youtube/`

#### TikTok
- Go to TikTok Developer Portal
- Update Redirect URI
- Add: `https://your-domain.com/oauth/callback/tiktok/`

#### Pinterest
- Go to Pinterest Developer Console
- Update Redirect URI
- Add: `https://your-domain.com/oauth/callback/pinterest/`

### 2. SSL Certificate

Ensure your deployment has SSL/HTTPS enabled. Most platforms require HTTPS for OAuth callbacks.

### 3. Domain Configuration

Update the following in your production environment:
- `ALLOWED_HOSTS` to include your domain
- `CSRF_TRUSTED_ORIGINS` to include your HTTPS domain
- OAuth platform redirect URIs

### 4. Security Checklist

- [ ] `DEBUG=False` in production
- [ ] Strong `DJANGO_SECRET_KEY`
- [ ] Secure `ENCRYPTION_KEY` for token storage
- [ ] Database connections are secure
- [ ] All environment variables are set
- [ ] OAuth redirect URIs use HTTPS
- [ ] Error pages don't leak sensitive information

## Monitoring and Maintenance

### 1. Logs Monitoring

- Monitor application logs for OAuth errors
- Check database connection logs
- Monitor token refresh operations

### 2. Database Maintenance

- Regular backups
- Monitor connection counts
- Clean up expired OAuth sessions

### 3. Token Management

- Monitor token expiration rates
- Check for failed refresh attempts
- Audit connection logs regularly

### 4. Security Updates

- Keep Django and dependencies updated
- Regularly rotate OAuth secrets
- Monitor for security advisories

## Troubleshooting Deployment Issues

### Common Issues

1. **OAuth Redirect URI Mismatch**
   - Ensure exact URL match including trailing slashes
   - Check HTTPS vs HTTP
   - Verify domain name is correct

2. **Environment Variables Not Set**
   - Double-check all required variables are configured
   - Restart application after setting new variables

3. **Database Connection Errors**
   - Verify DATABASE_URL format
   - Check database service is running
   - Ensure migrations are applied

4. **Static Files Not Loading**
   - Run `python manage.py collectstatic`
   - Check STATIC_ROOT configuration
   - Verify web server serves static files

5. **Token Encryption Errors**
   - Ensure ENCRYPTION_KEY is exactly 32 characters
   - Verify cryptography package is installed

### Getting Help

- Check application logs for detailed error messages
- Review Django debug information when DEBUG=True
- Consult platform-specific documentation
- Test OAuth flows with minimal examples

## Performance Optimization

### 1. Database Optimization

- Add appropriate database indexes
- Use connection pooling
- Regular database maintenance

### 2. Caching

Consider adding Redis for session storage and caching:

```python
# Add to settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
```

### 3. Monitoring

Set up monitoring for:
- Response times
- Error rates
- Database performance
- OAuth success rates

This completes the comprehensive deployment guide for the Django OAuth Hub application.
