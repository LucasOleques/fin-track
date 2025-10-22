from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'accounts'

router = routers.DefaultRouter()
router.register('', views.AccountViewSet, basename='accounts')

urlspatterns = [
    path('', include(router.urls)),
    path('accounts/', views.AccountViewSet.as_view({'get':'list'}), name='accounts'),
]