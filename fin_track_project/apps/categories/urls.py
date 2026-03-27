from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'categories'

router = routers.DefaultRouter()
router.register(r'', views.CategoryViewSet,basename='categories')

urlpatterns = [
    path('list/', views.CategoryViewSet.categories_list_view, name='list'),
    path('create/', views.CategoryViewSet.categories_create_view, name='create'),
    path('edit/', views.CategoryViewSet.categories_edit_view, name='edit'),
    path('edit/<int:pk>/', views.CategoryViewSet.categories_edit_view, name='edit'),
    path('delete/<int:pk>/', views.CategoryViewSet.categories_delete_view, name='delete'),

    path('', include(router.urls)),
]