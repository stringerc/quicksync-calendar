from django.urls import path
from . import views
from .views_legal import privacy_policy, data_deletion, terms_of_service

urlpatterns = [
    # Main dashboard
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Demo user creation (for testing)
    path('create-demo-user/', views.create_demo_user, name='create_demo_user'),
    
    # OAuth flow
    path('oauth/initiate/<str:platform>/', views.initiate_oauth, name='oauth_initiate'),
    path('oauth/callback/<str:platform>/', views.oauth_callback, name='oauth_callback'),
    
    # Platform management
    path('platform/disconnect/<str:platform>/', views.disconnect_platform, name='disconnect_platform'),
    path('platform/status/<str:platform>/', views.connection_status, name='connection_status'),
    
    # Legal pages
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
    path('data-deletion/', data_deletion, name='data_deletion'),
    path('terms-of-service/', terms_of_service, name='terms_of_service'),
]
