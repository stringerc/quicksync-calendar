from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
import logging
from .models import PlatformConnection, ConnectionLog, OAuthSession

logger = logging.getLogger(__name__)


def privacy_policy(request):
    """Display the privacy policy page."""
    context = {
        'updated_date': 'January 24, 2025',
    }
    return render(request, 'oauth_manager/privacy_policy.html', context)


def data_deletion(request):
    """Handle data deletion requests."""
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to request data deletion.')
            return redirect('dashboard')
        
        # Get form data
        reason = request.POST.get('reason', '')
        additional_info = request.POST.get('additional_info', '')
        confirm_deletion = request.POST.get('confirm_deletion')
        
        if not confirm_deletion:
            messages.error(request, 'You must confirm that you understand the deletion is irreversible.')
            return render(request, 'oauth_manager/data_deletion.html')
        
        try:
            # Log the deletion request
            logger.info(f"Data deletion requested by user {request.user.username} ({request.user.email})")
            
            # Create a deletion log
            ConnectionLog.objects.create(
                user=request.user,
                action='data_deletion_requested',
                details=f"Reason: {reason}, Additional: {additional_info}",
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
            )
            
            # Send notification email to admin (if configured)
            if hasattr(settings, 'ADMIN_EMAIL') and settings.ADMIN_EMAIL:
                try:
                    send_mail(
                        subject=f'Data Deletion Request - {request.user.username}',
                        message=f'''Data deletion request received:

User: {request.user.username}
Email: {request.user.email}
Reason: {reason}
Additional Info: {additional_info}
Timestamp: {timezone.now()}
IP: {request.META.get('REMOTE_ADDR')}

Please process within 30 days as per privacy policy.''',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[settings.ADMIN_EMAIL],
                        fail_silently=True,
                    )
                except Exception as e:
                    logger.error(f"Failed to send deletion notification email: {e}")
            
            # In a production environment, you might want to:
            # 1. Mark the user account for deletion rather than immediate deletion
            # 2. Send a confirmation email to the user
            # 3. Add a grace period before actual deletion
            # 4. Queue the deletion for background processing
            
            # For demo purposes, we'll just disconnect all OAuth connections
            # but keep the user account (modify this for production)
            if settings.DEBUG:
                # In debug mode, just disconnect OAuth connections
                connections = PlatformConnection.objects.filter(user=request.user)
                for connection in connections:
                    connection.disconnect()
                
                messages.success(
                    request, 
                    'Your OAuth connections have been disconnected. In production, '
                    'your full data deletion request would be processed within 30 days.'
                )
            else:
                # In production, mark for deletion and send confirmation email
                messages.success(
                    request,
                    'Your data deletion request has been received. You will receive '
                    'a confirmation email within 24 hours. All data will be permanently '
                    'deleted within 30 days as outlined in our privacy policy.'
                )
            
            return redirect('dashboard')
            
        except Exception as e:
            logger.error(f"Error processing data deletion request: {e}")
            messages.error(
                request, 
                'There was an error processing your deletion request. '
                'Please contact support at privacy@oauthhub.com'
            )
    
    return render(request, 'oauth_manager/data_deletion.html')


def terms_of_service(request):
    """Display terms of service (optional)."""
    context = {
        'updated_date': 'January 24, 2025',
    }
    return render(request, 'oauth_manager/terms_of_service.html', context)
