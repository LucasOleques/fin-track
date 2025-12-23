from django.db import models
from django.conf import settings

class Account(models.Model):
    ACCOUNT_TYPES = [
        ('corrente', 'Conta Corrente'),
        ('poupanca', 'Poupança'),
        ('cartao', 'Cartão de Crédito'),
        ('carteira', 'Dinheiro Físico'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='accounts')
    name_bank = models.CharField(max_length=100)
    bank = models.CharField(max_length=100, blank=True, null=True)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Conta'
        verbose_name_plural = 'Contas'
        ordering = ['name_bank']

    def __str__(self):
        return f"{self.name_bank}"