from django.db import models
from users.models import Users
from categories.models import Category

class Account(models.Model):
    user = models.ForeignKey(Users, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    name_bank = models.TextField('Banco', max_length=100)
    type_account = models.CharField('Tipo Conta', max_length=50)
    type_card = models.CharField('Tipo Cartão', max_length=50)
    balance = models.DecimalField('Saldo', max_digits=20, decimal_places=2)
    status = models.BooleanField('Status', default=True)
    

    class Meta:
        verbose_name = 'Conta'
        verbose_name_plural = 'Contas'
        ordering = ['id']

    def __str__(self):
        return f"{self.name_bank} - {self.status}"