from django.db import models
from django.conf import settings
from accounts.models import Account
from categories.models import Category

class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField('Valor', max_digits=10, decimal_places=2)
    date = models.DateField('Data')
    description = models.CharField('Descrição', max_length=200)
    TRANSACTION_TYPE_CHOICES = [
        ('expense','Despesa'),
        ('income','Receita')
        ]
    transaction_type = models.CharField('Tipo', max_length=7, choices=TRANSACTION_TYPE_CHOICES)

    class Meta:
        verbose_name = 'Transacao'
        verbose_name_plural = 'Transacoes'
        ordering = ['-date', '-id']

    def __str__(self):
        return f"{self.description} - {self.amount}"
