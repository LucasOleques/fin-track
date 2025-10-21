from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'transactions'

router = routers.DefaultRouter()
router.register('', views.TransactionsViewSet, basename='transactions')

urlpatterns = [
    path('', include(router.urls)),
    path('transactions/', views.TransactionsViewSet.as_view({'get': 'list'}), name='transactions'),
]