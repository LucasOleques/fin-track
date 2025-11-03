from .models import Account
from rest_framework import serializers

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'id_account',
            'user',
            'name_bank',
            'type_account',
            'type_card',
            'balance_init',
            'balance_end',
            'status',
            'category',
        ]

        read_only_fields = ['user']
