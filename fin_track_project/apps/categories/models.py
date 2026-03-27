from django.db import models
from django.conf import settings

class Category(models.Model):
    CATEGORY_TYPES = [
        ('despesa', 'Despesa'),
        ('receita', 'Receita'),
        ('ambos', 'Ambos'),
    ]
        
    CATEGORY_COLOR = [
            ('danger', 'Vermelho'),
            ('success', 'Verde'),
            ('primary', 'Azul'),
    ]

    id_category = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text='Usuário proprietário da categoria')
    name = models.CharField('Nome', max_length=100, help_text='Nome da categoria')
    type = models.CharField(max_length=20, choices=CATEGORY_TYPES, help_text='Tipo de categoria')
    category_color = models.CharField(max_length=20, choices=CATEGORY_COLOR, help_text='Cor da categoria')
    description = models.CharField('Descrição', max_length=500, help_text='Descrição da categoria')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Data e hora de criação da categoria')
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"
