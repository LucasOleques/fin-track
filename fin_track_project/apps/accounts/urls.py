from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'accounts'

router = routers.DefaultRouter()
router.register(r'', views.AccountViewSet, basename='accounts')

urlpatterns = [
    path('create/', views.AccountViewSet.accounts_create_view, name='create'),
    path('list/', views.AccountViewSet.accounts_list_view, name='list'),
    path('detail/<int:pk>/', views.AccountViewSet.accounts_detail_view, name='detail'),
    path('edit/<int:pk>/', views.AccountViewSet.accounts_edit_view, name='edit'),
    path('delete/<int:pk>/', views.AccountViewSet.accounts_delete_view, name='delete'),

    path('', include(router.urls)),
]