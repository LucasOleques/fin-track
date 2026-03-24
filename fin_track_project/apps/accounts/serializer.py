from .models import Account
from rest_framework import serializers

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'id_account',
            'user',
            'name',
            'bank',
            'type',
            'account_color',
            'balance',
            'credit_limit',
            'is_active',
        ]

        read_only_fields = ['id_account','user']

    def create(self, validated_data):
        account = Account.objects.create(**validated_data)
        return account