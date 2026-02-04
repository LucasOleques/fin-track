from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'accounts'

router = routers.DefaultRouter()
router.register(r'', views.AccountViewSet, basename='accounts')

urlpatterns = [
    path('create/', views.accounts_create_view, name='create'),
    path('list/', views.accounts_list_view, name='list'),
    path('detail/<int:pk>/', views.accounts_detail_view, name='detail'),
    path('edit/<int:pk>/', views.accounts_edit_view, name='edit'),
    path('delete/<int:pk>/', views.accounts_delete_view, name='delete'),

    path('', include(router.urls)),
]