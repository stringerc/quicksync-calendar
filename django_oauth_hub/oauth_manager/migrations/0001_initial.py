from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PlatformConnection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.CharField(choices=[('facebook', 'Facebook'), ('instagram', 'Instagram'), ('twitter', 'Twitter/X'), ('linkedin', 'LinkedIn'), ('youtube', 'YouTube'), ('tiktok', 'TikTok'), ('pinterest', 'Pinterest')], max_length=20)),
                ('status', models.CharField(choices=[('disconnected', 'Disconnected'), ('connecting', 'Connecting'), ('connected', 'Connected'), ('expired', 'Token Expired'), ('error', 'Connection Error')], default='disconnected', max_length=20)),
                ('encrypted_access_token', models.TextField(blank=True, null=True)),
                ('encrypted_refresh_token', models.TextField(blank=True, null=True)),
                ('platform_user_id', models.CharField(blank=True, max_length=100, null=True)),
                ('platform_username', models.CharField(blank=True, max_length=100, null=True)),
                ('platform_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('token_expires_at', models.DateTimeField(blank=True, null=True)),
                ('scope_granted', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('last_used_at', models.DateTimeField(blank=True, null=True)),
                ('last_error_message', models.TextField(blank=True, null=True)),
                ('error_count', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='platform_connections', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Platform Connection',
                'verbose_name_plural': 'Platform Connections',
                'indexes': [
                    models.Index(fields=['user', 'platform'], name='oauth_manag_user_id_8c5c52_idx'),
                    models.Index(fields=['status'], name='oauth_manag_status_4b3e91_idx'),
                    models.Index(fields=['token_expires_at'], name='oauth_manag_token_e_a8b0f7_idx'),
                ],
            },
        ),
        migrations.CreateModel(
            name='OAuthSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.CharField(choices=[('facebook', 'Facebook'), ('instagram', 'Instagram'), ('twitter', 'Twitter/X'), ('linkedin', 'LinkedIn'), ('youtube', 'YouTube'), ('tiktok', 'TikTok'), ('pinterest', 'Pinterest')], max_length=20)),
                ('state', models.CharField(max_length=255, unique=True)),
                ('code_verifier', models.CharField(blank=True, max_length=128, null=True)),
                ('redirect_uri', models.URLField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='oauth_sessions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'OAuth Session',
                'verbose_name_plural': 'OAuth Sessions',
                'indexes': [
                    models.Index(fields=['state'], name='oauth_manag_state_9f5e7a_idx'),
                    models.Index(fields=['user', 'platform'], name='oauth_manag_user_id_7c4a3b_idx'),
                    models.Index(fields=['created_at'], name='oauth_manag_created_a85f32_idx'),
                ],
            },
        ),
        migrations.CreateModel(
            name='ConnectionLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('initiated', 'OAuth Initiated'), ('callback_received', 'Callback Received'), ('token_exchanged', 'Token Exchanged'), ('connected', 'Successfully Connected'), ('disconnected', 'Disconnected'), ('token_refreshed', 'Token Refreshed'), ('error', 'Error Occurred')], max_length=20)),
                ('details', models.TextField(blank=True, null=True)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('user_agent', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('connection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='oauth_manager.platformconnection')),
            ],
            options={
                'verbose_name': 'Connection Log',
                'verbose_name_plural': 'Connection Logs',
                'ordering': ['-created_at'],
                'indexes': [
                    models.Index(fields=['connection', 'created_at'], name='oauth_manag_connect_6b9e81_idx'),
                    models.Index(fields=['action'], name='oauth_manag_action_9c7f2a_idx'),
                ],
            },
        ),
        migrations.AlterUniqueTogether(
            name='platformconnection',
            unique_together={('user', 'platform')},
        ),
    ]
