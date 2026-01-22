from django.db import models
from django.conf import settings

class Account(models.Model):
    ACCOUNT_TYPES = [
        ('corrente', 'Conta Corrente'),
        ('poupanca', 'Poupança'),
        ('cartao', 'Cartão de Crédito'),
        ('carteira', 'Dinheiro Físico'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='accounts', help_text='Usuário proprietário da conta')
    bank = models.CharField(max_length=100, blank=True, null=True, help_text='Nome do banco da conta')
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, help_text='Tipo de conta')
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, help_text='Saldo atual da conta')
    active = models.BooleanField(default=True, help_text='Indica se a conta está ativa')

    class Meta:
        verbose_name = 'Conta'
        verbose_name_plural = 'Contas'
        ordering = ['bank']

    def __str__(self):
        return f"{self.bank} - {self.account_type}"