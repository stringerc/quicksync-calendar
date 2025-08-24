# Django OAuth Hub - Railway Deployment Guide

## Quick Deploy to Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https%3A%2F%2Fgithub.com%2Fyourusername%2Fdjango-oauth-hub)

### Step 1: Deploy to Railway

1. **Create Railway Account**: Go to [railway.app](https://railway.app) and sign up
2. **New Project**: Click "New Project" → "Deploy from GitHub repo"
3. **Upload Code**: Upload the `django_oauth_hub` folder or connect a GitHub repo
4. **Auto-Deploy**: Railway will automatically detect Django and deploy

### Step 2: Configure Environment Variables

In Railway dashboard, go to your project → **Variables** tab and add:

```env
# Essential Django Settings
DJANGO_SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=*.railway.app,yourdomain.com

# Database (Railway provides PostgreSQL automatically)
DATABASE_URL=postgresql://... (auto-provided by Railway)

# OAuth Platform Credentials
FACEBOOK_CLIENT_ID=your_facebook_app_id
FACEBOOK_CLIENT_SECRET=your_facebook_app_secret

INSTAGRAM_CLIENT_ID=your_instagram_app_id
INSTAGRAM_CLIENT_SECRET=your_instagram_app_secret

# Add other platforms as needed...

# Security
ENCRYPTION_KEY=your-32-character-encryption-key
CSRF_TRUSTED_ORIGINS=https://your-app.railway.app

# Optional: Admin user creation
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@yoursite.com
DJANGO_SUPERUSER_PASSWORD=secure-password
```

### Step 3: Get Your App URL

After deployment, Railway will provide a URL like:
```
https://django-oauth-hub-production.railway.app
```

### Step 4: Facebook App Configuration

Use this **exact redirect URI** in your Facebook app:
```
https://YOUR-RAILWAY-URL.railway.app/oauth/callback/facebook/
```

**Example:**
```
https://django-oauth-hub-production.railway.app/oauth/callback/facebook/
```

## What Railway Provides

- **✅ PostgreSQL Database** - Automatically provisioned
- **✅ HTTPS SSL Certificate** - Automatic and free
- **✅ Custom Domain Support** - Connect your domain
- **✅ Environment Variables** - Secure credential storage
- **✅ Automatic Deployments** - Deploy on git push
- **✅ Logs & Monitoring** - Built-in logging and metrics

## Railway Pricing

- **Hobby Plan**: Free tier with 500 execution hours/month
- **Pro Plan**: $5/month for unlimited usage
- **Database**: $5/month for PostgreSQL

## Alternative Quick Deploy Commands

If you prefer command line:

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway link
railway up
```

## Custom Domain Setup

1. In Railway dashboard → **Settings** → **Domains**
2. Add your custom domain: `oauthhub.yourdomain.com`
3. Update DNS with provided CNAME record
4. Update `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` in environment variables

## Troubleshooting

- **Deploy Failed**: Check Railway logs in dashboard
- **Database Issues**: Railway auto-provides PostgreSQL, no setup needed
- **Static Files**: Run `python manage.py collectstatic` (done automatically)
- **Migrations**: Run automatically during deployment

## Support

For Railway-specific issues:
- [Railway Documentation](https://docs.railway.app/)
- [Railway Discord Community](https://railway.app/discord)

For OAuth Hub issues:
- Check application logs in Railway dashboard
- Review Django logs for OAuth flow issues
