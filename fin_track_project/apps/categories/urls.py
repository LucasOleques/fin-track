from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'categories'

router = routers.DefaultRouter()
router.register(r'', views.CategoryViewSet,basename='categories')

urlpatterns = [
    path('', include(router.urls)),
]