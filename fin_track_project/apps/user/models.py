from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# AbstractUser já recebe username, email, first_name e last_name
class Admin(AbstractUser):
    date_save = models.DateTimeField(auto_now_add=True)
    avatar = models.BinaryField(null=True, blank=True)
    class Meta:
        verbose_name = 'Usuario Admin'
        verbose_name_plural = 'Usuarios Admins'
        ordering =['id']

    def __str__(self):
        return self.username
    
class Client(models.Model):
    id_client = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='clients')
    client_name = models.CharField(max_length=255, help_text='Nome do cliente')
    client_email = models.EmailField(max_length=255, unique=True, help_text='Email do cliente')
    password = models.CharField(max_length=128, help_text='Senha do cliente')
    date_save = models.DateTimeField(auto_now_add=True)
    avatar = models.BinaryField(null=True, blank=True)

    class Meta:
        verbose_name = 'Usuario Cliente'
        verbose_name_plural = 'Usuarios Clientes'
        ordering = ['id_client']

    def __str__(self):
        return self.client_name
    