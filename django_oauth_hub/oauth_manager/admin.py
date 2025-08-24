from django.contrib import admin
from .models import PlatformConnection, OAuthSession, ConnectionLog


@admin.register(PlatformConnection)
class PlatformConnectionAdmin(admin.ModelAdmin):
    list_display = ['user', 'platform', 'status', 'platform_username', 'created_at', 'last_used_at']
    list_filter = ['platform', 'status', 'created_at']
    search_fields = ['user__username', 'platform_username', 'platform_email']
    readonly_fields = ['encrypted_access_token', 'encrypted_refresh_token', 'created_at', 'updated_at']
    
    fieldsets = [
        ('Basic Information', {
            'fields': ['user', 'platform', 'status']
        }),
        ('Platform User Info', {
            'fields': ['platform_user_id', 'platform_username', 'platform_email']
        }),
        ('Token Information', {
            'fields': ['token_expires_at', 'scope_granted'],
            'classes': ['collapse']
        }),
        ('Error Tracking', {
            'fields': ['last_error_message', 'error_count'],
            'classes': ['collapse']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at', 'last_used_at'],
            'classes': ['collapse']
        }),
    ]


@admin.register(OAuthSession)
class OAuthSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'platform', 'state', 'is_active', 'created_at', 'completed_at']
    list_filter = ['platform', 'is_active', 'created_at']
    search_fields = ['user__username', 'state']
    readonly_fields = ['created_at', 'completed_at']


@admin.register(ConnectionLog)
class ConnectionLogAdmin(admin.ModelAdmin):
    list_display = ['connection', 'action', 'ip_address', 'created_at']
    list_filter = ['action', 'created_at']
    search_fields = ['connection__user__username', 'connection__platform', 'details']
    readonly_fields = ['created_at']
    
    def has_add_permission(self, request):
        return False  # Logs should only be created programmatically
    
    def has_change_permission(self, request, obj=None):
        return False  # Logs should be immutable
