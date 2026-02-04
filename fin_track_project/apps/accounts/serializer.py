from .models import Account
from rest_framework import serializers

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'user',
            'bank',
            'account_type',
            'balance',
            'active',
        ]

        read_only_fields = ['user']
