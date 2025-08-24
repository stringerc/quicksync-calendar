"""
Django OAuth Hub - Test Suite

This module contains tests for the OAuth Hub functionality.
Run with: python manage.py test
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from unittest.mock import patch, Mock
import json
from oauth_manager.models import PlatformConnection, OAuthSession, ConnectionLog
from oauth_manager.views import generate_state, exchange_code_for_token


class OAuthHubTestCase(TestCase):
    """Base test case with common setup."""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')


class ModelsTestCase(OAuthHubTestCase):
    """Test cases for OAuth Hub models."""
    
    def test_platform_connection_creation(self):
        """Test creating a platform connection."""
        connection = PlatformConnection.objects.create(
            user=self.user,
            platform='facebook',
            status='disconnected'
        )
        
        self.assertEqual(connection.user, self.user)
        self.assertEqual(connection.platform, 'facebook')
        self.assertEqual(connection.status, 'disconnected')
        self.assertFalse(connection.is_connected)
    
    def test_token_encryption(self):
        """Test token encryption and decryption."""
        connection = PlatformConnection.objects.create(
            user=self.user,
            platform='facebook',
        )
        
        test_token = 'test_access_token_123'
        connection.access_token = test_token
        connection.save()
        
        # Token should be encrypted in database
        self.assertNotEqual(connection.encrypted_access_token, test_token)
        
        # But should decrypt correctly
        self.assertEqual(connection.access_token, test_token)
    
    def test_set_connected(self):
        """Test setting a connection as connected."""
        connection = PlatformConnection.objects.create(
            user=self.user,
            platform='facebook',
        )
        
        user_info = {
            'id': '12345',
            'name': 'Test User',
            'email': 'test@example.com'
        }
        
        connection.set_connected(
            access_token='test_token',
            expires_in=3600,
            user_info=user_info,
            scope='email,profile'
        )
        
        self.assertEqual(connection.status, 'connected')
        self.assertTrue(connection.is_connected)
        self.assertEqual(connection.platform_user_id, '12345')
        self.assertEqual(connection.platform_username, 'Test User')
        self.assertEqual(connection.platform_email, 'test@example.com')
    
    def test_oauth_session_creation(self):
        """Test OAuth session creation and management."""
        session = OAuthSession.objects.create(
            user=self.user,
            platform='facebook',
            state='test_state_123',
            redirect_uri='http://localhost:8000/callback/'
        )
        
        self.assertEqual(session.user, self.user)
        self.assertEqual(session.platform, 'facebook')
        self.assertEqual(session.state, 'test_state_123')
        self.assertTrue(session.is_active)
        
        # Test session completion
        session.complete_session()
        self.assertFalse(session.is_active)
        self.assertIsNotNone(session.completed_at)
    
    def test_connection_log_creation(self):
        """Test connection logging functionality."""
        connection = PlatformConnection.objects.create(
            user=self.user,
            platform='facebook',
        )
        
        log = ConnectionLog.objects.create(
            connection=connection,
            action='initiated',
            details='Test OAuth initiation',
            ip_address='127.0.0.1'
        )
        
        self.assertEqual(log.connection, connection)
        self.assertEqual(log.action, 'initiated')
        self.assertEqual(log.details, 'Test OAuth initiation')
        self.assertEqual(log.ip_address, '127.0.0.1')


class ViewsTestCase(OAuthHubTestCase):
    """Test cases for OAuth Hub views."""
    
    def test_home_page(self):
        """Test home page loads correctly."""
        self.client.logout()  # Test as anonymous user
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'OAuth Hub')
    
    def test_dashboard_requires_login(self):
        """Test dashboard requires authentication."""
        self.client.logout()
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, '/admin/login/?next=/dashboard/')
    
    def test_dashboard_authenticated(self):
        """Test dashboard loads for authenticated users."""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Social Media Connections')
    
    def test_initiate_oauth_invalid_platform(self):
        """Test OAuth initiation with invalid platform."""
        response = self.client.post(reverse('oauth_initiate', kwargs={'platform': 'invalid'}))
        self.assertRedirects(response, reverse('dashboard'))
    
    @patch('oauth_manager.views.settings.OAUTH_PLATFORMS')
    def test_initiate_oauth_unconfigured_platform(self, mock_platforms):
        """Test OAuth initiation with unconfigured platform."""
        mock_platforms.get.return_value = None
        
        response = self.client.post(reverse('oauth_initiate', kwargs={'platform': 'facebook'}))
        self.assertRedirects(response, reverse('dashboard'))
    
    def test_oauth_callback_missing_parameters(self):
        """Test OAuth callback with missing parameters."""
        response = self.client.get(reverse('oauth_callback', kwargs={'platform': 'facebook'}))
        self.assertRedirects(response, reverse('dashboard'))
    
    def test_oauth_callback_error(self):
        """Test OAuth callback with error parameter."""
        response = self.client.get(
            reverse('oauth_callback', kwargs={'platform': 'facebook'}),
            {'error': 'access_denied', 'error_description': 'User denied access'}
        )
        self.assertRedirects(response, reverse('dashboard'))
    
    def test_disconnect_platform(self):
        """Test platform disconnection."""
        # Create a connected platform
        connection = PlatformConnection.objects.create(
            user=self.user,
            platform='facebook',
            status='connected'
        )
        
        response = self.client.post(
            reverse('disconnect_platform', kwargs={'platform': 'facebook'}),
            HTTP_ACCEPT='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        
        # Check connection is disconnected
        connection.refresh_from_db()
        self.assertEqual(connection.status, 'disconnected')
    
    def test_connection_status_api(self):
        """Test connection status API endpoint."""
        connection = PlatformConnection.objects.create(
            user=self.user,
            platform='facebook',
            status='connected',
            platform_username='Test User'
        )
        
        response = self.client.get(
            reverse('connection_status', kwargs={'platform': 'facebook'})
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['platform'], 'facebook')
        self.assertEqual(data['status'], 'connected')
        self.assertEqual(data['platform_username'], 'Test User')
    
    def test_create_demo_user(self):
        """Test demo user creation (only in DEBUG mode)."""
        with self.settings(DEBUG=True):
            self.client.logout()
            response = self.client.get(reverse('create_demo_user'))
            self.assertRedirects(response, reverse('dashboard'))
            
            # Check that demo user was created and logged in
            demo_user = User.objects.get(username='demo_user')
            self.assertEqual(demo_user.email, 'demo@example.com')


class UtilityTestCase(TestCase):
    """Test cases for utility functions."""
    
    def test_generate_state(self):
        """Test OAuth state generation."""
        state1 = generate_state()
        state2 = generate_state()
        
        # States should be 32 characters long
        self.assertEqual(len(state1), 32)
        self.assertEqual(len(state2), 32)
        
        # States should be unique
        self.assertNotEqual(state1, state2)
        
        # States should be alphanumeric
        self.assertTrue(state1.isalnum())
        self.assertTrue(state2.isalnum())
    
    @patch('oauth_manager.views.requests.post')
    def test_exchange_code_for_token_success(self, mock_post):
        """Test successful token exchange."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'access_token': 'test_access_token',
            'token_type': 'bearer',
            'expires_in': 3600
        }
        mock_post.return_value = mock_response
        
        platform_config = settings.OAUTH_PLATFORMS['facebook']
        result = exchange_code_for_token(
            'facebook',
            'test_auth_code',
            'http://localhost:8000/callback/',
            platform_config
        )
        
        self.assertIsNotNone(result)
        self.assertEqual(result['access_token'], 'test_access_token')
        self.assertEqual(result['expires_in'], 3600)
    
    @patch('oauth_manager.views.requests.post')
    def test_exchange_code_for_token_failure(self, mock_post):
        """Test failed token exchange."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = 'Invalid authorization code'
        mock_post.return_value = mock_response
        
        platform_config = settings.OAUTH_PLATFORMS['facebook']
        result = exchange_code_for_token(
            'facebook',
            'invalid_auth_code',
            'http://localhost:8000/callback/',
            platform_config
        )
        
        self.assertIsNone(result)


class SecurityTestCase(OAuthHubTestCase):
    """Test cases for security features."""
    
    def test_csrf_protection(self):
        """Test CSRF protection on OAuth initiation."""
        # Test without CSRF token (should fail)
        self.client = Client(enforce_csrf_checks=True)
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(reverse('oauth_initiate', kwargs={'platform': 'facebook'}))
        self.assertEqual(response.status_code, 403)
    
    def test_token_encryption_security(self):
        """Test that tokens are properly encrypted."""
        connection = PlatformConnection.objects.create(
            user=self.user,
            platform='facebook',
        )
        
        sensitive_token = 'very_sensitive_access_token_123456'
        connection.access_token = sensitive_token
        connection.save()
        
        # Raw database value should not contain the original token
        connection.refresh_from_db()
        self.assertNotIn(sensitive_token, connection.encrypted_access_token)
        
        # But decryption should work
        self.assertEqual(connection.access_token, sensitive_token)
    
    def test_state_parameter_validation(self):
        """Test OAuth state parameter validation."""
        # Create OAuth session
        session = OAuthSession.objects.create(
            user=self.user,
            platform='facebook',
            state='valid_state_123',
            redirect_uri='http://localhost:8000/callback/'
        )
        
        # Test with invalid state
        response = self.client.get(
            reverse('oauth_callback', kwargs={'platform': 'facebook'}),
            {'code': 'test_code', 'state': 'invalid_state'}
        )
        self.assertEqual(response.status_code, 404)  # Should not find session


class IntegrationTestCase(OAuthHubTestCase):
    """Integration test cases."""
    
    def test_complete_oauth_flow(self):
        """Test a complete OAuth flow simulation."""
        # 1. Initiate OAuth
        with patch('oauth_manager.views.settings.OAUTH_PLATFORMS') as mock_platforms:
            mock_platforms.get.return_value = {
                'client_id': 'test_client_id',
                'client_secret': 'test_client_secret',
                'auth_url': 'https://facebook.com/oauth/authorize',
                'scope': 'email,profile'
            }
            
            response = self.client.post(reverse('oauth_initiate', kwargs={'platform': 'facebook'}))
            
            # Should redirect to OAuth provider
            self.assertEqual(response.status_code, 302)
            self.assertIn('facebook.com', response.url)
        
        # 2. Check that OAuth session was created
        session = OAuthSession.objects.get(user=self.user, platform='facebook')
        self.assertTrue(session.is_active)
        
        # 3. Check that platform connection status was updated
        connection = PlatformConnection.objects.get(user=self.user, platform='facebook')
        self.assertEqual(connection.status, 'connecting')
        
        # 4. Simulate callback (would normally come from OAuth provider)
        with patch('oauth_manager.views.exchange_code_for_token') as mock_exchange:
            mock_exchange.return_value = {
                'access_token': 'test_access_token',
                'refresh_token': 'test_refresh_token',
                'expires_in': 3600
            }
            
            with patch('oauth_manager.views.get_platform_user_info') as mock_user_info:
                mock_user_info.return_value = {
                    'id': '12345',
                    'name': 'Test User',
                    'email': 'test@facebook.com'
                }
                
                response = self.client.get(
                    reverse('oauth_callback', kwargs={'platform': 'facebook'}),
                    {'code': 'test_auth_code', 'state': session.state}
                )
                
                # Should redirect back to dashboard
                self.assertRedirects(response, reverse('dashboard'))
        
        # 5. Verify final state
        connection.refresh_from_db()
        session.refresh_from_db()
        
        self.assertEqual(connection.status, 'connected')
        self.assertTrue(connection.is_connected)
        self.assertEqual(connection.platform_username, 'Test User')
        self.assertEqual(connection.platform_email, 'test@facebook.com')
        self.assertFalse(session.is_active)
        self.assertIsNotNone(session.completed_at)
        
        # 6. Check that logs were created
        logs = ConnectionLog.objects.filter(connection=connection)
        self.assertTrue(logs.filter(action='initiated').exists())
        self.assertTrue(logs.filter(action='callback_received').exists())
        self.assertTrue(logs.filter(action='connected').exists())
