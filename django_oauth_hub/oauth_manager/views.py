from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
import requests
import secrets
import string
import json
import logging
from urllib.parse import urlencode, parse_qs, urlparse
from .models import PlatformConnection, OAuthSession, ConnectionLog
from .utils import get_client_ip, get_user_agent

logger = logging.getLogger(__name__)


def generate_state():
    """Generate a secure random state parameter for OAuth."""
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))


def log_connection_event(connection, action, details=None, request=None):
    """Log connection events for debugging and monitoring."""
    ConnectionLog.objects.create(
        connection=connection,
        action=action,
        details=details,
        ip_address=get_client_ip(request) if request else None,
        user_agent=get_user_agent(request) if request else None,
    )


def create_demo_user(request):
    """Create a demo user for testing purposes."""
    if settings.DEBUG:
        demo_user, created = User.objects.get_or_create(
            username='demo_user',
            defaults={
                'email': 'demo@example.com',
                'first_name': 'Demo',
                'last_name': 'User',
            }
        )
        if created:
            demo_user.set_password('demo_password_123')
            demo_user.save()
        
        login(request, demo_user)
        messages.success(request, 'Logged in as demo user for testing.')
        return redirect('dashboard')
    else:
        messages.error(request, 'Demo user creation is only available in DEBUG mode.')
        return redirect('dashboard')


@login_required
def dashboard(request):
    """Main dashboard showing all platform connections."""
    # Get or create connections for all supported platforms
    connections = {}
    
    for platform_key, platform_name in PlatformConnection.PLATFORM_CHOICES:
        connection, created = PlatformConnection.objects.get_or_create(
            user=request.user,
            platform=platform_key,
            defaults={'status': 'disconnected'}
        )
        
        # Check if token has expired
        if connection.is_connected and connection.is_token_expired:
            connection.status = 'expired'
            connection.save()
        
        connections[platform_key] = connection
    
    # Clean up expired OAuth sessions
    OAuthSession.cleanup_expired_sessions()
    
    context = {
        'connections': connections,
        'platforms': settings.OAUTH_PLATFORMS,
    }
    
    return render(request, 'oauth_manager/dashboard.html', context)


@login_required
@require_http_methods(["POST"])
def initiate_oauth(request, platform):
    """Initiate OAuth flow for a specific platform."""
    if platform not in dict(PlatformConnection.PLATFORM_CHOICES):
        messages.error(request, f'Unsupported platform: {platform}')
        return redirect('dashboard')
    
    platform_config = settings.OAUTH_PLATFORMS.get(platform)
    if not platform_config or not platform_config.get('client_id'):
        messages.error(request, f'Platform {platform} is not configured. Please check your environment variables.')
        return redirect('dashboard')
    
    try:
        # Get or create platform connection
        connection, _ = PlatformConnection.objects.get_or_create(
            user=request.user,
            platform=platform,
            defaults={'status': 'disconnected'}
        )
        
        # Generate secure state parameter
        state = generate_state()
        
        # Build redirect URI
        redirect_uri = request.build_absolute_uri(reverse('oauth_callback', kwargs={'platform': platform}))
        
        # Create OAuth session for tracking
        oauth_session = OAuthSession.objects.create(
            user=request.user,
            platform=platform,
            state=state,
            redirect_uri=redirect_uri,
        )
        
        # Update connection status
        connection.status = 'connecting'
        connection.save()
        
        # Log the initiation
        log_connection_event(connection, 'initiated', f'OAuth flow initiated for {platform}', request)
        
        # Build authorization URL
        auth_params = {
            'client_id': platform_config['client_id'],
            'redirect_uri': redirect_uri,
            'scope': platform_config['scope'],
            'state': state,
            'response_type': 'code',
        }
        
        # Platform-specific parameters
        if platform == 'facebook':
            auth_params['display'] = 'popup'
        elif platform == 'linkedin':
            auth_params['response_type'] = 'code'
        elif platform == 'twitter':
            auth_params['code_challenge_method'] = 'plain'
            auth_params['code_challenge'] = state  # Simple PKCE for Twitter
        
        auth_url = f"{platform_config['auth_url']}?{urlencode(auth_params)}"
        
        logger.info(f"Redirecting user {request.user.username} to {platform} OAuth: {auth_url}")
        
        return redirect(auth_url)
    
    except Exception as e:
        logger.error(f"Error initiating OAuth for {platform}: {e}")
        messages.error(request, f'Failed to initiate {platform} connection. Please try again.')
        return redirect('dashboard')


