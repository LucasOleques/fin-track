from django.db import models
from accounts.models import Account
from categories.models import Category

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('receita', 'Receita'),
        ('despesa', 'Despesa'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    value = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Transacao'
        verbose_name_plural = 'Transacoes'
        ordering = ['-date', '-value']

    def __str__(self):
        return f"{self.description} - {self.amount}"
