# Django OAuth Hub - Social Media Integration Platform

A complete Django application for managing OAuth 2.0 connections to multiple social media platforms including Facebook, Instagram, Twitter, LinkedIn, YouTube, TikTok, and Pinterest.

## Features

- **Secure OAuth 2.0 Implementation**: Industry-standard OAuth 2.0 Authorization Code flow
- **Multi-Platform Support**: Connect to 7+ social media platforms
- **Encrypted Token Storage**: Tokens are encrypted using Fernet encryption
- **Real-time Status Monitoring**: Track connection status and token expiration
- **Comprehensive Logging**: Detailed logging for debugging and monitoring
- **Responsive UI**: Modern Bootstrap-based interface
- **CSRF Protection**: Built-in security measures
- **Session Management**: Secure OAuth session tracking

## Supported Platforms

| Platform | Status | Features |
|----------|--------|----------|
| Facebook | ✅ Ready | Profile access, pages management |
| Instagram | ✅ Ready | Business account integration |
| Twitter/X | ✅ Ready | Tweet management, profile access |
| LinkedIn | ✅ Ready | Profile, company pages |
| YouTube | ✅ Ready | Channel management via Google OAuth |
| TikTok | ✅ Ready | Profile and video access |
| Pinterest | ✅ Ready | Board and pin management |

## Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd django_oauth_hub
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment Configuration

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and configure your OAuth credentials:

```env
# Django Settings
DJANGO_SECRET_KEY=your-super-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Platform OAuth Credentials
FACEBOOK_CLIENT_ID=your_facebook_app_id
FACEBOOK_CLIENT_SECRET=your_facebook_app_secret

INSTAGRAM_CLIENT_ID=your_instagram_app_id
INSTAGRAM_CLIENT_SECRET=your_instagram_app_secret

# ... add other platform credentials
```

### 3. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 4. Run Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000` to access the OAuth Hub dashboard.

## OAuth Platform Setup

### Facebook Setup

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create a new app or use existing one
3. Add Facebook Login product
4. Configure redirect URI: `https://your-domain.com/oauth/callback/facebook/`
5. Copy App ID and App Secret to your `.env` file

### Instagram Setup

1. Use the same Facebook app or create a new one
2. Add Instagram Basic Display product
3. Configure redirect URI: `https://your-domain.com/oauth/callback/instagram/`
4. Copy Client ID and Client Secret

### Twitter Setup

