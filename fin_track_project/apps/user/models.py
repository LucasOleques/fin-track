from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# AbstractUser já recebe username, email, first_name e last_name
class UserAdmin(AbstractUser):
    date_save = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'Usuario Admin'
        verbose_name_plural = 'Usuarios Admins'
        ordering =['id']

    def __str__(self):
        return self.username
    
class UserClient(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='clients')
    client_name = models.CharField(max_length=255)
    client_email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    date_save = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Usuario Cliente'
        verbose_name_plural = 'Usuarios Clientes'
        ordering = ['id']

    def __str__(self):
        return self.client_name