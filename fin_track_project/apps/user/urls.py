from django.urls import path, include, reverse_lazy
from rest_framework import routers
from . import views
from django.contrib.auth import views as auth_views

app_name = 'user'

router = routers.DefaultRouter()
router.register(r'users', views.AdminViewSet, basename='users')
router.register(r'clients', views.ClientViewSet, basename='clients')

urlpatterns = [
    path('login/', views.ClientViewSet.user_login_view, name='login'),
    path('logout/', views.ClientViewSet.user_logout_view, name='logout'),
    path('password_change', views.ClientViewSet.user_password_change_view, name='password_change'),
    path('register/', views.ClientViewSet.user_register_view, name='register'),
    path(
        'update-pending-email/',
        views.ClientViewSet.user_update_pending_email_view,
        name='update_pending_email',
    ),
    path('verify-email/<uidb64>/<token>/',views.ClientViewSet.user_verify_email_view, name='verify_email'),
    path('profile/', views.ClientViewSet.user_profile_view, name='profile'),
    path('profile_update', views.ClientViewSet.user_profile_update_view, name='profile_update'),

    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='apps/user/password_reset.html',
        email_template_name='apps/user/password_reset_email.html',
        success_url=reverse_lazy('user:password_reset_done')
    ), name="password_reset"),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
        template_name='apps/user/password_reset_done.html'
    ), name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='apps/user/password_reset_confirm.html',
        success_url=reverse_lazy('user:password_reset_complete')
    ), name="password_reset_confirm"),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='apps/user/password_reset_complete.html'
    ), name="password_reset_complete"),

    path('', include(router.urls)),
]