1. Go to [Twitter Developer Portal](https://developer.twitter.com/)
2. Create a new app
3. Enable OAuth 2.0
4. Configure callback URL: `https://your-domain.com/oauth/callback/twitter/`
5. Copy Client ID and Client Secret

### LinkedIn Setup

1. Go to [LinkedIn Developers](https://www.linkedin.com/developers/)
2. Create a new app
3. Add Sign In with LinkedIn product
4. Configure redirect URL: `https://your-domain.com/oauth/callback/linkedin/`
5. Copy Client ID and Client Secret

### YouTube (Google) Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project and enable YouTube Data API v3
3. Create OAuth 2.0 credentials
4. Configure redirect URI: `https://your-domain.com/oauth/callback/youtube/`
5. Copy Client ID and Client Secret

### TikTok Setup

1. Go to [TikTok Developers](https://developers.tiktok.com/)
2. Create a new app
3. Configure redirect URI: `https://your-domain.com/oauth/callback/tiktok/`
4. Copy Client Key and Client Secret

### Pinterest Setup

1. Go to [Pinterest Developers](https://developers.pinterest.com/)
2. Create a new app
3. Configure redirect URI: `https://your-domain.com/oauth/callback/pinterest/`
4. Copy App ID and App Secret

## Project Structure

```
django_oauth_hub/
├── oauth_hub/               # Django project settings
│   ├── settings.py         # Main settings file
│   ├── urls.py            # URL configuration
│   ├── wsgi.py            # WSGI configuration
│   └── asgi.py            # ASGI configuration
├── oauth_manager/          # Main OAuth app
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── urls.py            # App URLs
│   ├── admin.py           # Admin configuration
│   ├── utils.py           # Utility functions
│   └── templatetags/      # Custom template filters
├── templates/             # HTML templates
│   ├── base.html         # Base template
│   └── oauth_manager/    # App templates
├── static/               # Static files (CSS, JS)
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── Procfile            # Heroku deployment
└── manage.py           # Django management script
```

## Database Models

### PlatformConnection
Stores OAuth connections and encrypted tokens for each user-platform combination.

### OAuthSession
Tracks OAuth sessions with state parameters for CSRF protection.

### ConnectionLog
Logs all connection events for debugging and monitoring.

## Security Features

- **Token Encryption**: All access and refresh tokens are encrypted using Fernet
- **CSRF Protection**: State parameter validation for OAuth flows
- **Session Security**: Secure session configuration
- **Input Validation**: Comprehensive input validation and sanitization
- **Error Handling**: Secure error handling without information leakage

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page |
| `/dashboard/` | GET | Main dashboard |
| `/oauth/initiate/<platform>/` | POST | Initiate OAuth flow |
| `/oauth/callback/<platform>/` | GET | OAuth callback handler |
| `/platform/disconnect/<platform>/` | POST | Disconnect platform |
| `/platform/status/<platform>/` | GET | Get connection status |
| `/create-demo-user/` | GET | Create demo user (DEBUG only) |

## Deployment

### Heroku Deployment

1. **Create Heroku App**
   ```bash
   heroku create your-oauth-hub-app
   ```

2. **Configure Environment Variables**
   ```bash
   heroku config:set DJANGO_SECRET_KEY=your-secret-key
   heroku config:set DEBUG=False
   heroku config:set FACEBOOK_CLIENT_ID=your-facebook-id
   # ... add all other environment variables
   ```

3. **Deploy**
   ```bash
   git push heroku main
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

### Railway Deployment

1. **Connect Repository**
   - Go to [Railway](https://railway.app)
   - Connect your GitHub repository

2. **Configure Environment Variables**
   - Add all variables from `.env.example`
   - Set `DEBUG=False` for production

3. **Deploy**
   - Railway will automatically build and deploy
   - Run migrations via Railway's web interface

### DigitalOcean App Platform

1. **Create App**
   - Go to DigitalOcean App Platform
   - Connect your repository

2. **Configure Environment Variables**
   - Add all required environment variables
   - Set appropriate app size and region

3. **Database Setup**
   - Add PostgreSQL database addon
   - Configure `DATABASE_URL`

### Local Development with Docker (Optional)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "oauth_hub.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## Testing

### Demo Mode

For quick testing, use the demo user feature:

1. Visit `/create-demo-user/` (only works when `DEBUG=True`)
2. This creates a demo user and logs you in automatically
3. Access the dashboard to test OAuth flows

### Manual Testing

1. Configure at least one platform's OAuth credentials
2. Access the dashboard
3. Click "Configure" for a platform
4. Complete the OAuth flow
5. Verify the connection status updates

## Monitoring and Logs

### Connection Logs

All OAuth events are logged in the `ConnectionLog` model:
- OAuth initiation
- Callback received
- Token exchange
- Successful connections
- Disconnections
- Errors

### Django Admin

Access `/admin/` to:
- View all platform connections
- Monitor OAuth sessions
- Review connection logs
- Manage users

## Troubleshooting

### Common Issues

1. **"Platform not configured" error**
   - Check that environment variables are set correctly
   - Verify client ID and secret are not empty

2. **OAuth callback errors**
   - Ensure redirect URIs match exactly in platform settings
   - Check that the domain is accessible (not localhost for production)

3. **Token encryption errors**
   - Verify `ENCRYPTION_KEY` is set and 32 characters long
   - Check that cryptography package is installed correctly

4. **Database connection errors**
   - For production, ensure `DATABASE_URL` is configured
   - For development, SQLite should work out of the box

### Debug Mode

Enable debug mode for detailed error information:
```env
DEBUG=True
```

Check Django logs for detailed OAuth flow information.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Support

For support and questions:
- Check the troubleshooting section
- Review the Django logs
- Open an issue on GitHub

## Changelog

### v1.0.0
- Initial release
- Support for 7 major social media platforms
- Secure OAuth 2.0 implementation
- Responsive web interface
- Comprehensive logging and monitoring
