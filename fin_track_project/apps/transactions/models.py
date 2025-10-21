from django.db import models
from users.models import Users

class Transaction(models.Model):
    users = models.ForeignKey(Users, on_delete=models.CASCADE)
    is_open = models.BooleanField('Em aberto', default=False)
    value_transaction = models.DecimalField('Valor', max_digits=10, decimal_places=2)
    description = models.TextField('Descricao', max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        verbose_name = 'Transacao'
        verbose_name_plural = 'Transacoes'
        ordering = ['id']

    def __str__(self):
        return f"{self.description} - {self.value_transaction}"
