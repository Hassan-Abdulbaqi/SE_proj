from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'services', views.ServiceViewSet, basename='service')
router.register(r'orders', views.OrderViewSet, basename='order')

urlpatterns = [
    # Authentication
    path('auth/signup/', views.signup, name='signup'),
    path('auth/signin/', views.signin, name='signin'),
    path('auth/signout/', views.signout, name='signout'),
    path('auth/csrf/', views.csrf_token, name='csrf_token'),
    
    # Debug (Development Only)
    path('debug/users/', views.debug_users, name='debug_users'),
    
    # Profile
    path('profile/', views.get_profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    
    # Router URLs
    path('', include(router.urls)),
]

