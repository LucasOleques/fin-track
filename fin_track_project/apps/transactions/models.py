from django.db import models
from user.models import User
from accounts.models import Account
from categories.models import Category

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    accounts = models.ForeignKey(Account, on_delete=models.CASCADE)
    value_transaction = models.DecimalField('Valor Transação', max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField('Descricao', max_length=100)
    type_transaction = models.CharField('Tipo Transação', max_length=50)

    class Meta:
        verbose_name = 'Transacao'
        verbose_name_plural = 'Transacoes'
        ordering = ['id']

    def __str__(self):
        return f"{self.description} - {self.value_transaction}"
