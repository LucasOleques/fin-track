from django.contrib import admin
from .models import UserAdmin, UserClient

admin.site.register(UserAdmin)
admin.site.register(UserClient)