from django.db import models
from django.conf import settings

class Account(models.Model):
    ACCOUNT_TYPES = [
        ('corrente', 'Conta Corrente'),
        ('poupanca', 'Poupança'),
        ('cartao', 'Cartão de Crédito'),
        ('investimento', 'Investimento'),
        ('dinheiro', 'Dinheiro'),
    ]
        
    ACCOUNT_COLOR = [
            ('primary', 'Azul'),
            ('success', 'Verde'),
            ('danger', 'Vermelho'),
            ('warning', 'Amarelo'),
            ('info', 'Ciano'),
            ('secondary', 'Cinza'),
    ]

    id_account = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='accounts', help_text='Usuário proprietário da conta')
    name = models.CharField(max_length=100, blank=True, null=True, help_text='Nome da conta')
    bank = models.CharField(max_length=100, blank=True, null=True, help_text='Nome do banco da conta')
    type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, help_text='Tipo de conta')
    account_color = models.CharField(max_length=20, choices=ACCOUNT_COLOR, help_text='Cor da conta')
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, help_text='Saldo atual da conta')
    credit_limit = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, help_text='Limite do cartão')
    is_active = models.BooleanField(default=True, help_text='Indica se a conta está ativa')

    class Meta:
        verbose_name = 'Conta'
        verbose_name_plural = 'Contas'
        ordering = ['name']

    @property
    def icon(self):
        icon_map = {
            'corrente': 'wallet2',
            'poupanca': 'piggy-bank',
            'cartao': 'credit-card',
            'investimento': 'graph-up',
            'carteira': 'cash',
        }
        return icon_map.get(self.type, 'bank')

    def __str__(self):
        return f"{self.name} - {self.bank} - {self.type}"