from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'transactions'

router = routers.DefaultRouter()
router.register(r'', views.TransactionViewSet, basename='transactions')

urlpatterns = [
    path('', include(router.urls)),
]