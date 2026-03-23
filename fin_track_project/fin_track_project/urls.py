from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.views import AccountViewSet
from transactions.views import TransactionViewSet
from categories.views import CategoryViewSet
from user.views import AdminViewSet, ClientViewSet
from .views import base_view, dashboard_view, footer_view, navbar_view, pagination_view

# Rotas para a API usando DRF
router = DefaultRouter()
router.register(r'accounts', AccountViewSet, basename='accounts')
router.register(r'transactions', TransactionViewSet, basename='transactions')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'users', AdminViewSet, basename='users')
router.register(r'clients', ClientViewSet, basename='clients')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('django.contrib.auth.urls')),
    
    # Rotas de Autenticação JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Rotas para templates
    path('', base_view, name='base'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('footer/', footer_view, name='footer'),
    path('navbar/', navbar_view, name='navbar'),
    path('pagination/', pagination_view, name='pagination'),

    # App routes
    path('accounts/', include('accounts.urls')),
    path('transactions/', include('transactions.urls')),
    path('categories/', include('categories.urls')),
    path('user/', include('user.urls')),

    # path('api/', include(router.urls)),
]