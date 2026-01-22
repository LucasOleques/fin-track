from django.db import models
from django.conf import settings

class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text='Usuário proprietário da categoria')
    name = models.CharField('Nome', max_length=100, help_text='Nome da categoria')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Data e hora de criação da categoria')
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"
