from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'user'

router = routers.DefaultRouter()
router.register('', views.UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('user/', views.UserViewSet.as_view({'get': 'list'}), name='user'),
]