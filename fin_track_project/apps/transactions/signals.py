from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Transaction
from decimal import Decimal

@receiver(post_save, sender=Transaction)
def update_balance_on_save(sender, instance, created, **kwargs):
    if created:
        account = instance.account
        if instance.transaction_type == 'receita':
            account.balance += instance.value
        else:
            account.balance -= instance.value
        account.save()

@receiver(post_delete, sender=Transaction)
def update_balance_on_delete(sender, instance, **kwargs):
    account = instance.account
    if instance.transaction_type == 'receita':
        account.balance -= instance.value # Remove a receita
    else:
        account.balance += instance.value # Estorna a despesa
    account.save()