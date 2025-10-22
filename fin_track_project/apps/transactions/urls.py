from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'transactions'

router = routers.DefaultRouter()
router.register('', views.TransactionViewSet, basename='transactions')

urlpatterns = [
    path('', include(router.urls)),
    path('transactions/', views.TransactionViewSet.as_view({'get': 'list'}), name='transactions'),
]