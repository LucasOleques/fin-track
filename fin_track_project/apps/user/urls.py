from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'user'

router = routers.DefaultRouter()
router.register(r'users', views.UserAdminViewSet, basename='users')
router.register(r'clients', views.UserClientViewSet, basename='clients')

urlpatterns = [
    path('register/', views.user_register_view, name='register'),
    path('profile/', views.user_profile_view, name='profile'),
    path('password_reset/', views.user_password_reset_view, name='password_reset'),
    path('login/', views.user_login_view, name='login'),
    path('logout/', views.user_logout_view, name='logout'),

    path('', include(router.urls)),
]