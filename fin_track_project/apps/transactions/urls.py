from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'transactions'

router = routers.DefaultRouter()
router.register(r'', views.TransactionViewSet, basename='transactions')

urlpatterns = [
    path('form/', views.TransactionViewSet.transactions_form_view, name='form'),
    path('list/', views.TransactionViewSet.transactions_list_view, name='list'),
    path('create/', views.TransactionViewSet.transactions_create, name='create'),
    path('edit/<int:pk>/', views.TransactionViewSet.transactions_edit_view, name='edit'),
    path('delete/<int:pk>/', views.TransactionViewSet.transactions_delete_view, name='delete'),

    path('', include(router.urls)),
]