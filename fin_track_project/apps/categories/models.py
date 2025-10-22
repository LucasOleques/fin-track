from django.db import models
from users.models import Users

class Category(models.Model):
    user=models.ForeignKey(Users, on_delete=models.PROTECT)
    classification_transaction=models.TextField('Classificação', max_length=100)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id']

    def __str__(self):
        return f"{self.classification_transaction}"