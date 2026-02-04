from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'transactions'

router = routers.DefaultRouter()
router.register(r'', views.TransactionViewSet, basename='transactions')

urlpatterns = [
    path('form/', views.transactions_form_view, name='form'),
    path('list/', views.transactions_list_view, name='list'),
    path('create/', views.transactions_create, name='create'),
    path('edit/<int:transaction_id>/', views.transactions_edit_view, name='edit'),

    path('', include(router.urls)),
]