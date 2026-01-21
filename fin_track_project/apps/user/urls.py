from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'user'

router = routers.DefaultRouter()
router.register(r'users', views.UserAdminViewSet, basename='users')
router.register(r'clients', views.UserClientViewSet, basename='clients')

urlpatterns = [
    path('', include(router.urls)),
]