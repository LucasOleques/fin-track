from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('transactions/', include('transactions.urls', namespace='transactions')),
    path('categories/', include('categories.urls', namespace='categories')),
]