def oauth_callback(request, platform):
    """Handle OAuth callback from platforms."""
    if platform not in dict(PlatformConnection.PLATFORM_CHOICES):
        return HttpResponseBadRequest(f'Unsupported platform: {platform}')
    
    code = request.GET.get('code')
    state = request.GET.get('state')
    error = request.GET.get('error')
    error_description = request.GET.get('error_description', '')
    
    if error:
        error_msg = f"{platform} OAuth error: {error}. {error_description}"
        logger.warning(f"OAuth error for platform {platform}: {error_msg}")
        messages.error(request, f'Authentication failed: {error_description or error}')
        return redirect('dashboard')
    
    if not code or not state:
        logger.warning(f"Missing code or state in OAuth callback for {platform}")
        messages.error(request, 'Invalid OAuth callback. Missing authorization code or state.')
        return redirect('dashboard')
    
    try:
        # Find and validate OAuth session
        oauth_session = get_object_or_404(OAuthSession, state=state, platform=platform, is_active=True)
        
        # Check if session is expired (1 hour)
        if timezone.now() - oauth_session.created_at > timezone.timedelta(hours=1):
            oauth_session.is_active = False
            oauth_session.save()
            messages.error(request, 'OAuth session expired. Please try connecting again.')
            return redirect('dashboard')
        
        # Get platform connection
        connection = get_object_or_404(
            PlatformConnection,
            user=oauth_session.user,
            platform=platform
        )
        
        # Log callback received
        log_connection_event(connection, 'callback_received', f'Code: {code[:10]}...', request)
        
        # Exchange authorization code for access token
        platform_config = settings.OAUTH_PLATFORMS[platform]
        token_data = exchange_code_for_token(platform, code, oauth_session.redirect_uri, platform_config)
        
        if not token_data:
            connection.set_error('Failed to exchange authorization code for access token')
            messages.error(request, f'Failed to complete {platform} authentication. Please try again.')
            return redirect('dashboard')
        
        # Log successful token exchange
        log_connection_event(connection, 'token_exchanged', 'Successfully exchanged code for token', request)
        
        # Get user information from platform
        user_info = get_platform_user_info(platform, token_data['access_token'], platform_config)
        
        # Update connection with token and user info
        connection.set_connected(
            access_token=token_data['access_token'],
            refresh_token=token_data.get('refresh_token'),
            expires_in=token_data.get('expires_in'),
            user_info=user_info,
            scope=token_data.get('scope')
        )
        
        # Complete OAuth session
        oauth_session.complete_session()
        
        # Log successful connection
        log_connection_event(
            connection, 
            'connected', 
            f"Connected as {user_info.get('name', user_info.get('username', 'Unknown'))}", 
            request
        )
        
        messages.success(request, f'Successfully connected to {platform.title()}!')
        logger.info(f"User {request.user.username} successfully connected to {platform}")
        
        return redirect('dashboard')
    
    except OAuthSession.DoesNotExist:
        logger.warning(f"Invalid OAuth session state: {state}")
        messages.error(request, 'Invalid OAuth session. Please try connecting again.')
        return redirect('dashboard')
    
    except Exception as e:
        logger.error(f"Error processing OAuth callback for {platform}: {e}")
        try:
            connection = PlatformConnection.objects.get(user__oauth_sessions__state=state, platform=platform)
            connection.set_error(f'OAuth callback error: {str(e)}')
        except PlatformConnection.DoesNotExist:
            pass
        
        messages.error(request, f'Failed to complete {platform} authentication. Please try again.')
        return redirect('dashboard')


