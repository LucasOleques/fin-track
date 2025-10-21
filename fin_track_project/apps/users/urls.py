from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'users'

router = routers.DefaultRouter()
router.register('', views.UsersViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('users/', views.UsersViewSet.as_view({'get': 'list'}), name='users'),
]