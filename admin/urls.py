from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import AppViewSet

# Initialize DRF router
router = DefaultRouter()
router.register(r'apps', AppViewSet)  # Register API endpoints for the App model

urlpatterns = [
    # Existing views
    path('', views.signin, name='signin'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('admin', views.admin, name='admin'),

    # API endpoints
    path('api/', include(router.urls)),  # DRF API routes
]