def exchange_code_for_token(platform, code, redirect_uri, platform_config):
    """Exchange authorization code for access token."""
    try:
        token_data = {
            'client_id': platform_config['client_id'],
            'client_secret': platform_config['client_secret'],
            'code': code,
            'redirect_uri': redirect_uri,
        }
        
        # Platform-specific token exchange parameters
        if platform == 'facebook':
            token_data['grant_type'] = 'authorization_code'
        elif platform == 'instagram':
            token_data['grant_type'] = 'authorization_code'
        elif platform == 'twitter':
            token_data['grant_type'] = 'authorization_code'
            token_data['code_verifier'] = code  # Simple PKCE
        elif platform == 'linkedin':
            token_data['grant_type'] = 'authorization_code'
        elif platform == 'youtube':
            token_data['grant_type'] = 'authorization_code'
        elif platform in ['tiktok', 'pinterest']:
            token_data['grant_type'] = 'authorization_code'
        
        headers = {'Accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
        
        response = requests.post(
            platform_config['token_url'],
            data=token_data,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            token_response = response.json()
            logger.info(f"Successfully exchanged code for {platform} token")
            return token_response
        else:
            logger.error(f"Token exchange failed for {platform}: {response.status_code} - {response.text}")
            return None
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error during token exchange for {platform}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during token exchange for {platform}: {e}")
        return None


def get_platform_user_info(platform, access_token, platform_config):
    """Get user information from platform API."""
    try:
        headers = {'Authorization': f'Bearer {access_token}'}
        
        # Platform-specific headers
        if platform == 'facebook':
            headers = {'Authorization': f'Bearer {access_token}'}
        elif platform == 'twitter':
            headers = {'Authorization': f'Bearer {access_token}'}
        
        response = requests.get(
            platform_config['user_info_url'],
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            user_info = response.json()
            logger.info(f"Successfully fetched user info for {platform}")
            return user_info
        else:
            logger.warning(f"Failed to fetch user info for {platform}: {response.status_code}")
            return {}
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error fetching user info for {platform}: {e}")
        return {}
    except Exception as e:
        logger.error(f"Unexpected error fetching user info for {platform}: {e}")
        return {}


@login_required
@require_http_methods(["POST"])
def disconnect_platform(request, platform):
    """Disconnect a platform connection."""
    if platform not in dict(PlatformConnection.PLATFORM_CHOICES):
        return JsonResponse({'error': 'Unsupported platform'}, status=400)
    
    try:
        connection = get_object_or_404(PlatformConnection, user=request.user, platform=platform)
        
        # Log disconnection
        log_connection_event(connection, 'disconnected', 'User manually disconnected', request)
        
        # Disconnect the platform
        connection.disconnect()
        
        logger.info(f"User {request.user.username} disconnected from {platform}")
        messages.success(request, f'Successfully disconnected from {platform.title()}.')
        
        if request.headers.get('Accept') == 'application/json':
            return JsonResponse({'success': True, 'message': f'Disconnected from {platform.title()}'})
        else:
            return redirect('dashboard')
    
    except Exception as e:
        logger.error(f"Error disconnecting from {platform}: {e}")
        error_msg = f'Failed to disconnect from {platform.title()}. Please try again.'
        
        if request.headers.get('Accept') == 'application/json':
            return JsonResponse({'error': error_msg}, status=500)
        else:
            messages.error(request, error_msg)
            return redirect('dashboard')


@login_required
def connection_status(request, platform):
    """Get connection status for a platform (API endpoint)."""
    if platform not in dict(PlatformConnection.PLATFORM_CHOICES):
        return JsonResponse({'error': 'Unsupported platform'}, status=400)
    
    try:
        connection = get_object_or_404(PlatformConnection, user=request.user, platform=platform)
        
        # Check token expiration
        if connection.is_connected and connection.is_token_expired:
            connection.status = 'expired'
            connection.save()
        
        data = {
            'platform': platform,
            'status': connection.status,
            'is_connected': connection.is_connected,
            'platform_username': connection.platform_username,
            'platform_email': connection.platform_email,
            'connected_at': connection.updated_at.isoformat() if connection.updated_at else None,
            'last_used_at': connection.last_used_at.isoformat() if connection.last_used_at else None,
            'token_expires_at': connection.token_expires_at.isoformat() if connection.token_expires_at else None,
            'error_message': connection.last_error_message,
        }
        
        return JsonResponse(data)
    
    except Exception as e:
        logger.error(f"Error fetching connection status for {platform}: {e}")
        return JsonResponse({'error': 'Failed to fetch connection status'}, status=500)


def home(request):
    """Home page - redirect to dashboard if authenticated, otherwise show login."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    return render(request, 'oauth_manager/home.html')
