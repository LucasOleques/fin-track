from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'user'

router = routers.DefaultRouter()
router.register(r'users', views.AdminViewSet, basename='users')
router.register(r'clients', views.ClientViewSet, basename='clients')

urlpatterns = [
    path('register/', views.ClientViewSet.user_register_view, name='register'),
    path('profile/', views.ClientViewSet.user_profile_view, name='profile'),
    path('profile_update', views.ClientViewSet.user_profile_update, name='profile_update'),
    path('password_change', views.ClientViewSet.user_password_change, name='password_change'),
    path('password_reset/', views.ClientViewSet.user_password_reset_view, name='password_reset'),
    path('login/', views.ClientViewSet.user_login_view, name='login'),
    path('logout/', views.ClientViewSet.user_logout_view, name='logout'),

    path('', include(router.urls)),
]