from django.db import models

class Users(models.Model):
    name = models.CharField('Nome', max_length=50, unique=True)
    password = models.CharField('Senha', max_length=50)
    email = models.EmailField('Email', unique=True)
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering =['id']

    def __str__(self):
        return self.name