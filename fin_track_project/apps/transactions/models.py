from django.db import models
from django.conf import settings
from accounts.models import Account
from categories.models import Category

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('receita', 'Receita'),
        ('despesa', 'Despesa'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions', help_text='Conta associada à transação')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, help_text='Categoria da transação')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES, help_text='Tipo de transação: receita ou despesa')
    value = models.DecimalField(max_digits=15, decimal_places=2, help_text='Valor da transação')
    description = models.CharField(max_length=255, blank=True, help_text='Descrição da transação')
    date = models.DateField( help_text='Data da transação')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Data e hora de criação da transação')

    class Meta:
        verbose_name = 'Transacao'
        verbose_name_plural = 'Transacoes'
        ordering = ['-date', '-value']

    def __str__(self):
        return f"{self.transaction_type} - {self.value}"
