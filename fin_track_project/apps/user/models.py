from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # AbstractUser já recebe username, email, first_name e last_name
    date_save = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering =['id']

    def __str__(self):
        return self.username