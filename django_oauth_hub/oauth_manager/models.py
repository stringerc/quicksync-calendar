from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from cryptography.fernet import Fernet
from django.conf import settings
import json
import logging

logger = logging.getLogger(__name__)

class PlatformConnection(models.Model):
    """Model to store OAuth connections for different social media platforms."""
    
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('twitter', 'Twitter/X'),
        ('linkedin', 'LinkedIn'),
        ('youtube', 'YouTube'),
        ('tiktok', 'TikTok'),
        ('pinterest', 'Pinterest'),
    ]
    
    STATUS_CHOICES = [
        ('disconnected', 'Disconnected'),
        ('connecting', 'Connecting'),
        ('connected', 'Connected'),
        ('expired', 'Token Expired'),
        ('error', 'Connection Error'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='platform_connections')
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='disconnected')
    
    # Encrypted token storage
    encrypted_access_token = models.TextField(blank=True, null=True)
    encrypted_refresh_token = models.TextField(blank=True, null=True)
    
    # Platform-specific user info
    platform_user_id = models.CharField(max_length=100, blank=True, null=True)
    platform_username = models.CharField(max_length=100, blank=True, null=True)
    platform_email = models.EmailField(blank=True, null=True)
    
    # Token metadata
    token_expires_at = models.DateTimeField(blank=True, null=True)
    scope_granted = models.TextField(blank=True, null=True)  # JSON array of granted scopes
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_used_at = models.DateTimeField(blank=True, null=True)
    
    # Error tracking
    last_error_message = models.TextField(blank=True, null=True)
    error_count = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['user', 'platform']
        verbose_name = 'Platform Connection'
        verbose_name_plural = 'Platform Connections'
        indexes = [
            models.Index(fields=['user', 'platform']),
            models.Index(fields=['status']),
            models.Index(fields=['token_expires_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.get_platform_display()} ({self.status})"
    
    @property
    def is_connected(self):
        """Check if the connection is active and valid."""
        return self.status == 'connected' and self.access_token and not self.is_token_expired
    
    @property
    def is_token_expired(self):
        """Check if the access token has expired."""
        if not self.token_expires_at:
            return False
        return timezone.now() > self.token_expires_at
    
    @property
    def access_token(self):
        """Decrypt and return the access token."""
        if not self.encrypted_access_token:
            return None
        try:
            fernet = Fernet(settings.ENCRYPTION_KEY)
            return fernet.decrypt(self.encrypted_access_token.encode()).decode()
        except Exception as e:
            logger.error(f"Failed to decrypt access token for {self}: {e}")
            return None
    
    @access_token.setter
    def access_token(self, value):
        """Encrypt and store the access token."""
        if not value:
            self.encrypted_access_token = None
            return
        try:
            fernet = Fernet(settings.ENCRYPTION_KEY)
            self.encrypted_access_token = fernet.encrypt(value.encode()).decode()
        except Exception as e:
            logger.error(f"Failed to encrypt access token for {self}: {e}")
            raise
    
    @property
    def refresh_token(self):
        """Decrypt and return the refresh token."""
        if not self.encrypted_refresh_token:
            return None
        try:
            fernet = Fernet(settings.ENCRYPTION_KEY)
            return fernet.decrypt(self.encrypted_refresh_token.encode()).decode()
        except Exception as e:
            logger.error(f"Failed to decrypt refresh token for {self}: {e}")
            return None
    
    @refresh_token.setter
    def refresh_token(self, value):
        """Encrypt and store the refresh token."""
        if not value:
            self.encrypted_refresh_token = None
            return
        try:
            fernet = Fernet(settings.ENCRYPTION_KEY)
            self.encrypted_refresh_token = fernet.encrypt(value.encode()).decode()
        except Exception as e:
            logger.error(f"Failed to encrypt refresh token for {self}: {e}")
            raise
    
    def set_connected(self, access_token, refresh_token=None, expires_in=None, user_info=None, scope=None):
        """Set the connection as connected with token data."""
        self.access_token = access_token
        self.refresh_token = refresh_token
        
        if expires_in:
            self.token_expires_at = timezone.now() + timezone.timedelta(seconds=expires_in)
        
        if user_info:
            self.platform_user_id = user_info.get('id')
            self.platform_username = user_info.get('username') or user_info.get('name')
            self.platform_email = user_info.get('email')
        
        if scope:
            self.scope_granted = json.dumps(scope if isinstance(scope, list) else scope.split(','))
        
        self.status = 'connected'
        self.last_used_at = timezone.now()
        self.last_error_message = None
        self.error_count = 0
        self.save()
    
    def set_error(self, error_message):
        """Set the connection as error state."""
        self.status = 'error'
        self.last_error_message = error_message
        self.error_count += 1
        self.save()
    
    def disconnect(self):
        """Disconnect and clear all token data."""
        self.status = 'disconnected'
        self.encrypted_access_token = None
        self.encrypted_refresh_token = None
        self.token_expires_at = None
        self.platform_user_id = None
        self.platform_username = None
        self.platform_email = None
        self.scope_granted = None
        self.last_error_message = None
        self.error_count = 0
        self.save()


class OAuthSession(models.Model):
    """Model to track OAuth sessions and state parameters for security."""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='oauth_sessions')
    platform = models.CharField(max_length=20, choices=PlatformConnection.PLATFORM_CHOICES)
    state = models.CharField(max_length=255, unique=True)  # CSRF protection
    code_verifier = models.CharField(max_length=128, blank=True, null=True)  # PKCE support
    redirect_uri = models.URLField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'OAuth Session'
        verbose_name_plural = 'OAuth Sessions'
        indexes = [
            models.Index(fields=['state']),
            models.Index(fields=['user', 'platform']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.platform} - {self.state[:10]}..."
    
    def complete_session(self):
        """Mark the session as completed."""
        self.completed_at = timezone.now()
        self.is_active = False
        self.save()
    
    @classmethod
    def cleanup_expired_sessions(cls):
        """Remove sessions older than 1 hour."""
        cutoff = timezone.now() - timezone.timedelta(hours=1)
        expired_sessions = cls.objects.filter(created_at__lt=cutoff, is_active=True)
        count = expired_sessions.count()
        expired_sessions.delete()
        logger.info(f"Cleaned up {count} expired OAuth sessions")
        return count


class ConnectionLog(models.Model):
    """Model to log connection events for debugging and monitoring."""
    
    ACTION_CHOICES = [
        ('initiated', 'OAuth Initiated'),
        ('callback_received', 'Callback Received'),
        ('token_exchanged', 'Token Exchanged'),
        ('connected', 'Successfully Connected'),
        ('disconnected', 'Disconnected'),
        ('token_refreshed', 'Token Refreshed'),
        ('error', 'Error Occurred'),
    ]
    
    connection = models.ForeignKey(PlatformConnection, on_delete=models.CASCADE, related_name='logs')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    details = models.TextField(blank=True, null=True)  # JSON data or error message
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Connection Log'
        verbose_name_plural = 'Connection Logs'
        indexes = [
            models.Index(fields=['connection', 'created_at']),
            models.Index(fields=['action']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.connection} - {self.get_action_display()} - {self.created_at}"