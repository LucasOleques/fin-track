from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls', namespace='user')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('transactions/', include('transactions.urls', namespace='transactions')),
    path('categories/', include('categories.urls', namespace='categories')),
    path('token-autenticacao/', obtain_auth_token),
]
