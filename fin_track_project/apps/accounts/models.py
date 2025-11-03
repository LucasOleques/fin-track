from django.db import models
from user.models import User
from categories.models import Category

class Account(models.Model):
    id_account = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name_bank = models.TextField('Banco', max_length=100)
    type_account = models.CharField('Tipo Conta', max_length=50)
    type_card = models.CharField('Tipo Cartão', max_length=50)
    balance_init = models.DecimalField('Saldo inicial', max_digits=20, decimal_places=2)
    balance_end = models.DecimalField('Saldo final', max_digits=20, decimal_places=2)
    status = models.BooleanField('Status', default=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    

    class Meta:
        verbose_name = 'Conta'
        verbose_name_plural = 'Contas'
        ordering = ['id_account']

    def __str__(self):
        return f"{self.name_bank}"